"""
SUMO Control Router
API endpoints để control SUMO simulation và lấy real-time data
Hỗ trợ 2 modes:
1. Connect to existing SUMO (recommended - không cần SUMO_HOME)
2. Start new SUMO instance (cần SUMO_HOME)

Updated: 2025-11-30 - Added TraCI connector support
"""
import logging
import time
import os
from typing import Dict, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.sumo_rl.agents.smart_traffic_controller import SmartTrafficController
from app.sumo_rl.agents.traci_connector import TraCIConnector

router = APIRouter(prefix="/sumo", tags=["SUMO Control"])
logger = logging.getLogger(__name__)

# Global TraCI connector instance (singleton)
traci_connector: Optional[TraCIConnector] = None

# Smart controllers for each traffic light (one per TLS)
smart_controllers: Dict[str, SmartTrafficController] = {}


class ConnectSimulationRequest(BaseModel):
    """Connect to running SUMO instance"""
    host: str = "localhost"
    port: int = 8813
    scenario: str = "Nga4ThuDuc"


class StartSimulationRequest(BaseModel):
    """Start new SUMO instance (requires SUMO_HOME)"""
    scenario: str = "Nga4ThuDuc"
    gui: bool = True
    port: int = 8813


class SetPhaseRequest(BaseModel):
    phase_index: int


class SetPhaseWithCountdownRequest(BaseModel):
    """Set phase with countdown timer for safety"""
    phase_index: int
    countdown_seconds: int = 5  # Default 5 seconds countdown


def start_sumo_on_host(scenario: str) -> bool:
    """
    Start SUMO on host machine via HTTP service
    
    Calls the SUMO Starter Service running on the host (port 9999)
    This service executes the start_sumo.sh script on the host.
    
    Returns:
        True if SUMO started successfully
    """
    try:
        import requests
        
        # Call the SUMO starter service on the host
        url = "http://172.17.0.1:9999/start"
        payload = {"scenario": scenario}
        
        logger.info(f"Calling SUMO starter service at {url} for scenario: {scenario}")
        
        response = requests.post(url, json=payload, timeout=20)
        
        if response.status_code == 200:
            result = response.json()
            logger.info(f"SUMO started successfully: {result.get('message')}")
            return True
        else:
            error = response.json() if response.headers.get('content-type') == 'application/json' else response.text
            logger.error(f"Failed to start SUMO: {error}")
            return False
            
    except requests.exceptions.ConnectionError:
        logger.error("Cannot connect to SUMO starter service at http://172.17.0.1:9999")
        logger.error("Please start it on the host with: python /scripts/sumo_starter_service.py")
        return False
    except Exception as e:
        logger.error(f"Error starting SUMO: {e}")
        return False


# --- SUMO Control Endpoints ---

