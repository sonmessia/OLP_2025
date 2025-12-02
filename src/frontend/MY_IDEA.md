Đây là một bài toán kinh điển về **Digital Twin** (Bản sao số) trong giao thông. Để thực hiện yêu cầu: "Chọn tên khu vực -\> Khóa góc nhìn camera vào đó -\> Hiển thị xe và đèn tín hiệu từ SUMO theo thời gian thực", bạn cần xây dựng một hệ thống gồm 3 tầng.

Dưới đây là kiến trúc và hướng dẫn chi tiết từng bước:

### Kiến trúc hệ thống

[Image of Digital Twin architecture diagram]

1.  **Mô phỏng (Simulation Layer):** SUMO chạy ngầm, tính toán vật lý xe và logic đèn.
2.  **Cầu nối (Backend Server):** Python script dùng **TraCI** để lấy dữ liệu từ SUMO và **WebSocket** để bắn dữ liệu ra ngoài.
3.  **Hiển thị (Frontend Web):** Bản đồ (Leaflet/Mapbox) nhận dữ liệu, tự động zoom vào khu vực chỉ định và vẽ xe/đèn.

---

### Bước 1: Chuẩn bị "Dictionary" các khu vực (Hardest Part First)

Để đạt được yêu cầu "bấm tên là rào quanh khu vực đó", bạn cần định nghĩa sẵn tọa độ biên (Bounding Box) cho từng khu vực trong code của Frontend.

**Ví dụ cấu trúc dữ liệu (Frontend):**

```javascript
const AREAS = {
  nga_tu_thu_duc: {
    name: "Ngã Tư Thủ Đức",
    // Tọa độ góc Tây-Nam và Đông-Bắc của khu vực
    bounds: [
      [10.848, 106.77], // South-West
      [10.855, 106.778], // North-East
    ],
    // Tọa độ trung tâm để đặt camera ban đầu
    center: [10.8515, 106.774],
  },
  hang_xanh: {
    // ... tương tự
  },
};
```

---

### Bước 2: Xây dựng Backend (Python + TraCI + WebSocket)

Backend đóng vai trò là "người quay phim", liên tục chụp lại trạng thái của SUMO và gửi đi.

**Logic chính của file `server.py`:**

1.  Khởi chạy SUMO với file bản đồ (`.net.xml`) đã cắt khu vực Thủ Đức.
2.  Mở cổng WebSocket server (dùng thư viện `websockets` hoặc `socketio`).
3.  Trong vòng lặp vô tận (`while True`):
    - Gọi `traci.simulationStep()` để SUMO nhích 1 bước thời gian.
    - **Lấy dữ liệu xe:** Quét tất cả xe, lấy ID, tọa độ (X, Y), góc quay, trạng thái đèn xi-nhan.
    - **Lấy dữ liệu đèn:** Lấy trạng thái Đỏ/Xanh của các cụm đèn (Traffic Light Logic).
    - **Chuyển đổi tọa độ:** Rất quan trọng\! SUMO dùng hệ tọa độ mét (Cartesian), Web dùng Kinh độ/Vĩ độ (Geo). Phải dùng hàm `traci.simulation.convertGeo` để đổi.
    - Đóng gói thành JSON và gửi qua WebSocket.

**Đoạn code mẫu (Python Pseudo-code):**

```python
import traci
import json
import asyncio
import websockets

async def send_traffic_data(websocket, path):
    traci.start(["sumo", "-c", "config.sumocfg"]) # Chạy SUMO

    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()

        # 1. Lấy dữ liệu xe
        vehicles = []
        for veh_id in traci.vehicle.getIDList():
            x, y = traci.vehicle.getPosition(veh_id)
            lon, lat = traci.simulation.convertGeo(x, y) # Chuyển sang Lat/Lon
            angle = traci.vehicle.getAngle(veh_id)
            speed = traci.vehicle.getSpeed(veh_id)
            vehicles.append({"id": veh_id, "lat": lat, "lon": lon, "angle": angle})

        # 2. Lấy dữ liệu đèn (Ví dụ ID đèn ngã tư thủ đức là 'tls_td')
        tls_state = traci.trafficlight.getRedYellowGreenState("tls_td")
        # tls_state trả về chuỗi kiểu "GrGr" (G=Green, r=red)

        # 3. Gửi JSON xuống client
        data = json.dumps({"vehicles": vehicles, "traffic_light": tls_state})
        await websocket.send(data)

        await asyncio.sleep(0.1) # Giả lập độ trễ thực tế

start_server = websockets.serve(send_traffic_data, "localhost", 8765)
# ... code để chạy server
```

