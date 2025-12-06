# Copyright (c) 2025 Green Wave Team
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

"""
IoT Agent - SUMO Simulation Controller
Receives commands from Orion → Applies to SUMO via TraCI
"""
import logging
import os
import sys
from typing import Any, Dict

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
    
    def connect_sumo(self, sumo_config: list, port: int = 8813):
        """
        Connect to SUMO simulation
        
        Args:
            sumo_config: SUMO command line configuration
            port: Port to listen/connect to
        """
        try:
            if 'SUMO_HOME' in os.environ:
                tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
                sys.path.append(tools)
            else:
                logger.warning("[IoT Agent] SUMO_HOME not set")
                return False
            
            import subprocess
            import time

            import traci
            
            # Use subprocess to start SUMO exactly as requested (no auto-magic arg injection)
            logger.info(f"[IoT Agent] Executing SUMO command: {' '.join(sumo_config)}")
            
            # Start process non-blocking
            self.sumo_proc = subprocess.Popen(sumo_config, stdout=sys.stdout, stderr=sys.stderr)
            
            # Wait for SUMO to initialize and open port (it might wait for clients)
            # With num-clients=2, it waits for client 1.
            time.sleep(2)
            
            # Check if process died immediately (e.g. Display error)
            if self.sumo_proc.poll() is not None:
                logger.error(f"[IoT Agent] SUMO process exited successfully with code {self.sumo_proc.returncode}")
                return False
            
            # Connect as Client
            if port:
                traci.init(port=port)
                traci.setOrder(2) # Order 2: IoT Agent (Master/Last Client) -> Drives Simulation
            else:
                # If no port, traci must guess or use default, but we are explicit now
                traci.init()
                
            self.traci = traci
            self.sumo_connected = True
            
            logger.info(f"[IoT Agent] ✅ Connected to SUMO on port {port}")
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
            
            # Kill process if we started it
            if hasattr(self, 'sumo_proc') and self.sumo_proc:
                self.sumo_proc.kill()

    # ... process_notification, apply_phase, get_traffic_state, get_status remain same ...
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

if __name__ == "__main__":
    import argparse
    import shutil
    
    parser = argparse.ArgumentParser(description='IoT Agent for SUMO')
    parser.add_argument('--scenario', type=str, default='Nga4ThuDuc', help='Scenario name')
    parser.add_argument('--gui', action='store_true', help='Run with GUI')
    args = parser.parse_args()
    
    logging.basicConfig(level=logging.INFO)
    
    # Check if DISPLAY is set
    has_display = os.environ.get('DISPLAY')
    sumo_binary = "sumo-gui" if (args.gui and has_display) else "sumo"
    
    if args.gui and not has_display:
        logging.warning("GUI requested but DISPLAY not set. Falling back to headless 'sumo'.")
    
    # Check if binary exists
    if not shutil.which(sumo_binary):
        logging.error(f"{sumo_binary} not found!")
        exit(1)

    agent = IoTAgent()

    # Check if SUMO_HOME is set
    if 'SUMO_HOME' not in os.environ:
        logger.warning("SUMO_HOME not set, using default /usr/share/sumo")
        os.environ['SUMO_HOME'] = '/usr/share/sumo'
        # Scenario config mapping
    scenario_configs = {
        'Nga4ThuDuc': 'Nga4ThuDuc/Nga4ThuDuc.sumocfg',
        'NguyenThaiSon': 'NguyenThaiSon/Nga6NguyenThaiSon.sumocfg',
        'QuangTrung': 'QuangTrung/quangtrungcar.sumocfg'
    }
    
    if args.scenario in scenario_configs:
         config_rel_path = scenario_configs[args.scenario]
    else:
         # Fallback to default naming convention
         config_rel_path = f"{args.scenario}/{args.scenario}.sumocfg"

    # Try different base paths to find the file
    possible_bases = [
        "/app/sumo_files",  # Container path
        "src/backend/app/sumo_rl/sumo_files", # Host relative path (fallback)
    ]
    
    config_file = None
    for base in possible_bases:
        path = os.path.join(base, config_rel_path)
        if os.path.exists(path):
            config_file = path
            break
            
    if not config_file:
         logger.error(f"Config file not found for scenario {args.scenario} in {possible_bases}")
         # Default fallback that might fail but shows intent
         config_file = os.path.join("/app/sumo_files", config_rel_path)

     # Explicitly construct arguments for subprocess
    # num-clients=2 (REMOVED): Caused blocking/connection closed errors.
    # We use explicit setOrder() in code to manage synchronization instead.
    base_cmd = ["-c", config_file, "--remote-port", "8813"]
    
    # Try GUI first if requested and DISPLAY is set
    success = False
    if args.gui and has_display:
        cmd = ["sumo-gui"] + base_cmd
        logger.info(f"Attempting to start SUMO GUI: {' '.join(cmd)}")
        if agent.connect_sumo(cmd, port=8813):
            success = True
        else:
            logger.warning("Failed to start SUMO GUI (likely Display issues). Falling back to headless.")
            # Ensure previous process is dead if it started but failed connection
            agent.disconnect_sumo()

    # Fallback to headless if GUI failed or not requested
    if not success:
        cmd = ["sumo"] + base_cmd
        logger.info(f"Starting SUMO Headless: {' '.join(cmd)}")
        if not agent.connect_sumo(cmd, port=8813):
            logger.error("Failed to start SUMO Headless. Exiting.")
            exit(1)
    
    # Keep alive loop
    import time
    try:
        while True:
            time.sleep(1)
            # Process Orion notifications or just fetch state
            # In a real deployment, this would be an HTTP server or MQTT client
            # listening for updates. For now, it just keeps the simulation open.
            if agent.sumo_connected and agent.traci:
                try:
                    agent.traci.simulationStep()
                except Exception as e:
                    # Look for specific connection errors
                    if "connection closed" in str(e).lower():
                        logger.error("SUMO connection closed, exiting...")
                        break
                    # If waiting for second client, this might throw?
                    # No, simulationStep usually blocks if waiting.
                    logger.error(f"Simulation step failed: {e}")
                    
    except KeyboardInterrupt:
        agent.disconnect_sumo()
