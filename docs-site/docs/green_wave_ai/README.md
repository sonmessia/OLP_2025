# 🚦 Smart AI Traffic Control System

**OLP 2025** - Intelligent Traffic Light Management using SUMO, FIWARE, and Priority-Based AI Algorithm

[![CI/CD](https://github.com/sonmessia/OLP_2025/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/sonmessia/OLP_2025/actions)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://www.docker.com/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

## 🎯 Features

- **🧠 Smart AI Traffic Controller**: Priority-based algorithm analyzing each traffic light independently
- **📊 Real-time Dashboard**: Monitor traffic flow, vehicle count, and AI decisions
- **🌐 FIWARE Integration**: Context broker for IoT data management
- **🚗 SUMO Simulation**: 3 real-world scenarios (Nga4ThuDuc, NguyenThaiSon, QuangTrung)
- **🐳 Fully Dockerized**: Run anywhere with Docker
- **🔄 Live Scenario Switching**: Change scenarios on-the-fly via dashboard

---

## 🚀 Quick Start (3 Steps)

### 1️⃣ Clone & Configure

```bash
git clone https://github.com/sonmessia/OLP_2025.git
cd OLP_2025
cp .env.example .env
```

### 2️⃣ Start Services

```bash
# Linux/macOS: Allow GUI access
xhost +local:docker

# Start all services
docker-compose up -d --build
```

### 3️⃣ Open Dashboard

**Browser:** [http://localhost:3001/demo-dashboard.html](http://localhost:3001/demo-dashboard.html)

**That's it!** 🎉

---

## 📦 System Architecture

```
┌─────────────────┐     ┌──────────────┐     ┌─────────────┐
│  Web Dashboard  │────▶│  Backend API │────▶│    SUMO     │
│  (Port 3001)    │     │  (Port 8000) │     │ (Port 8813) │
└─────────────────┘     └──────────────┘     └─────────────┘
                              │
                              ▼
                        ┌──────────────┐
                        │ FIWARE Orion │
                        │  (Port 1026) │
                        └──────────────┘
```

**Services:**

- **Backend**: FastAPI (Python 3.9)
- **SUMO**: Traffic simulation with TraCI
- **Orion-LD**: FIWARE context broker
- **QuantumLeap**: Time-series data
- **PostgreSQL + MongoDB**: Data storage

---

## 🎮 Usage

### Start SUMO Simulation

1. Open dashboard: `http://localhost:3001/demo-dashboard.html`
2. Select scenario: **Nga4ThuDuc** / **NguyenThaiSon** / **QuangTrung**
3. Click **"Start SUMO"**
4. Enable **"AI Traffic Control"**

### AI Control Features

- **Independent TLS Analysis**: Each traffic light controlled separately
- **Priority Metrics**:
  - Occupancy (30%)
  - Queue Length (40%)
  - Waiting Time (30%)
- **Real-time Decisions**: Dashboard shows AI actions every 2 seconds

### API Endpoints

```bash
# Check SUMO connection
curl http://localhost:8000/sumo/status

# Enable AI control
curl -X POST http://localhost:8000/sumo/ai-control

# Execute AI decision step
curl -X POST http://localhost:8000/sumo/ai-step
```

---

## 📚 Documentation

- **[Deployment Guide](DEPLOYMENT_GUIDE.md)** - Deploy on any machine (Linux/macOS/Windows/Cloud)
- **[AI Traffic Control Guide](AI_TRAFFIC_CONTROL_GUIDE.md)** - Algorithm details and usage
- **[Scenario Switching Guide](SCENARIO_SWITCHING_GUIDE.md)** - Manage multiple scenarios
- **[Dashboard Quickstart](DASHBOARD_QUICKSTART.md)** - UI walkthrough

---

## 🛠️ Development

### Local Development Setup

```bash
# Install Python dependencies
cd src/backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Install SUMO (Ubuntu/Debian)
sudo add-apt-repository ppa:sumo/stable
sudo apt-get update
sudo apt-get install sumo sumo-tools sumo-doc

# Run backend
uvicorn app.main:app --reload

# Run SUMO starter service
python3 scripts/sumo_starter_service.py
```

### Code Quality

```bash
# Format code
black src/backend/app/

# Lint
ruff check src/backend/app/

# Type check
mypy src/backend/app/

# Run tests
pytest src/backend/tests/
```

---

## 🌍 Platform Support

| Platform    | GUI Support      | Status     |
| ----------- | ---------------- | ---------- |
| **Linux**   | ✅ Native X11    | ✅ Tested  |
| **macOS**   | ✅ XQuartz       | ✅ Tested  |
| **Windows** | ✅ WSL2 + VcXsrv | ⚠️ Partial |
| **Cloud**   | ❌ Headless only | ✅ Works   |

**See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for platform-specific instructions.**

---

## 🔧 Troubleshooting

### SUMO GUI doesn't show

```bash
# Linux
xhost +local:docker
docker-compose restart sumo-simulation

# macOS
open -a XQuartz
xhost + $(ipconfig getifaddr en0)
```

### Port conflicts

```bash
# Check ports
lsof -i :8000  # Backend
lsof -i :8813  # SUMO

# Change ports in docker-compose.yaml
```

### Connection errors

```bash
# Restart all services
docker-compose down
docker-compose up -d

# Check logs
docker-compose logs -f
```

---

## 📊 Scenarios

### 1. Nga4ThuDuc

- **Vehicles**: 200
- **Traffic Lights**: 7
- **Main Intersection**: 4066470692

### 2. NguyenThaiSon

- **Vehicles**: 200
- **Traffic Lights**: 7
- **Main Intersection**: 11777727352

### 3. QuangTrung

- **Vehicles**: 300
- **Traffic Lights**: 11
- **Main Intersection**: 2269043920

---

## 🤝 Contributing

```bash
# Create feature branch
git checkout -b feat/your-feature

# Make changes and commit
git add .
git commit -m "feat: Add your feature"

# Push and create PR
git push origin feat/your-feature
```

**Before submitting PR:**

- [ ] Tests pass: `pytest`
- [ ] Code formatted: `black .`
- [ ] No lint errors: `ruff check .`
- [ ] Type hints valid: `mypy .`

---

## 📝 License

MIT License - see [LICENSE](LICENSE) file

---

## 🙏 Acknowledgments

- **SUMO**: [Eclipse SUMO](https://www.eclipse.org/sumo/)
- **FIWARE**: [FIWARE Foundation](https://www.fiware.org/)
- **Team**: OLP 2025 Contributors

---

## 📧 Contact

- **GitHub Issues**: [Report bugs](https://github.com/sonmessia/OLP_2025/issues)
- **Pull Requests**: [Contribute](https://github.com/sonmessia/OLP_2025/pulls)

---

**⭐ Star this repo if you find it useful!**
