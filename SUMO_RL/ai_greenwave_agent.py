import os
import sys
import time
import random
import numpy as np
import requests
import json
from flask import Flask, request, jsonify
from flask_cors import CORS # Cần cài: pip install flask-cors
from threading import Thread

# --- CẤU HÌNH ---
# 1. Orion Broker (Database)
ORION_URL = "http://localhost:1026/ngsi-ld/v1"

# 2. Địa chỉ máy bạn (Để Orion gọi ngược lại báo tin)
# Nếu chạy Docker Orion, phải dùng "http://host.docker.internal:5000"
# Nếu chạy Linux thuần hoặc Native, dùng "http://localhost:5000"
MY_NOTIFY_HOST = "http://host.docker.internal:5000" 

MODEL_PATH = "dqn_model.h5"
TLS_ID = "4066470692"
NUM_PHASES = 2

app = Flask(__name__)
CORS(app) # <--- QUAN TRỌNG: Cho phép Dashboard kết nối

# --- AI LOGIC ---
dqn_model = None

def load_model_safe():
    global dqn_model
    try:
        import tensorflow as tf
        from tensorflow import keras
        if os.path.exists(MODEL_PATH):
            print(f"[AI] Đang tải model {MODEL_PATH}...")
            dqn_model = keras.models.load_model(MODEL_PATH, compile=False)
        else:
            print("[AI] Không thấy file model. Chạy chế độ Random (Demo).")
    except Exception as e:
        print(f"[AI] Lỗi thư viện AI: {e}. Chạy chế độ Random.")

def get_action(state):
    if dqn_model:
        state_array = np.array(state, dtype=np.float32).reshape((1, -1))
        return int(np.argmax(dqn_model.predict(state_array, verbose=0)[0]))
    return random.choice([0, 1]) # Random nếu chưa có model

# --- PROXY ROUTE (CẦU NỐI CHO DASHBOARD) ---
# Dashboard sẽ gọi vào đây thay vì gọi trực tiếp Orion
@app.route('/proxy/orion/<path:subpath>', methods=['GET'])
def proxy_get(subpath):
    try:
        url = f"{ORION_URL}/{subpath}"
        resp = requests.get(url, headers={"Accept": "application/json"})
        return jsonify(resp.json()), resp.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/proxy/orion/<path:subpath>', methods=['PATCH'])
def proxy_patch(subpath):
    try:
        url = f"{ORION_URL}/{subpath}"
        resp = requests.patch(url, json=request.json, headers={"Content-Type": "application/json"})
        return "", resp.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- NOTIFY ROUTE (NHẬN DỮ LIỆU TỪ ORION) ---
@app.route('/notify', methods=['POST'])
def receive_notification():
    """
    [PHASE 2 UPDATE] Nhận notification từ Orion qua NGSI-LD subscription.
    Subscribe 3 entities: TrafficFlowObserved, AirQualityObserved, TrafficEnvironmentImpact
    """
    data = request.json
    # print("[AI] Nhận dữ liệu từ Orion...") # Uncomment để debug
    
    try:
        # Parse NGSI-LD notification format
        entities = data.get('data', [])
        
        # Tìm các entities cần thiết
        traffic_ent = next((e for e in entities if e['type'] == 'TrafficFlowObserved'), None)
        air_ent = next((e for e in entities if e['type'] == 'AirQualityObserved'), None)
        impact_ent = next((e for e in entities if e['type'] == 'TrafficEnvironmentImpact'), None)

        if traffic_ent and air_ent:
            # Parse state từ entities
            queues = traffic_ent.get('queues', {}).get('value', [0, 0])
            phase = traffic_ent.get('phase', {}).get('value', 0)
            pm25 = air_ent.get('pm25', {}).get('value', 0)
            
            # State 4-tuple: (queue_e2_0, queue_e2_2, phase, pm25)
            state = (*queues, phase, pm25)
            
            # Optional: Log TrafficEnvironmentImpact metrics
            if impact_ent:
                co2 = impact_ent.get('co2', {}).get('value', 0)
                avg_speed = impact_ent.get('averageSpeed', {}).get('value', 0)
                # print(f"[AI] Impact - CO2: {co2}g, Speed: {avg_speed}m/s")

            # RA QUYẾT ĐỊNH
            action = get_action(state)
            
            if action == 1:  # Đổi pha
                next_phase = (phase + 1) % NUM_PHASES
                send_command_via_orion(next_phase)
                
    except Exception as e:
        print(f"[AI] ❌ Lỗi xử lý notification: {e}")
        import traceback
        traceback.print_exc()
        
    return "OK", 200

