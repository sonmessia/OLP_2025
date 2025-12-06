#!/bin/bash
# Copyright (c) 2025 Green Wave Team
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

# Script to run SUMO simulation on host and connect to backend API
# Usage: ./run_sumo.sh [scenario]
# Scenarios: Nga4ThuDuc (default), NguyenThaiSon, QuangTrung

SCENARIO=${1:-Nga4ThuDuc}
SUMO_FILES="./src/backend/app/sumo_rl/sumo_files"

# Export SUMO_HOME if not set
export SUMO_HOME=${SUMO_HOME:-/usr/share/sumo}

echo "🚦 Starting SUMO Simulation"
echo "📍 Scenario: $SCENARIO"
echo "🏠 SUMO_HOME: $SUMO_HOME"
echo "📁 Files: $SUMO_FILES"
echo ""

# Map scenario to config file
case $SCENARIO in
  "Nga4ThuDuc")
    CONFIG="$SUMO_FILES/Nga4ThuDuc/Nga4ThuDuc.sumocfg"
    ;;
  "NguyenThaiSon")
    CONFIG="$SUMO_FILES/NguyenThaiSon/Nga6NguyenThaiSon.sumocfg"
    ;;
  "QuangTrung")
    CONFIG="$SUMO_FILES/QuangTrung/quangtrungcar.sumocfg"
    ;;
  *)
    echo "❌ Unknown scenario: $SCENARIO"
    echo "Available: Nga4ThuDuc, NguyenThaiSon, QuangTrung"
    exit 1
    ;;
esac

# Check if config exists
if [ ! -f "$CONFIG" ]; then
  echo "❌ Config file not found: $CONFIG"
  exit 1
fi

echo "✅ Config: $CONFIG"
echo ""
echo "🎮 Starting SUMO-GUI..."
echo "📡 TraCI will be available on port 8813"
echo ""

# Start SUMO with TraCI (port 8813)
sumo-gui -c "$CONFIG" --remote-port 8813 --start --quit-on-end

echo ""
echo "✅ SUMO simulation finished"
