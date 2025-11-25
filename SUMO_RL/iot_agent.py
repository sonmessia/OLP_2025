import os
import sys
import traci
import requests
import json
from flask import Flask, request, jsonify
from threading import Thread
from datetime import datetime

# --- Cấu hình ---
ORION_HOST = "http://localhost:1026/ngsi-ld/v1"
AGENT_HOST = "http://localhost:4041" # Cổng mà agent này lắng nghe

SUMO_CONFIG = [
    'sumo',  # Dùng sumo headless (không GUI) để chạy nhanh hơn
    '-c', 'sumo_files/Nga4ThuDuc/Nga4ThuDuc.sumocfg',
    '--step-length', '1',
]
# Các ID từ Nga4ThuDuc scenario
EDGE_IDS = ["1106838009#1", "720360980", "720360983#1", "720360983#2"]  # Edges kết nối với junction
DETECTOR_IDS = ["e2_0", "e2_2"]  # 2 detectors từ Nga4ThuDuc
TLS_ID = "4066470692"  # Junction ID từ Nga4ThuDuc
ROAD_SEGMENT_ID = f"urn:ngsi-ld:RoadSegment:{TLS_ID}"  # Link to RoadSegment entity

# --- Thiết lập Flask Server để nhận lệnh ---
app = Flask(__name__)

@app.route('/cmd', methods=['POST'])
def receive_command():
    """[LEGACY] Lắng nghe lệnh điều khiển đèn từ AI Agent (Direct call - deprecated)."""
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


