# 🔄 Hướng dẫn chuyển Scenario trong Dashboard

## Cách chuyển từ scenario này sang scenario khác

### Bước 1: Stop SUMO hiện tại

**Trong Terminal:**
```bash
# Kill tất cả SUMO processes
pkill -9 -f "sumo -c"
pkill -9 -f "sumo-gui"

# Hoặc kill specific port
lsof -ti :8813 | xargs kill -9

# Verify port đã trống
lsof -i :8813  # Không có output = OK
```

**Trong Dashboard:**
1. Click nút **"⏹️ Stop SUMO"**
2. Đợi status đổi thành "⚫ Not Connected"

### Bước 2: Start SUMO scenario mới

Chọn **1 trong 3** cách sau:

#### Cách 1: Dùng helper script (KHUYẾN NGHỊ)
```bash
cd /home/thaianh/OLP2025/OLP_2025

# Nga 4 Thủ Đức
nohup python3 scripts/auto_start_sumo.py Nga4ThuDuc > /tmp/sumo.log 2>&1 &

# Ngã 6 Nguyễn Thái Sơn  
nohup python3 scripts/auto_start_sumo.py NguyenThaiSon > /tmp/sumo.log 2>&1 &

# Quang Trung
nohup python3 scripts/auto_start_sumo.py QuangTrung > /tmp/sumo.log 2>&1 &
```

#### Cách 2: Start SUMO trực tiếp
```bash
cd /home/thaianh/OLP2025/OLP_2025

# Nga 4 Thủ Đức
cd src/backend/app/sumo_rl/sumo_files/Nga4ThuDuc
nohup sumo -c Nga4ThuDuc.sumocfg --remote-port 8813 --step-length 1.0 > /tmp/sumo.log 2>&1 &

# Ngã 6 Nguyễn Thái Sơn
cd src/backend/app/sumo_rl/sumo_files/NguyenThaiSon
nohup sumo -c Nga6NguyenThaiSon.sumocfg --remote-port 8813 --step-length 1.0 > /tmp/sumo.log 2>&1 &

# Quang Trung
cd src/backend/app/sumo_rl/sumo_files/QuangTrung
nohup sumo -c quangtrungcar.sumocfg --remote-port 8813 --step-length 1.0 > /tmp/sumo.log 2>&1 &
```

#### Cách 3: Start với GUI (để debug)
```bash
# Thêm --gui flag
python3 scripts/auto_start_sumo.py NguyenThaiSon --gui
```

### Bước 3: Verify SUMO đã start

```bash
# Check process đang chạy
ps aux | grep "sumo.*8813" | grep -v grep

# Check port đang listen
lsof -i :8813
# Output mẫu:
# sumo    123456 user  3u  IPv4 1234567  0t0  TCP *:8813 (LISTEN)
```

### Bước 4: Kết nối Dashboard

1. Trong Dashboard, chọn scenario **khớp** với SUMO vừa start
   - Ngã Tư Thủ Đức → chọn "Ngã Tư Thủ Đức (4-way)"
   - Ngã 6 Nguyễn Thái Sơn → chọn "Ngã 6 Nguyễn Thái Sơn (6-way)"
   - Quang Trung → chọn "Quang Trung (Complex)"

2. Click **"🚦 Start SUMO"**

3. Đợi 2-3 giây, status sẽ hiện:
   - ✅ "🟢 Connected" = Thành công
   - ❌ "⚫ Not Connected" = Thất bại, kiểm tra lại

4. Nếu thành công, click **"▶ Start"** để chạy simulation

## ⚠️ Lưu ý quan trọng

### Lỗi "ERR_NETWORK_CHANGED" khi chuyển scenario
**Nguyên nhân:** Backend vẫn giữ kết nối cũ với SUMO scenario cũ

**Giải pháp:**
```bash
# 1. Stop SUMO cũ
pkill -9 -f "sumo -c"

# 2. Restart backend để xóa connection cũ
docker restart backend
sleep 5

# 3. Start SUMO scenario mới
python3 scripts/auto_start_sumo.py NguyenThaiSon

# 4. Trong dashboard, click "Start SUMO"
```

### Lỗi "500 Internal Server Error"
**Nguyên nhân:** SUMO chưa chạy hoặc port 8813 bị block

**Giải pháp:**
```bash
# Verify SUMO đang chạy
lsof -i :8813  # Phải có output

# Nếu không có, start lại SUMO
python3 scripts/auto_start_sumo.py Nga4ThuDuc

# Test connection từ container
docker exec backend python3 -c "
import socket
result = socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect_ex(('172.17.0.1', 8813))
print(f'Connection result: {result}')  # 0 = success
"
```

### Dashboard không update data
**Nguyên nhân:** Simulation chưa được start

**Giải pháp:**
1. Check status: "🟢 Connected" phải xuất hiện
2. Click **"▶ Start"** button trong Control Panel
3. Check browser console (F12) xem có lỗi không

## 🎯 Quick Commands

```bash
# Stop tất cả + restart NguyenThaiSon
pkill -9 -f sumo && \
docker restart backend && \
sleep 5 && \
cd /home/thaianh/OLP2025/OLP_2025 && \
python3 scripts/auto_start_sumo.py NguyenThaiSon

# Verify everything
lsof -i :8813 && \
docker logs backend --tail 5 && \
echo "✅ Ready! Open dashboard and click 'Start SUMO'"
```

## 📋 Checklist chuyển scenario

- [ ] Stop SUMO cũ: `pkill -9 -f "sumo -c"`
- [ ] Verify port trống: `lsof -i :8813` (no output)
- [ ] Start SUMO mới: `python3 scripts/auto_start_sumo.py <scenario>`
- [ ] Verify SUMO running: `ps aux | grep sumo`
- [ ] Chọn scenario trong dashboard dropdown
- [ ] Click "🚦 Start SUMO"
- [ ] Wait for "🟢 Connected"
- [ ] Click "▶ Start" để chạy simulation

---

**Last Updated:** 2025-11-30
