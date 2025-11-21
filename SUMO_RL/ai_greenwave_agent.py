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
# Nếu chạy Docker Orion, phải dùng "http://host.docker.internal:8080"
# Nếu chạy Linux thuần hoặc Native, dùng "http://localhost:8080"
MY_NOTIFY_HOST = "http://host.docker.internal:8080" 

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
    data = request.json
    # print("[AI] Nhận dữ liệu từ Orion...") # Uncomment để debug
    
    try:
        # Logic parse dữ liệu từ Orion (Normalized format)
        entities = data.get('data', [])
        traffic_ent = next((e for e in entities if e['type'] == 'TrafficFlowObserved'), None)
        air_ent = next((e for e in entities if e['type'] == 'AirQualityObserved'), None)

        if traffic_ent and air_ent:
            queues = traffic_ent['queues']['value']
            phase = traffic_ent['phase']['value']
            pm25 = air_ent['pm25']['value']
            
            state = (*queues, phase, pm25)
            # print(f"[AI] State: {state}")

            # RA QUYẾT ĐỊNH
            action = get_action(state)
            
            if action == 1: # Đổi pha
                next_phase = (phase + 1) % NUM_PHASES
                send_command(next_phase)
                
    except Exception as e:
        print(f"[AI] Lỗi xử lý: {e}")
        
    return "OK", 200

def send_command(next_phase):
    url = f"{ORION_URL}/entities/urn:ngsi-ld:TrafficLight:{TLS_ID}/attrs"
    data = {"forcePhase": {"type": "Property", "value": next_phase}}
    try:
        requests.patch(url, json=data, headers={'Content-Type': 'application/json'})
        print(f"[AI] Đã gửi lệnh đổi sang Pha {next_phase}")
    except Exception as e:
        print(f"[AI] Lỗi gửi lệnh: {e}")

# --- TỰ ĐỘNG ĐĂNG KÝ (SUBSCRIPTION) ---
def setup_subscription():
    time.sleep(5) # Đợi Orion khởi động xong
    print("[Init] Đang tạo Subscription...")
    
    sub_url = f"{ORION_URL}/subscriptions/"
    body = {
        "description": "AI Agent Subscription",
        "type": "Subscription",
        "entities": [
            {"id": f"urn:ngsi-ld:TrafficFlowObserved:{TLS_ID}", "type": "TrafficFlowObserved"},
            {"id": f"urn:ngsi-ld:AirQualityObserved:{TLS_ID}", "type": "AirQualityObserved"}
        ],
        "notification": {
            "endpoint": {"uri": f"{MY_NOTIFY_HOST}/notify", "accept": "application/json"}
        }
    }
    try:
        # Xóa sub cũ (nếu cần) - ở đây ta cứ tạo mới, Orion sẽ handle
        requests.post(sub_url, json=body, headers={"Content-Type": "application/ld+json"})
        print("[Init] Đăng ký thành công! Orion sẽ gửi dữ liệu về /notify")
    except Exception as e:
        print(f"[Init] Không thể kết nối Orion: {e}")

if __name__ == "__main__":
    load_model_safe()
    
    # Chạy luồng đăng ký riêng
    Thread(target=setup_subscription).start()
    
    print("🚀 AI Agent & Proxy đang chạy tại cổng 8080...")
    app.run(host='0.0.0.0', port=8080)