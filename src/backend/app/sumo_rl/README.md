<!--
 Copyright (c) 2025 Green Wave Team
 
 This software is released under the MIT License.
 https://opensource.org/licenses/MIT
-->

# SUMO RL - Smart Traffic Light Control

**Deep Reinforcement Learning for Adaptive Traffic Signal Control**

## 📁 Module Structure

```
app/sumo_rl/
├── __init__.py              # Main module exports
├── config.py                # Configuration settings
├── agents/                  # Agent components
│   ├── __init__.py
│   ├── ai_agent.py         # AI GreenWave Agent (DQN decision-making)
│   └── iot_agent.py        # IoT Agent (SUMO control via TraCI)
├── models/                  # Neural network models
│   ├── __init__.py
│   ├── dqn_model.py        # DQN model architecture
│   └── dqn_model.keras     # Trained model (334 KB, 25,538 params)
├── training/                # Training scripts
│   ├── __init__.py
│   └── train_dqn_production.py  # Production training script
├── evaluation/              # Evaluation scripts
│   ├── __init__.py
│   ├── evaluate_dqn.py     # Comprehensive evaluation
│   └── baseline.py         # Baseline comparison
├── environment/             # SUMO environment wrappers
│   └── __init__.py
└── sumo_files/             # SUMO scenarios
    ├── Nga4ThuDuc/         # Main scenario (Nga Tu Thu Duc)
    ├── NguyenThaiSon/
    └── QuangTrung/
```

## 🎯 Quick Start

### 1. Run Backend with SUMO RL

```bash
cd /path/to/src/backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Test Endpoints

```bash
# Check system status
curl http://localhost:8000/sumo-rl/status

# Get model info
curl http://localhost:8000/sumo-rl/model-info
```

### 3. Training (Optional)

```bash
cd /path/to/src/backend
python3 -m app.sumo_rl.training.train_dqn_production
```

### 4. Evaluation

```bash
cd /path/to/src/backend
python3 -m app.sumo_rl.evaluation.evaluate_dqn
```

## 🧠 Model Architecture

**DQN (Deep Q-Network) - 128-128-64 Architecture**

```
Input (4):        [queue_1, queue_2, current_phase, pm25]
Dense 128:        ReLU + Dropout(0.2)
Dense 128:        ReLU + Dropout(0.2)
Dense 64:         ReLU
Output (2):       [Q(hold), Q(switch)]
```

**Model Stats:**
- Parameters: 25,538
- Size: 334 KB
- Training: 10,000 steps (~34 mins)
- Performance: 13% better than baseline

## 📊 Performance Results

**DQN vs Baseline (Fixed-time) Comparison:**

| Metric | DQN | Baseline | Improvement |
|--------|-----|----------|-------------|
| Total Score | 1383.03 | 1590.90 | **-13.07%** ⬇️ |
| Waiting Time | 8659s | 9937s | **-13%** ⬇️ |
| PM2.5 | 10.17mg | 21.43mg | **-53%** ⬇️ |
| CO2 | 35.34g | 67.82g | **-48%** ⬇️ |
| Fuel | 13.97ml | 26.82ml | **-48%** ⬇️ |
| Avg Speed | 4.59 m/s | 4.34 m/s | **+6%** ⬆️ |

## 🔧 Configuration

Configuration is managed via `config.py` and environment variables:

```python
# Environment variables (in .env file)
SUMO_RL_ORION_URL=http://localhost:1026/ngsi-ld/v1
SUMO_RL_TLS_ID=4066470692
SUMO_RL_NUM_PHASES=2
SUMO_RL_MODEL_PATH=app/sumo_rl/models/dqn_model.keras
```

## 🚀 API Endpoints

### AI Agent (Decision Making)

- **POST** `/sumo-rl/ai/notify` - Receive traffic data from Orion
- **POST** `/sumo-rl/ai/cmd` - Legacy command endpoint
- **GET** `/sumo-rl/status` - System status
- **GET** `/sumo-rl/model-info` - Model information

### IoT Agent (SUMO Control)

- **POST** `/sumo-rl/iot/notify` - Receive commands from Orion
- **POST** `/sumo-rl/iot/cmd` - Legacy command endpoint

### Proxy (Dashboard Support)

- **GET** `/sumo-rl/proxy/orion/{path}` - Proxy GET to Orion
- **PATCH** `/sumo-rl/proxy/orion/{path}` - Proxy PATCH to Orion

## 🔄 Architecture Flow

```
┌─────────────┐
│ SUMO Sim    │ ──→ Publish traffic data
└─────────────┘
       ↓
