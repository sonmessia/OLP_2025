"""
IoT Service for SUMO simulation integration via TraCI
"""
import os
import sys
import logging
from typing import Optional, Callable, Dict, Any, List
from threading import Thread, Event
import time

logger = logging.getLogger(__name__)


class IoTService:
    """Service for SUMO simulation integration"""
    
    def __init__(
        self,
        sumo_config_path: str,
        tls_id: str,
        detector_ids: List[str],
        edge_ids: List[str],
        use_gui: bool = False,
        step_length: float = 1.0
    ):
        """
        Initialize IoT Service
        
        Args:
            sumo_config_path: Path to SUMO config file (.sumocfg)
            tls_id: Traffic light system ID
            detector_ids: List of detector IDs for queue measurement
            edge_ids: List of edge IDs for emission calculation
            use_gui: Whether to use SUMO GUI
            step_length: Simulation step length in seconds
        """
        self.sumo_config_path = sumo_config_path
        self.tls_id = tls_id
        self.detector_ids = detector_ids
        self.edge_ids = edge_ids
        self.use_gui = use_gui
        self.step_length = step_length
        
        # SUMO connection
        self.traci = None
        self.is_connected = False
        self.is_running = False
        
        # Simulation thread
        self.sim_thread: Optional[Thread] = None
        self.stop_event = Event()
        
        # Callbacks
        self.state_update_callback: Optional[Callable[[Dict[str, Any]], None]] = None
        
        # State tracking
        self.current_step = 0
        self.current_state: Optional[Dict[str, Any]] = None
        
        self._check_sumo_home()
    
    def _check_sumo_home(self):
        """Check if SUMO_HOME is set"""
        if 'SUMO_HOME' not in os.environ:
            logger.warning("SUMO_HOME environment variable not set")
            logger.warning("Please set SUMO_HOME to use SUMO simulation")
        else:
            tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
            if tools not in sys.path:
                sys.path.append(tools)
            logger.info(f"SUMO_HOME: {os.environ['SUMO_HOME']}")
    
    def set_state_update_callback(self, callback: Callable[[Dict[str, Any]], None]):
        """Set callback for state updates"""
        self.state_update_callback = callback
    
    def start(self) -> bool:
        """Start SUMO simulation"""
        if self.is_running:
            logger.warning("Simulation already running")
            return False
        
        try:
            # Import traci
            import traci
            self.traci = traci
            
            # Build SUMO command
            sumo_binary = 'sumo-gui' if self.use_gui else 'sumo'
            sumo_cmd = [
                sumo_binary,
                '-c', self.sumo_config_path,
                '--step-length', str(self.step_length),
            ]
            
            logger.info(f"Starting SUMO: {' '.join(sumo_cmd)}")
            
            # Start SUMO
            traci.start(sumo_cmd)
            self.is_connected = True
            
            # Start simulation thread
            self.stop_event.clear()
            self.sim_thread = Thread(target=self._simulation_loop, daemon=True)
            self.sim_thread.start()
            
            self.is_running = True
            logger.info("SUMO simulation started")
            return True
            
        except ImportError:
            logger.error("traci module not found. Please install SUMO and set SUMO_HOME")
            return False
        except Exception as e:
            logger.error(f"Error starting SUMO: {e}")
            return False
    
    def stop(self):
        """Stop SUMO simulation"""
        if not self.is_running:
            logger.warning("Simulation not running")
            return
        
        logger.info("Stopping SUMO simulation...")
        self.stop_event.set()
        
        # Wait for thread to finish
        if self.sim_thread:
            self.sim_thread.join(timeout=5.0)
        
        # Close TraCI connection
        if self.is_connected and self.traci:
            try:
                self.traci.close()
            except Exception as e:
                logger.error(f"Error closing TraCI: {e}")
        
        self.is_connected = False
        self.is_running = False
        logger.info("SUMO simulation stopped")
    
    def _simulation_loop(self):
        """Main simulation loop (runs in separate thread)"""
        try:
            while not self.stop_event.is_set():
                # Check if simulation is still active
                if self.traci.simulation.getMinExpectedNumber() <= 0:
                    logger.info("No more vehicles in simulation")
                    break
                
                # Perform simulation step
                self.traci.simulationStep()
                self.current_step += 1
                
                # Get current state
                state = self._get_state_from_sumo()
                self.current_state = state
                
                # Call state update callback
                if self.state_update_callback:
                    self.state_update_callback(state)
                
                # Log periodically
                if self.current_step % 100 == 0:
                    logger.info(f"Step {self.current_step} | State: {state}")
                
        except Exception as e:
            logger.error(f"Error in simulation loop: {e}")
        finally:
            self.is_running = False
            logger.info("Simulation loop ended")
    
    def _get_state_from_sumo(self) -> Dict[str, Any]:
        """Get current state from SUMO"""
        try:
            # Get queue lengths from detectors
            queues = [
                self.traci.lanearea.getLastStepVehicleNumber(det)
                for det in self.detector_ids
            ]
            
            # Get current traffic light phase
            phase = self.traci.trafficlight.getPhase(self.tls_id)
            
            # Calculate PM2.5 emissions
            total_pm25 = sum(
                self.traci.edge.getPMxEmission(edge)
                for edge in self.edge_ids
            )
            
            # Get vehicle count
            vehicle_count = self.traci.vehicle.getIDCount()
            
            return {
                "queues": queues,
                "phase": phase,
                "pm25": total_pm25,
                "vehicle_count": vehicle_count,
                "step": self.current_step
            }
        except Exception as e:
            logger.error(f"Error getting state from SUMO: {e}")
            return {
                "queues": [0] * len(self.detector_ids),
                "phase": 0,
                "pm25": 0,
                "vehicle_count": 0,
                "step": self.current_step
            }
    
    def set_phase(self, phase: int) -> bool:
        """Set traffic light phase"""
        if not self.is_connected or not self.traci:
            logger.warning("SUMO not connected")
            return False
        
        try:
            self.traci.trafficlight.setPhase(self.tls_id, phase)
            logger.info(f"Set traffic light {self.tls_id} to phase {phase}")
            return True
        except Exception as e:
            logger.error(f"Error setting phase: {e}")
            return False
    
    def get_status(self) -> dict:
        """Get IoT service status"""
        return {
            "is_connected": self.is_connected,
            "is_running": self.is_running,
            "current_step": self.current_step,
            "sumo_config": self.sumo_config_path,
            "tls_id": self.tls_id,
            "use_gui": self.use_gui,
            "current_state": self.current_state
        }
