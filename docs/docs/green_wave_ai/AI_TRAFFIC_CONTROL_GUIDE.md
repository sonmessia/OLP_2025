# 🚦 AI Traffic Control - Hướng Dẫn Sử Dụng

## 📋 Tổng Quan

Hệ thống AI điều khiển giao thông thông minh đã được nâng cấp với thuật toán ĐÚNG LOGIC:

### ❌ Vấn Đề Cũ (ĐÃ SỬA)
- Set tất cả đèn giao thông cùng một phase → Toàn xanh hoặc toàn đỏ
- Không phân tích traffic thực tế
- Gây ùn tắc và nguy cơ tai nạn
- Switch scenario gặp lỗi "Connection already active"

### ✅ Giải Pháp Mới
1. **Phân tích TỪNG đèn giao thông riêng lẻ**
2. **Tính toán phase tối ưu dựa trên:**
   - Mật độ xe (occupancy) - 30% weight
   - Số xe chờ (queue length) - 40% weight
   - Thời gian chờ (waiting time) - 30% weight
3. **CHỈ cho đèn xanh ở hướng CẦN THIẾT**
4. **Tự động tránh xung đột giao thông**
5. **Smooth scenario switching** - Tự động cleanup khi chuyển scenario

---

## 🚀 Cách Sử Dụng

### Bước 1: Khởi Động Hệ Thống

```bash
# Terminal 1: Start SUMO Starter Service (nếu chưa chạy)
cd /home/thaianh/OLP2025/OLP_2025
nohup python3 scripts/sumo_starter_service.py > /tmp/sumo_starter.log 2>&1 &

# Verify service running
lsof -i :9999  # Should show python3 listening

# Terminal 2: Start Backend (Docker)
docker-compose up -d backend

# Verify backend running
docker ps | grep backend
curl http://localhost:8000/sumo/status
```

### Bước 2: Mở Dashboard

```bash
# Open dashboard in browser
http://localhost:3001/demo-dashboard.html
```

### Bước 3: Start SUMO Scenario

Trong dashboard:

1. **Chọn Scenario** từ dropdown:
   - ✅ Nga4ThuDuc (4-way intersection) - TLS ID: 4066470692
   - ✅ NguyenThaiSon (6-way intersection) - TLS ID: 11777727352 (7 lights total)
   - ✅ QuangTrung (Complex intersection) - TLS ID: 2269043920 (11 lights total)

2. **Click "Start SUMO"**
   - SUMO GUI sẽ tự động mở
   - Backend sẽ connect via TraCI
   - Status hiển thị "🟢 Connected"

3. **Click "▶ Start"** để chạy simulation
   - Simulation bắt đầu chạy
   - Dashboard cập nhật real-time data

### Bước 4: Enable AI Traffic Control

1. **Scroll xuống "🧠 AI Traffic Control (Smart)"** panel

2. **Click "🤖 Enable AI Control"**
   ```
   Logs sẽ hiển thị:
   ✅ AI Control enabled!
      Traffic Lights: 7
      Algorithm: Smart Priority-Based Phase Selection
      ✓ Phân tích mật độ xe theo thời gian thực
      ✓ Tính toán phase tối ưu cho từng đèn
      ✓ Đèn xanh chỉ cho hướng ưu tiên cao
   ```

3. **AI tự động hoạt động**
   - AI phân tích traffic mỗi 2 giây
   - Quyết định switch phase cho từng đèn độc lập
   - Log hiển thị các quyết định quan trọng:
     ```
     🚦 TLS 11777727: Phase 0→2
     🚦 TLS 24933640: Phase 1→3
     ```

4. **Theo dõi hiệu quả**
   - **Controlled Traffic Lights**: Số đèn được AI điều khiển
   - **Last Decision**: Quyết định gần nhất (t=45s)
   - **Actions Taken**: Tổng số lần switch phase

---

## 🧠 Thuật Toán AI

### Smart Priority-Based Phase Selection

```python
# Cho MỖI traffic light:
for tls_id in all_traffic_lights:
    # 1. Lấy metrics từ TẤT CẢ lanes của đèn này
    for lane in controlled_lanes:
        occupancy = traci.lane.getLastStepOccupancy(lane)
        queue_length = traci.lane.getLastStepHaltingNumber(lane)
        waiting_time = traci.lane.getWaitingTime(lane)
    
    # 2. Tính priority cho MỖI phase có thể
    for phase in available_phases:
        # Chỉ tính cho lanes sẽ được xanh trong phase này
        green_lanes = get_green_lanes(phase)
        
        # Weighted priority score
        priority[phase] = (
            0.30 * avg_occupancy(green_lanes) +
            0.40 * avg_queue(green_lanes) +
            0.30 * avg_waiting(green_lanes)
        )
    
    # 3. Chọn phase có priority CAO NHẤT
    best_phase = max(priority)
    
    # 4. Switch nếu cần (với threshold để tránh oscillation)
    if best_phase != current_phase:
        if priority[best_phase] > priority[current_phase] + 0.15:
            switch_to_phase(best_phase)
```

### Đặc Điểm Quan Trọng

1. **Independence**: Mỗi đèn được phân tích và điều khiển RIÊNG BIỆT
2. **Real-time**: Dựa trên dữ liệu traffic THỰC TẾ mỗi giây
3. **Safety**: Thời gian xanh tối thiểu 10s (tránh nhấp nháy)
4. **Stability**: Threshold 15% để tránh switch liên tục (oscillation)
5. **Conflict-Free**: Không có trường hợp "toàn đèn xanh" - mỗi đèn tự quyết định

