# Hướng dẫn chạy DQN Training

## ✅ Cấu trúc hiện tại

### 1. Scenario được sử dụng: **Nga4ThuDuc**
- **Vị trí**: `sumo_files/Nga4ThuDuc/`
- **Lý do chọn**: Junction có traffic light được cấu hình đầy đủ
- **Files chính**:
  - `Nga4ThuDuc.sumocfg` - File cấu hình SUMO
  - `Nga4ThuDuc.net.xml` - Network với traffic lights
  - `Nga4ThuDuc.add.xml` - Detectors và additional files
  - `routes.rou.xml` - Routes và vehicle flows

### 2. Thông tin Traffic Light Junction
- **Junction ID**: `4066470692`
- **Type**: traffic_light
- **Incoming Edges**: 
  - `720360980`
  - `720360983#1`
  - `1106838009#1`
- **Detectors**:
  - `e2_0`: Lane area detector (queue detection)
  - `e2_2`: Lane area detector (queue detection)
- **Number of Phases**: 2

## 🚀 Cách chạy

### Bước 1: Activate virtual environment
```bash
cd /home/thaianh/OLP2025/OLP_2025/SUMO_RL
source venv/bin/activate
```

### Bước 2: Kiểm tra SUMO_HOME
```bash
echo $SUMO_HOME
# Nếu chưa set, chạy:
# export SUMO_HOME=/usr/share/sumo  # hoặc đường dẫn SUMO của bạn
```

### Bước 3: Chạy training
```bash
python train_dqn.py
```

## 📊 Output
- File `dqn_model.h5` sẽ được tạo sau khi training hoàn tất (10,000 steps)
- Progress sẽ được in ra console mỗi 500 steps
- Target model được cập nhật mỗi 100 steps

## ⚙️ Hyperparameters
Có thể điều chỉnh trong file `train_dqn.py`:
- `TOTAL_STEPS`: 10,000 (số bước huấn luyện)
- `STATE_SIZE`: 4 (2 queue detectors + 1 phase + 1 pm25)
- `MIN_GREEN_STEPS`: 100 (10 giây - thời gian xanh tối thiểu)
- `NUM_PHASES`: 2 (số pha của traffic light)
- `GAMMA`: 0.95 (discount factor)
- `EPSILON_START`: 1.0
- `EPSILON_END`: 0.01
- `EPSILON_DECAY_STEPS`: 5,000
- `LEARNING_RATE`: 0.001
- `BATCH_SIZE`: 64
- `W_TRAFFIC`: 0.6 (60% ưu tiên giảm ùn tắc)
- `W_ENV`: 0.4 (40% ưu tiên giảm ô nhiễm)

## 🐛 Troubleshooting

### Lỗi: "Please declare environment variable 'SUMO_HOME'"
```bash
export SUMO_HOME=/usr/share/sumo  # Linux
# hoặc
export SUMO_HOME=/opt/homebrew/share/sumo  # macOS
```

### Lỗi: Import không tìm thấy
Đảm bảo đã activate virtual environment:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Lỗi: SUMO connection failed
Kiểm tra xem SUMO đã được cài đặt chưa:
```bash
sumo --version
```

## 📝 Notes
- Code sử dụng `sumo` (không có GUI) để training nhanh hơn
- Nếu muốn xem visualization, đổi `'sumo'` thành `'sumo-gui'` trong `SUMO_CONFIG`
- Replay buffer có capacity 5,000 experiences
- DQN sử dụng 2 networks: main và target (Double DQN)
