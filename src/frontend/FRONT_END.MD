A. Thiết bị Giao thông (Traffic Sensors):

Camera AI / IP Camera: Dùng để đếm xe, nhận diện biển số, phát hiện ùn tắc qua xử lý hình ảnh (Computer Vision). Giao thức thường dùng: RTSP, HTTP, ONVIF.

Cảm biến từ (Inductive Loop) / Radar: Chôn dưới đường hoặc gắn trên cột để đo lưu lượng và tốc độ xe. Giao thức: MQTT, Modbus TCP.

Đèn tín hiệu thông minh: Nhận lệnh điều khiển từ server. Giao thức: MQTT, CoAP.

B. Thiết bị Môi trường (Air Quality Sensors):

Trạm quan trắc không khí (Air Node): Đo chỉ số PM2.5, PM10, CO, NO2, nhiệt độ, độ ẩm.

Giao thức truyền nhận: Thường sử dụng MQTT (phổ biến nhất vì nhẹ và realtime) hoặc LoRaWAN (nếu truyền xa).

2. Danh sách dữ liệu cần nhập (File Markdown)
   Dưới đây là nội dung cho file iot_device_config.md. Bạn có thể dùng file này làm tài liệu tham khảo để thiết kế Database hoặc API payload.

Markdown

# Cấu hình Kết nối Thiết bị IoT - Smart City System

Tài liệu này định nghĩa các trường dữ liệu cần thiết khi thêm mới hoặc chỉnh sửa một thiết bị IoT (Sensor/Camera) vào hệ thống.

## 1. Thông tin chung (General Information)

Nhóm thông tin để định danh và quản lý thiết bị.

| Tên trường (Field) | Kiểu dữ liệu | Bắt buộc | Mô tả                             | Ví dụ                  |
| :----------------- | :----------- | :------: | :-------------------------------- | :--------------------- |
| `device_name`      | String       |   Yes    | Tên gợi nhớ của thiết bị          | Camera Ngã 4 Hàng Xanh |
| `device_type`      | Enum         |   Yes    | Loại thiết bị (Traffic/Air/Light) | `TRAFFIC_CAM_01`       |
| `manufacturer`     | String       |    No    | Hãng sản xuất                     | Bosch, Honeywell       |
| `serial_number`    | String       |   Yes    | Số serial hoặc UUID phần cứng     | SN-2024-X99            |
| `install_date`     | Date         |    No    | Ngày lắp đặt                      | 2024-11-25             |

## 2. Cấu hình Kết nối (Connectivity & Protocol)

Nhóm thông tin quan trọng để Backend có thể "nói chuyện" với thiết bị.

### Giao thức MQTT (Khuyên dùng cho IoT)

| Tên trường (Field) | Kiểu dữ liệu | Mô tả                                  | Ví dụ                          |
| :----------------- | :----------- | :------------------------------------- | :----------------------------- |
| `mqtt_broker_url`  | String       | Địa chỉ Broker (nếu dùng broker riêng) | `mqtt://broker.hivemq.com`     |
| `mqtt_port`        | Number       | Cổng kết nối                           | 1883 (TCP) hoặc 8883 (SSL)     |
| `mqtt_topic_sub`   | String       | Topic hệ thống lắng nghe dữ liệu       | `hcm/d1/hangxanh/traffic/data` |
| `mqtt_topic_pub`   | String       | Topic hệ thống gửi lệnh (nếu có)       | `hcm/d1/hangxanh/traffic/cmd`  |
| `auth_username`    | String       | Tên đăng nhập MQTT                     | `iot_client_01`                |
| `auth_password`    | String       | Mật khẩu (được mã hóa)                 | `******`                       |

### Giao thức HTTP/RTSP (Cho Camera)

| Tên trường (Field) | Kiểu dữ liệu | Mô tả                        | Ví dụ                       |
| :----------------- | :----------- | :--------------------------- | :-------------------------- |
| `ip_address`       | String       | Địa chỉ IP tĩnh của thiết bị | `192.168.1.105`             |
| `api_endpoint`     | String       | Đường dẫn API lấy dữ liệu    | `/api/v1/stream`            |
| `rtsp_url`         | String       | Đường dẫn stream video       | `rtsp://admin:12345@192...` |