def send_command_via_orion(next_phase):
    """
    [PHASE 2] Gửi lệnh điều khiển lên Orion-LD bằng PATCH.
    Orion sẽ tự động notify IoT Agent qua subscription.
    Đây là event-driven architecture đúng chuẩn FIWARE.
    """
    url = f"{ORION_URL}/entities/urn:ngsi-ld:TrafficLight:{TLS_ID}/attrs"
    data = {"forcePhase": {"type": "Property", "value": int(next_phase)}}
    
    try:
        response = requests.patch(
            url, 
            json=data, 
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code in [204, 200]:
            print(f"[AI] ✅ Đã PATCH lên Orion: forcePhase={next_phase}")
            print(f"[AI] → Orion sẽ notify IoT Agent...")
        else:
            print(f"[AI] ⚠️ PATCH response: {response.status_code}")
            
    except Exception as e:
        print(f"[AI] ❌ Lỗi gửi lệnh: {e}")


def send_command(next_phase):
    """[LEGACY] Direct call - deprecated, use send_command_via_orion instead."""
    send_command_via_orion(next_phase)

# --- TỰ ĐỘNG ĐĂNG KÝ (SUBSCRIPTION) ---
def setup_subscription():
    """
    [PHASE 2 UPDATE] Subscribe vào 3 entities:
    - TrafficFlowObserved (queues, phase, vehicleCount, avgSpeed)
    - AirQualityObserved (pm25)
    - TrafficEnvironmentImpact (co2, nox, emissions) ⭐ MỚI
    """
    time.sleep(5)  # Đợi Orion khởi động xong
    print("[Init] Đang tạo NGSI-LD Subscription...")
    
    sub_url = f"{ORION_URL}/subscriptions/"
    body = {
        "description": "AI Agent subscribes to traffic & environment data (Phase 2)",
        "type": "Subscription",
        "entities": [
            {"id": f"urn:ngsi-ld:TrafficFlowObserved:{TLS_ID}", "type": "TrafficFlowObserved"},
            {"id": f"urn:ngsi-ld:AirQualityObserved:{TLS_ID}", "type": "AirQualityObserved"},
            {"id": f"urn:ngsi-ld:TrafficEnvironmentImpact:{TLS_ID}", "type": "TrafficEnvironmentImpact"}
        ],
        "watchedAttributes": ["queues", "phase", "pm25", "co2", "averageSpeed"],
        "notification": {
            "endpoint": {
                "uri": f"{MY_NOTIFY_HOST}/notify",
                "accept": "application/json"
            }
        },
        "@context": [
            "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"
        ]
    }
    
    try:
        response = requests.post(
            sub_url,
            json=body,
            headers={"Content-Type": "application/ld+json"}
        )
        
        if response.status_code in [201, 200]:
            print("[Init] ✅ Subscription created successfully!")
            print("[Init] Watching: TrafficFlowObserved, AirQualityObserved, TrafficEnvironmentImpact")
            print(f"[Init] Notifications will be sent to {MY_NOTIFY_HOST}/notify")
        else:
            print(f"[Init] ⚠️ Subscription response: {response.status_code}")
            print(f"[Init] {response.text}")
            
    except Exception as e:
        print(f"[Init] ❌ Không thể kết nối Orion: {e}")

if __name__ == "__main__":
    load_model_safe()
    
    # Chạy luồng đăng ký riêng
    Thread(target=setup_subscription).start()
    
    print("🚀 AI Agent & Proxy đang chạy tại cổng 5000...")
    app.run(host='0.0.0.0', port=5000)