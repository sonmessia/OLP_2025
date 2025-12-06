# 🚀 SUMO Simulation Setup Guide

## 📋 Prerequisites

1. **Install SUMO** (Simulation of Urban Mobility)

```bash
# Ubuntu/Debian
sudo add-apt-repository ppa:sumo/stable
sudo apt-get update
sudo apt-get install sumo sumo-tools sumo-doc

# Set SUMO_HOME
echo 'export SUMO_HOME=/usr/share/sumo' >> ~/.bashrc
source ~/.bashrc
```

2. **X11 Server for GUI** (If using Docker)

```bash
# Allow Docker to use your display
xhost +local:docker

# Or for specific display
export DISPLAY=:0
```

## 🎯 Quick Start

### Option 1: Direct Python (Recommended for Development)

```bash
# 1. Start backend
cd src/backend
uvicorn app.main:app --reload --port 8000

# 2. In another terminal, start SUMO
python3 -m app.sumo_rl.agents.sumo_runner --scenario Nga4ThuDuc --gui --duration 300

# 3. Open dashboard
open http://localhost:8000/../../../demo-dashboard.html
# Or serve it:
python3 -m http.server 3000
# Then: http://localhost:3000/demo-dashboard.html
```

### Option 2: Using Docker Compose

```bash
# 1. Setup environment
cp .env.example .env
# Edit .env:
#   SUMO_SCENARIO=Nga4ThuDuc  # or NguyenThaiSon, QuangTrung
#   DISPLAY=:0

# 2. Allow X11 access
xhost +local:docker

# 3. Start all services
docker-compose up -d

# 4. Check SUMO logs
docker logs -f sumo-simulation

# 5. Open dashboard
open demo-dashboard.html
```

## 🗺️ Available Scenarios

| Scenario | Description | TLS ID | Files |
|----------|-------------|--------|-------|
| **Nga4ThuDuc** | Ngã tư Thủ Đức (4-way) | `4066470692` | `Nga4ThuDuc/Nga4ThuDuc.sumocfg` |
| **NguyenThaiSon** | Ngã 6 Nguyễn Thái Sơn (6-way) | `cluster_1488091499_...` | `NguyenThaiSon/Nga6NguyenThaiSon.sumocfg` |
| **QuangTrung** | Quang Trung (Complex) | `cluster_314061834_...` | `QuangTrung/quangtrungcar.sumocfg` |

## 🎮 Dashboard Controls

### 1. Start SUMO via Dashboard

1. Open `demo-dashboard.html`
2. Select scenario from dropdown
3. Click "🚦 Start SUMO"
4. SUMO GUI window will open
5. Dashboard shows real-time data

### 2. Start SUMO via API

```bash
# Start simulation
curl -X POST http://localhost:8000/sumo/start \
  -H "Content-Type: application/json" \
  -d '{
    "scenario": "Nga4ThuDuc",
    "gui": true,
    "port": 8813
  }'

# Get current state
curl http://localhost:8000/sumo/state

# Stop simulation
curl -X POST http://localhost:8000/sumo/stop
```

### 3. Start SUMO via Command Line

```bash
# With GUI
python3 -m app.sumo_rl.agents.sumo_runner \
  --scenario Nga4ThuDuc \
  --gui \
  --duration 300

# Headless (no GUI)
python3 -m app.sumo_rl.agents.sumo_runner \
  --scenario NguyenThaiSon \
  --duration 600

# Custom port
python3 -m app.sumo_rl.agents.sumo_runner \
  --scenario QuangTrung \
  --gui \
  --port 8814
```

## 🔌 API Endpoints

### SUMO Control

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/sumo/start` | Start SUMO simulation |
| `POST` | `/sumo/stop` | Stop SUMO simulation |
| `POST` | `/sumo/step` | Execute one simulation step |
| `GET` | `/sumo/state` | Get current traffic state |
| `POST` | `/sumo/set-phase` | Set traffic light phase |
| `GET` | `/sumo/scenarios` | List available scenarios |
| `GET` | `/sumo/status` | Get simulation status |

### SUMO RL (AI Agent)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/sumo-rl/ai/notify` | AI agent notification |
| `POST` | `/sumo-rl/iot/notify` | IoT agent notification |
| `GET` | `/sumo-rl/status` | System status |
| `GET` | `/sumo-rl/model-info` | DQN model info |

