# FILE 7: baseline.py
# Chạy mô phỏng với đèn cố định (không có AI) để làm baseline.

import os
import sys
import numpy as np
import matplotlib.pyplot as plt

# --- Cấu hình SUMO ---
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("Please declare environment variable 'SUMO_HOME'")
import traci

SUMO_CONFIG = [
    'sumo-gui',
    '-c', 'sumo_files/RL.sumocfg', # File .sumocfg này NÊN đã định nghĩa đèn cố định
    '--step-length', '0.1',
    '--delay', '1000',
    '--lateral-resolution', '0'
]

# --- Cấu hình (Giống File 1 của bạn) ---
TOTAL_STEPS = 10000

# IDs (SỬA LẠI CHO ĐÚNG)
DETECTOR_IDS = ["Node1_2_EB_0", "Node1_2_EB_1", "Node1_2_EB_2", "Node2_7_SB_0", "Node2_7_SB_1", "Node2_7_SB_2"]
TLS_ID = "Node2"

# --- Các hàm (Copy từ File 1) ---
def get_queue_length(detector_id):
    return traci.lanearea.getLastStepVehicleNumber(detector_id)

def get_current_phase(tls_id):
    return traci.trafficlight.getPhase(tls_id)

def get_state():
    queues = [get_queue_length(det) for det in DETECTOR_IDS]
    phase = get_current_phase(TLS_ID)
    return (*queues, phase)

def get_reward(state):
    total_queue = sum(state[:-1])
    reward = -float(total_queue)
    return reward

# --- Vòng lặp Chính ---
def run_baseline():
    print("\n=== Bắt đầu chạy Baseline (Đèn cố định) ===")
    traci.start(SUMO_CONFIG)
    
    step_history = []
    reward_history = []
    queue_history = []
    cumulative_reward = 0.0

    for step in range(TOTAL_STEPS):
        if traci.simulation.getMinExpectedNumber() == 0:
            print("Hết xe, dừng mô phỏng baseline.")
            break
            
        # CHỈ chạy mô phỏng, KHÔNG gọi AI
        traci.simulationStep()
        
        new_state = get_state()
        reward = get_reward(new_state)
        cumulative_reward += reward
        
        # Ghi lại dữ liệu
        if step % 100 == 0:
            print(f"Step {step}, Reward: {reward:.2f}, Cum. Reward: {cumulative_reward:.2f}")
            step_history.append(step)
            reward_history.append(cumulative_reward)
            queue_history.append(sum(new_state[:-1])) # Tổng hàng chờ

    traci.close()
    
    # --- Vẽ Biểu đồ (Như File 1) ---
    print("\nBaseline hoàn tất. Đang vẽ biểu đồ...")

    plt.figure(figsize=(10, 6))
    plt.plot(step_history, reward_history, label="Cumulative Reward")
    plt.xlabel("Simulation Step")
    plt.ylabel("Cumulative Reward")
    plt.title("Fixed Timing: Cumulative Reward over Steps")
    plt.grid(True)
    plt.show()

    plt.figure(figsize=(10, 6))
    plt.plot(step_history, queue_history, label="Total Queue Length")
    plt.xlabel("Simulation Step")
    plt.ylabel("Total Queue Length")
    plt.title("Fixed Timing: Queue Length over Steps")
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    run_baseline()