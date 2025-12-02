# SUMO Simulator: Thiết bị Đo lường và Công cụ Điều chỉnh

Tài liệu này tổng hợp và giải thích rõ ràng các loại **detector**, **công cụ điều chỉnh**, và **hỗ trợ thời gian** trong SUMO. Đây là bản tóm lược chuẩn để dùng khi cấu hình mô phỏng.

---

## I. Thiết bị Đo lường (Detectors)

Các detector trong SUMO giúp thu thập dữ liệu giao thông theo từng điểm, khu vực hoặc tuyến đường.

### 1. inductionLoop – Vòng từ cảm ứng

- **Mục đích:** Phát hiện xe tại một điểm cố định.
- **Đại lượng thu thập:** Lưu lượng (flow), tốc độ, thời gian chiếm dụng (occupancy).
- **Ứng dụng:** Thu thập dữ liệu tức thời tại nút giao hoặc đoạn đường.

### 2. instantInductionLoop – Vòng từ tức thời

- **Mục đích:** Phát hiện và ghi nhận xe ngay lúc đi qua.
- **Đại lượng thu thập:** Thời điểm xe đi qua, tốc độ tức thời, ID xe.
- **Ứng dụng:** Dùng trong phân tích vi mô cần thông tin chi tiết từng xe.

### 3. laneAreaDetector – Cảm biến khu vực làn đường

- **Mục đích:** Giám sát một đoạn làn (có chiều dài cụ thể).
- **Đại lượng thu thập:** Độ dài hàng chờ, số lượng xe, mật độ.
- **Ứng dụng:** Đánh giá tắc nghẽn, hàng chờ tại nút giao.

### 4. multiLaneAreaDetector – Cảm biến khu vực nhiều làn

- **Mục đích:** Giám sát toàn bộ đoạn đường có nhiều làn.
- **Đại lượng thu thập:** Tổng hợp dữ liệu của các laneAreaDetector.

### 5. entryExitDetector – Cảm biến Ra/Vào

- **Mục đích:** Đếm và đo thời gian xe đi vào/ra một khu vực.
- **Đại lượng thu thập:** Lượng xe vào/ra, thời gian di chuyển trong khu vực.

### 6. detEntry / detExit – Điểm vào/ra (Legacy)

- **Mục đích:** Phiên bản cũ hơn của entryExitDetector.
- **Đại lượng thu thập:** Tương tự entryExitDetector.

### 7. routeProbe – Thăm dò tuyến đường

- **Mục đích:** Theo dõi hiệu suất của toàn tuyến đường.
- **Đại lượng thu thập:** Thời gian hành trình trung bình, chi phí tuyến.
- **Ứng dụng:** Đánh giá hiệu quả tổ chức giao thông theo tuyến.

---

## II. Công cụ Điều chỉnh & Can thiệp (Control & Intervention)

Các công cụ này cho phép tác động vào mô phỏng theo thời gian thực hoặc theo kịch bản.

### 1. calibrator – Bộ hiệu chỉnh lưu lượng

- **Mục đích:** Điều chỉnh lưu lượng xe để khớp dữ liệu thực tế.
- **Chức năng:** Tự động chèn thêm hoặc loại bỏ xe.

### 2. calibratorLane – Làn hiệu chỉnh

- **Mục đích:** Áp dụng calibrator lên một làn cụ thể.

### 3. rerouter – Bộ định tuyến lại

- **Mục đích:** Buộc xe đổi đường khi chạy qua một điểm.
- **Chức năng:** Thay đổi lộ trình (route change).

### 4. variableSpeedSign (VSS) – Biển báo tốc độ biến thiên

- **Mục đích:** Tự động thay đổi giới hạn tốc độ.
- **Ứng dụng:** ITS, kiểm soát tốc độ khi tắc nghẽn.

### 5. vaporizer – Bộ bốc hơi xe

- **Mục đích:** Loại bỏ xe ngay lập tức tại một điểm.
- **Ứng dụng:** Reset giao thông, tạo tình huống mô phỏng.

---

## III. Hỗ trợ Thời gian (Time Support)

### interval – Khoảng thời gian

- **Mục đích:** Định nghĩa chu kỳ để thu thập dữ liệu hoặc áp dụng hành động.
- **Thông số:** Thời gian bắt đầu/kết thúc.

---

## Ghi chú

- Các detector thường khai báo trong file **additional.xml**.
- Thường đi kèm với phân tích bằng TraCI hoặc output XML/CSV.
- Mỗi detector phù hợp từng mục đích: điểm – đoạn – khu vực – tuyến đường.

---

Nếu cần mình có thể tạo thêm ví dụ XML cho từng thiết bị hoặc hướng dẫn cách gắn vào bản đồ mô phỏng.
