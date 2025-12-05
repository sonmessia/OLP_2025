# 🚦 Quick Start - SUMO + Dashboard

## ✅ Hiện tại đang chạy
- ✅ Backend API: http://localhost:8000
- ✅ Dashboard: http://localhost:3001/demo-dashboard.html
- ✅ Orion-LD: http://localhost:1026

## 🎮 Cách chạy SUMO Simulation

### Option 1: Chạy SUMO trên Host (Recommended - Đơn giản nhất)

```bash
# 1. Chạy script trong terminal mới
cd /home/thaianh/OLP2025/OLP_2025
./run_sumo.sh NguyenThaiSon

# Hoặc các scenario khác:
./run_sumo.sh Nga4ThuDuc
./run_sumo.sh QuangTrung
```

SUMO-GUI sẽ mở với:
- ✅ Giao diện đồ họa để xem traffic
- ✅ TraCI server on port 8813
- ✅ Có thể control từ dashboard

### Option 2: Chạy bằng Python script

```bash
cd /home/thaianh/OLP2025/OLP_2025/src/backend

# Set SUMO_HOME nếu chưa có
export SUMO_HOME=/usr/share/sumo

# Chạy IoT Agent (auto-connect SUMO)
python3 -m app.sumo_rl.agents.iot_agent --scenario NguyenThaiSon --gui
```

### Option 3: Manual SUMO với TraCI

```bash
# Terminal 1: Start SUMO với TraCI
cd /home/thaianh/OLP2025/OLP_2025/src/backend/app/sumo_rl/sumo_files
sumo-gui -c NguyenThaiSon/Nga6NguyenThaiSon.sumocfg --remote-port 8813 --start

# Terminal 2: Backend API sẽ auto-detect và connect
# (Hiện tại chưa hỗ trợ auto-connect, cần update code)
```

## 🎯 Dashboard Features

1. **Traffic Metrics** 📊
   - Vehicle count real-time
   - Average speed
   - Queue length
   - Waiting time

2. **Environment Metrics** 🌍
   - CO₂ emissions
   - NOx levels
   - PM2.5 air quality

3. **Traffic Light Control** 🚦
   - View current phase
   - Manual phase control
   - AI-based optimization (khi model loaded)

## 🔧 Troubleshooting

### Lỗi "SUMO_HOME not set"
```bash
# Add to ~/.zshrc or ~/.bashrc
export SUMO_HOME=/usr/share/sumo
export PATH=$PATH:$SUMO_HOME/bin
```

### Lỗi "Connection refused" khi dashboard call API
- ✅ Check backend: `curl http://localhost:8000/`
- ✅ Check CORS settings trong main.py
- ✅ Dashboard đang dùng port 3001, backend port 8000

### SUMO không hiển thị GUI
```bash
# Check DISPLAY
echo $DISPLAY  # Nên là :0 hoặc :1

# Nếu lỗi, set lại
export DISPLAY=:0
```

## 📝 Current Status

**Working:**
- ✅ Backend API with all routers
- ✅ Dashboard HTML with charts
- ✅ SUMO scenarios configured (3 scenarios)
- ✅ Traffic light router with AI/IoT agents

**Pending:**
- ⏳ SUMO integration in Docker (cần SUMO_HOME in container)
- ⏳ Auto-connect TraCI from backend
- ⏳ DQN model loading (TensorFlow compatibility issue)

**Recommended Next Steps:**
1. Chạy SUMO trên host với `./run_sumo.sh`
2. Mở dashboard để xem real-time data
3. Test traffic light control manual
4. (Optional) Fix DQN model để enable AI control

## 🚀 Demo Flow

```bash
# Terminal 1: Start SUMO
./run_sumo.sh NguyenThaiSon

# Terminal 2: Watch backend logs
docker logs -f backend

# Browser: Open dashboard
# http://localhost:3001/demo-dashboard.html
```

Enjoy! 🎉
