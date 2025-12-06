# Copyright (c) 2025 Green Wave Team
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

"""
SUMO Simulation Runner
Tự động khởi động SUMO với GUI và kết nối TraCI
Hỗ trợ 3 scenarios: Nga4ThuDuc, NguyenThaiSon, QuangTrung
"""
import argparse
import logging
import os
import sys
import time
from pathlib import Path

import sumolib
import traci

# Add SUMO tools to path (optional - will check later)
_SUMO_AVAILABLE = False
try:
    if 'SUMO_HOME' in os.environ:
        tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
        sys.path.append(tools)
       
        _SUMO_AVAILABLE = True
    else:
        print("Please declare environment variable 'SUMO_HOME'", file=sys.stderr)
except Exception as e:
    print(f"SUMO not available: {e}", file=sys.stderr)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class SumoRunner:
    """
    SUMO Simulation Runner với GUI support
    """
    
    SCENARIOS = {
        'Nga4ThuDuc': {
            'config': 'Nga4ThuDuc/Nga4ThuDuc.sumocfg',
            'tls_id': '4066470692',
            'description': 'Nga Tu Thu Duc - 4-way intersection'
        },
        'NguyenThaiSon': {
            'config': 'NguyenThaiSon/Nga6NguyenThaiSon.sumocfg',
            'tls_id': 'cluster_1488091499_314059003_314059004_314059006_314059008',
            'description': 'Nga 6 Nguyen Thai Son - 6-way intersection'
        },
        'QuangTrung': {
            'config': 'QuangTrung/quangtrungcar.sumocfg',
            'tls_id': 'cluster_314061834_314061898',
            'description': 'Quang Trung - Complex intersection'
        }
    }
    
    def __init__(self, scenario: str = 'Nga4ThuDuc', gui: bool = True):
        """
        Initialize SUMO Runner
        
        Args:
            scenario: One of 'Nga4ThuDuc', 'NguyenThaiSon', 'QuangTrung'
            gui: Use sumo-gui (True) or sumo (False)
        """
        if not _SUMO_AVAILABLE:
            raise RuntimeError("SUMO is not available. Please set SUMO_HOME environment variable.")
        
        self.scenario = scenario
        self.use_gui = gui
        
        if scenario not in self.SCENARIOS:
            raise ValueError(f"Unknown scenario: {scenario}. Choose from {list(self.SCENARIOS.keys())}")
        
        self.scenario_config = self.SCENARIOS[scenario]
        self.tls_id = self.scenario_config['tls_id']
        
        # Get absolute path to sumo_files
        base_path = Path(__file__).parent.parent / 'sumo_files'
        self.config_path = base_path / self.scenario_config['config']
        
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config file not found: {self.config_path}")
        
        self.connection = None
        logger.info(f"🚦 SUMO Runner initialized for scenario: {scenario}")
        logger.info(f"   Description: {self.scenario_config['description']}")
        logger.info(f"   TLS ID: {self.tls_id}")
        logger.info(f"   Config: {self.config_path}")
    
    def start(self, port: int = 8813, step_length: float = 1.0):
        """
        Start SUMO simulation with TraCI
        
        Args:
            port: TraCI port (default: 8813)
            step_length: Simulation step length in seconds
        """
        try:
            sumo_binary = sumolib.checkBinary('sumo-gui' if self.use_gui else 'sumo')
            
            sumo_cmd = [
                sumo_binary,
                '-c', str(self.config_path),
                '--step-length', str(step_length),
                '--quit-on-end', 'false',  # Don't quit when simulation ends
                '--start', 'true',  # Auto-start simulation (for GUI)
                '--delay', '100',  # Delay between steps (ms) for GUI visibility
            ]
            
            logger.info(f"🚀 Starting SUMO with command: {' '.join(sumo_cmd)}")
            
            # Start SUMO
            traci.start(sumo_cmd, port=port)
            self.connection = traci
            
            logger.info(f"✅ SUMO simulation started successfully on port {port}")
            logger.info(f"   Simulation time: {traci.simulation.getTime()}s")
            logger.info(f"   Number of traffic lights: {len(traci.trafficlight.getIDList())}")
            
            # Verify traffic light exists
            tls_list = traci.trafficlight.getIDList()
            if self.tls_id not in tls_list:
                logger.warning(f"⚠️  Traffic light {self.tls_id} not found!")
                logger.warning(f"   Available TLS: {tls_list}")
            else:
                logger.info(f"✅ Traffic light {self.tls_id} found")
                current_phase = traci.trafficlight.getRedYellowGreenState(self.tls_id)
                logger.info(f"   Current phase: {current_phase}")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to start SUMO: {e}")
            raise
    
    def step(self):
        """Execute one simulation step"""
        if self.connection:
            traci.simulationStep()
            return traci.simulation.getTime()
        return None
    
    def get_traffic_state(self):
        """
        Get current traffic state from detectors
        Returns: dict with traffic metrics
        """
        if not self.connection:
            return None
        
        try:
            # Get all detectors
            detector_ids = traci.lanearea.getIDList()
            
            state = {
                'time': traci.simulation.getTime(),
                'tls_id': self.tls_id,
                'current_phase': traci.trafficlight.getRedYellowGreenState(self.tls_id),
                'vehicle_count': 0,
                'avg_speed': 0,
                'occupancy': 0,
                'detectors': {}
            }
            
            total_speed = 0
            total_vehicles = 0
            
            for det_id in detector_ids:
                vehicles = traci.lanearea.getLastStepVehicleNumber(det_id)
                speed = traci.lanearea.getLastStepMeanSpeed(det_id)
                occupancy = traci.lanearea.getLastStepOccupancy(det_id)
                
                state['detectors'][det_id] = {
                    'vehicles': vehicles,
                    'speed': speed,
                    'occupancy': occupancy
                }
                
                total_vehicles += vehicles
                total_speed += speed * vehicles
            
            state['vehicle_count'] = total_vehicles
            state['avg_speed'] = total_speed / total_vehicles if total_vehicles > 0 else 0
            state['occupancy'] = sum(d['occupancy'] for d in state['detectors'].values()) / len(detector_ids) if detector_ids else 0
            
            return state
            
        except Exception as e:
            logger.error(f"Error getting traffic state: {e}")
            return None
    
    def set_phase(self, phase_index: int):
        """
        Set traffic light phase
        
        Args:
            phase_index: Phase index (0, 1, 2, 3, etc.)
        """
        if not self.connection:
            logger.error("SUMO not connected")
            return False
        
        try:
            traci.trafficlight.setPhase(self.tls_id, phase_index)
            logger.info(f"✅ Set traffic light {self.tls_id} to phase {phase_index}")
            return True
        except Exception as e:
            logger.error(f"Error setting phase: {e}")
            return False
    
    def close(self):
        """Close SUMO simulation"""
        if self.connection:
            try:
                traci.close()
                logger.info("🛑 SUMO simulation closed")
            except Exception as e:
                logger.error(f"Error closing SUMO: {e}")
    
    def run_demo(self, duration: int = 300):
        """
        Run demo simulation for specified duration
        
        Args:
            duration: Simulation duration in seconds
        """
        logger.info(f"🎬 Starting demo run for {duration} seconds...")
        
        self.start()
        
        try:
            step = 0
            while step < duration:
                self.step()
                step += 1
                
                # Log state every 10 seconds
                if step % 10 == 0:
                    state = self.get_traffic_state()
                    if state:
                        logger.info(f"[{step}s] Vehicles: {state['vehicle_count']}, "
                                  f"Speed: {state['avg_speed']:.1f} km/h, "
                                  f"Phase: {state['current_phase']}")
                
                time.sleep(0.1)  # Small delay for GUI visibility
                
        except KeyboardInterrupt:
            logger.info("⏸️  Demo interrupted by user")
        finally:
            self.close()


def main():
    """Main entry point for SUMO runner"""
    parser = argparse.ArgumentParser(description='SUMO Traffic Simulation Runner')
    parser.add_argument('--scenario', 
                       choices=['Nga4ThuDuc', 'NguyenThaiSon', 'QuangTrung'],
                       default='Nga4ThuDuc',
                       help='Scenario to run')
    parser.add_argument('--gui', 
                       action='store_true',
                       help='Use SUMO GUI (default: headless)')
    parser.add_argument('--duration', 
                       type=int, 
                       default=300,
                       help='Simulation duration in seconds (default: 300)')
    parser.add_argument('--port',
                       type=int,
                       default=8813,
                       help='TraCI port (default: 8813)')
    
    args = parser.parse_args()
    
    logger.info("=" * 80)
    logger.info("🚦 SUMO Traffic Simulation Runner")
    logger.info("=" * 80)
    
    runner = SumoRunner(scenario=args.scenario, gui=args.gui)
    runner.run_demo(duration=args.duration)


if __name__ == "__main__":
    main()
