#!/bin/bash
# Setup script for SUMO RL Integration

set -e

echo "🚀 Setting up SUMO RL integration in backend..."
echo ""

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
BACKEND_DIR="$(dirname $SCRIPT_DIR)"
PROJECT_ROOT="$(dirname $(dirname $BACKEND_DIR))"
SUMO_RL_DIR="$PROJECT_ROOT/SUMO_RL"

echo "📂 Directories:"
echo "  Backend:  $BACKEND_DIR"
echo "  SUMO_RL:  $SUMO_RL_DIR"
echo ""

# 1. Copy DQN model
if [ -f "$SUMO_RL_DIR/dqn_model.keras" ]; then
    echo "✅ Found trained model: dqn_model.keras"
    cp "$SUMO_RL_DIR/dqn_model.keras" "$BACKEND_DIR/dqn_model.keras"
    echo "   Copied to: $BACKEND_DIR/dqn_model.keras"
    
    # Get file size
    MODEL_SIZE=$(du -h "$BACKEND_DIR/dqn_model.keras" | cut -f1)
    echo "   Size: $MODEL_SIZE"
else
    echo "⚠️  Warning: dqn_model.keras not found in SUMO_RL/"
    echo "   Model will run in RANDOM mode"
fi
echo ""

# 2. Create .env if not exists
if [ ! -f "$BACKEND_DIR/.env" ]; then
    echo "📝 Creating .env file..."
    cp "$BACKEND_DIR/.env.example" "$BACKEND_DIR/.env"
    echo "   Created: $BACKEND_DIR/.env"
    echo "   Please edit this file with your configuration"
else
    echo "✅ .env file already exists"
fi
echo ""

# 3. Install dependencies
echo "📦 Installing Python dependencies..."
if [ -f "$BACKEND_DIR/requirements.txt" ]; then
    pip install -r "$BACKEND_DIR/requirements.txt"
    echo "   ✅ Dependencies installed"
else
    echo "   ⚠️  requirements.txt not found"
fi
echo ""

# 4. Check TensorFlow
echo "🔍 Checking TensorFlow installation..."
python3 -c "import tensorflow as tf; print(f'   ✅ TensorFlow {tf.__version__} installed')" 2>/dev/null || \
    echo "   ⚠️  TensorFlow not available - will run in RANDOM mode"
echo ""

# 5. Verify structure
echo "📁 Verifying structure..."
if [ -f "$BACKEND_DIR/app/services/sumo_rl_service.py" ]; then
    echo "   ✅ sumo_rl_service.py"
else
    echo "   ❌ sumo_rl_service.py not found"
fi

if [ -f "$BACKEND_DIR/app/api/routers/traffic_light_router.py" ]; then
    echo "   ✅ traffic_light_router.py"
else
    echo "   ❌ traffic_light_router.py not found"
fi
echo ""

# 6. Print next steps
echo "✨ Setup complete!"
echo ""
echo "🏃 Next steps:"
echo ""
echo "1. Edit configuration:"
echo "   nano $BACKEND_DIR/.env"
echo ""
echo "2. Run backend:"
echo "   cd $BACKEND_DIR"
echo "   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
echo ""
echo "3. Test endpoints:"
echo "   curl http://localhost:8000/sumo-rl/status"
echo "   curl http://localhost:8000/sumo-rl/model-info"
echo ""
echo "4. Read integration guide:"
echo "   cat $BACKEND_DIR/SUMO_RL_INTEGRATION.md"
echo ""
