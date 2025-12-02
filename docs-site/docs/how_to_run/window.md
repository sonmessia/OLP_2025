# 🪟 Hướng dẫn chạy trên Windows

Do hạn chế về việc chạy GUI từ Docker trên Windows (cần cấu hình X11 phức tạp), giải pháp ổn định nhất là **chạy SUMO trên máy Windows (Host)** và để Backend (trong Docker) kết nối tới nó.

## 📋 Yêu cầu

1.  **Docker Desktop** đã được cài đặt và đang chạy.
2.  **Python 3.x** đã cài đặt trên Windows.
3.  **SUMO Traffic Simulator** đã cài đặt trên Windows và đã thêm vào biến môi trường `PATH`.
    - Tải về tại: [Eclipse SUMO Downloads](https://sumo.dlr.de/docs/Downloads.php)
    - Kiểm tra bằng cách mở CMD và gõ: `sumo-gui` (nếu hiện cửa sổ SUMO là OK).

---

## 🚀 Các bước thực hiện

### Bước 1: Khởi động hệ thống Backend

Mở terminal (CMD/PowerShell) tại thư mục dự án và chạy:

```bash
docker-compose up -d
```

Đợi khoảng 1-2 phút để các service (Backend, Database, Orion...) khởi động hoàn tất.

### Bước 2: Chạy SUMO trên máy Windows (Host)

Mở một terminal **mới** (CMD/PowerShell), di chuyển vào thư mục dự án và chạy script khởi động SUMO:

```powershell
# Chạy scenario mặc định (Nga4ThuDuc)
python scripts/auto_start_sumo.py --gui
```

Nếu thành công, cửa sổ SUMO GUI sẽ hiện lên và terminal sẽ báo:
`✅ SUMO is ready for TraCI connections on port 8813`

> **Lưu ý:** Giữ terminal này mở để SUMO tiếp tục chạy.

### Bước 3: Kết nối Backend với SUMO

Vì Backend chạy trong Docker và SUMO chạy trên Windows, chúng ta cần kết nối thủ công qua địa chỉ `host.docker.internal`.

Mở một terminal **mới** và chạy lệnh sau để kết nối:

```python
python scripts/connect_sumo.py
```

Nếu thành công, bạn sẽ nhận được phản hồi JSON có `"status": "connected"`.

### Bước 4: Mở Dashboard và Sử dụng

1.  Truy cập Dashboard tại: [http://localhost:3001/demo-dashboard.html](http://localhost:3001/demo-dashboard.html)
2.  Dashboard sẽ tự động nhận diện kết nối và chuyển trạng thái sang **Connected** (màu xanh).
3.  Bây giờ bạn có thể sử dụng các tính năng:
    - **Start Simulation**: Để bắt đầu mô phỏng.
    - **Enable AI Control**: Để bật tính năng điều khiển đèn giao thông bằng AI.

---

## ❓ Khắc phục sự cố

**Lỗi: "Failed to connect to SUMO"**

- Đảm bảo SUMO đang chạy trên máy Windows (Bước 2).
- Đảm bảo port 8813 không bị chặn bởi Firewall.
- Thử restart lại Backend: `docker-compose restart backend`.

**Lỗi: Dashboard không hiện thông số**

- Kiểm tra xem đã bấm nút "Start Simulation" (nút Play ▶️) trên Dashboard chưa.
- Kiểm tra log của backend: `docker-compose logs -f backend`.
