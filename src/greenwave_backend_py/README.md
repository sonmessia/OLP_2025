# GreenWave Backend - Unified AI Traffic Control System

Backend thống nhất cho hệ thống điều khiển giao thông thông minh GreenWave, tích hợp AI (DQN), SUMO simulation, và Orion Context Broker.

## 🌟 Tính năng

### Core Features

- ✅ **Real-time WebSocket**: Truyền dữ liệu mô phỏng theo thời gian thực
- ✅ **RESTful API**: Endpoints đầy đủ cho điều khiển và truy vấn
- ✅ **Orion Integration**: Kết nối với Orion Context Broker (NGSI-LD)
- ✅ **Area Management**: Quản lý nhiều khu vực giao thông

### AI Features

- 🤖 **DQN Agent**: Deep Q-Network cho điều khiển đèn giao thông thông minh
- 📊 **Training Tools**: Scripts để train model mới
- 📈 **Evaluation**: So sánh hiệu suất với baseline
- 🔄 **Hot Reload**: Reload model mà không cần restart server

### SUMO Integration

- 🚗 **SUMO Simulation**: Tích hợp TraCI để điều khiển SUMO
- 📡 **Real-time Data**: Đọc queue, phase, emissions từ SUMO
- 🎮 **GUI Support**: Chạy với hoặc không có SUMO GUI
- 🔧 **Multi-scenario**: Hỗ trợ nhiều scenarios (Nga4ThuDuc, NguyenThaiSon, QuangTrung)

## 🏗️ Kiến trúc

```
┌─────────────┐      TraCI       ┌──────────────┐
│  SUMO       │◄─────────────────┤  IoT Service │
│  Simulation │                  │  (Python)    │
└─────────────┘                  └──────┬───────┘
                                        │
                                        ▼
                                 ┌──────────────┐
                                 │  AI Service  │
                                 │  DQN Agent   │
                                 └──────┬───────┘
                                        │
                                        ▼
┌─────────────┐    WebSocket    ┌──────────────┐      HTTP      ┌──────────────┐
│  Frontend   │◄────────────────┤  GreenWave   │◄───────────────┤    Orion     │
│  (React)    │                 │   Backend    │                │   Broker     │
└─────────────┘                 │  (FastAPI)   │                └──────────────┘
                                └──────────────┘
```

## 📦 Tech Stack

- **FastAPI** - Modern, fast web framework
- **Uvicorn** - ASGI server
- **WebSockets** - Real-time communication
- **TensorFlow/Keras** - Deep learning framework
- **SUMO/TraCI** - Traffic simulation
- **HTTPX** - Async HTTP client
- **Pydantic** - Data validation

## 🚀 Cài đặt

### 1. Clone repository

```bash
cd greenwave_backend_py
```

### 2. Tạo virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Cài đặt dependencies

```bash
pip install -r requirements.txt
```

### 4. Cấu hình môi trường

Copy `.env.example` thành `.env` và điều chỉnh:

```bash
cp .env.example .env
```

Chỉnh sửa `.env`:

```env
# Bật AI control
AI_ENABLED=true

# Bật SUMO simulation
SUMO_ENABLED=true
```

### 5. Cài đặt SUMO (nếu dùng SUMO)

#### Windows