## 3. Vị trí địa lý (Geolocation)

Dùng để hiển thị trên bản đồ số.

| Tên trường (Field) | Kiểu dữ liệu | Mô tả                | Ví dụ                         |
| :----------------- | :----------- | :------------------- | :---------------------------- |
| `latitude`         | Float        | Vĩ độ                | 10.8231                       |
| `longitude`        | Float        | Kinh độ              | 106.6297                      |
| `location_desc`    | String       | Mô tả vị trí thực tế | Cột đèn số 5, hướng về Quận 1 |

## 4. Ngưỡng cảnh báo (Thresholds & Metadata)

Cấu hình xử lý dữ liệu đầu ra.

| Tên trường (Field) | Kiểu dữ liệu | Mô tả                                               |
| :----------------- | :----------- | :-------------------------------------------------- |
| `update_interval`  | Number       | Tần suất gửi dữ liệu (giây)                         |
| `active_status`    | Boolean      | Trạng thái kích hoạt (On/Off)                       |
| `alert_threshold`  | JSON         | Cấu hình ngưỡng báo động (VD: AQI > 150 thì báo đỏ) |

3. Ý tưởng thiết kế UI/UX
   Để quản lý hàng trăm thiết bị IoT, giao diện cần tập trung vào tính trực quan và khả năng kiểm tra kết nối ngay lập tức.

A. Trang Danh sách thiết bị (Device Dashboard)
Thay vì một bảng (table) nhàm chán, hãy thiết kế dạng Card View (lưới thẻ) kết hợp bản đồ nhỏ.

Bộ lọc (Filter Bar): Ở trên cùng. Cho phép lọc theo:

Khu vực (Quận/Huyện).

Loại thiết bị (Camera/Cảm biến không khí/Đèn).

Trạng thái (Online/Offline/Bảo trì).

Thẻ thiết bị (Device Card): Mỗi thiết bị là một thẻ hình chữ nhật bao gồm:

Icon: Biểu tượng loại thiết bị (Ví dụ: Icon Camera hoặc Icon Đám mây cho không khí).

Trạng thái: Dấu chấm tròn màu Xanh lá (Online) hoặc Đỏ (Offline) nhấp nháy nhẹ.

Thông số nhanh: Hiển thị dữ liệu mới nhất (VD: "35 xe/phút" hoặc "AQI: 80").

Nút tác vụ: "Chỉnh sửa", "Xem Logs", "Khởi động lại".

B. Trang Nhập/Chỉnh sửa thiết bị (Add Device Wizard)
Vì có quá nhiều trường dữ liệu (như file MD ở trên), không nên dồn hết vào một form dài. Hãy chia thành các bước (Stepper) hoặc Tabs.

Gợi ý luồng nhập liệu:

Bước 1: Chọn loại thiết bị:

Người dùng chọn Icon "Camera Giao thông" hoặc "Cảm biến Không khí".

Hệ thống tự động ẩn/hiện các trường không cần thiết (VD: Chọn Camera thì ẩn trường đo nồng độ bụi).

Bước 2: Thông tin kết nối (Quan trọng nhất):

Nhập IP, MQTT Topic, User/Pass.

Tính năng đặc biệt: Nút "Test Connection" (Kiểm tra kết nối).

Logic: Người dùng ấn nút này -> Server ping thử đến thiết bị -> Nếu trả về "Success" màu xanh thì mới cho phép nút "Lưu" hiện lên. Điều này tránh việc lưu các thiết bị sai cấu hình vào hệ thống.

Bước 3: Định vị bản đồ:

Hiển thị một bản đồ nhỏ (Mini Map).

Người dùng có thể gõ toạ độ hoặc kéo thả Pin (ghim) trực tiếp trên bản đồ để lấy toạ độ chính xác.

Bước 4: Xác nhận:

Hiển thị tóm tắt thông tin và nút "Kích hoạt ngay".
