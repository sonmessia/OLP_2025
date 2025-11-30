"""
TraCI Connector - Connect to running SUMO instance
Không cần SUMO_HOME, chỉ cần SUMO đang chạy với --remote-port
"""
import logging
import os
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

# Try to import traci, but don't fail if not available
_TRACI_AVAILABLE = False
try:
    import traci
    _TRACI_AVAILABLE = True
except ImportError:
    logger.warning("TraCI not available - SUMO features will be disabled")


class TraCIConnector:
    """
    Connect to running SUMO simulation via TraCI
    User phải start SUMO trước với: sumo-gui -c <config> --remote-port 8813
    """
    
    SCENARIOS = {
        'Nga4ThuDuc': {
            'tls_id': '4066470692',
            'description': 'Nga Tu Thu Duc - 4-way intersection'
        },
        'NguyenThaiSon': {
            'tls_id': 'cluster_1488091499_314059003_314059006_314059008',
            'description': 'Nga 6 Nguyen Thai Son - 6-way intersection'
        },
        'QuangTrung': {
            'tls_id': 'cluster_314061834_314061898',
            'description': 'Quang Trung - Complex intersection'
        }
    }
    
    def __init__(self):
        """Initialize TraCI connector"""
        self.connected = False
        self.scenario = None
        self.tls_id = None
        self.host = None
        self.port = None
        self.sumo_process = None  # Store SUMO process if we start it
    
    def start_sumo(self, scenario: str = 'Nga4ThuDuc', gui: bool = False, port: int = 8813) -> bool:
        """
        Start new SUMO process using traci.start()
        
        Args:
            scenario: Scenario name
            gui: Use sumo-gui (True) or sumo (False)
            port: TraCI port
            
        Returns:
            True if started successfully
        """
        if not _TRACI_AVAILABLE:
            logger.error("TraCI not available - cannot start SUMO")
            return False
        
        try:
            # Close existing connection if any
            if self.connected:
                self.close()
            
            # Get scenario config path
            base_path = os.path.join(os.path.dirname(__file__), '..', 'sumo_files')
            
            scenario_configs = {
                'Nga4ThuDuc': os.path.join(base_path, 'Nga4ThuDuc', 'Nga4ThuDuc.sumocfg'),
                'NguyenThaiSon': os.path.join(base_path, 'NguyenThaiSon', 'Nga6NguyenThaiSon.sumocfg'),
                'QuangTrung': os.path.join(base_path, 'QuangTrung', 'quangtrungcar.sumocfg')
            }
            
            if scenario not in scenario_configs:
                logger.error(f"Unknown scenario: {scenario}")
                return False
            
            config_file = scenario_configs[scenario]
            
            if not os.path.exists(config_file):
                logger.error(f"Config file not found: {config_file}")
                return False
            
            # Build SUMO command
            sumo_binary = 'sumo-gui' if gui else 'sumo'
            
            sumo_cmd = [
                sumo_binary,
                '-c', config_file,
                '--remote-port', str(port),
                '--step-length', '1.0',
                '--no-warnings', 'true'
            ]
            
            logger.info(f"Starting SUMO with: {' '.join(sumo_cmd)}")
            
            # Start SUMO using traci.start()
            traci.start(sumo_cmd)
            
            # Get scenario info
            if scenario in self.SCENARIOS:
                self.scenario = scenario
                self.tls_id = self.SCENARIOS[scenario]['tls_id']
            else:
                # Try to detect TLS from simulation
                tls_list = traci.trafficlight.getIDList()
                if tls_list:
                    self.tls_id = tls_list[0]
                    logger.warning(f"Unknown scenario '{scenario}', using first TLS: {self.tls_id}")
                else:
                    logger.error("No traffic lights found in simulation")
                    traci.close()
                    return False
            
            self.connected = True
            self.host = 'localhost'
            self.port = port
            
            logger.info(f"✅ Started SUMO for scenario: {scenario}")
            logger.info(f"   TLS ID: {self.tls_id}")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to start SUMO: {e}")
            import traceback
            traceback.print_exc()
            self.connected = False
            return False
        
    def connect(self, host: str = 'localhost', port: int = 8813, scenario: str = 'Nga4ThuDuc') -> bool:
        """
        Connect to running SUMO instance
        
        Args:
            host: SUMO TraCI host (default: localhost)
            port: SUMO TraCI port (default: 8813)
            scenario: Scenario name to get TLS ID
            
        Returns:
            True if connected successfully
        """
        if not _TRACI_AVAILABLE:
            logger.error("TraCI not available - cannot connect to SUMO")
            return False
            
        try:
            # Close existing connection if any
            if self.connected:
                self.close()
            
            logger.info(f"Connecting to SUMO at {host}:{port}...")
            
            # Connect to TraCI - this blocks until SUMO responds
            # BUT SUMO won't respond until simulation starts!
            # Solution: use traci.init with numRetries=10 (wait ~10s)
            traci.init(port=port, host=host, numRetries=10)
            
            logger.info("TraCI init successful, starting simulation...")
            
            # CRITICAL: Do one simulation step to actually start SUMO
            # Without this, SUMO is connected but paused at t=0
            traci.simulationStep()
            
            logger.info(f"Simulation started at time: {traci.simulation.getTime()}")
            
            # Get scenario info
            if scenario in self.SCENARIOS:
                self.scenario = scenario
                self.tls_id = self.SCENARIOS[scenario]['tls_id']
            else:
                # Try to detect TLS from simulation
                tls_list = traci.trafficlight.getIDList()
                if tls_list:
                    self.tls_id = tls_list[0]
                    logger.warning(f"Unknown scenario '{scenario}', using first TLS: {self.tls_id}")
                else:
                    logger.error("No traffic lights found in simulation")
                    traci.close()
                    return False
            
            self.connected = True
            self.host = host
            self.port = port
            
            logger.info(f"✅ Connected to SUMO at {host}:{port}")
            logger.info(f"   Scenario: {scenario}")
            logger.info(f"   TLS ID: {self.tls_id}")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to connect to SUMO: {e}")
            import traceback
            logger.error(traceback.format_exc())
            self.connected = False
            return False
    
    def is_connected(self) -> bool:
        """Check if connected to SUMO"""
        if not self.connected:
            return False
            
        try:
            # Test connection by getting simulation time
            traci.simulation.getTime()
            return True
        except:
            self.connected = False
            return False
    
    def step(self) -> Optional[float]:
        """
        Execute one simulation step
        
        Returns:
            Current simulation time or None if not connected
        """
        if not self.is_connected():
            return None
            
        try:
            traci.simulationStep()
            return traci.simulation.getTime()
        except Exception as e:
            logger.error(f"Failed to step simulation: {e}")
            return None
    
    def get_traffic_state(self) -> Optional[Dict[str, Any]]:
        """
        Get current traffic state from SUMO
        
        Returns:
            Dictionary with traffic metrics or None if not connected
        """
        if not self.is_connected():
            return None
            
        try:
            # Get traffic light state
            current_phase = traci.trafficlight.getPhase(self.tls_id)
            phase_duration = traci.trafficlight.getPhaseDuration(self.tls_id)
            
            # Get vehicle metrics
            vehicle_ids = traci.vehicle.getIDList()
            vehicle_count = len(vehicle_ids)
            
            # Calculate average speed
            if vehicle_count > 0:
                speeds = [traci.vehicle.getSpeed(vid) for vid in vehicle_ids]
                avg_speed = sum(speeds) / len(speeds)
                max_speed = max(speeds)
                min_speed = min(speeds)
            else:
                avg_speed = max_speed = min_speed = 0.0
            
            # Get lane metrics for TLS
            controlled_lanes = traci.trafficlight.getControlledLanes(self.tls_id)
            
            # Queue length (vehicles waiting)
            queue_length = 0
            waiting_time = 0.0
            
            for lane in set(controlled_lanes):  # Use set to avoid duplicates
                queue_length += traci.lane.getLastStepHaltingNumber(lane)
                waiting_time += traci.lane.getWaitingTime(lane)
            
            # Occupancy
            total_occupancy = 0.0
            for lane in set(controlled_lanes):
                total_occupancy += traci.lane.getLastStepOccupancy(lane)
            
            avg_occupancy = total_occupancy / len(set(controlled_lanes)) if controlled_lanes else 0.0
            
            return {
                'simulation_time': traci.simulation.getTime(),
                'current_phase': current_phase,
                'phase_duration': phase_duration,
                'vehicle_count': vehicle_count,
                'avg_speed': round(avg_speed, 2),
                'max_speed': round(max_speed, 2),
                'min_speed': round(min_speed, 2),
                'queue_length': queue_length,
                'waiting_time': round(waiting_time, 2),
                'avg_occupancy': round(avg_occupancy * 100, 2),  # Convert to percentage
                'controlled_lanes': len(set(controlled_lanes))
            }
            
        except Exception as e:
            logger.error(f"Failed to get traffic state: {e}")
            return None
    
    def set_phase(self, phase_index: int) -> bool:
        """
        Set traffic light phase
        
        Args:
            phase_index: Phase index to set
            
        Returns:
            True if successful
        """
        if not self.is_connected():
            return False
            
        try:
            traci.trafficlight.setPhase(self.tls_id, phase_index)
            logger.info(f"Traffic light phase set to: {phase_index}")
            return True
        except Exception as e:
            logger.error(f"Failed to set phase: {e}")
            return False
    
    def get_scenario_info(self) -> Dict[str, Any]:
        """Get current scenario information"""
        return {
            'connected': self.connected,
            'scenario': self.scenario,
            'tls_id': self.tls_id,
            'host': self.host,
            'port': self.port,
            'description': self.SCENARIOS.get(self.scenario, {}).get('description', 'Unknown')
        }
    
    def close(self):
        """Close TraCI connection"""
        if self.connected:
            try:
                traci.close()
                logger.info("TraCI connection closed")
            except:
                pass
            
            self.connected = False
            self.scenario = None
            self.tls_id = None
            self.host = None
            self.port = None
