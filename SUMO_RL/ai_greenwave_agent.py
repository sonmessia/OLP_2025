import os
import random
import numpy as np
import tensorflow as tf
from tensorflow import keras
import requests
import json
from flask import Flask, request, jsonify
from threading import Thread

# --- Cấu hình ---
ORION_HOST = "http://localhost:1026/ngsi-ld/v1"
MODEL_PATH = "dqn_model.h5" # Tên file model đã huấn luyện
ACTIONS = [0, 1] # 0 = Giữ pha, 1 = Đổi pha
STATE_SIZE = 4 # 2 queues, 1 phase, 1 pm25
TLS_ID = "4066470692" # Junction ID từ Nga4ThuDuc
NUM_PHASES = 2 # Nga4ThuDuc có 2 pha

# --- Thiết lập Flask Server để nhận dữ liệu ---
app = Flask(__name__)

# --- Tải Model & Logic AI ---
def load_dqn_model(path, state_size, action_size):
    """Tải mô hình Keras đã huấn luyện."""
    # (Bạn có thể dùng lại hàm build_model từ File 3 và load_weights)
    if not os.path.exists(path):
        print(f"[AI Agent] Lỗi: Không tìm thấy model '{path}'. Hãy chạy train_dqn.py trước.")
        sys.exit(1)
    print(f"[AI Agent] Tải model từ {path}...")
    # Load model without compilation to avoid metric deserialization error
    return keras.models.load_model(path, compile=False)

def to_array(state_tuple):
    """Chuyển state tuple sang numpy array cho model."""
    return np.array(state_tuple, dtype=np.float32).reshape((1, -1))

def get_action_from_policy(model, state_tuple):
    """Chạy model để lấy quyết định (inference)."""
    # Ở chế độ demo, chúng ta luôn "tham lam" (không khám phá)
    state_array = to_array(state_tuple)
    q_values = model.predict(state_array, verbose=0)[0]
    return int(np.argmax(q_values))

# --- Hàm NGSI-LD ---
def send_command_to_orion(tls_id, next_phase):
    """Gửi lệnh đổi pha đèn lên Orion Broker."""
    headers = {'Content-Type': 'application/json'}
    url = f"{ORION_HOST}/entities/urn:ngsi-ld:TrafficLight:{tls_id}/attrs"
    
    # Thuộc tính `forcePhase` là thuộc tính mà IoT Agent đang lắng nghe
    command_data = {
        "forcePhase": {
            "type": "Property",
            "value": next_phase
        }
    }
    
    try:
        response = requests.patch(url, data=json.dumps(command_data), headers=headers)
        if response.status_code == 204:
            print(f"[AI Agent] Gửi lệnh thành công: Đổi pha {next_phase}")
        else:
            print(f"[AI Agent] Lỗi khi gửi lệnh: {response.status_code}")
    except requests.exceptions.ConnectionError as e:
        print(f"[AI Agent] Lỗi kết nối Orion: {e}")

def parse_state_from_orion(data):
    """Hàm này cực kỳ quan trọng: Dịch JSON-LD thành state tuple."""
    try:
        # Giả sử Orion gửi 2 thực thể trong 1 thông báo
        traffic_data = data['data'][0]
        env_data = data['data'][1]
        
        # Sắp xếp lại
        if traffic_data['type'] != 'TrafficFlowObserved':
            traffic_data, env_data = env_data, traffic_data
            
        queues = traffic_data['queues']['value']  # List of 2 queue values
        phase = traffic_data['phase']['value']
        pm25 = env_data['pm25']['value']
        
        # Trả về state 4-tuple (2 queues, 1 phase, 1 pm25)
        return (*queues, phase, pm25)
        
    except Exception as e:
        print(f"[AI Agent] Lỗi khi parse state: {e} | Data: {data}")
        return None

# --- API Route chính: Nơi AI "lắng nghe" ---
@app.route('/notify', methods=['POST'])
def receive_notification():
    """Lắng nghe trạng thái mới từ Orion (qua Subscription)."""
    global dqn_model # Sử dụng model đã tải
    
    data = request.json
    
    # 1. Dịch JSON-LD thành State
    current_state = parse_state_from_orion(data)
    if current_state is None:
        return jsonify({"status": "error", "message": "Invalid state data"}), 400
    
    print(f"[AI Agent] Nhận State: {current_state}")
    
    # 2. Ra quyết định (Inference)
    action = get_action_from_policy(dqn_model, current_state)
    
    # 3. Gửi lệnh (nếu cần)
    if action == 1: # 1 = Đổi pha
        current_phase = current_state[2]  # Phase is at index 2 (after 2 queues)
        next_phase = (current_phase + 1) % NUM_PHASES
        send_command_to_orion(TLS_ID, next_phase)
    else: # 0 = Giữ pha
        print(f"[AI Agent] Quyết định: Giữ pha")

    return jsonify({"status": "ok"}), 200

# --- Hàm Main ---
if __name__ == "__main__":
    # Tải model AI đã huấn luyện
    dqn_model = load_dqn_model(MODEL_PATH, STATE_SIZE, ACTIONS[1]+1)
    
    # (Bạn cần code để tạo Subscriptions cho Orion tại đây)
    # Ví dụ: Sub 1: Báo cho AI (port 8080) khi `AirQualityObserved` thay đổi
    # Ví dụ: Sub 2: Báo cho IoT Agent (port 4041) khi `TrafficLight` có lệnh
    
    # Khởi động server
    print("[AI Agent] Khởi động server lắng nghe trạng thái tại http://localhost:8080/notify...")
    app.run(host='0.0.0.0', port=8080)