#!/usr/bin/env python3
"""
Script test AI agent với SUMO (không cần Orion broker)
Tương tự train_dqn.py nhưng dùng model đã train để inference
"""
import os
import sys
import traci
import numpy as np
from tensorflow import keras

# Cấu hình
SUMO_CONFIG = [
    'sumo',
    '-c', 'sumo_files/Nga4ThuDuc/Nga4ThuDuc.sumocfg',
    '--step-length', '1',
]
MODEL_PATH = "dqn_model.h5"
EDGE_IDS = ["1106838009#1", "720360980", "720360983#1", "720360983#2"]
DETECTOR_IDS = ["e2_0", "e2_2"]
TLS_ID = "4066470692"
NUM_PHASES = 2
STATE_SIZE = 4
ACTIONS = [0, 1]  # 0=giữ pha, 1=đổi pha

# Trọng số reward
W_TRAFFIC = 0.6
W_ENV = 0.4

def load_model():
    """Load model đã train (không compile để tránh lỗi metric)."""
    if not os.path.exists(MODEL_PATH):
        print(f"[ERROR] Không tìm thấy model: {MODEL_PATH}")
        sys.exit(1)
    print(f"[AI Agent] Loading model từ {MODEL_PATH}...")
    return keras.models.load_model(MODEL_PATH, compile=False)

def get_state():
    """Lấy state từ SUMO."""
    queues = [traci.lanearea.getLastStepVehicleNumber(det) for det in DETECTOR_IDS]
    phase = traci.trafficlight.getPhase(TLS_ID)
    
    total_pm25 = 0
    for edge in EDGE_IDS:
        total_pm25 += traci.edge.getPMxEmission(edge)
        
    return np.array([*queues, phase, total_pm25], dtype=np.float32)

def get_action(model, state):
    """Chọn action từ model (greedy - không explore)."""
    state_batch = state.reshape(1, -1)
    q_values = model.predict(state_batch, verbose=0)[0]
    return int(np.argmax(q_values))

def calculate_reward(state):
    """Tính reward từ state."""
    queue_length = state[0] + state[1]
    pm25 = state[3]
    return W_TRAFFIC * (-queue_length) + W_ENV * (-pm25 / 1000.0)

if __name__ == "__main__":
    # Kiểm tra SUMO_HOME
    if 'SUMO_HOME' in os.environ:
        tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
        sys.path.append(tools)
    else:
        sys.exit("Thiếu SUMO_HOME")
    
    # Load model
    model = load_model()
    
    # Khởi động SUMO
    print("[AI Agent] Khởi động SUMO...")
    traci.start(SUMO_CONFIG)
    
    # Metrics
    total_reward = 0
    total_steps = 0
    actions_taken = {0: 0, 1: 0}
    
    # Chạy simulation
    while traci.simulation.getMinExpectedNumber() > 0 and total_steps < 1000:
        traci.simulationStep()
        
        # Lấy state
        state = get_state()
        
        # Chọn action từ AI
        action = get_action(model, state)
        actions_taken[action] += 1
        
        # Thực hiện action
        if action == 1:  # Đổi pha
            current_phase = traci.trafficlight.getPhase(TLS_ID)
            next_phase = (current_phase + 1) % NUM_PHASES
            traci.trafficlight.setPhase(TLS_ID, next_phase)
        
        # Tính reward
        reward = calculate_reward(state)
        total_reward += reward
        
        # Log
        if total_steps % 100 == 0:
            avg_reward = total_reward / (total_steps + 1)
            print(f"Step {total_steps}: Q={state[:2]}, Phase={int(state[2])}, PM25={state[3]:.1f}, Reward={reward:.2f}, AvgReward={avg_reward:.2f}")
        
        total_steps += 1
    
    traci.close()
    
    # Tổng kết
    print("\n" + "="*60)
    print(f"[AI Agent] Hoàn tất!")
    print(f"Total Steps: {total_steps}")
    print(f"Total Reward: {total_reward:.2f}")
    print(f"Average Reward: {total_reward/total_steps:.2f}")
    print(f"Actions: Hold={actions_taken[0]}, Change={actions_taken[1]}")
    print("="*60)