@app.route('/notification', methods=['POST'])
def receive_notification():
    """
    [NGSI-LD] Nhận notification từ Orion khi TrafficLight.forcePhase thay đổi.
    Đây là cách đúng chuẩn FIWARE - Event-driven architecture.
    """
    data = request.json
    try:
        print(f"[IoT Agent] Nhận notification từ Orion")
        
        # Parse NGSI-LD notification format
        notification_data = data.get('data', [])
        
        for entity in notification_data:
            if entity.get('type') == 'TrafficLight':
                entity_id = entity.get('id', '')
                
                # Kiểm tra forcePhase attribute
                force_phase_attr = entity.get('forcePhase', {})
                if force_phase_attr:
                    phase_index = force_phase_attr.get('value')
                    
                    if phase_index is not None and phase_index >= 0:  # Only apply if phase >= 0 (-1 means no command)
                        print(f"[IoT Agent] Orion → forcePhase={phase_index} cho {entity_id}")
                        traci.trafficlight.setPhase(TLS_ID, int(phase_index))
                        print(f"[IoT Agent] ✅ Đã chuyển đèn sang pha {phase_index}")
        
        return jsonify({"status": "ok"}), 200
        
    except Exception as e:
        print(f"[IoT Agent] ❌ Lỗi khi xử lý notification: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


def start_flask_server():
    print(f"[IoT Agent] Khởi động server lắng nghe tại {AGENT_HOST}...")
    print(f"[IoT Agent] Endpoints: /cmd (legacy), /notification (NGSI-LD)")
    app.run(host='0.0.0.0', port=4041)


# --- Các hàm NGSI-LD ---
def create_subscription_to_traffic_light():
    """
    Tạo subscription để nhận notification khi TrafficLight.forcePhase thay đổi.
    AI Agent sẽ PATCH lên Orion → Orion notify IoT Agent → IoT Agent apply to SUMO.
    """
    subscription = {
        "description": "IoT Agent subscribes to TrafficLight commands",
        "type": "Subscription",
        "entities": [
            {
                "type": "TrafficLight",
                "id": f"urn:ngsi-ld:TrafficLight:{TLS_ID}"
            }
        ],
        "watchedAttributes": ["forcePhase"],
        "notification": {
            "endpoint": {
                "uri": f"{AGENT_HOST}/notification",
                "accept": "application/json"
            }
        },
        "@context": [
            "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"
        ]
    }
    
    headers = {'Content-Type': 'application/ld+json'}
    
    try:
        response = requests.post(
            f"{ORION_HOST}/subscriptions",
            json=subscription,
            headers=headers
        )
        
        if response.status_code in [201, 200]:
            print(f"[IoT Agent] ✅ Subscription created successfully")
            print(f"[IoT Agent] Watching: TrafficLight:{TLS_ID}.forcePhase")
        else:
            print(f"[IoT Agent] ⚠️ Subscription response: {response.status_code}")
            print(f"[IoT Agent] {response.text}")
            
    except requests.exceptions.ConnectionError:
        print(f"[IoT Agent] ⚠️ Không kết nối được Orion - chạy standalone mode")
    except Exception as e:
        print(f"[IoT Agent] ❌ Lỗi tạo subscription: {e}")


def publish_traffic_light_state():
    """
    Publish trạng thái hiện tại của đèn giao thông lên Orion.
    AI Agent sẽ PATCH thuộc tính forcePhase lên entity này.
    """
    try:
        phase = traci.trafficlight.getPhase(TLS_ID)
        
        tl_data = {
            "id": f"urn:ngsi-ld:TrafficLight:{TLS_ID}",
            "type": "TrafficLight",
            "currentPhase": {
                "type": "Property",
                "value": int(phase)
            },
            "forcePhase": {
                "type": "Property",
                "value": -1,  # -1 means "no forced phase", None/null not allowed in NGSI-LD
                "observedAt": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
            },
            "refRoadSegment": {
                "type": "Relationship",
                "object": ROAD_SEGMENT_ID
            },
            "location": {
                "type": "GeoProperty",
                "value": {
                    "type": "Point",
                    "coordinates": [106.6297, 10.8231]  # Nga Tu Thu Duc coords
                }
            },
            "@context": [
                "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"
            ]
        }
        
        headers = {'Content-Type': 'application/ld+json'}
        url = f"{ORION_HOST}/entities"
        
        response = requests.post(url, json=tl_data, headers=headers)
        
        if response.status_code == 409:  # Already exists
            # Update instead - keep attributes only
            url = f"{ORION_HOST}/entities/{tl_data['id']}/attrs"
            attrs_only = {
                "currentPhase": tl_data["currentPhase"],
                "forcePhase": tl_data["forcePhase"]
            }
            response = requests.patch(url, json=attrs_only, headers={'Content-Type': 'application/json'})
        
        if response.status_code not in [201, 204]:
            print(f"[IoT Agent] TrafficLight publish warning: {response.status_code} {response.text[:200]}")
        
        print(f"[IoT Agent] TrafficLight state published: phase={phase}")
        
    except requests.exceptions.ConnectionError:
        pass  # Standalone mode
    except Exception as e:
        print(f"[IoT Agent] Lỗi publish TrafficLight: {e}")


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
    """Đọc dữ liệu từ Traci và tính toán PM2.5, vehicle count, average speed."""
    queues = [traci.lanearea.getLastStepVehicleNumber(det) for det in DETECTOR_IDS]
    phase = traci.trafficlight.getPhase(TLS_ID)
    
    # Tính toán PM2.5 emissions
    total_pm25 = 0
    for edge in EDGE_IDS:
        total_pm25 += traci.edge.getPMxEmission(edge)
    
    # Tính toán traffic metrics cho TrafficEnvironmentImpact
    total_vehicles = 0
    total_speed = 0
    vehicle_count = 0
    
    for edge in EDGE_IDS:
        vehicles_on_edge = traci.edge.getLastStepVehicleIDs(edge)
        total_vehicles += len(vehicles_on_edge)
        
        for veh_id in vehicles_on_edge:
            total_speed += traci.vehicle.getSpeed(veh_id)
            vehicle_count += 1
    
    average_speed = (total_speed / vehicle_count) if vehicle_count > 0 else 0.0
        
    # State 4-tuple (2 queues, 1 phase, 1 pm25)
    # Return thêm metrics cho TrafficEnvironmentImpact
    return {
        'queues': queues,
        'phase': phase,
        'pm25': total_pm25,
        'vehicle_count': total_vehicles,
        'average_speed': average_speed
    }

def calculate_emissions(vehicle_count, average_speed, pm25):
    """
    Tính toán emissions dựa trên traffic metrics.
    Sử dụng emission factors đơn giản hóa.
    
    Args:
        vehicle_count: Số lượng xe
        average_speed: Tốc độ trung bình (m/s)
        pm25: PM2.5 emissions từ SUMO (mg)
    
    Returns:
        dict: CO2, NOx, PM10 emissions
    """
    # Emission factors (đơn giản hóa - trong thực tế phức tạp hơn)
    # CO2: ~120g/km/vehicle at average speed
    # NOx: ~0.5g/km/vehicle
    # PM10: ~1.5 * PM2.5
    
    # Convert speed m/s to km/h
    speed_kmh = average_speed * 3.6
    
    # CO2 emission (g/h) - tăng khi tốc độ thấp (tắc đường)
    if speed_kmh < 10:
        co2_factor = 180  # g/km - tắc đường
    elif speed_kmh < 30:
        co2_factor = 140
    else:
        co2_factor = 120
    
    # Giả sử mỗi xe di chuyển với tốc độ trung bình trong 1 giây
    distance_km = (speed_kmh / 3600)  # km in 1 second
    co2_emission = vehicle_count * co2_factor * distance_km
    
    # NOx emission (mg/h)
    nox_factor = 0.5  # g/km
    nox_emission = vehicle_count * nox_factor * distance_km * 1000  # convert to mg
    
    # PM10 emission (mg/h) - ước tính từ PM2.5
    pm10_emission = pm25 * 1.5
    
    return {
        'co2': round(co2_emission, 2),
        'nox': round(nox_emission, 2),
        'pm10': round(pm10_emission, 2)
    }


def send_state_to_orion(state):
    """Gói state thành JSON-LD và gửi lên Orion."""
    queues = state['queues']
    phase = state['phase']
    pm25 = state['pm25']
    vehicle_count = state['vehicle_count']
    average_speed = state['average_speed']
    
    # Tính toán emissions
    emissions = calculate_emissions(vehicle_count, average_speed, pm25)
    
    # Timestamp hiện tại
    timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

    # 1. Gửi dữ liệu Giao thông (TrafficFlowObserved)
    traffic_data = {
        "queues": {"type": "Property", "value": queues},
        "phase": {"type": "Property", "value": phase},
        "vehicleCount": {"type": "Property", "value": vehicle_count},
        "averageSpeed": {
            "type": "Property", 
            "value": round(average_speed, 2),
            "unitCode": "MTS"  # meters per second
        },
        "dateObserved": {"type": "Property", "value": timestamp}
    }
    create_ngsi_ld_entity(
        f"urn:ngsi-ld:TrafficFlowObserved:{TLS_ID}", 
        "TrafficFlowObserved", 
        traffic_data
    )
    
    # 2. Gửi dữ liệu Môi trường (AirQualityObserved)
    env_data = {
        "pm25": {
            "type": "Property", 
            "value": round(pm25, 2), 
            "unitCode": "M1"  # mg
        },
        "dateObserved": {"type": "Property", "value": timestamp}
    }
    create_ngsi_ld_entity(
        f"urn:ngsi-ld:AirQualityObserved:{TLS_ID}", 
        "AirQualityObserved", 
        env_data
    )
    
    # 3. Gửi dữ liệu Tác động Môi trường (TrafficEnvironmentImpact) ⭐ MỚI
    impact_data = {
        "co2": {
            "type": "Property",
            "value": emissions['co2'],
            "unitCode": "GRM"  # grams
        },
        "dateObservedFrom": {"type": "Property", "value": timestamp},
        "dateObservedTo": {"type": "Property", "value": timestamp},
        "traffic": {
            "type": "Property",
            "value": [
                {
                    "refTrafficFlowObserved": f"urn:ngsi-ld:TrafficFlowObserved:{TLS_ID}",
                    "vehicleClass": "all"
                }
            ]
        },
        # Thêm relationship đến RoadSegment (nếu có)
        "refRoadSegment": {
            "type": "Relationship",
            "object": ROAD_SEGMENT_ID
        },
        # Metrics bổ sung
        "vehicleCount": {"type": "Property", "value": vehicle_count},
        "averageSpeed": {
            "type": "Property",
            "value": round(average_speed, 2),
            "unitCode": "MTS"
        },
        "pm25Emission": {
            "type": "Property",
            "value": round(pm25, 2),
            "unitCode": "M1"
        },
        "noxEmission": {
            "type": "Property",
            "value": emissions['nox'],
            "unitCode": "M1"
        },
        "pm10Emission": {
            "type": "Property",
            "value": emissions['pm10'],
            "unitCode": "M1"
        }
    }
    create_ngsi_ld_entity(
        f"urn:ngsi-ld:TrafficEnvironmentImpact:{TLS_ID}",
        "TrafficEnvironmentImpact",
        impact_data
    )

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
    
    # 2. Setup NGSI-LD Subscriptions ⭐ PHASE 2
    print("[IoT Agent] Setting up NGSI-LD subscriptions...")
    create_subscription_to_traffic_light()  # Subscribe to TrafficLight.forcePhase
    publish_traffic_light_state()  # Publish initial TrafficLight state
    
    # 3. Chạy vòng lặp mô phỏng
    step = 0
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        
        # Lấy state và gửi lên Orion
        current_state = get_state_from_sumo()
        send_state_to_orion(current_state)
        
        # Update TrafficLight state mỗi step
        if step % 10 == 0:  # Update every 10 steps to reduce load
            publish_traffic_light_state()
        
        if step % 100 == 0:
            print(f"[IoT Agent] Step {step}")
            print(f"  Queues: {current_state['queues']}")
            print(f"  Phase: {current_state['phase']}")
            print(f"  PM2.5: {current_state['pm25']:.2f} mg")
            print(f"  Vehicles: {current_state['vehicle_count']}")
            print(f"  Avg Speed: {current_state['average_speed']:.2f} m/s")
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