Download từ [SUMO website](https://sumo.dlr.de/docs/Downloads.php)

Set environment variable:

```
SUMO_HOME=C:\Program Files (x86)\Eclipse\Sumo
```

#### Linux

```bash
sudo apt-get install sumo sumo-tools sumo-doc
export SUMO_HOME=/usr/share/sumo
```

#### Mac

```bash
brew install sumo
export SUMO_HOME=/opt/homebrew/share/sumo
```

## 🎮 Chạy ứng dụng

### Development mode

```bash
python -m uvicorn src.main:app --reload --port 3001
```

Hoặc:

```bash
python -m src.main
```

### Production mode

```bash
uvicorn src.main:app --host 0.0.0.0 --port 3001 --workers 4
```

### Docker

```bash
docker build -t greenwave-backend .
docker run -p 3001:3001 greenwave-backend
```

## 📚 API Documentation

Sau khi chạy server, truy cập:

- **Swagger UI**: http://localhost:3001/docs
- **ReDoc**: http://localhost:3001/redoc

### Core Endpoints

#### Health Check

```
GET /health
```

#### Areas

```
GET /api/areas
GET /api/areas/{area_name}
```

#### Simulation Control

```
POST /api/simulation/start
POST /api/simulation/stop
GET  /api/simulation/status
POST /api/command/phase
```

### AI Control Endpoints

```
POST /api/ai/start          # Bật AI control
POST /api/ai/stop           # Tắt AI control
POST /api/ai/toggle         # Toggle AI control
GET  /api/ai/status         # Trạng thái AI
POST /api/ai/reload         # Reload model
```

### SUMO Control Endpoints

```
POST /api/sumo/start        # Bắt đầu SUMO simulation
POST /api/sumo/stop         # Dừng SUMO simulation
GET  /api/sumo/status       # Trạng thái SUMO
POST /api/sumo/phase        # Set traffic light phase
```

### WebSocket

```
WS /ws
```

#### Client → Server

```json
{
  "type": "command",
  "data": {
    "command": "setPhase",
    "params": { "phase": 0 }
  },
  "timestamp": 1234567890
}
```

#### Server → Client

```json
{
  "type": "simulation_update",
  "data": {
    "vehicles": [...],
    "trafficLights": [...],
    "trafficFlow": {
      "queues": [3, 5],
      "phase": 0,
      "timestamp": 1234567890
    },
    "airQuality": {
      "pm25": 45.2,
      "timestamp": 1234567890
    },
    "reward": -2.34
  },
  "timestamp": 1234567890
}
```

## 🎓 Training DQN Model

### Chạy training

```bash
cd src/training
python train_dqn.py
```

Model sẽ được lưu vào `models/dqn_model.h5`

### Hyperparameters

Chỉnh sửa trong `train_dqn.py`:

- `TOTAL_STEPS`: 10,000
- `STATE_SIZE`: 4 (2 queues + phase + pm25)
- `MIN_GREEN_STEPS`: 100
- `GAMMA`: 0.95
- `LEARNING_RATE`: 0.001
- `BATCH_SIZE`: 64

### Evaluation

```bash
python evaluator.py
```

### Baseline comparison

```bash
python baseline.py
```

## 📁 Cấu trúc thư mục

```
greenwave_backend_py/
├── src/
│   ├── config/
│   │   ├── settings.py           # Pydantic settings
│   │   └── areas.py              # Area definitions
│   ├── models/
│   │   ├── simulation.py         # Pydantic models
│   │   └── dqn_agent.py          # DQN Agent class
│   ├── services/
│   │   ├── orion_service.py      # Orion integration
│   │   ├── websocket_service.py  # WebSocket server
│   │   ├── simulation_service.py # Simulation coordinator
│   │   ├── ai_service.py         # AI control service
│   │   └── iot_service.py        # SUMO TraCI integration
│   ├── training/
│   │   ├── train_dqn.py          # Training script
│   │   ├── evaluator.py          # Evaluation script
│   │   └── baseline.py           # Baseline comparison
│   └── main.py                   # Main FastAPI app
├── sumo_files/                   # SUMO scenarios
│   ├── Nga4ThuDuc/
│   ├── NguyenThaiSon/
│   └── QuangTrung/
├── models/                       # Trained models
│   └── dqn_model.h5
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env.example
└── README.md
```

## 🔧 Configuration

### Environment Variables

| Variable           | Description            | Default                                  |
| ------------------ | ---------------------- | ---------------------------------------- |
| `PORT`             | Server port            | 3001                                     |
| `ORION_URL`        | Orion broker URL       | http://localhost:1026/ngsi-ld/v1         |
| `TLS_ID`           | Traffic light ID       | 4066470692                               |
| `AI_ENABLED`       | Enable AI control      | false                                    |
| `AI_MODEL_PATH`    | Path to DQN model      | models/dqn_model.h5                      |
| `SUMO_ENABLED`     | Enable SUMO simulation | false                                    |
| `SUMO_CONFIG_PATH` | SUMO config file       | sumo_files/Nga4ThuDuc/Nga4ThuDuc.sumocfg |
| `SUMO_USE_GUI`     | Use SUMO GUI           | false                                    |

## 🧪 Testing

```bash
# Test AI service
curl -X POST http://localhost:3001/api/ai/start

# Test SUMO service
curl -X POST http://localhost:3001/api/sumo/start

# Check status
curl http://localhost:3001/health
```

## 📊 Monitoring

### Logs

Logs được output ra console với format:

```
[2025-11-22 22:00:00] INFO - service_name - Message
```

### Health Check

```bash
curl http://localhost:3001/health
```

Response:

```json
{
  "status": "ok",
  "timestamp": "2025-11-22T22:00:00",
  "services": {
    "simulation": true,
    "websocket": 2,
    "orion": "http://localhost:1026/ngsi-ld/v1"
  }
}
```

## 🐛 Troubleshooting

### SUMO_HOME not found

```bash
# Windows
set SUMO_HOME=C:\Program Files (x86)\Eclipse\Sumo

# Linux/Mac
export SUMO_HOME=/usr/share/sumo
```

### TensorFlow not found

```bash
pip install tensorflow
```

### Port already in use

```bash
# Change port in .env
PORT=3002
```

## 📄 License

MIT

## 👥 Contributors

- GreenWave Team

## 📞 Support

For issues and questions, please open an issue on GitHub.