---

## 📊 So Sánh với Phương Pháp Cũ

| Tiêu Chí | Cũ (Manual) | Mới (AI Smart) |
|----------|-------------|----------------|
| **Phân tích** | Không | ✅ Real-time per TLS |
| **Phase selection** | 1 phase cho TẤT CẢ | ✅ Optimal per TLS |
| **Traffic data** | Ignored | ✅ Occupancy + Queue + Wait |
| **Xung đột** | Có thể xảy ra | ✅ Tự động tránh |
| **Adaptability** | Fixed timing | ✅ Dynamic by traffic |
| **Hiệu quả** | Thấp | ✅ Tối ưu theo thời gian thực |

---

## 🔧 Troubleshooting

### 1. SUMO GUI không mở khi click "Start SUMO"

**Nguyên nhân**: SUMO Starter Service chưa chạy

**Giải pháp**:
```bash
# Check service
lsof -i :9999

# If not running, start it
nohup python3 /home/thaianh/OLP2025/OLP_2025/scripts/sumo_starter_service.py > /tmp/sumo_starter.log 2>&1 &

# Check logs
tail -f /tmp/sumo_starter.log
```

### 2. Lỗi "Connection already active" khi switch scenario

**Đã fix!** Script giờ tự động:
- Kill SUMO cũ hoàn toàn
- Đợi port 8813 free (timeout 5s)
- Force close TraCI connection trước khi connect mới

**Nếu vẫn gặp**:
```bash
# Manual cleanup
lsof -ti :8813 | xargs kill -9
docker-compose restart backend
```

### 3. AI Control không hoạt động

**Check list**:
```bash
# 1. SUMO phải connected
curl http://localhost:8000/sumo/status
# Phải thấy "connected": true

# 2. Simulation phải đang chạy
# Click "▶ Start" trong dashboard

# 3. Backend logs
docker logs backend --tail 50 | grep -i "ai\|smart"
```

### 4. QuangTrung scenario trắng màn hình

**Đã fix!** Additional files (eed.xml, probes.xml) đã bị disable vì edge IDs không tồn tại.

**Verify**:
```bash
# Check config
cat src/backend/app/sumo_rl/sumo_files/QuangTrung/quangtrungcar.sumocfg
# Should see <!-- <additional-files ... /> --> commented out

# If not, disable it:
sed -i 's/<additional-files/<\\!-- <additional-files/' quangtrungcar.sumocfg
sed -i 's/\/>/\/> -->/' quangtrungcar.sumocfg
```

---

## 📈 Metrics & Performance

### Vehicle Statistics (Real-time)
- **Active Vehicles**: Số xe đang chạy
- **Loaded/Departed**: Xe đã spawn / đã vào road network
- **Arrived**: Xe đã hoàn thành route (arrived = loaded → simulation kết thúc)
- **Queue Length**: Tổng xe đang chờ
- **Waiting Time**: Tổng thời gian chờ

### AI Performance
- **Actions Taken**: Số lần AI đã switch phase
- **Controlled TLS**: Số đèn đang được AI điều khiển
- **Last Decision**: Quyết định gần nhất với timestamp

### Expected Behavior
- **High traffic** (queue > 5): AI switch phase thường xuyên (mỗi 10-15s)
- **Low traffic** (queue < 2): AI giữ phase ổn định (30-60s)
- **Mixed**: AI cân bằng giữa stability và responsiveness

---

## 🎯 Demo Scenarios

### Scenario 1: NguyenThaiSon (Recommended)
- **7 traffic lights** - Best for testing multi-TLS coordination
- **Complex intersection** - Shows AI advantages clearly
- **Good vehicle distribution** - Realistic traffic patterns

**Demo steps**:
1. Start NguyenThaiSon
2. Enable AI Control
3. Watch "All Traffic Lights" panel - see each light adapt independently
4. Compare with manual control (disable AI, use fixed phases)

### Scenario 2: QuangTrung
- **11 traffic lights** - Maximum complexity
- **Large network** - Press Ctrl+H to fit view
- **Heavy traffic** - Best for stress testing AI

### Scenario 3: Nga4ThuDuc  
- **1 main traffic light** - Simple baseline
- **Small network** - Fast simulation
- **Quick demo** - Good for explaining algorithm

---

## 🔑 Key Takeaways

1. ✅ **AI không điều khiển TẤT CẢ đèn cùng lúc** - Mỗi đèn độc lập!
2. ✅ **Không có "toàn đèn xanh"** - Chỉ xanh ở hướng cần thiết
3. ✅ **Dựa trên dữ liệu thực tế** - Không phải giả định/pattern cố định
4. ✅ **Tự động tránh xung đột** - Safety by design
5. ✅ **Adaptive** - Thay đổi theo traffic conditions real-time

**ĐÂY MỚI LÀ ĐIỀU HƯỚNG GIAO THÔNG THÔNG MINH!** 🚦🧠

---

## 📞 Support

Nếu gặp vấn đề:
1. Check backend logs: `docker logs backend --tail 100`
2. Check SUMO logs: `cat /tmp/sumo_*.log`
3. Check browser console: F12 → Console tab
4. Check this guide's Troubleshooting section

Happy Traffic Controlling! 🎉
