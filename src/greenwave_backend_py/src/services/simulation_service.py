"""
Service that orchestrates simulation data flow
"""
import asyncio
import logging
from typing import Optional
from datetime import datetime

from .orion_service import OrionService
from .websocket_service import WebSocketService
from ..models.simulation import SimulationState, TrafficLightState

logger = logging.getLogger(__name__)


class SimulationService:
    """Orchestrates simulation data flow between Orion and WebSocket clients"""
    
    def __init__(
        self,
        orion_service: OrionService,
        ws_service: WebSocketService,
        tls_id: str,
        update_interval: int = 2000
    ):
        self.orion_service = orion_service
        self.ws_service = ws_service
        self.tls_id = tls_id
        self.update_interval = update_interval / 1000.0  # Convert to seconds
        self.is_running = False
        self.task: Optional[asyncio.Task] = None
    
    def start(self):
        """Start the simulation loop"""
        if self.is_running:
            logger.warning("Simulation already running")
            return
        
        logger.info(f"Starting simulation with update interval: {self.update_interval}s")
        self.is_running = True
        self.task = asyncio.create_task(self._simulation_loop())
    
    def stop(self):
        """Stop the simulation loop"""
        if not self.is_running:
            return
        
        logger.info("Stopping simulation")
        self.is_running = False
        
        if self.task:
            self.task.cancel()
            self.task = None
    
    async def _simulation_loop(self):
        """Main simulation loop"""
        try:
            while self.is_running:
                await self._fetch_and_broadcast()
                await asyncio.sleep(self.update_interval)
        except asyncio.CancelledError:
            logger.info("Simulation loop cancelled")
        except Exception as e:
            logger.error(f"Error in simulation loop: {e}")
    
    async def _fetch_and_broadcast(self):
        """Fetch data from Orion and broadcast to WebSocket clients"""
        try:
            # Fetch traffic flow and air quality in parallel
            traffic_flow, air_quality = await asyncio.gather(
                self.orion_service.get_traffic_flow(self.tls_id),
                self.orion_service.get_air_quality(self.tls_id),
                return_exceptions=True
            )
            
            if not traffic_flow or not air_quality:
                logger.warning("Missing data from Orion")
                return
            
            # Calculate reward (same formula as in dashboard)
            reward = -(traffic_flow.queues[0] + traffic_flow.queues[1]) * 0.6 - (air_quality.pm25 / 100) * 0.4
            
            # Build simulation state
            state = SimulationState(
                vehicles=[],  # Will be populated from SUMO TraCI if needed
                traffic_lights=[
                    TrafficLightState(
                        id=self.tls_id,
                        state=self._get_traffic_light_state(traffic_flow.phase),
                        phase=traffic_flow.phase,
                        program="default"
                    )
                ],
                traffic_flow=traffic_flow,
                air_quality=air_quality,
                reward=reward
            )
            
            # Broadcast to all connected clients
            await self.ws_service.broadcast_simulation_state(state)
            
            # Log occasionally (10% of the time)
            import random
            if random.random() < 0.1:
                logger.info(
                    f"State: queues={traffic_flow.queues}, phase={traffic_flow.phase}, "
                    f"pm25={air_quality.pm25:.2f}, reward={reward:.2f}, "
                    f"clients={self.ws_service.get_client_count()}"
                )
            
        except Exception as e:
            logger.error(f"Error fetching data: {e}")
            await self.ws_service.broadcast_error("Failed to fetch simulation data")
    
    def _get_traffic_light_state(self, phase: int) -> str:
        """Convert phase number to traffic light state string"""
        # Phase 0: East-West green, North-South red
        # Phase 1: East-West red, North-South green
        phase_map = {
            0: "GrGr",  # Green-red-Green-red
            1: "rGrG",  # red-Green-red-Green
            2: "yryy",  # yellow transition
        }
        return phase_map.get(phase, "rrrr")  # all red (safety)
    
    async def set_phase(self, phase: int) -> bool:
        """Send command to change traffic light phase"""
        logger.info(f"Setting phase to {phase}")
        success = await self.orion_service.set_traffic_light_phase(self.tls_id, phase)
        
        if success:
            # Immediately fetch and broadcast new state
            await asyncio.sleep(0.2)
            await self._fetch_and_broadcast()
        
        return success
    
    def is_active(self) -> bool:
        """Get current running status"""
        return self.is_running
