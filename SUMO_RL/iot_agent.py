import os
import sys
import traci
import requests
import json
from flask import Flask, request, jsonify
from threading import Thread

# --- Cấu hình ---
ORION_HOST = "http://localhost:1026/ngsi-ld/v1"
AGENT_HOST = "http://localhost:4041" # Cổng mà agent này lắng nghe

SUMO_CONFIG = [
    'sumo-gui',
    '-c', 'sumo_files/RL.sumocfg',
    '--step-length', '0.1', # Giảm step-length để nhanh hơn
]
# Các ID này phải khớp với file .sumocfg của bạn
EDGE_IDS = ["217609239#1", "33285483#6", "683902013#5", "211081657#2"]
DETECTOR_IDS = ["det_1", "det_2", "det_3", "det_4", "det_5", "det_6"]
TLS_ID = "cluster_5758101431_5758101433"

# --- Thiết lập Flask Server để nhận lệnh ---
app = Flask(__name__)
@app.route('/cmd', methods=['POST'])
def receive_command():
    """Lắng nghe lệnh điều khiển đèn từ AI Agent."""
    data = request.json
    try:
        # Giả sử AI gửi lệnh trong 'forcePhase'
        command_data = data['data'][0].get('forcePhase')
        if command_data:
            phase_index = command_data['value']
            print(f"[IoT Agent] Nhận lệnh: Chuyển đèn {TLS_ID} sang pha {phase_index}")
            traci.trafficlight.setPhase(TLS_ID, phase_index)
    except Exception as e:
        print(f"[IoT Agent] Lỗi khi xử lý lệnh: {e}")
    return jsonify({"status": "ok"}), 200

def start_flask_server():
    print(f"[IoT Agent] Khởi động server lắng nghe lệnh tại {AGENT_HOST}...")
    app.run(host='0.0.0.0', port=4041)

# --- Các hàm NGSI-LD ---
def create_ngsi_ld_entity(entity_id, entity_type, data):
    """Tạo hoặc cập nhật một thực thể trên Orion."""
    headers = {'Content-Type': 'application/json'}
    # Dùng 'NGSILD-Tenant: smartcity' nếu bạn cấu hình
    
    # Cập nhật (PATCH) các thuộc tính
    url = f"{ORION_HOST}/entities/{entity_id}/attrs"
    try:
        response = requests.patch(url, data=json.dumps(data), headers=headers)
        if response.status_code == 404: # Nếu chưa có, tạo mới
            url = f"{ORION_HOST}/entities"
            full_entity = {"id": entity_id, "type": entity_type, **data}
            response = requests.post(url, data=json.dumps(full_entity), headers=headers)
        
        if response.status_code not in [201, 204]:
             print(f"[IoT Agent] Lỗi khi gửi dữ liệu lên Orion: {response.status_code} {response.text}")
             
    except requests.exceptions.ConnectionError as e:
        print(f"[IoT Agent] Lỗi kết nối Orion: {e}")

def get_state_from_sumo():
    """Đọc dữ liệu từ Traci và tính toán PM2.5."""
    queues = [traci.lanearea.getLastStepVehicleNumber(det) for det in DETECTOR_IDS]
    phase = traci.trafficlight.getPhase(TLS_ID)
    
    total_pm25 = 0
    for edge in EDGE_IDS:
        total_pm25 += traci.edge.getPMxEmission(edge)
        
    # State 8-tuple
    return (*queues, phase, total_pm25)

def send_state_to_orion(state):
    """Gói state thành JSON-LD và gửi lên Orion."""
    queues = state[:6]
    phase = state[6]
    pm25 = state[7]

    # 1. Gửi dữ liệu Giao thông
    traffic_data = {
        "queues": {"type": "Property", "value": queues},
        "phase": {"type": "Property", "value": phase}
    }
    create_ngsi_ld_entity(f"urn:ngsi-ld:TrafficFlowObserved:{TLS_ID}", "TrafficFlowObserved", traffic_data)
    
    # 2. Gửi dữ liệu Môi trường
    env_data = {
        "pm25": {"type": "Property", "value": pm25, "unitCode": "M1"} # M1 = mg
    }
    create_ngsi_ld_entity(f"urn:ngsi-ld:AirQualityObserved:{TLS_ID}", "AirQualityObserved", env_data)

# --- Hàm Main ---
def run_simulation():
    # 1. Khởi động SUMO
    if 'SUMO_HOME' in os.environ:
        tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
        sys.path.append(tools)
    else:
        sys.exit("Thiếu SUMO_HOME")
        
    print("[IoT Agent] Khởi động SUMO...")
    traci.start(SUMO_CONFIG)
    
    # (Bạn có thể thêm code tạo Subscriptions ở đây)
    
    # 2. Chạy vòng lặp mô phỏng
    step = 0
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        
        # Lấy state và gửi lên Orion
        current_state = get_state_from_sumo()
        send_state_to_orion(current_state)
        
        if step % 100 == 0:
            print(f"[IoT Agent] Step {step} | State: {current_state}")
        step += 1

    traci.close()
    print("[IoT Agent] Mô phỏng kết thúc.")

if __name__ == "__main__":
    # Chạy Flask server trong một luồng riêng
    flask_thread = Thread(target=start_flask_server)
    flask_thread.daemon = True
    flask_thread.start()
    
    # Chạy mô phỏng ở luồng chính
    run_simulation()