# FILE 5: train_dqn.py
# Dùng để huấn luyện OFFLINE và tạo ra file 'dqn_model.h5'

import os
import sys
import random
import numpy as np
import matplotlib.pyplot as plt
from collections import deque # Dùng cho Replay Buffer

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

# --- Cấu hình SUMO ---
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("Please declare environment variable 'SUMO_HOME'")
import traci

# Chạy không có GUI để huấn luyện nhanh hơn
SUMO_CONFIG = [
    'sumo', # Thay 'sumo-gui' bằng 'sumo'
    '-c', 'sumo_files/RL.sumocfg',
    '--step-length', '0.1',
    '--lateral-resolution', '0',
    '--no-step-log', 'true', # Tắt bớt log
    '--no-warnings', 'true' # Tắt cảnh báo
]

# --- Cấu hình AI (Hyperparameters) ---
TOTAL_STEPS = 10000
ACTIONS = [0, 1]  # 0 = Giữ pha, 1 = Đổi pha
STATE_SIZE = 8    # 6 queues, 1 phase, 1 pm25
ACTION_SIZE = len(ACTIONS)

# Trọng số cho hàm Reward (ĐA MỤC TIÊU)
W_TRAFFIC = 0.6  # 60% ưu tiên giảm ùn tắc
W_ENV = 0.4      # 40% ưu tiên giảm ô nhiễm

# Cấu hình DQN
GAMMA = 0.95                # Discount factor
EPSILON_START = 1.0         # Tỷ lệ khám phá lúc đầu
EPSILON_END = 0.01          # Tỷ lệ khám phá cuối cùng
EPSILON_DECAY_STEPS = 5000  # Số bước để giảm Epsilon
LEARNING_RATE = 0.001
REPLAY_BUFFER_SIZE = 5000   # Kích thước bộ nhớ
BATCH_SIZE = 64             # Số mẫu lấy ra từ bộ nhớ để học
TARGET_UPDATE_FREQ = 100    # Số bước cập nhật Target Model

# Cấu hình Mô phỏng
MIN_GREEN_STEPS = 100 # 10 giây (100 steps * 0.1s)
last_switch_step = -MIN_GREEN_STEPS

# IDs (SỬA LẠI CHO ĐÚNG VỚI FILE .sumocfg)
TLS_ID = "cluster_5758101431_5758101433"
EDGE_IDS = ["217609239#1", "33285483#6", "683902013#5", "211081657#2"] # Các cạnh đi vào ngã tư
# Sửa lại ID các cảm biến bạn vừa VẼ
DETECTOR_IDS = ["det_1", "det_2", "det_3", "det_4", "det_5", "det_6"] # (Số lượng và tên phải khớp)
NUM_PHASES = 4 # Sửa lại cho đúng

# --- Class ReplayBuffer (Cực kỳ quan trọng) ---
class ReplayBuffer:
    def __init__(self, capacity):
        self.buffer = deque(maxlen=capacity)
    
    def add(self, state, action, reward, next_state, done):
        """Lưu trữ một trải nghiệm."""
        self.buffer.append((state, action, reward, next_state, done))
    
    def sample(self, batch_size):
        """Lấy một batch ngẫu nhiên."""
        return random.sample(self.buffer, batch_size)
    
    def __len__(self):
        return len(self.buffer)

# --- Các hàm của AI ---
def build_model(state_size, action_size):
    """Xây dựng Mạng Nơ-ron (DQN Model)."""
    model = keras.Sequential([
        layers.Input(shape=(state_size,)),
        layers.Dense(64, activation='relu'),
        layers.Dense(64, activation='relu'),
        layers.Dense(action_size, activation='linear')
    ])
    model.compile(
        loss='mse',
        optimizer=keras.optimizers.Adam(learning_rate=LEARNING_RATE)
    )
    return model

def to_array(state_tuple):
    """Chuyển tuple state sang numpy array."""
    return np.array(state_tuple, dtype=np.float32).reshape((1, -1))

def get_state():
    """Lấy state 8-tuple (6 queues, 1 phase, 1 pm25)."""
    queues = [traci.lanearea.getLastStepVehicleNumber(det) for det in DETECTOR_IDS]
    phase = traci.trafficlight.getPhase(TLS_ID)
    
    total_pm25 = 0
    for edge in EDGE_IDS:
        # getPMxEmission trả về mg/s, nhân với step_length
        total_pm25 += traci.edge.getPMxEmission(edge) * 0.1 
        
    return (*queues, phase, total_pm25)

def get_reward(state, last_state):
    """Hàm phần thưởng ĐA MỤC TIÊU."""
    
    # 1. Mục tiêu Giao thông (lấy từ state)
    total_queue = sum(state[:6]) 
    reward_traffic = -float(total_queue)
    
    # 2. Mục tiêu Môi trường (lấy từ state)
    total_pm25 = state[7]
    reward_env = -float(total_pm25) # Càng ô nhiễm càng bị phạt nặng

    # 3. Phần thưởng Tổng hợp
    total_reward = (W_TRAFFIC * reward_traffic) + (W_ENV * reward_env)
    
    return total_reward

