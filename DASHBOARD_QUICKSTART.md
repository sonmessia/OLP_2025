# 🚦 SUMO Dashboard - Quick Start Guide

## ✅ Hệ thống đã hoạt động!

### 📊 Dashboard đang chạy tại:
- **URL**: http://localhost:3001/demo-dashboard.html
- **Backend API**: http://localhost:8000

### 🎯 Cách sử dụng Dashboard:

#### Bước 1: Start SUMO trên HOST (QUAN TRỌNG!)
Dashboard **KHÔNG thể tự start SUMO** từ container. Bạn phải start SUMO trên máy host trước:

```bash
# Terminal 1: Start SUMO và giữ nó chạy
cd /home/thaianh/OLP2025/OLP_2025
nohup python3 scripts/auto_start_sumo.py Nga4ThuDuc > /tmp/sumo.log 2>&1 &

# Verify SUMO đang chạy:
ps aux | grep "sumo.*8813" | grep -v grep
lsof -i :8813  # Phải thấy sumo listening
```

**Các scenario khác:**
```bash
# Với GUI
nohup python3 scripts/auto_start_sumo.py NguyenThaiSon --gui > /tmp/sumo.log 2>&1 &

# Headless
nohup python3 scripts/auto_start_sumo.py QuangTrung > /tmp/sumo.log 2>&1 &
```

#### Bước 2: Mở Dashboard
1. Dashboard tại: http://localhost:3001/demo-dashboard.html
2. Chọn scenario **PHẢI KHỚP** với SUMO đang chạy (vd: Nga4ThuDuc)
3. Click nút **"Start SUMO"** (màu xanh lá)
   - Dashboard sẽ gọi API để **KẾT NỐI** đến SUMO đã chạy
   - Chờ 2-3 giây để kết nối
   - Status đổi từ "Not Running" → "Connected"

#### Bước 3: Điều khiển Simulation
- **▶ Start**: Bắt đầu simulation (vehicles sẽ di chuyển)
- **⏸ Pause**: Tạm dừng
- **🔄 Reset**: Restart simulation
- **Speed slider**: Điều chỉnh tốc độ 1x-10x

### 📝 System Logs
Dashboard hiển thị real-time logs về:
- Traffic light phase changes
- Vehicle counts
- Speed metrics
- Simulation events

### 🔧 Technical Details

**Backend đã kết nối SUMO thành công:**
```json
{
  "connected": true,
  "scenario": "Nga4ThuDuc",
  "tls_id": "4066470692",
  "host": "172.17.0.1",
  "port": 8813
}
```

**Các endpoint API:**
- `GET  /sumo/status` - Check connection status
- `POST /sumo/start` - Connect to SUMO
- `POST /sumo/stop` - Disconnect
- `POST /sumo/step` - Execute 1 simulation step
- `GET  /sumo/state` - Get current traffic state
- `POST /sumo/set-phase` - Change traffic light phase

### 🐛 Troubleshooting

**Dashboard hiển thị "Failed to start SUMO":**

**Nguyên nhân:** SUMO chưa chạy trên host hoặc đã tắt

**Giải pháp:**
```bash
# 1. Kill processes cũ
pkill -9 -f auto_start_sumo
pkill -9 -f "sumo -c"

# 2. Verify port 8813 trống
lsof -i :8813  # Không nên có output

# 3. Start SUMO lại
cd /home/thaianh/OLP2025/OLP_2025
nohup python3 scripts/auto_start_sumo.py Nga4ThuDuc > /tmp/sumo.log 2>&1 &

# 4. Verify SUMO đang chạy
sleep 3
ps aux | grep "sumo.*8813" | grep -v grep  # Phải thấy process
lsof -i :8813                                # Phải thấy sumo LISTEN

# 5. Restart backend để refresh connection
docker restart backend
sleep 5

# 6. Test connection
curl -X POST http://localhost:8000/sumo/start \
  -H "Content-Type: application/json" \
  -d '{"scenario": "Nga4ThuDuc", "gui": false, "port": 8813}'
  
# 7. Trong dashboard, click "Start SUMO" lại
```

**Dashboard status "Not Running" dù SUMO đang chạy:**
- Click nút "Start SUMO" trong dashboard để kết nối
- Đảm bảo scenario dropdown khớp với SUMO đang chạy
- Check backend logs: `docker logs backend --tail 50`

**Port 8813 bị chiếm:**
```bash
# Kill process đang dùng port
lsof -ti :8813 | xargs kill -9
```

**Backend không phản hồi:**
```bash
docker restart backend
sleep 5
```

**SUMO bị crash:**
```bash
# Check logs
cat /tmp/sumo.log

# Restart với --gui để debug
python3 scripts/auto_start_sumo.py Nga4ThuDuc --gui
```

### 📦 Available Scenarios

1. **Nga4ThuDuc** (Default)
   - 4-way intersection in Thu Duc
   - TLS ID: `4066470692`
   
2. **NguyenThaiSon**
   - 6-way intersection
   - TLS ID: `cluster_1488091499_314059003_314059006_314059008`
   
3. **QuangTrung**
   - Complex intersection
   - TLS ID: `cluster_314061834_314061898`

### 🎉 Success Indicators

✅ SUMO process running (check with `ps aux | grep sumo`)
✅ Port 8813 listening (check with `lsof -i :8813`)
✅ Backend connected (check `/sumo/status` returns `connected: true`)
✅ Dashboard showing "Connected" status
✅ Real-time logs updating in dashboard

---

**Current Status**: ✅ **ALL SYSTEMS OPERATIONAL**
- SUMO: Running (PID found)
- Backend: Connected to SUMO
- Dashboard: Open at localhost:3001
- TraCI: Communication established via 172.17.0.1:8813
