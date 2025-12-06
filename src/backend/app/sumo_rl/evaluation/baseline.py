# Copyright (c) 2025 Green Wave Team
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

# FILE 7: baseline.py
# Chạy mô phỏng với đèn cố định (không có AI) để làm baseline.

import os
import sys

import matplotlib.pyplot as plt
import numpy as np

# --- Cấu hình SUMO ---
_SUMO_AVAILABLE = False
try:
    if 'SUMO_HOME' in os.environ:
        tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
        sys.path.append(tools)
    import traci
    _SUMO_AVAILABLE = True
except ImportError:
    print("Warning: SUMO/TraCI not available", file=sys.stderr)
    traci = None

SUMO_CONFIG = [
    'sumo',  # Không dùng GUI để chạy nhanh (đổi thành 'sumo-gui' nếu muốn xem)
    '-c', 'sumo_files/Nga4ThuDuc/Nga4ThuDuc.sumocfg',  # Sử dụng scenario Nga4ThuDuc
    '--step-length', '0.1',
    '--lateral-resolution', '0',
    '--no-step-log', 'true',
    '--no-warnings', 'true'
]

# --- Cấu hình (Giống train_dqn.py) ---
TOTAL_STEPS = 10000

# IDs từ scenario Nga4ThuDuc
DETECTOR_IDS = ["e2_0", "e2_2"]  # Lane area detectors
TLS_ID = "4066470692"  # Traffic light junction

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
    if not _SUMO_AVAILABLE:
        raise RuntimeError("SUMO is not available. Please set SUMO_HOME environment variable.")
    
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
    
    # --- Vẽ và Lưu Biểu đồ ---
    print("\nBaseline hoàn tất. Đang vẽ biểu đồ...")

    # Biểu đồ Cumulative Reward
    plt.figure(figsize=(10, 6))
    plt.plot(step_history, reward_history, label="Cumulative Reward", color='red')
    plt.xlabel("Simulation Step")
    plt.ylabel("Cumulative Reward")
    plt.title("Baseline (Fixed Timing): Cumulative Reward over Steps")
    plt.legend()
    plt.grid(True)
    plt.savefig("baseline_reward.png", dpi=150, bbox_inches='tight')
    print("✅ Đã lưu biểu đồ: baseline_reward.png")
    plt.close()

    # Biểu đồ Queue Length
    plt.figure(figsize=(10, 6))
    plt.plot(step_history, queue_history, label="Total Queue Length", color='blue')
    plt.xlabel("Simulation Step")
    plt.ylabel("Total Queue Length")
    plt.title("Baseline (Fixed Timing): Queue Length over Steps")
    plt.legend()
    plt.grid(True)
    plt.savefig("baseline_queue.png", dpi=150, bbox_inches='tight')
    print("✅ Đã lưu biểu đồ: baseline_queue.png")
    plt.close()
    
    print("\n=== KẾT QUẢ BASELINE ===")
    print(f"Total Steps: {len(step_history) * 100}")
    print(f"Final Cumulative Reward: {cumulative_reward:.2f}")
    print(f"Average Queue Length: {np.mean(queue_history):.2f}")
    print(f"Max Queue Length: {max(queue_history)}")
    print(f"Min Queue Length: {min(queue_history)}")

if __name__ == "__main__":
    run_baseline()