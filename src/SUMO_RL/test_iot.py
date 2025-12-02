#!/usr/bin/env python3
"""
Script test để chạy IoT Agent với SUMO (không cần Orion)
"""
import os
import sys
import traci

# Cấu hình
SUMO_CONFIG = [
    'sumo',  # Dùng sumo headless thay vì sumo-gui
    '-c', 'sumo_files/Nga4ThuDuc/Nga4ThuDuc.sumocfg',
    '--step-length', '1',
]
EDGE_IDS = ["1106838009#1", "720360980", "720360983#1", "720360983#2"]
DETECTOR_IDS = ["e2_0", "e2_2"]
TLS_ID = "4066470692"

def get_state_from_sumo():
    """Đọc state từ SUMO."""
    queues = [traci.lanearea.getLastStepVehicleNumber(det) for det in DETECTOR_IDS]
    phase = traci.trafficlight.getPhase(TLS_ID)
    
    total_pm25 = 0
    for edge in EDGE_IDS:
        total_pm25 += traci.edge.getPMxEmission(edge)
        
    return (*queues, phase, total_pm25)

if __name__ == "__main__":
    # Kiểm tra SUMO_HOME
    if 'SUMO_HOME' in os.environ:
        tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
        sys.path.append(tools)
    else:
        sys.exit("Thiếu SUMO_HOME environment variable")
        
    print("[Test IoT] Khởi động SUMO...")
    traci.start(SUMO_CONFIG)
    
    # Chạy vài step để test
    for step in range(100):
        traci.simulationStep()
        
        if step % 20 == 0:
            state = get_state_from_sumo()
            print(f"Step {step}: Queues={state[:2]}, Phase={state[2]}, PM25={state[3]:.2f}")
    
    traci.close()
    print("[Test IoT] Test hoàn tất!")