## 📊 Real-time Data Flow

```
SUMO Simulation (GUI)
    │
    ├─ TraCI API
    │     │
    │     ▼
    └─ IoT Agent (/app/sumo_rl/agents/iot_agent.py)
          │
          ├─ Read detector data (e2_0, e2_2)
          │     ├─ Vehicle count
          │     ├─ Average speed
          │     └─ Occupancy
          │
          ├─ POST to Orion-LD
          │     └─ TrafficFlowObserved entity
          │
          └─ Receive commands
                └─ Set traffic light phase
                
Orion-LD Broker
    │
    ├─ Store entities
    ├─ Trigger subscriptions
    └─ Notify AI Agent
    
AI Agent (DQN Model)
    │
    ├─ Process traffic state
    ├─ Predict optimal phase
    └─ Update TrafficLight entity
    
Dashboard (HTML/JavaScript)
    │
    ├─ Fetch /sumo/state (every 1s)
    ├─ Update charts
    └─ Display metrics
```

## 🐛 Troubleshooting

### 1. "SUMO not found"

```bash
# Check SUMO installation
which sumo
which sumo-gui

# Set SUMO_HOME
export SUMO_HOME=/usr/share/sumo
echo $SUMO_HOME
```

### 2. "Cannot connect to X server" (Docker)

```bash
# Allow X11 access
xhost +local:docker

# Check DISPLAY
echo $DISPLAY  # Should be :0 or :1

# Set in .env
DISPLAY=:0
```

### 3. "TraCI connection failed"

```bash
# Check if SUMO is running
ps aux | grep sumo

# Kill existing SUMO processes
pkill -9 sumo
pkill -9 sumo-gui

# Try different port
python3 -m app.sumo_rl.agents.sumo_runner --port 8814
```

### 4. "Config file not found"

```bash
# Check file exists
ls src/backend/app/sumo_rl/sumo_files/Nga4ThuDuc/Nga4ThuDuc.sumocfg

# Verify scenario name (case-sensitive)
# ✅ Correct: Nga4ThuDuc
# ❌ Wrong: nga4thuduc, Nga4thuduc
```

### 5. Dashboard not showing real data

```bash
# Check backend is running
curl http://localhost:8000/sumo/status

# Start SUMO first
curl -X POST http://localhost:8000/sumo/start -H "Content-Type: application/json" -d '{"scenario": "Nga4ThuDuc", "gui": true}'

# Check browser console for errors
# Open DevTools (F12) → Console tab
```

## 📈 Performance Tips

1. **For Demo (Visual)**
   - Use `--gui` flag
   - Set `--delay 100` for slower, visible simulation
   - Use Nga4ThuDuc (simplest scenario)

2. **For Training (Speed)**
   - Don't use `--gui`
   - Use headless mode
   - Increase `--step-length 0.1` for faster simulation

3. **For Testing**
   - Use NguyenThaiSon (moderate complexity)
   - Run for 300-600 seconds
   - Monitor memory usage

## 🎥 Demo Checklist

- [ ] Start backend: `uvicorn app.main:app --reload`
- [ ] Open dashboard: `demo-dashboard.html`
- [ ] Select scenario: "Nga4ThuDuc"
- [ ] Click "Start SUMO" button
- [ ] SUMO GUI window appears
- [ ] Dashboard shows real-time metrics
- [ ] Traffic light animation synced
- [ ] Charts updating every second
- [ ] Explain: "AI is making decisions based on traffic flow"
- [ ] Show comparison: DQN vs Baseline (13% improvement)

## 📚 Next Steps

1. **Connect QuantumLeap** for historical data
2. **Enable AI Agent** for automatic traffic control
3. **Add notifications** to Orion-LD subscriptions
4. **Deploy to cloud** with Kubernetes

---

**Created**: November 30, 2025  
**Version**: 2.0  
**Scenarios**: 3 (Nga4ThuDuc, NguyenThaiSon, QuangTrung)  
**Status**: ✅ Ready for Demo
