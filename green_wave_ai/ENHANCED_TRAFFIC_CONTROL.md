# 🚦 Enhanced Traffic Light Control System

## Các cải tiến mới (Dec 1, 2025)

### ✅ 1. SUMO GUI Auto-start
- Dashboard tự động mở SUMO GUI khi click "Start SUMO"
- Xem trực quan các xe, đường, đèn giao thông
- Không cần chạy lệnh terminal thủ công

### ✅ 2. Hiển thị TẤT CẢ đèn giao thông
Backend giờ trả về trạng thái của **TẤT CẢ traffic lights** trong ngã tư:

```json
{
  "traffic_lights": [
    {
      "id": "11777727352",
      "current_phase": 0,
      "time_until_switch": 23.5,
      "signal_state": "GGrrrrGGrrrr",
      "lights": [
        {"index": 0, "state": "G", "color": "green"},
        {"index": 1, "state": "G", "color": "green"},
        {"index": 2, "state": "r", "color": "red"},
        ...
      ],
      "is_main": true
    },
    ...
  ]
}
```

**Ý nghĩa các màu:**
- `G` / `green` = 🟢 Đèn xanh - Xe được đi
- `y` / `yellow` = 🟡 Đèn vàng - Chuẩn bị dừng
- `r` / `red` = 🔴 Đèn đỏ - Phải dừng
- `o` / `off` = ⚫ Tắt

### ✅ 3. Countdown Timer - An toàn tối đa

**Vấn đề cũ:** Đèn đổi đột ngột → Xe phanh gấp → Tai nạn!

**Giải pháp mới:** Countdown timer trước khi đổi đèn

#### API Endpoint mới:
```bash
POST /sumo/set-phase-countdown
{
  "phase_index": 2,
  "countdown_seconds": 5  # Đếm ngược 5 giây
}
```

**Flow hoạt động:**
1. Dashboard hiển thị: "⏱️ Đổi sang phase 2 sau 5 giây..."
2. Countdown: 5... 4... 3... 2... 1...
3. Sau đó mới đổi phase với yellow transition
4. An toàn cho cả xe và người đi bộ!

### ✅ 4. Safe Phase Transition

Hệ thống tự động chèn đèn vàng khi cần:

```
Trước: 🟢 Green → 🔴 Red (NGUY HIỂM!)
Sau:  🟢 Green → 🟡 Yellow (3s) → 🔴 Red (AN TOÀN!)
```

**Logic:**
- Phát hiện chuyển đổi nguy hiểm (G→r)
- Tự động tìm yellow phase trong signal program
- Chèn vào giữa với duration 3 giây
- Log rõ ràng: "🟡 Safe transition: 0 → 1 (yellow) → 2"

### ✅ 5. Thông tin chi tiết về xe cộ

Thêm metrics mới:
```json
{
  "loaded_vehicles": 150,     // Tổng xe trong simulation
  "departed_vehicles": 120,   // Xe đã xuất phát
  "arrived_vehicles": 80,     // Xe đã đến đích
  "vehicle_count": 40,        // Xe đang chạy (120 - 80)
  "queue_length": 15,         // Xe đang đợi đèn đỏ
  "waiting_time": 234.5       // Tổng thời gian chờ (giây)
}
```

**Giải thích tại sao xe đứng im:**
- Nếu `vehicle_count = 0` → Hết xe trong simulation
- Nếu `arrived_vehicles = loaded_vehicles` → Tất cả xe đã về đích
- Cần kiểm tra file `routes.rou.xml` để thêm xe

---

## 📋 API Endpoints mới

### GET `/sumo/phases`
Xem tất cả phases có sẵn trong signal program:

```json
{
  "tls_id": "11777727352",
  "current_phase": 0,
  "total_phases": 4,
  "phases": [
    {
      "index": 0,
      "state": "GGrrrrGGrrrr",
      "type": "green",
      "duration": 30.0,
      "description": "Phase 0 - green"
    },
    {
      "index": 1,
      "state": "yyrrrryyrrrr",
      "type": "yellow",
      "duration": 3.0,
      "description": "Phase 1 - yellow"
    },
    ...
  ]
}
```

### POST `/sumo/set-phase`
Đổi phase với safe transition (tự động yellow):

```bash
curl -X POST http://localhost:8000/sumo/set-phase \
  -H "Content-Type: application/json" \
  -d '{"phase_index": 2}'
```

### POST `/sumo/set-phase-countdown`
Đổi phase với countdown timer:

```bash
curl -X POST http://localhost:8000/sumo/set-phase-countdown \
  -H "Content-Type: application/json" \
  -d '{"phase_index": 2, "countdown_seconds": 5}'
```

---

## 🎯 Cách sử dụng trong Dashboard

### Bước 1: Start SUMO
1. Mở dashboard: http://localhost:3001/demo-dashboard.html
2. Chọn scenario (Nga4ThuDuc / NguyenThaiSon / QuangTrung)
3. Click "🚦 Start SUMO"
4. SUMO GUI sẽ tự động mở → Xem trực quan!

### Bước 2: Điều khiển simulation
1. Click "▶ Start" để chạy simulation
2. Xem xe di chuyển trong SUMO GUI
3. Xem metrics real-time trong dashboard

### Bước 3: Điều khiển đèn giao thông
**Cách 1: Thủ công (không countdown)**
- Gọi API `/sumo/set-phase` với phase_index

**Cách 2: An toàn (có countdown)** ⭐ KHUYẾN NGHỊ
1. Gọi API `/sumo/set-phase-countdown` với countdown_seconds
2. Dashboard hiển thị countdown
3. Sau khi hết giờ, tự động đổi phase an toàn