┌─────────────┐
│ Orion-LD    │ ──→ Notify AI Agent
└─────────────┘
       ↓
┌─────────────┐
│ AI Agent    │ ──→ DQN predicts action
│ (Backend)   │
└─────────────┘
       ↓
┌─────────────┐
│ Orion-LD    │ ──→ Notify IoT Agent
└─────────────┘
       ↓
┌─────────────┐
│ IoT Agent   │ ──→ Apply to SUMO
│ (TraCI)     │
└─────────────┘
```

## 📖 Training Details

**Hyperparameters (Optimized for Vietnam Traffic):**

```python
GAMMA = 0.95                    # Discount factor
EPSILON_START = 1.0             # Exploration start
EPSILON_END = 0.01              # Exploration end
EPSILON_DECAY_STEPS = 7000      # Decay period
LEARNING_RATE = 0.0005          # Adam optimizer
REPLAY_BUFFER_SIZE = 10000      # Experience replay
BATCH_SIZE = 64                 # Training batch
TARGET_UPDATE_FREQ = 200        # Target network update
```

**Reward Function:**

```python
reward = -0.6 * queue_length - 0.4 * pm25_emissions
```

- 60% weight on traffic flow (queue reduction)
- 40% weight on environmental impact (PM2.5 reduction)

## 🧪 Testing

**Test AI Notification:**

```bash
curl -X POST http://localhost:8000/sumo-rl/ai/notify \
  -H "Content-Type: application/json" \
  -d '{
    "data": [
      {
        "id": "urn:ngsi-ld:TrafficFlowObserved:4066470692",
        "type": "TrafficFlowObserved",
        "queues": {"type": "Property", "value": [3, 5]},
        "phase": {"type": "Property", "value": 0}
      },
      {
        "id": "urn:ngsi-ld:AirQualityObserved:4066470692",
        "type": "AirQualityObserved",
        "pm25": {"type": "Property", "value": 25.5}
      }
    ]
  }'
```

**Expected Response:**

```json
{
  "status": "ok",
  "action": "switch",
  "current_phase": 0,
  "next_phase": 1,
  "state": [3, 5, 0, 25.5]
}
```

## 📚 Documentation

See `docs/sumo_rl/` for detailed documentation:

- **DEMO_GUIDE.md** - Competition demo guide
- **FINAL_VERDICT.md** - Complete evaluation analysis
- **RESULTS_SUMMARY.md** - Performance summary
- **evaluation_results_*.png** - Visualization charts

## 🛠️ Development

**Add new scenario:**

1. Place SUMO files in `sumo_files/NewScenario/`
2. Update `config.py` with new IDs
3. Retrain model or test with existing model

**Modify DQN architecture:**

1. Edit `models/dqn_model.py` → `build_model()`
2. Retrain with `training/train_dqn_production.py`

**Custom reward function:**

1. Edit `training/train_dqn_production.py` → `get_reward()`
2. Adjust weights `W_TRAFFIC` and `W_ENV`

## 🤝 Integration

This module integrates with:

- **FastAPI Backend** - Main application server
- **Orion-LD** - Context broker for NGSI-LD entities
- **SUMO** - Traffic simulation engine
- **TensorFlow/Keras** - Deep learning framework

## 📄 License

Part of OLP 2025 Project - Green Smart City

## 👥 Authors

OLP 2025 Team

---

**Status:** ✅ Production Ready  
**Last Updated:** November 29, 2025  
**Version:** 1.0.0