def apply_action(action, current_sim_step):
    """Thực thi hành động (0: Giữ, 1: Đổi)."""
    global last_switch_step
    
    if action == 1: # 1 = Đổi pha
        # Kiểm tra thời gian xanh tối thiểu
        if current_sim_step - last_switch_step >= MIN_GREEN_STEPS:
            current_phase = traci.trafficlight.getPhase(TLS_ID)
            next_phase = (current_phase + 1) % NUM_PHASES
            traci.trafficlight.setPhase(TLS_ID, next_phase)
            last_switch_step = current_sim_step
    # Nếu action == 0: Không làm gì

def get_action_from_policy(model, state_tuple, epsilon):
    """Chọn hành động (Epsilon-Greedy)."""
    if random.random() < epsilon:
        return random.choice(ACTIONS)
    else:
        state_array = to_array(state_tuple)
        q_values = model.predict(state_array, verbose=0)[0]
        return int(np.argmax(q_values))

def train_model(main_model, target_model, replay_buffer):
    """Huấn luyện model từ Replay Buffer."""
    if len(replay_buffer) < BATCH_SIZE:
        return # Chưa đủ dữ liệu
        
    # Lấy 1 batch mẫu
    minibatch = replay_buffer.sample(BATCH_SIZE)
    
    # Tách dữ liệu
    states = np.array([to_array(s[0])[0] for s in minibatch])
    actions = np.array([s[1] for s in minibatch])
    rewards = np.array([s[2] for s in minibatch])
    next_states = np.array([to_array(s[3])[0] for s in minibatch])
    
    # Tính Q-values mục tiêu
    # Dùng Target Model để dự đoán Q(s', a')
    q_next = target_model.predict(next_states, verbose=0)
    target_q = rewards + GAMMA * np.amax(q_next, axis=1)
    
    # Lấy Q-values hiện tại
    # Dùng Main Model để dự đoán
    current_q = main_model.predict(states, verbose=0)
    
    # Cập nhật Q-value cho hành động đã chọn
    for i in range(BATCH_SIZE):
        current_q[i][actions[i]] = target_q[i]
        
    # Huấn luyện Main Model
    main_model.fit(states, current_q, verbose=0)

# --- Vòng lặp Huấn luyện Chính ---
def main_loop():
    print("\n=== Bắt đầu Huấn luyện DQN 'GreenWave' ===")
    
    # Khởi tạo models
    main_dqn_model = build_model(STATE_SIZE, ACTION_SIZE)
    target_dqn_model = build_model(STATE_SIZE, ACTION_SIZE)
    target_dqn_model.set_weights(main_dqn_model.get_weights()) # Đồng bộ weight
    
    replay_buffer = ReplayBuffer(REPLAY_BUFFER_SIZE)
    
    epsilon = EPSILON_START
    
    # Mở SUMO
    traci.start(SUMO_CONFIG)
    
    state = get_state()
    
    for step in range(TOTAL_STEPS):
        global last_switch_step
        current_simulation_step = step
        
        # 1. Chọn hành động
        action = get_action_from_policy(main_dqn_model, state, epsilon)
        
        # 2. Thực thi hành động
        apply_action(action, current_simulation_step)
        
        # 3. Tiến 1 bước
        traci.simulationStep()
        
        # 4. Lấy trạng thái mới và phần thưởng
        new_state = get_state()
        reward = get_reward(new_state, state)
        # (done=False vì đây là học liên tục)
        
        # 5. Lưu vào bộ nhớ
        replay_buffer.add(state, action, reward, new_state, False)
        
        # 6. Huấn luyện (nếu đủ dữ liệu)
        train_model(main_dqn_model, target_dqn_model, replay_buffer)
        
        state = new_state
        
        # 7. Cập nhật Epsilon
        if epsilon > EPSILON_END:
            epsilon -= (EPSILON_START - EPSILON_END) / EPSILON_DECAY_STEPS
            
        # 8. Cập nhật Target Model
        if step % TARGET_UPDATE_FREQ == 0:
            print(f"--- Step {step}: Cập nhật Target Model ---")
            target_dqn_model.set_weights(main_dqn_model.get_weights())
            
        if step % 500 == 0:
            print(f"Step {step}, Epsilon: {epsilon:.4f}, Buffer: {len(replay_buffer)}")

    # Đóng SUMO
    traci.close()
    
    # Lưu model
    main_dqn_model.save("dqn_model.h5")
    print("\nHuấn luyện hoàn tất. Model đã được lưu vào 'dqn_model.h5'.")

if __name__ == "__main__":
    main_loop()