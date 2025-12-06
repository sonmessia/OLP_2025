#!/bin/bash
# Copyright (c) 2025 Green Wave Team
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

# Auto-start SUMO script for any scenario
# Usage: ./start_sumo.sh <scenario_name>

SCENARIO=$1
BASE_DIR="/home/thaianh/OLP2025/OLP_2025/src/backend/app/sumo_rl/sumo_files"

# Kill existing SUMO and wait until port is free
echo "🔄 Checking for existing SUMO on port 8813..."
if lsof -ti :8813 > /dev/null 2>&1; then
    echo "⚠️  Found existing SUMO, killing it..."
    lsof -ti :8813 | xargs kill -9 2>/dev/null
    
    # Wait up to 5 seconds for port to be freed
    for i in {1..10}; do
        if ! lsof -ti :8813 > /dev/null 2>&1; then
            echo "✅ Port 8813 is now free"
            break
        fi
        sleep 0.5
    done
fi
sleep 1

# Map scenario to config file
case $SCENARIO in
    "Nga4ThuDuc")
        CONFIG="$BASE_DIR/Nga4ThuDuc/Nga4ThuDuc.sumocfg"
        ;;
    "NguyenThaiSon")
        CONFIG="$BASE_DIR/NguyenThaiSon/Nga6NguyenThaiSon.sumocfg"
        ;;
    "QuangTrung")
        CONFIG="$BASE_DIR/QuangTrung/quangtrungcar.sumocfg"
        ;;
    *)
        echo "Unknown scenario: $SCENARIO"
        exit 1
        ;;
esac

# Start SUMO with GUI (no auto-quit for demo purposes)
cd "$(dirname "$CONFIG")"

# Check if viewsettings.xml exists for auto-zoom
VIEW_SETTINGS=""
if [ -f "viewsettings.xml" ]; then
    VIEW_SETTINGS="--gui-settings-file viewsettings.xml"
fi

nohup sumo-gui -c "$(basename "$CONFIG")" \
    --remote-port 8813 \
    --step-length 1.0 \
    --start \
    $VIEW_SETTINGS \
    > /tmp/sumo_$SCENARIO.log 2>&1 &

# Wait and verify
sleep 3
if lsof -i :8813 > /dev/null 2>&1; then
    echo "✅ SUMO started successfully for $SCENARIO"
    exit 0
else
    echo "❌ Failed to start SUMO"
    cat /tmp/sumo_$SCENARIO.log
    exit 1
fi
