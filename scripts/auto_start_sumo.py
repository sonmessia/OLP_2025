#!/usr/bin/env python3
# Copyright (c) 2025 Green Wave Team
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

"""
Auto-start SUMO script for dashboard integration
This script starts SUMO on the host machine and keeps it running
"""
import subprocess
import sys
import os
import signal
import time

# SUMO config paths (relative to OLP_2025 root)
BASE_DIR = os.path.join(os.path.dirname(__file__), '..', 'src', 'backend', 'app', 'sumo_rl', 'sumo_files')

SCENARIOS = {
    'Nga4ThuDuc': os.path.join(BASE_DIR, 'Nga4ThuDuc', 'Nga4ThuDuc.sumocfg'),
    'NguyenThaiSon': os.path.join(BASE_DIR, 'NguyenThaiSon', 'Nga6NguyenThaiSon.sumocfg'),
    'QuangTrung': os.path.join(BASE_DIR, 'QuangTrung', 'quangtrungcar.sumocfg')
}

# Global process handle
sumo_process = None

def signal_handler(sig, frame):
    """Handle Ctrl+C to cleanup SUMO"""
    global sumo_process
    print("\n🛑 Stopping SUMO...")
    if sumo_process:
        sumo_process.terminate()
        sumo_process.wait()
    sys.exit(0)

def start_sumo(scenario='Nga4ThuDuc', gui=False, port=8813):
    """
    Start SUMO process
    
    Args:
        scenario: Scenario name
        gui: Use sumo-gui (True) or sumo (False) 
        port: TraCI port
    """
    global sumo_process
    
    if scenario not in SCENARIOS:
        print(f"❌ Unknown scenario: {scenario}")
        print(f"Available scenarios: {', '.join(SCENARIOS.keys())}")
        return False
    
    config_file = os.path.abspath(SCENARIOS[scenario])
    
    if not os.path.exists(config_file):
        print(f"❌ Config file not found: {config_file}")
        return False
    
    # Build SUMO command
    sumo_binary = 'sumo-gui' if gui else 'sumo'
    
    # Try to find full path to binary on Windows to avoid ambiguity
    if os.name == 'nt':
        try:
            result = subprocess.run(['where', sumo_binary], capture_output=True, text=True)
            if result.returncode == 0:
                found_path = result.stdout.strip().split('\n')[0]
                if found_path:
                    sumo_binary = found_path
        except Exception:
            pass
            
    cmd = [
        sumo_binary,
        '-c', config_file,
        '--remote-port', str(port),
        '--step-length', '1.0',
        '--start'
    ]
    
    print("🚦 Starting SUMO...")
    print("   Scenario: {scenario}")
    print("   Binary: {sumo_binary}")
    print("   Port: {port}")
    print("   Config: {config_file}")
    print()
    print("✅ SUMO is ready for TraCI connections on port {port}")
    print("💡 Backend will connect using: http://localhost:8000/sumo/start")
    print("   Press Ctrl+C to stop SUMO")
    print()
    
    try:
        # Start SUMO
        # Removed stdout=subprocess.DEVNULL to see output in console
        sumo_process = subprocess.Popen(
            cmd,
            cwd=os.path.dirname(config_file)
        )
        
        # Wait a bit to ensure SUMO started
        time.sleep(2)
        
        # Check if process is still running
        if sumo_process.poll() is not None:
            # Process died
            _, stderr = sumo_process.communicate()
            print("❌ SUMO failed to start:")
            if stderr:
                print(stderr.decode())
            return False
        
        print(f"✅ SUMO started (PID: {sumo_process.pid})")
        print()
        
        # Keep process alive
        signal.signal(signal.SIGINT, signal_handler)
        sumo_process.wait()  # Wait for SUMO to finish
        
        return True
        
    except FileNotFoundError:
        print(f"❌ SUMO binary '{sumo_binary}' not found")
        print("   Please install SUMO or add it to PATH")
        return False
    except Exception as e:
        print(f"❌ Failed to start SUMO: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Start SUMO for dashboard')
    parser.add_argument('scenario', nargs='?', default='Nga4ThuDuc',
                       choices=SCENARIOS.keys(),
                       help='Scenario to run (default: Nga4ThuDuc)')
    parser.add_argument('--gui', action='store_true',
                       help='Use sumo-gui instead of sumo')
    parser.add_argument('--port', type=int, default=8813,
                       help='TraCI port (default: 8813)')
    
    args = parser.parse_args()
    
    success = start_sumo(
        scenario=args.scenario,
        gui=args.gui,
        port=args.port
    )
    
    sys.exit(0 if success else 1)
