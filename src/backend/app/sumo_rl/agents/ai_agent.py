"""
AI GreenWave Agent - Decision Making Component
Chuyển đổi từ Flask sang FastAPI Service
"""

# Import asyncio at module level
import asyncio
import logging
from typing import Any, Dict, Optional

import httpx

from app.sumo_rl.config import config
from app.sumo_rl.models.dqn_model import DQNModel

logger = logging.getLogger(__name__)


class AIGreenWaveAgent:
    """
    AI Agent for traffic light control using DQN
    Receives traffic data → Makes decisions → Sends commands
    """

    def __init__(self, model_path: Optional[str] = None):
        self.config = config
        self.model = DQNModel(
            model_path=model_path or self.config.model_path,
            state_size=self.config.state_size,
            action_size=self.config.action_size,
        )

        logger.info("[AI Agent] Initialized")
        logger.info(f"  Model: {self.model.model_path}")
        logger.info(f"  Loaded: {self.model.loaded}")
        logger.info(f"  Orion: {self.config.orion_url}")

    def process_notification(self, notification_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process notification from Orion-LD

        Args:
            notification_data: NGSI-LD notification with traffic/environment entities

        Returns:
            dict with action result
        """
        try:
            entities = notification_data.get("data", [])

            # Extract required entities
            traffic_ent = next(
                (e for e in entities if e["type"] == "TrafficFlowObserved"), None
            )
            air_ent = next(
                (e for e in entities if e["type"] == "AirQualityObserved"), None
            )
            impact_ent = next(
                (e for e in entities if e["type"] == "TrafficEnvironmentImpact"), None
            )

            if not traffic_ent or not air_ent:
                logger.warning("[AI Agent] Missing required entities")
                return {"action": "skip", "reason": "incomplete_data"}

            # Parse state
            queues = traffic_ent.get("queues", {}).get("value", [0, 0])
            phase = traffic_ent.get("phase", {}).get("value", 0)
            pm25 = air_ent.get("pm25", {}).get("value", 0)

            # State tuple: (queue_1, queue_2, phase, pm25)
            state = (*queues, phase, pm25)

            # Log environmental impact (optional)
            if impact_ent:
                co2 = impact_ent.get("co2", {}).get("value", 0)
                avg_speed = impact_ent.get("averageSpeed", {}).get("value", 0)
                logger.debug(f"[AI Agent] Impact - CO2: {co2}g, Speed: {avg_speed}m/s")

            # Get action from DQN model
            action = self.model.predict(state)

            # Apply action
            if action == 1:  # Switch phase
                next_phase = (phase + 1) % self.config.num_phases
                # Send command via Orion
                asyncio.create_task(self.send_command(next_phase))

                logger.info(f"[AI Agent] Decision: SWITCH {phase} → {next_phase}")
                return {
                    "action": "switch",
                    "current_phase": phase,
                    "next_phase": next_phase,
                    "state": list(state),
                }
            else:  # Hold current phase
                logger.debug(f"[AI Agent] Decision: HOLD phase {phase}")
                return {"action": "hold", "current_phase": phase, "state": list(state)}

        except Exception as e:
            logger.error(f"[AI Agent] Error processing notification: {e}")
            raise

    async def send_command(self, next_phase: int):
        """
        Send traffic light command to Orion-LD

        Args:
            next_phase: Target phase index
        """
        url = f"{self.config.orion_url}/entities/urn:ngsi-ld:TrafficLight:{self.config.tls_id}/attrs"
        payload = {"forcePhase": {"type": "Property", "value": int(next_phase)}}

        try:
            async with httpx.AsyncClient() as client:
                response = await client.patch(
                    url,
                    json=payload,
                    headers={"Content-Type": "application/json"},
                    timeout=5.0,
                )

                if response.status_code in [204, 200]:
                    logger.info(f"[AI Agent] ✅ Sent command: forcePhase={next_phase}")
                else:
                    logger.warning(
                        f"[AI Agent] Command response: {response.status_code}"
                    )

        except httpx.ConnectError:
            logger.error(
                f"[AI Agent] Cannot connect to Orion at {self.config.orion_url}"
            )
        except Exception as e:
            logger.error(f"[AI Agent] Error sending command: {e}")

    async def proxy_orion(
        self, method: str, path: str, data: Optional[Dict] = None
    ) -> Dict:
        """
        Proxy requests to Orion-LD (for Dashboard)

        Args:
            method: HTTP method (GET, PATCH, etc.)
            path: URL path
            data: Optional JSON data

        Returns:
            Response from Orion
        """
        url = f"{self.config.orion_url}/{path}"

        try:
            async with httpx.AsyncClient() as client:
                if method == "GET":
                    response = await client.get(
                        url, headers={"Accept": "application/json"}, timeout=5.0
                    )
                elif method == "PATCH":
                    response = await client.patch(
                        url,
                        json=data,
                        headers={"Content-Type": "application/json"},
                        timeout=5.0,
                    )
                else:
                    raise ValueError(f"Unsupported method: {method}")

                if response.status_code == 200:
                    return response.json()
                else:
                    return {"error": response.text, "status_code": response.status_code}

        except Exception as e:
            logger.error(f"[AI Agent] Proxy error: {e}")
            raise

    def get_status(self) -> Dict[str, Any]:
        """Get agent status"""
        return {
            "agent": "AI GreenWave Agent",
            "model_info": self.model.get_info(),
            "orion_url": self.config.orion_url,
            "traffic_light_id": self.config.tls_id,
            "num_phases": self.config.num_phases,
        }
