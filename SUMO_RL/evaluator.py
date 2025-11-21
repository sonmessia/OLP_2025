# FILE 6: evaluator.py
# (Dựa trên File 4 của bạn)
# Dùng để đo 'Average Travel Time' sau khi chạy mô phỏng.

import os
import sys

# --- Cấu hình SUMO ---
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("Please declare environment variable 'SUMO_HOME'")
import traci

# --- Cấu hình Mô phỏng ---
# File config sử dụng scenario Nga4ThuDuc (giống với train_dqn.py)
SUMO_CONFIG = [
    'sumo', # Không dùng GUI để chạy nhanh hơn (đổi thành 'sumo-gui' nếu muốn xem)
    '-c', 'sumo_files/Nga4ThuDuc/Nga4ThuDuc.sumocfg',
    '--step-length', '0.1',
    '--lateral-resolution', '0',
    '--no-step-log', 'true',
    '--no-warnings', 'true'
]
# LƯU Ý: File này đánh giá hiệu suất mô phỏng
# Chạy độc lập để đo Average Travel Time

# --- Biến ---
depart_times = {}
travel_times = {}

# --- Hàm ---
def update_vehicle_times(current_time, depart_times, travel_times):
    """
    Cập nhật thời gian khởi hành cho xe mới và tính toán thời gian di chuyển cho xe đã đến.
    """
    # Ghi lại thời gian khởi hành
    for veh_id in traci.vehicle.getIDList():
        if veh_id not in depart_times:
            depart_times[veh_id] = current_time

    # Tính toán thời gian di chuyển
    arrived_vehicles = traci.simulation.getArrivedIDList()
    for veh_id in arrived_vehicles:
        if veh_id in depart_times:
            travel_times[veh_id] = current_time - depart_times[veh_id]
            print(f"Vehicle {veh_id} travel time: {travel_times[veh_id]:.2f} s")
            # Xóa để tiết kiệm bộ nhớ
            del depart_times[veh_id] 

# --- Vòng lặp Chính ---
def run_evaluation():
    print("=== Bắt đầu chạy Đánh giá (Evaluator) ===")
    traci.start(SUMO_CONFIG)
    
    # Chạy mô phỏng trong 2000 giây (hoặc cho đến khi hết xe)
    while traci.simulation.getTime() < 2000:
        if traci.simulation.getMinExpectedNumber() == 0:
             print("Không còn xe nào. Kết thúc sớm.")
             break
        traci.simulationStep()
        current_time = traci.simulation.getTime()
        update_vehicle_times(current_time, depart_times, travel_times)

    traci.close()
    
    # --- In Kết quả ---
    if travel_times:
        average_travel_time = sum(travel_times.values()) / len(travel_times)
        print("\n--- KẾT QUẢ ĐÁNH GIÁ ---")
        print(f"Tổng số xe đã đến đích: {len(travel_times)}")
        print(f"Thời gian di chuyển Trung bình: {average_travel_time:.2f} giây")
    else:
        print("Không có xe nào đến đích để tính toán.")

if __name__ == "__main__":
    run_evaluation()