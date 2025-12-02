"""
IoT Agent - SUMO Simulation Controller
Receives commands from Orion → Applies to SUMO via TraCI
"""
import logging
from typing import Dict, Any, Optional
import sys
import os

logger = logging.getLogger(__name__)


class IoTAgent:
    """
    IoT Agent for controlling SUMO traffic simulation
    Receives TrafficLight commands → Applies to SUMO
    """
    
    def __init__(self, sumo_connection=None):
        """
        Initialize IoT Agent
        
        Args:
            sumo_connection: Optional TraCI connection (for testing)
        """
        self.traci = sumo_connection
        self.sumo_connected = sumo_connection is not None
        
        logger.info("[IoT Agent] Initialized")
        logger.info(f"  SUMO Connected: {self.sumo_connected}")
    
    def connect_sumo(self, sumo_config: list):
        """
        Connect to SUMO simulation
        
        Args:
            sumo_config: SUMO command line configuration
        """
        try:
            if 'SUMO_HOME' in os.environ:
                tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
                sys.path.append(tools)
            else:
                logger.warning("[IoT Agent] SUMO_HOME not set")
                return False
            
            import traci
            
            traci.start(sumo_config)
            self.traci = traci
            self.sumo_connected = True
            
            logger.info("[IoT Agent] ✅ Connected to SUMO")
            return True
            
        except Exception as e:
            logger.error(f"[IoT Agent] Error connecting to SUMO: {e}")
            return False
    
    def disconnect_sumo(self):
        """Disconnect from SUMO"""
        if self.traci and self.sumo_connected:
            try:
                self.traci.close()
                self.sumo_connected = False
                logger.info("[IoT Agent] Disconnected from SUMO")
            except Exception as e:
                logger.error(f"[IoT Agent] Error disconnecting: {e}")
    
    def process_notification(self, notification_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process notification from Orion-LD with TrafficLight commands
        
        Args:
            notification_data: NGSI-LD notification
        
        Returns:
            dict with application result
        """
        try:
            entities = notification_data.get('data', [])
            
            for entity in entities:
                if entity.get('type') == 'TrafficLight':
                    entity_id = entity.get('id', '')
                    
                    force_phase_attr = entity.get('forcePhase', {})
                    if force_phase_attr:
                        phase_index = force_phase_attr.get('value')
                        
                        if phase_index is not None and phase_index >= 0:
                            logger.info(f"[IoT Agent] Received command: forcePhase={phase_index}")
                            
                            # Apply to SUMO if connected
                            if self.sumo_connected and self.traci:
                                success = self.apply_phase(phase_index, entity_id)
                                return {"applied": success, "phase": phase_index}
                            else:
                                logger.warning("[IoT Agent] SUMO not connected - command logged only")
                                return {"applied": False, "phase": phase_index, "reason": "sumo_not_connected"}
            
            return {"applied": False, "reason": "no_command"}
            
        except Exception as e:
            logger.error(f"[IoT Agent] Error processing notification: {e}")
            raise
    
    def apply_phase(self, phase_index: int, tls_id: str) -> bool:
        """
        Apply phase to traffic light in SUMO
        
        Args:
            phase_index: Target phase
            tls_id: Traffic light ID (URN format)
        
        Returns:
            Success status
        """
        if not self.sumo_connected or not self.traci:
            logger.warning("[IoT Agent] Cannot apply phase - SUMO not connected")
            return False
        
        try:
            # Extract actual TLS ID from URN
            # urn:ngsi-ld:TrafficLight:4066470692 → 4066470692
            actual_tls_id = tls_id.split(':')[-1]
            
            self.traci.trafficlight.setPhase(actual_tls_id, phase_index)
            logger.info(f"[IoT Agent] ✅ Applied phase {phase_index} to {actual_tls_id}")
            return True
            
        except Exception as e:
            logger.error(f"[IoT Agent] Error applying phase: {e}")
            return False
    
    def get_traffic_state(self, tls_id: str, detector_ids: list) -> Dict[str, Any]:
        """
        Get current traffic state from SUMO
        
        Args:
            tls_id: Traffic light ID
            detector_ids: List of detector IDs
        
        Returns:
            State dictionary
        """
        if not self.sumo_connected or not self.traci:
            return {"error": "SUMO not connected"}
        
        try:
            queues = [self.traci.lanearea.getLastStepVehicleNumber(det) for det in detector_ids]
            phase = self.traci.trafficlight.getPhase(tls_id)
            
            return {
                "queues": queues,
                "phase": phase,
                "connected": True
            }
            
        except Exception as e:
            logger.error(f"[IoT Agent] Error getting state: {e}")
            return {"error": str(e)}
    
    def get_status(self) -> Dict[str, Any]:
        """Get agent status"""
        return {
            "agent": "IoT Agent",
            "sumo_connected": self.sumo_connected,
            "traci_available": self.traci is not None
        }