@router.post("/connect")
async def connect_to_simulation(request: ConnectSimulationRequest):
    """
    Connect to running SUMO simulation (RECOMMENDED)
    
    Prerequisites:
    1. Start SUMO manually with TraCI:
       sumo-gui -c <config> --remote-port 8813 --start
    
    2. Call this endpoint to connect
    
    Scenarios:
    - Nga4ThuDuc: Ngã tư Thủ Đức (4-way intersection)
    - NguyenThaiSon: Ngã 6 Nguyễn Thái Sơn (6-way intersection)
    - QuangTrung: Quang Trung (Complex intersection)
    """
    global traci_connector
    
    try:
        # Create connector if not exists
        if traci_connector is None:
            traci_connector = TraCIConnector()
        
        # Connect to SUMO
        success = traci_connector.connect(
            host=request.host,
            port=request.port,
            scenario=request.scenario
        )
        
        if not success:
            raise HTTPException(
                status_code=500,
                detail="Failed to connect to SUMO. Make sure SUMO is running with --remote-port 8813"
            )
        
        # Get initial state
        state = traci_connector.get_traffic_state()
        scenario_info = traci_connector.get_scenario_info()
        
        return {
            "status": "connected",
            "message": "Successfully connected to SUMO",
            **scenario_info,
            "initial_state": state
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to connect to SUMO: {e}")
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("/start")
async def start_simulation(request: StartSimulationRequest):
    """
    Start SUMO simulation - AUTOMATED with FALLBACK
    
    Attempts:
    1. Start on Host (via starter service)
    2. Fallback: Connect directly to 'sumo-simulation' container
    """
    global traci_connector
    
    # Track errors to report if all methods fail
    errors = []
    
    # HOT SWAP TRIGGER
    # Write requested scenario to shared volume to trigger SUMO hot-reload if needed
    try:
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        trigger_file = os.path.join(base_path, "app", "sumo_rl", "sumo_files", "current_scenario.txt")
        
        # Verify if file exists (it should be mounted)
        # We only write if the content is different to avoid unnecessary restarts if launcher logic changes
        current_content = ""
        if os.path.exists(trigger_file):
            with open(trigger_file, "r") as f:
                current_content = f.read().strip()
        
        if current_content != request.scenario:
            logger.info(f"REQUESTING SCENARIO SWITCH: {request.scenario}")
            with open(trigger_file, "w") as f:
                f.write(request.scenario)
            
            # Wait a bit for the launcher to restart SUMO
            logger.info("Waiting for SUMO to restart with new scenario...")
            time.sleep(5) 
    except Exception as e:
        logger.warning(f"Failed to write hot-swap trigger file: {e}")

    # METHOD 1: Try Host Starter Service
    host_started = False
    try:
        logger.info(f"Method 1: Attempting to start SUMO on host via starter service...")
        if start_sumo_on_host(request.scenario):
            logger.info("Host starter service returned success. Waiting for initialization...")
            time.sleep(3)
            
            # Connect via TraCI using Docker Bridge IP
            if traci_connector is None:
                traci_connector = TraCIConnector()
            elif traci_connector.is_connected():
                traci_connector.close()
                
            success = traci_connector.connect(
                host="172.17.0.1",
                port=request.port,
                scenario=request.scenario
            )
            
            if success:
                return _build_connection_response(request.scenario, "connected_host")
            else:
                 errors.append("Host starter succeeded but TraCI connection failed")
        else:
             errors.append("Host starter service returned failure")
             
    except Exception as e:
        logger.warning(f"Method 1 failed: {e}")
        errors.append(f"Host starter exception: {e}")

    # METHOD 2: Fallback to Direct Container Connection (Headless/Containerized)
    logger.info("Method 2: Falling back to direct container connection (sumo-simulation)...")
    try:
        if traci_connector is None:
            traci_connector = TraCIConnector()
        elif traci_connector.is_connected():
            traci_connector.close()
            
        target_host = os.getenv("SUMO_HOST", "sumo-simulation")
        
        # Determine port - if running in same network, use 8813
        # If testing locally outside docker, might need localhost
        success = traci_connector.connect(
            host=target_host,
            port=request.port, # default 8813
            scenario=request.scenario
        )
        
        if success:
            return _build_connection_response(request.scenario, "connected_container_fallback")
        else:
            errors.append(f"Direct connection to {target_host}:{request.port} failed")
            
    except Exception as e:
        logger.error(f"Method 2 failed: {e}")
        errors.append(f"Direct connection exception: {e}")

    # If we get here, all methods failed
    error_msg = "; ".join(errors)
    logger.error(f"All SUMO start methods failed. Errors: {error_msg}")
    raise HTTPException(
        status_code=500, 
        detail=f"Failed to start/connect to SUMO. Details: {error_msg}"
    )

def _build_connection_response(scenario, mode):
    global traci_connector
    state = traci_connector.get_traffic_state()
    scenario_info = traci_connector.get_scenario_info()
    return {
        "status": "connected",
        "mode": mode,
        "message": f"Successfully connected to SUMO scenario {scenario}",
        **scenario_info,
        "initial_state": state
    }



@router.post("/stop")
async def stop_simulation():
    """Disconnect from SUMO simulation"""
    global traci_connector
    
    try:
        if traci_connector is None or not traci_connector.is_connected():
            raise HTTPException(status_code=400, detail="No simulation connected")
        
        traci_connector.close()
        
        return {"status": "disconnected"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to disconnect: {e}")
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("/step")
async def simulation_step():
    """Execute one simulation step"""
    global traci_connector
    
    try:
        if traci_connector is None or not traci_connector.is_connected():
            raise HTTPException(status_code=400, detail="No simulation connected")
        
        sim_time = traci_connector.step()
        if sim_time is None:
            raise HTTPException(status_code=500, detail="Failed to step simulation")
        
        state = traci_connector.get_traffic_state()
        
        return {
            "status": "ok",
            "time": sim_time,
            "state": state
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to step simulation: {e}")
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/state")
async def get_current_state():
    """
    Get current traffic state from SUMO
    Returns real-time metrics: vehicle count, speed, occupancy, etc.
    """
    global traci_connector
    
    try:
        if traci_connector is None or not traci_connector.is_connected():
            raise HTTPException(status_code=400, detail="No simulation connected")
        
        state = traci_connector.get_traffic_state()
        
        if state is None:
            raise HTTPException(status_code=500, detail="Failed to get traffic state")
        
        return state
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get state: {e}")
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("/set-phase")
async def set_traffic_light_phase(request: SetPhaseRequest):
    """
    Manually set traffic light phase with SAFE TRANSITIONS
    
    The system will automatically insert yellow phases when needed
    to prevent dangerous green->red transitions.
    
    Phase indices vary by scenario - use GET /sumo/phases to see available phases
    """
    global traci_connector
    
    try:
        if traci_connector is None or not traci_connector.is_connected():
            raise HTTPException(status_code=400, detail="No simulation connected")
        
        success = traci_connector.set_phase(request.phase_index)
        
        if not success:
            raise HTTPException(status_code=500, detail="Failed to set phase")
        
        state = traci_connector.get_traffic_state()
        
        return {
            "status": "ok",
            "phase_index": request.phase_index,
            "current_phase": state['current_phase'] if state else None,
            "message": "Phase change initiated with safe transition"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to set phase: {e}")
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/phases")
async def get_traffic_light_phases():
    """
    Get all available traffic light phases for current scenario
    
    Returns detailed information about each phase including:
    - Phase index
    - Signal state (G=green, y=yellow, r=red)
    - Duration
    - Min/Max durations
    """
    global traci_connector
    
    try:
        if traci_connector is None or not traci_connector.is_connected():
            raise HTTPException(status_code=400, detail="No simulation connected")
        
        import traci
        
        tls_id = traci_connector.tls_id
        all_programs = traci.trafficlight.getAllProgramLogics(tls_id)
        
        if not all_programs:
            raise HTTPException(status_code=500, detail="No signal program found")
        
        program = all_programs[0]
        phases_info = []
        
        for idx, phase in enumerate(program.phases):
            # Interpret the phase state
            phase_type = "unknown"
            if 'G' in phase.state or 'g' in phase.state:
                if 'y' not in phase.state.lower():
                    phase_type = "green"
                else:
                    phase_type = "transition"
            elif 'y' in phase.state.lower():
                phase_type = "yellow"
            elif 'r' in phase.state or 'R' in phase.state:
                phase_type = "red"
            
            phases_info.append({
                "index": idx,
                "state": phase.state,
                "type": phase_type,
                "duration": phase.duration,
                "minDur": phase.minDur,
                "maxDur": phase.maxDur,
                "description": f"Phase {idx} - {phase_type}"
            })
        
        return {
            "tls_id": tls_id,
            "program_id": program.programID,
            "current_phase": traci.trafficlight.getPhase(tls_id),
            "phases": phases_info,
            "total_phases": len(phases_info)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get phases: {e}")
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("/set-phase-countdown")
async def set_phase_with_countdown(request: SetPhaseWithCountdownRequest):
    """
    Set traffic light phase with COUNTDOWN TIMER for maximum safety
    
    This provides advance warning to drivers before phase changes:
    1. Shows countdown timer on dashboard
    2. Waits for countdown to complete
    3. Then changes phase with safe yellow transition
    
    This prevents sudden braking and accidents!
    """
    global traci_connector
    
    try:
        if traci_connector is None or not traci_connector.is_connected():
            raise HTTPException(status_code=400, detail="No simulation connected")
        
        # Return countdown status - actual phase change happens on frontend after countdown
        return {
            "status": "countdown_started",
            "phase_index": request.phase_index,
            "countdown_seconds": request.countdown_seconds,
            "message": f"Countdown {request.countdown_seconds}s before switching to phase {request.phase_index}"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to start countdown: {e}")
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("/ai-control")
async def enable_ai_traffic_control():
    """
    Bật AI điều khiển giao thông THÔNG MINH
    
    Khác với manual phase control, AI sẽ:
    1. Phân tích traffic tại MỖI đèn giao thông
    2. Tính toán phase tối ưu DỰA TRÊN:
       - Mật độ xe (occupancy)
       - Số xe chờ (queue length)  
       - Thời gian chờ (waiting time)
    3. Chỉ cho ĐÈN XANH tại những hướng CẦN THIẾT
    4. Đảm bảo không xung đột (không toàn đèn xanh!)
    
    Đây mới là điều hướng giao thông ĐÚNG NGHĨA!
    """
    global traci_connector, smart_controllers
    
    try:
        if traci_connector is None or not traci_connector.is_connected():
            raise HTTPException(status_code=400, detail="No simulation connected")
        
        import traci
        
        # Get all traffic lights in current scenario
        all_tls_ids = traci.trafficlight.getIDList()
        
        if not all_tls_ids:
            raise HTTPException(status_code=500, detail="No traffic lights found")
        
        # Initialize smart controller for each traffic light
        smart_controllers.clear()
        for tls_id in all_tls_ids:
            smart_controllers[tls_id] = SmartTrafficController(
                tls_id=tls_id,
                min_green_time=10  # Minimum 10s green time
            )
        
        logger.info(f"✅ AI Traffic Control enabled for {len(smart_controllers)} traffic lights")
        
        return {
            "status": "enabled",
            "message": "AI Traffic Control activated",
            "num_traffic_lights": len(smart_controllers),
            "traffic_lights": list(smart_controllers.keys()),
            "algorithm": "Smart Priority-Based Phase Selection",
            "features": [
                "Phân tích mật độ xe theo thời gian thực",
                "Tính toán phase tối ưu cho từng đèn",
                "Đèn xanh chỉ cho hướng ưu tiên cao",
                "Tránh xung đột giao thông",
                "Thời gian xanh tối thiểu 10s"
            ]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to enable AI control: {e}")
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("/ai-step")
async def ai_traffic_control_step():
    """
    Thực hiện MỘT BƯỚC điều khiển AI
    
    AI sẽ:
    1. Phân tích traffic tại mỗi đèn
    2. Chọn phase tối ưu
    3. Thực thi quyết định
    
    Returns:
        Decisions made for each traffic light
    """
    global traci_connector, smart_controllers
    
    try:
        if traci_connector is None or not traci_connector.is_connected():
            raise HTTPException(status_code=400, detail="No simulation connected")
        
        if not smart_controllers:
            raise HTTPException(
                status_code=400, 
                detail="AI control not enabled. Call POST /sumo/ai-control first"
            )
        
        import traci
        
        decisions = []
        
        # Process each traffic light independently
        for tls_id, controller in smart_controllers.items():
            try:
                # Let AI select best phase based on traffic
                best_phase = controller.select_best_phase()
                current_phase = traci.trafficlight.getPhase(tls_id)
                
                # Apply if different
                if best_phase != current_phase:
                    logger.info(f"🚦 TLS {tls_id}: Switching {current_phase} → {best_phase}")
                    traci.trafficlight.setPhase(tls_id, best_phase)
                    
                    decisions.append({
                        "tls_id": tls_id,
                        "action": "switch",
                        "from_phase": current_phase,
                        "to_phase": best_phase,
                        "explanation": controller.get_phase_explanation(best_phase)
                    })
                else:
                    decisions.append({
                        "tls_id": tls_id,
                        "action": "hold",
                        "current_phase": current_phase,
                        "explanation": controller.get_phase_explanation(current_phase)
                    })
                    
            except Exception as e:
                logger.error(f"Error controlling TLS {tls_id}: {e}")
                decisions.append({
                    "tls_id": tls_id,
                    "action": "error",
                    "error": str(e)
                })
        
        return {
            "status": "ok",
            "simulation_time": traci.simulation.getTime(),
            "decisions": decisions,
            "num_controlled": len([d for d in decisions if d['action'] != 'error'])
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed AI control step: {e}")
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/scenarios")
async def list_scenarios():
    """List all available SUMO scenarios"""
    return {
        "scenarios": [
            {
                "id": "Nga4ThuDuc",
                "name": "Ngã Tư Thủ Đức",
                "description": "4-way intersection in Thu Duc",
                "tls_id": "4066470692"
            },
            {
                "id": "NguyenThaiSon",
                "name": "Ngã 6 Nguyễn Thái Sơn",
                "description": "6-way intersection on Nguyen Thai Son street",
                "tls_id": "11777727352"
            },
            {
                "id": "QuangTrung",
                "name": "Quang Trung",
                "description": "Complex intersection on Quang Trung street",
                "tls_id": "cluster_314061834_314061898"
            }
        ]
    }


@router.get("/status")
async def get_simulation_status():
    """Get SUMO simulation connection status"""
    global traci_connector
    
    if traci_connector is None or not traci_connector.is_connected():
        return {
            "connected": False,
            "scenario": None,
            "message": "Not connected to SUMO. Start SUMO with: sumo-gui -c <config> --remote-port 8813 --start"
        }
    
    info = traci_connector.get_scenario_info()
    state = traci_connector.get_traffic_state()
    
    return {
        **info,
        "current_state": state
    }
