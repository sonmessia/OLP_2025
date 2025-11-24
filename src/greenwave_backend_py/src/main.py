"""
Main FastAPI application for GreenWave Backend
"""
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

from .config.settings import settings
from .config.areas import AREAS, get_area_by_name
from .services.orion_service import OrionService
from .services.websocket_service import WebSocketService
from .services.simulation_service import SimulationService
from .services.ai_service import AIService
from .services.iot_service import IoTService
from .models.simulation import CommandRequest

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s - %(name)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize services
orion_service = OrionService(settings.orion_url)
ws_service = WebSocketService()
simulation_service = SimulationService(
    orion_service,
    ws_service,
    settings.tls_id,
    settings.update_interval
)

# Initialize AI Service
ai_service = AIService(
    model_path=settings.ai_model_path,
    tls_id=settings.tls_id,
    num_phases=settings.ai_num_phases,
    min_green_steps=settings.ai_min_green_steps,
    enabled=settings.ai_enabled
)

# Initialize IoT Service (SUMO)
iot_service = None
if settings.sumo_enabled:
    detector_ids = [d.strip() for d in settings.sumo_detector_ids.split(',')]
    edge_ids = [e.strip() for e in settings.sumo_edge_ids.split(',')]
    
    iot_service = IoTService(
        sumo_config_path=settings.sumo_config_path,
        tls_id=settings.tls_id,
        detector_ids=detector_ids,
        edge_ids=edge_ids,
        use_gui=settings.sumo_use_gui,
        step_length=settings.sumo_step_length
    )



@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    logger.info("Starting GreenWave Backend...")
    logger.info(f"Orion URL: {settings.orion_url}")
    logger.info(f"Traffic Light ID: {settings.tls_id}")
    
    # Auto-start simulation
    simulation_service.start()
    
    yield
    
    # Shutdown
    logger.info("Shutting down GreenWave Backend...")
    simulation_service.stop()
    await orion_service.close()


# Create FastAPI app
app = FastAPI(
    title="GreenWave Backend",
    description="Backend service for GreenWave Traffic Control System",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "ok",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "simulation": simulation_service.is_active(),
            "websocket": ws_service.get_client_count(),
            "orion": settings.orion_url
        }
    }


# Get available areas
@app.get("/api/areas")
async def get_areas():
    """Get all available areas"""
    return {
        "areas": [
            {
                "id": key,
                "name": area.name,
                "bounds": area.bounds,
                "center": area.center,
                "tlsId": area.tls_id
            }
            for key, area in AREAS.items()
        ]
    }


# Get specific area
@app.get("/api/areas/{area_name}")
async def get_area(area_name: str):
    """Get specific area by name"""
    area = get_area_by_name(area_name)
    
    if not area:
        raise HTTPException(status_code=404, detail="Area not found")
    
    return area.model_dump()


# Proxy endpoint for Orion (GET)
@app.get("/api/orion/{path:path}")
async def proxy_orion_get(path: str):
    """Proxy GET requests to Orion"""
    entity = await orion_service.get_entity(f"urn:ngsi-ld:{path}")
    
    if not entity:
        raise HTTPException(status_code=404, detail="Entity not found")
    
    return entity


# Send command to traffic light
@app.post("/api/command/phase")
async def set_phase(request: CommandRequest):
    """Set traffic light phase"""
    if request.phase < 0 or request.phase > 3:
        raise HTTPException(status_code=400, detail="Invalid phase number")
    
    success = await simulation_service.set_phase(request.phase)
    
    if success:
        return {"success": True, "phase": request.phase}
    else:
        raise HTTPException(status_code=500, detail="Failed to set phase")


# Start simulation
@app.post("/api/simulation/start")
async def start_simulation():
    """Start simulation"""
    simulation_service.start()
    return {"success": True, "message": "Simulation started"}


# Stop simulation
@app.post("/api/simulation/stop")
async def stop_simulation():
    """Stop simulation"""
    simulation_service.stop()
    return {"success": True, "message": "Simulation stopped"}


