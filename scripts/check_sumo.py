import os
import subprocess
from pathlib import Path

def check_sumo_setup():
    print("🔍 Checking SUMO Setup for Windows...")
    print("-" * 50)

    # 1. Check SUMO Installation
    print("1️⃣  Checking SUMO binary...")
    try:
        result = subprocess.run(['where', 'sumo-gui'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"   ✅ Found sumo-gui at: {result.stdout.strip()}")
        else:
            print("   ❌ 'sumo-gui' command not found!")
            print("      👉 Please install SUMO and add it to your System PATH.")
            print("      Download: https://sumo.dlr.de/docs/Downloads.php")
            return
    except Exception as e:
        print(f"   ❌ Error checking sumo-gui: {e}")
        return

    # 2. Check Configuration File
    print("\n2️⃣  Checking Configuration File...")
    
    # Define path based on project structure
    base_dir = Path(__file__).parent.parent / 'src' / 'backend' / 'app' / 'sumo_rl' / 'sumo_files'
    config_path = base_dir / 'Nga4ThuDuc' / 'Nga4ThuDuc.sumocfg'
    
    print(f"   Looking for: {config_path}")
    
    if config_path.exists():
        print("   ✅ Config file found!")
    else:
        print("   ❌ Config file NOT found!")
        print("      👉 Please check if the project structure is correct.")
        print(f"      Current working directory: {os.getcwd()}")
        return

    # 3. Test Launch (Dry Run)
    print("\n3️⃣  Test Launching SUMO (Dry Run)...")
    try:
        # Try to launch with --help just to see if it runs
        cmd = ['sumo-gui', '--help']
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print("   ✅ SUMO GUI binary is executable.")
        else:
            print("   ❌ SUMO GUI failed to run.")
            print(f"      Error: {result.stderr}")
    except Exception as e:
        print(f"   ❌ Failed to launch SUMO: {e}")

    print("-" * 50)
    print("✅ Setup check complete.")

if __name__ == "__main__":
    check_sumo_setup()
