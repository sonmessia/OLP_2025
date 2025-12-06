import os
import time
import subprocess
import signal
import sys
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("SUMO-Launcher")

# Configuration
SUMO_FILES_DIR = "/app/sumo_files"
TRIGGER_FILE = os.path.join(SUMO_FILES_DIR, "current_scenario.txt")
IOT_AGENT_SCRIPT = "/app/sumo_rl/agents/iot_agent.py"
DEFAULT_SCENARIO = os.environ.get("SCENARIO", "Nga4ThuDuc")

def read_scenario():
    """Read current scenario from file"""
    try:
        if os.path.exists(TRIGGER_FILE):
            with open(TRIGGER_FILE, "r") as f:
                return f.read().strip()
    except Exception as e:
        logger.error(f"Error reading trigger file: {e}")
    return None

def write_scenario(scenario):
    """Write scenario to file (initialization)"""
    try:
        with open(TRIGGER_FILE, "w") as f:
            f.write(scenario)
    except Exception as e:
        logger.error(f"Error writing trigger file: {e}")

def start_agent(scenario):
    """Start IoT Agent with specific scenario"""
    cmd = ["python3", IOT_AGENT_SCRIPT, "--scenario", scenario, "--gui"]
    logger.info(f"Starting IoT Agent: {' '.join(cmd)}")
    return subprocess.Popen(cmd)

def main():
    logger.info("Starting SUMO Scenario Launcher...")
    
    # Initialize trigger file if missing
    current_scenario = read_scenario()
    if not current_scenario:
        logger.info(f"No scenario file found. initializing with default: {DEFAULT_SCENARIO}")
        current_scenario = DEFAULT_SCENARIO
        write_scenario(current_scenario)
    
    # Start initial process
    process = start_agent(current_scenario)
    
    try:
        while True:
            time.sleep(2)
            
            # Check for scenario change
            target_scenario = read_scenario()
            
            if target_scenario and target_scenario != current_scenario:
                logger.info(f"♻️ Scenario change detected: {current_scenario} -> {target_scenario}")
                
                # Kill existing process
                if process.poll() is None:
                    logger.info("Stopping current simulation...")
                    process.terminate()
                    try:
                        process.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        process.kill()
                
                # Start new process
                current_scenario = target_scenario
                process = start_agent(current_scenario)
                
            # Check if process died unexpectedly (restart)
            if process.poll() is not None:
                logger.warning(f"Process died with code {process.returncode}. Restarting {current_scenario}...")
                process = start_agent(current_scenario)
                
    except KeyboardInterrupt:
        logger.info("Stopping launcher...")
        if process.poll() is None:
            process.terminate()

if __name__ == "__main__":
    main()