# Get simulation status
@app.get("/api/simulation/status")
async def get_simulation_status():
    """Get simulation status"""
    return {
        "running": simulation_service.is_active(),
        "clients": ws_service.get_client_count(),
        "updateInterval": settings.update_interval
    }


# WebSocket endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time communication"""
    await ws_service.connect(websocket)
    
    try:
        while True:
            data = await websocket.receive_text()
            await ws_service.handle_message(websocket, data)
    except WebSocketDisconnect:
        ws_service.disconnect(websocket)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        ws_service.disconnect(websocket)


# Register WebSocket event handlers
async def handle_command(data: dict):
    """Handle command from WebSocket"""
    logger.info(f"Received WebSocket command: {data}")
    
    if data.get("type") == "setPhase":
        phase = data.get("phase")
        if isinstance(phase, int):
            await simulation_service.set_phase(phase)


async def handle_subscribe(data: dict):
    """Handle subscription request"""
    logger.info(f"Client subscribed to: {data}")


ws_service.on("command", handle_command)
ws_service.on("subscribe", handle_subscribe)


# ========== AI Control Endpoints ==========

@app.post("/api/ai/start")
async def start_ai():
    """Enable AI control"""
    ai_service.enable()
    return {"success": True, "message": "AI control enabled"}


@app.post("/api/ai/stop")
async def stop_ai():
    """Disable AI control"""
    ai_service.disable()
    return {"success": True, "message": "AI control disabled"}


@app.get("/api/ai/status")
async def get_ai_status():
    """Get AI service status"""
    return ai_service.get_status()


@app.post("/api/ai/toggle")
async def toggle_ai():
    """Toggle AI control"""
    enabled = ai_service.toggle()
    return {
        "success": True,
        "enabled": enabled,
        "message": f"AI control {'enabled' if enabled else 'disabled'}"
    }


@app.post("/api/ai/reload")
async def reload_ai_model():
    """Reload AI model"""
    try:
        ai_service.reload_model()
        return {"success": True, "message": "AI model reloaded"}
    except Exception as e:
        logger.error(f"Error reloading AI model: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ========== SUMO Control Endpoints ==========

@app.post("/api/sumo/start")
async def start_sumo():
    """Start SUMO simulation"""
    if not iot_service:
        raise HTTPException(status_code=400, detail="SUMO service not initialized")
    
    success = iot_service.start()
    if success:
        return {"success": True, "message": "SUMO simulation started"}
    else:
        raise HTTPException(status_code=500, detail="Failed to start SUMO simulation")


@app.post("/api/sumo/stop")
async def stop_sumo():
    """Stop SUMO simulation"""
    if not iot_service:
        raise HTTPException(status_code=400, detail="SUMO service not initialized")
    
    iot_service.stop()
    return {"success": True, "message": "SUMO simulation stopped"}


@app.get("/api/sumo/status")
async def get_sumo_status():
    """Get SUMO service status"""
    if not iot_service:
        return {"enabled": False, "message": "SUMO service not initialized"}
    
    return iot_service.get_status()


@app.post("/api/sumo/phase")
async def set_sumo_phase(request: CommandRequest):
    """Set traffic light phase in SUMO"""
    if not iot_service:
        raise HTTPException(status_code=400, detail="SUMO service not initialized")
    
    success = iot_service.set_phase(request.phase)
    if success:
        return {"success": True, "phase": request.phase}
    else:
        raise HTTPException(status_code=500, detail="Failed to set phase")


if __name__ == "__main__":
    import uvicorn
    
    print("""
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║         🚦 GreenWave Backend Server (Python) 🚦          ║
║                                                           ║
║  HTTP API:       http://localhost:{port}                    ║
║  WebSocket:      ws://localhost:{port}/ws                   ║
║  Orion Broker:   {orion_url}                             ║
║  Traffic Light:  {tls_id}                                ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
    """.format(
        port=settings.port,
        orion_url=settings.orion_url,
        tls_id=settings.tls_id
    ))
    
    uvicorn.run(
        "src.main:app",
        host=settings.host,
        port=settings.port,
        reload=True,
        log_level="info"
    )
