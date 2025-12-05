#!/usr/bin/env python3
"""
Quick SUMO Launcher
Start SUMO-GUI with TraCI for dashboard integration
"""
import os
import sys
import subprocess
from pathlib import Path

# Scenarios
SCENARIOS = {
    '1': {
        'name': 'Nga4ThuDuc',
        'config': 'Nga4ThuDuc/Nga4ThuDuc.sumocfg',
        'desc': 'Ngã Tư Thủ Đức (4-way intersection)'
    },
    '2': {
        'name': 'NguyenThaiSon',
        'config': 'NguyenThaiSon/Nga6NguyenThaiSon.sumocfg',
        'desc': 'Ngã 6 Nguyễn Thái Sơn (6-way intersection)'
    },
    '3': {
        'name': 'QuangTrung',
        'config': 'QuangTrung/quangtrungcar.sumocfg',
        'desc': 'Quang Trung (Complex intersection)'
    }
}

def main():
    print("🚦 SUMO Quick Launcher")
    print("=" * 50)
    
    # Check SUMO_HOME
    sumo_home = os.environ.get('SUMO_HOME', '/usr/share/sumo')
    print(f"SUMO_HOME: {sumo_home}")
    
    # Get sumo-gui path
    sumo_gui = 'sumo-gui'
    if not os.path.exists("{sumo_home}/bin/sumo-gui"):
        # Try to find in PATH
        try:
            result = subprocess.run(['which', 'sumo-gui'], capture_output=True, text=True)
            if result.returncode == 0:
                sumo_gui = result.stdout.strip()
            else:
                print("❌ sumo-gui not found!")
                print("   Install SUMO or set SUMO_HOME")
                sys.exit(1)
        except Exception:
            print("❌ sumo-gui not found!")
            sys.exit(1)
    else:
        sumo_gui = f"{sumo_home}/bin/sumo-gui"
    
    print("SUMO Binary: {sumo_gui}")
    print()
    
    # Select scenario
    print("Select scenario:")
    for key, scenario in SCENARIOS.items():
        print("  {key}) {scenario['name']} - {scenario['desc']}")
    
    choice = input("\nChoice (1-3) [1]: ").strip() or '1'
    
    if choice not in SCENARIOS:
        print("❌ Invalid choice: {choice}")
        sys.exit(1)
    
    scenario = SCENARIOS[choice]
    
    # Get config path
    script_dir = Path(__file__).parent
    sumo_files = script_dir / 'src' / 'backend' / 'app' / 'sumo_rl' / 'sumo_files'
    config_path = sumo_files / scenario['config']
    
    if not config_path.exists():
        print("❌ Config not found: {config_path}")
        sys.exit(1)
    
    # TraCI port
    port = input("\nTraCI Port [8813]: ").strip() or '8813'
    
    print()
    print("✅ Starting SUMO-GUI...")
    print("   Scenario: {scenario['name']}")
    print("   Config: {config_path}")
    print("   TraCI Port: {port}")
    print()
    print("📡 After SUMO opens, connect from dashboard:")
    print("   POST http://localhost:8000/sumo/connect")
    print("   {{'scenario': '{scenario['name']}', 'port': {port}}}")
    print()
    print("Press Ctrl+C to stop SUMO")
    print("-" * 50)
    
    # Start SUMO
    try:
        cmd = [
            sumo_gui,
            '-c', str(config_path),
            '--remote-port', port,
            '--start',
            '--quit-on-end'
        ]
        
        subprocess.run(cmd)
        
    except KeyboardInterrupt:
        print("\n\n✅ SUMO stopped")
    except Exception as e:
        print("\n❌ Error: ", e)
        sys.exit(1)

if __name__ == '__main__':
    main()
