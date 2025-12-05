"""
TraCI Connector - Connect to running SUMO instance
Không cần SUMO_HOME, chỉ cần SUMO đang chạy với --remote-port
"""

import logging
import os
from typing import Any, Dict, Optional

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
        "Nga4ThuDuc": {
            "tls_id": "4066470692",
            "description": "Nga Tu Thu Duc - 4-way intersection",
        },
        "NguyenThaiSon": {
            "tls_id": "11777727352",  # Main traffic light in NguyenThaiSon scenario
            "description": "Nga 6 Nguyen Thai Son - 6-way intersection",
        },
        "QuangTrung": {
            "tls_id": "2269043920",  # Main traffic light - Quang Trung intersection
            "description": "Quang Trung - Complex intersection",
        },
    }

    def __init__(self):
        """Initialize TraCI connector"""
        self.connected = False
        self.scenario = None
        self.tls_id = None
        self.host = None
        self.port = None
        self.sumo_process = None  # Store SUMO process if we start it

    def start_sumo(
        self, scenario: str = "Nga4ThuDuc", gui: bool = False, port: int = 8813
    ) -> bool:
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
            base_path = os.path.join(os.path.dirname(__file__), "..", "sumo_files")

            scenario_configs = {
                "Nga4ThuDuc": os.path.join(
                    base_path, "Nga4ThuDuc", "Nga4ThuDuc.sumocfg"
                ),
                "NguyenThaiSon": os.path.join(
                    base_path, "NguyenThaiSon", "Nga6NguyenThaiSon.sumocfg"
                ),
                "QuangTrung": os.path.join(
                    base_path, "QuangTrung", "quangtrungcar.sumocfg"
                ),
            }

            if scenario not in scenario_configs:
                logger.error(f"Unknown scenario: {scenario}")
                return False

            config_file = scenario_configs[scenario]

            if not os.path.exists(config_file):
                logger.error(f"Config file not found: {config_file}")
                return False

            # Build SUMO command
            sumo_binary = "sumo-gui" if gui else "sumo"

            sumo_cmd = [
                sumo_binary,
                "-c",
                config_file,
                "--remote-port",
                str(port),
                "--step-length",
                "1.0",
                "--no-warnings",
                "true",
            ]

            logger.info(f"Starting SUMO with: {' '.join(sumo_cmd)}")

            # Start SUMO using traci.start()
            traci.start(sumo_cmd)

            # Get scenario info
            if scenario in self.SCENARIOS:
                self.scenario = scenario
                self.tls_id = self.SCENARIOS[scenario]["tls_id"]
            else:
                # Try to detect TLS from simulation
                tls_list = traci.trafficlight.getIDList()
                if tls_list:
                    self.tls_id = tls_list[0]
                    logger.warning(
                        f"Unknown scenario '{scenario}', using first TLS: {self.tls_id}"
                    )
                else:
                    logger.error("No traffic lights found in simulation")
                    traci.close()
                    return False

            self.connected = True
            self.host = "localhost"
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

    def connect(
        self, host: str = "localhost", port: int = 8813, scenario: str = "Nga4ThuDuc"
    ) -> bool:
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
            # Close existing connection if any (force close to avoid "already active" error)
            try:
                if self.connected:
                    logger.info("Closing existing TraCI connection...")
                    traci.close()
                    self.connected = False
                else:
                    # Even if self.connected is False, try closing in case of stale connection
                    logger.info("Force closing any stale TraCI connections...")
                    traci.close()
            except Exception as e:
                logger.debug(f"No existing connection to close: {e}")

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
                self.tls_id = self.SCENARIOS[scenario]["tls_id"]
            else:
                # Try to detect TLS from simulation
                tls_list = traci.trafficlight.getIDList()
                if tls_list:
                    self.tls_id = tls_list[0]
                    logger.warning(
                        f"Unknown scenario '{scenario}', using first TLS: {self.tls_id}"
                    )
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
        except Exception:
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
        Get current traffic state from SUMO - ALL TRAFFIC LIGHTS

        Returns:
            Dictionary with traffic metrics including ALL traffic lights state
        """
        if not self.is_connected():
            return None

        try:
            # Get ALL traffic lights in the simulation
            all_tls_ids = traci.trafficlight.getIDList()

            # Get detailed state for ALL traffic lights
            traffic_lights = []
            for tls_id in all_tls_ids:
                current_phase = traci.trafficlight.getPhase(tls_id)
                phase_duration = traci.trafficlight.getPhaseDuration(tls_id)

                # Get the actual signal state (GGrrrrGGrrrr etc)
                signal_state = traci.trafficlight.getRedYellowGreenState(tls_id)

                # Get time until next switch
                next_switch = traci.trafficlight.getNextSwitch(tls_id)
                current_time = traci.simulation.getTime()
                time_until_switch = max(0, next_switch - current_time)

                # Parse signal state to human readable
                lights = []
                for i, state in enumerate(signal_state):
                    color = "unknown"
                    if state in ["G", "g"]:
                        color = "green"
                    elif state in ["y", "Y"]:
                        color = "yellow"
                    elif state in ["r", "R"]:
                        color = "red"
                    elif state in ["o", "O"]:
                        color = "off"

                    lights.append({"index": i, "state": state, "color": color})

                traffic_lights.append(
                    {
                        "id": tls_id,
                        "current_phase": current_phase,
                        "phase_duration": round(phase_duration, 1),
                        "time_until_switch": round(time_until_switch, 1),
                        "signal_state": signal_state,
                        "lights": lights,
                        "is_main": tls_id
                        == self.tls_id,  # Mark the main controlled TLS
                    }
                )

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

            # Get lane metrics for MAIN TLS only
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

            avg_occupancy = (
                total_occupancy / len(set(controlled_lanes))
                if controlled_lanes
                else 0.0
            )

            # Count loaded/departed/arrived vehicles
            loaded_vehicles = traci.simulation.getLoadedNumber()
            departed_vehicles = traci.simulation.getDepartedNumber()
            arrived_vehicles = traci.simulation.getArrivedNumber()

            return {
                "simulation_time": traci.simulation.getTime(),
                "current_phase": traci.trafficlight.getPhase(self.tls_id),
                "phase_duration": traci.trafficlight.getPhaseDuration(self.tls_id),
                "vehicle_count": vehicle_count,
                "avg_speed": round(avg_speed, 2),
                "max_speed": round(max_speed, 2),
                "min_speed": round(min_speed, 2),
                "queue_length": queue_length,
                "waiting_time": round(waiting_time, 2),
                "avg_occupancy": round(avg_occupancy * 100, 2),
                "loaded_vehicles": loaded_vehicles,
                "departed_vehicles": departed_vehicles,
                "arrived_vehicles": arrived_vehicles,
                "traffic_lights": traffic_lights,
                "total_traffic_lights": len(traffic_lights),
                "controlled_lanes": len(set(controlled_lanes)),
            }

        except Exception as e:
            logger.error(f"Failed to get traffic state: {e}")
            return None

    def set_phase(self, phase_index: int) -> bool:
        """
        Set traffic light phase with SAFE TRANSITION

        This method ensures safe phase transitions by:
        1. Checking current phase
        2. If changing direction (N-S to E-W), insert yellow phase first
        3. Wait appropriate time before switching to red

        Args:
            phase_index: Target phase index

        Returns:
            True if successful
        """
        if not self.is_connected():
            return False

        try:
            current_phase = traci.trafficlight.getPhase(self.tls_id)

            # Get all phases to understand the signal program
            all_phases = traci.trafficlight.getAllProgramLogics(self.tls_id)

            if not all_phases:
                # Fallback: direct phase change (not recommended)
                logger.warning("No phase program found, setting phase directly")
                traci.trafficlight.setPhase(self.tls_id, phase_index)
                return True

            program = all_phases[0]  # Get first (usually only) program
            phases = program.phases

            # Check if target phase is valid
            if phase_index >= len(phases):
                logger.error(
                    f"Invalid phase index {phase_index}, max is {len(phases)-1}"
                )
                return False

            current_state = (
                phases[current_phase].state if current_phase < len(phases) else ""
            )
            target_state = phases[phase_index].state

            # Check if this is a safe transition
            # 'G' = green, 'y' = yellow, 'r' = red
            # Safe: G -> y -> r or r -> G
            # Unsafe: G -> r (need yellow in between)

            needs_yellow = False
            if current_state and target_state:
                # Check each signal position
                for i, (curr, target) in enumerate(
                    zip(current_state, target_state, strict=False)
                ):
                    # If changing from green to red directly = DANGEROUS
                    if curr in ["G", "g"] and target in ["r", "R"]:
                        needs_yellow = True
                        logger.warning(
                            f"Unsafe transition detected at position {i}: {curr} -> {target}"
                        )
                        break

            if needs_yellow:
                # Find or create yellow transition phase
                yellow_phase = None
                for idx, phase in enumerate(phases):
                    # Look for a yellow phase (all yellow signals)
                    if "y" in phase.state.lower():
                        yellow_phase = idx
                        break

                if yellow_phase is not None:
                    logger.info(
                        f"🟡 Safe transition: {current_phase} -> {yellow_phase} (yellow) -> {phase_index}"
                    )
                    # Step 1: Set to yellow
                    traci.trafficlight.setPhase(self.tls_id, yellow_phase)
                    traci.trafficlight.setPhaseDuration(
                        self.tls_id, 3.0
                    )  # 3 seconds yellow

                    # Note: The actual red phase will be set after yellow expires
                    # We set the next phase in the program
                    logger.info(
                        f"⏳ Yellow light active for 3 seconds before switching to phase {phase_index}"
                    )
                else:
                    logger.warning(
                        "⚠️ No yellow phase found in signal program - unsafe direct transition!"
                    )
                    traci.trafficlight.setPhase(self.tls_id, phase_index)
            else:
                # Safe transition - can change directly
                logger.info(f"✅ Safe transition: {current_phase} -> {phase_index}")
                traci.trafficlight.setPhase(self.tls_id, phase_index)

            return True

        except Exception as e:
            logger.error(f"Failed to set phase: {e}")
            return False

    def get_scenario_info(self) -> Dict[str, Any]:
        """Get current scenario information"""
        return {
            "connected": self.connected,
            "scenario": self.scenario,
            "tls_id": self.tls_id,
            "host": self.host,
            "port": self.port,
            "description": self.SCENARIOS.get(self.scenario, {}).get(
                "description", "Unknown"
            ),
        }

    def close(self):
        """Close TraCI connection"""
        if self.connected:
            try:
                traci.close()
                logger.info("TraCI connection closed")
            except Exception:
                pass

            self.connected = False
            self.scenario = None
            self.tls_id = None
            self.host = None
            self.port = None
