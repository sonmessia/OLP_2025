"""
SUMO RL Traffic Light Control Router
Chuyển đổi từ Flask sang FastAPI cho AI GreenWave Agent
"""

import logging
from typing import Any, Dict, List

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel

from app.sumo_rl.agents.ai_agent import AIGreenWaveAgent
from app.sumo_rl.agents.iot_agent import IoTAgent

router = APIRouter(prefix="/sumo-rl", tags=["SUMO RL"])
logger = logging.getLogger(__name__)

# Initialize agents lazily (avoid module-level initialization that causes crash loop)
_ai_agent = None
_iot_agent = None


def get_ai_agent():
    """Get or create AI agent singleton"""
    global _ai_agent
    if _ai_agent is None:
        _ai_agent = AIGreenWaveAgent()
    return _ai_agent


def get_iot_agent():
    """Get or create IoT agent singleton"""
    global _iot_agent
    if _iot_agent is None:
        _iot_agent = IoTAgent()
    return _iot_agent


# --- Pydantic Models ---
class CommandRequest(BaseModel):
    """Legacy direct command format"""

    data: List[Dict[str, Any]]


class NotificationData(BaseModel):
    """NGSI-LD Notification format"""

    id: str
    type: str
    # Dynamic fields based on entity type


class OrionNotification(BaseModel):
    """Full Orion notification structure"""

    subscriptionId: str = ""
    data: List[Dict[str, Any]]


# --- AI Agent Endpoints ---
@router.post("/ai/notify")
async def receive_ai_notification(request: Request):
    """
    [AI Agent] Nhận notification từ Orion về traffic & environment data.
    Subscribe 3 entities:
    - TrafficFlowObserved (queues, phase, vehicleCount, avgSpeed)
    - AirQualityObserved (pm25)
    - TrafficEnvironmentImpact (co2, nox, emissions)
    """
    try:
        data = await request.json()
        logger.debug("[AI Agent] Received notification from Orion")

        # Process notification and make decision
        ai_agent = get_ai_agent()
        result = ai_agent.process_notification(data)

        return {"status": "ok", **result}

    except Exception as e:
        logger.error(f"[AI Agent] Error processing notification: {e}")
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("/ai/cmd")
async def receive_ai_command(cmd_data: CommandRequest):
    """
    [AI Agent - LEGACY] Direct command endpoint (deprecated).
    Use /ai/notify with NGSI-LD subscriptions instead.
    """
    try:
        logger.warning(
            "[AI Agent] Using legacy /cmd endpoint - consider migrating to /notify"
        )

        # Extract command from legacy format
        ai_agent = get_ai_agent()
        command_data = cmd_data.data[0].get("forcePhase")
        if command_data:
            phase_index = command_data["value"]
            await ai_agent.send_command(phase_index)

        return {"status": "ok"}

    except Exception as e:
        logger.error(f"[AI Agent] Error processing command: {e}")
        raise HTTPException(status_code=500, detail=str(e)) from e


# --- IoT Agent Endpoints ---
@router.post("/iot/notify")
async def receive_iot_notification(request: Request):
    """
    [IoT Agent] Nhận notification từ Orion khi TrafficLight.forcePhase thay đổi.
    Event-driven architecture: Orion → IoT Agent → SUMO
    """
    try:
        data = await request.json()
        logger.debug("[IoT Agent] Received notification from Orion")

        # Apply command to SUMO simulation
        iot_agent = get_iot_agent()
        result = iot_agent.process_notification(data)

        return {"status": "ok", **result}

    except Exception as e:
        logger.error(f"[IoT Agent] Error processing notification: {e}")
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("/iot/cmd")
async def receive_iot_command(cmd_data: CommandRequest):
    """
    [IoT Agent - LEGACY] Direct command endpoint (deprecated).
    Use /iot/notify with NGSI-LD subscriptions instead.
    """
    try:
        logger.warning(
            "[IoT Agent] Using legacy /cmd endpoint - consider migrating to /notify"
        )

        # command_data = cmd_data.data[0].get("forcePhase")
        # if command_data:
        # phase_index = command_data["value"]
        # Direct SUMO control would happen here
        # But we need SUMO connection in service

        return {"status": "ok"}

    except Exception as e:
        logger.error(f"[IoT Agent] Error processing command: {e}")
        raise HTTPException(status_code=500, detail=str(e)) from e


# --- Proxy Endpoints (Dashboard Support) ---
@router.get("/proxy/orion/{path:path}")
async def proxy_orion_get(path: str, request: Request):
    """
    Proxy GET requests to Orion-LD for Dashboard.
    Avoids CORS issues when Dashboard calls Orion directly.
    """
    try:
        ai_agent = get_ai_agent()
        result = await ai_agent.proxy_orion("GET", path)
        return result

    except Exception as e:
        logger.error(f"[Proxy] GET error: {e}")
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.patch("/proxy/orion/{path:path}")
async def proxy_orion_patch(path: str, request: Request):
    """
    Proxy PATCH requests to Orion-LD for Dashboard.
    """
    try:
        ai_agent = get_ai_agent()
        data = await request.json()
        result = await ai_agent.proxy_orion("PATCH", path, data)
        return result

    except Exception as e:
        logger.error(f"[Proxy] PATCH error: {e}")
        raise HTTPException(status_code=500, detail=str(e)) from e


# --- Health & Status Endpoints ---
@router.get("/status")
async def get_status():
    """
    Get current SUMO RL system status.
    Returns model info, SUMO connection status, etc.
    """
    try:
        ai_agent = get_ai_agent()
        iot_agent = get_iot_agent()
        ai_status = ai_agent.get_status()
        iot_status = iot_agent.get_status()

        return {
            "system": "SUMO RL Traffic Control",
            "ai_agent": ai_status,
            "iot_agent": iot_status,
        }

    except Exception as e:
        logger.error(f"[Status] Error: {e}")
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/model-info")
async def get_model_info():
    """
    Get information about loaded DQN model.
    """
    try:
        ai_agent = get_ai_agent()
        info = ai_agent.model.get_info()
        return info

    except Exception as e:
        logger.error(f"[Model Info] Error: {e}")
        raise HTTPException(status_code=500, detail=str(e)) from e