### Bước 4: Monitoring
Dashboard hiển thị:
- **Tất cả traffic lights** với màu sắc từng đèn
- **Time until switch**: Đếm ngược đến khi đổi phase
- **Vehicle count**: Số xe đang chạy
- **Queue length**: Số xe đang chờ đèn đỏ
- **Waiting time**: Thời gian chờ đợi

---

## 🔧 Troubleshooting

### Xe đứng im không chạy?
**Nguyên nhân:**
1. Simulation không step → Kiểm tra dashboard có đang pause không
2. Hết xe trong simulation → Check `departed_vehicles = loaded_vehicles`
3. File routes hết thời gian → Xe đã về hết

**Giải pháp:**
```bash
# Kiểm tra số xe
curl http://localhost:8000/sumo/state | grep vehicle

# Xem trong SUMO GUI:
# View → Vehicles → Show all

# Nếu hết xe, restart SUMO để load lại routes
```

### Đèn giao thông không đổi?
**Nguyên nhân:**
1. Phase index sai → Dùng `/sumo/phases` để xem phases hợp lệ
2. TLS ID sai → Kiểm tra scenario có đúng không

**Giải pháp:**
```bash
# Xem phases hợp lệ
curl http://localhost:8000/sumo/phases

# Thử đổi phase
curl -X POST http://localhost:8000/sumo/set-phase \
  -H "Content-Type: application/json" \
  -d '{"phase_index": 0}'
```

### SUMO GUI không hiện?
**Nguyên nhân:**
- Script vẫn dùng `sumo` thay vì `sumo-gui`
- DISPLAY variable chưa set

**Giải pháp:**
```bash
# Check script
cat /home/thaianh/OLP2025/OLP_2025/scripts/start_sumo.sh | grep sumo-gui

# Should see: sumo-gui -c ...
# If not, the script needs to be updated
```

---

## 📊 Ví dụ response từ API

### GET /sumo/state (Enhanced)
```json
{
  "simulation_time": 123.5,
  "vehicle_count": 42,
  "loaded_vehicles": 150,
  "departed_vehicles": 120,
  "arrived_vehicles": 78,
  "avg_speed": 8.5,
  "queue_length": 12,
  "traffic_lights": [
    {
      "id": "11777727352",
      "current_phase": 0,
      "phase_duration": 30.0,
      "time_until_switch": 18.3,
      "signal_state": "GGrrrrGGrrrr",
      "lights": [
        {"index": 0, "state": "G", "color": "green"},
        {"index": 1, "state": "G", "color": "green"},
        {"index": 2, "state": "r", "color": "red"},
        {"index": 3, "state": "r", "color": "red"},
        {"index": 4, "state": "r", "color": "red"},
        {"index": 5, "state": "r", "color": "red"},
        {"index": 6, "state": "G", "color": "green"},
        {"index": 7, "state": "G", "color": "green"},
        {"index": 8, "state": "r", "color": "red"},
        {"index": 9, "state": "r", "color": "red"},
        {"index": 10, "state": "r", "color": "red"},
        {"index": 11, "state": "r", "color": "red"}
      ],
      "is_main": true
    },
    {
      "id": "2493364036",
      "current_phase": 2,
      "time_until_switch": 25.1,
      "signal_state": "rrrGGG",
      "lights": [...],
      "is_main": false
    }
  ],
  "total_traffic_lights": 7
}
```

---

## 🎨 Dashboard UI Suggestions

Để tận dụng tối đa các tính năng mới, dashboard nên hiển thị:

### 1. Traffic Lights Panel
```html
<div class="traffic-lights-grid">
  <!-- For each traffic light -->
  <div class="tls-card">
    <h4>TLS: 11777727352 (Main)</h4>
    <div class="countdown">⏱️ Switch in: 18s</div>
    <div class="lights-row">
      🟢🟢🔴🔴🔴🔴🟢🟢🔴🔴🔴🔴
    </div>
    <div>Phase: 0 (Green)</div>
  </div>
</div>
```

### 2. Countdown Timer
```html
<div class="phase-change-countdown">
  <h3>⏱️ Phase change in progress</h3>
  <div class="countdown-circle">
    <span class="countdown-number">5</span>
  </div>
  <p>Changing to Phase 2 (East-West Green)</p>
</div>
```

### 3. Vehicle Statistics
```html
<div class="vehicle-stats">
  <div class="stat">
    <span class="label">Active Vehicles:</span>
    <span class="value">42</span>
  </div>
  <div class="stat">
    <span class="label">Completed Trips:</span>
    <span class="value">78 / 150</span>
  </div>
  <div class="stat">
    <span class="label">Queue Length:</span>
    <span class="value">12 vehicles</span>
  </div>
</div>
```

---

## 🔐 Safety Features Summary

| Feature | Before | After |
|---------|--------|-------|
| Phase transition | Direct G→R | G→Y→R (3s yellow) |
| Driver warning | None | Countdown timer |
| Traffic light visibility | 1 TLS only | All TLS with colors |
| Accident prevention | ❌ | ✅ Multiple layers |

---

## 📝 Notes

- **Yellow phase duration**: 3 seconds (configurable in code)
- **Countdown default**: 5 seconds (configurable per request)
- **Time until switch**: Real-time from SUMO TraCI
- **Color coding**: Standard traffic light colors (green/yellow/red)

Hệ thống bây giờ **AN TOÀN** và **TRỰC QUAN** hơn rất nhiều! 🎉