---

### Bước 3: Xây dựng Frontend (Hiển thị & Khóa góc nhìn)

Đây là nơi thực hiện yêu cầu "rào quanh khu vực" và hiển thị.

**1. Xử lý sự kiện chọn khu vực (Khóa góc nhìn):**

Khi người dùng bấm nút "Ngã tư Thủ Đức", dùng hàm `fitBounds` của Leaflet để ép bản đồ chỉ hiển thị đúng khung hình chữ nhật đã định nghĩa ở Bước 1.

```javascript
function selectArea(areaKey) {
  const area = AREAS[areaKey];

  // Hàm này tự động zoom và pan để vừa khít khu vực, không thừa không thiếu
  map.fitBounds(area.bounds);

  // Tùy chọn: Vô hiệu hóa zoom/pan để người dùng không kéo ra ngoài được (Lock view)
  // map.dragging.disable();
  // map.touchZoom.disable();
}
```

**2. Render Xe (Cập nhật vị trí):**

Bạn không xóa marker cũ đi vẽ lại (sẽ bị nháy), mà hãy _cập nhật tọa độ_ của marker xe hiện có.

```javascript
const carMarkers = {}; // Lưu trữ các marker xe theo ID: { "veh1": MarkerObj }

socket.onmessage = function (event) {
  const data = JSON.parse(event.data);

  // Cập nhật xe
  data.vehicles.forEach((veh) => {
    if (carMarkers[veh.id]) {
      // Xe đã có -> Cập nhật vị trí và xoay icon
      carMarkers[veh.id].setLatLng([veh.lat, veh.lon]);
      carMarkers[veh.id].setRotationAngle(veh.angle);
    } else {
      // Xe mới -> Tạo marker mới
      const carIcon = L.divIcon({ className: "car-icon" }); // Dùng CSS vẽ hình chữ nhật
      const marker = L.marker([veh.lat, veh.lon], { icon: carIcon }).addTo(map);
      carMarkers[veh.id] = marker;
    }
  });

  // Xử lý đèn giao thông (Vẽ các hình tròn tại vị trí cột đèn)
  updateTrafficLights(data.traffic_light);
};
```

**3. Render Đèn Giao Thông:**

Để thấy đèn "tự vận hành", bạn cần biết vị trí các cột đèn trên bản đồ (lấy từ OSM).

- Chuỗi trạng thái SUMO gửi về (ví dụ: `"GrGr"`) sẽ tương ứng với các luồng (link index).
- Trên Web, bạn vẽ các hình tròn (CircleMarker) tại các điểm dừng (stop line).
- Nếu ký tự là `G` hoặc `g` -\> Tô màu Xanh.
- Nếu ký tự là `r` -\> Tô màu Đỏ.
- Nếu ký tự là `y` -\> Tô màu Vàng.

---

### Tổng kết quy trình hoạt động

1.  **User** truy cập web, bản đồ trống hoặc hiển thị toàn cảnh.
2.  **User** bấm nút "Ngã Tư Thủ Đức".
3.  **Frontend** gọi `map.fitBounds(...)`, màn hình zoom chặt vào ngã tư.
4.  **Frontend** gửi tín hiệu socket lên Server: "Bắt đầu mô phỏng khu vực Thủ Đức".
5.  **Backend** nhận lệnh, load file `thuduc.net.xml` vào SUMO.
6.  **Backend** liên tục loop, lấy tọa độ xe và trạng thái đèn đỏ/xanh, convert sang Lat/Lon, gửi về Frontend.
7.  **Frontend** vẽ các chấm đỏ/xanh (đèn) và các hình chữ nhật (xe) di chuyển mượt mà trên nền bản đồ đã bị khóa góc nhìn.

Cách này đảm bảo người dùng thấy chính xác luồng giao thông được điều khiển bởi thuật toán trong SUMO mà không bị xao nhãng bởi các khu vực khác.
