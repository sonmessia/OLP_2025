import React, { useState, useEffect, useCallback } from "react";
import { TrafficMap } from "../components/feature/TrafficMap";
import { AreaSelector } from "../components/feature/AreaSelector";
import { TrafficStats } from "../components/feature/TrafficStats";
import { TrafficControl } from "../components/feature/TrafficControl";
import { useWebSocket } from "../hooks/useWebSocket";
import { Area, SimulationState } from "../../domain/models/simulation.types";

const WS_URL = import.meta.env.VITE_WS_URL || "ws://localhost:8765";
const API_URL = import.meta.env.VITE_API_URL || "http://localhost:3001";

// Predefined areas (should match backend configuration)
const AREAS: Area[] = [
  {
    id: "nga_tu_thu_duc",
    name: "Ngã Tư Thủ Đức",
    bounds: [
      [10.848, 106.77],
      [10.855, 106.778],
    ],
    center: [10.8515, 106.774],
    tlsId: "4066470692",
  },
  {
    id: "hang_xanh",
    name: "Ngã Tư Hàng Xanh",
    bounds: [
      [10.798, 106.698],
      [10.805, 106.706],
    ],
    center: [10.8015, 106.702],
    tlsId: "hang_xanh_tls",
  },
];

export const DigitalTwinPage: React.FC = () => {
  const [selectedArea, setSelectedArea] = useState<string | null>(
    "nga_tu_thu_duc"
  );
  const [simulationState, setSimulationState] =
    useState<SimulationState | null>(null);

  const currentArea = AREAS.find((a) => a.id === selectedArea) || AREAS[0];

  // WebSocket connection
  const { isConnected, lastMessage, sendCommand, subscribe } = useWebSocket({
    url: WS_URL,
    onMessage: (data: SimulationState) => {
      setSimulationState(data);
    },
    onConnect: () => {
      console.log("[DigitalTwin] Connected to WebSocket");
      if (selectedArea) {
        subscribe(selectedArea);
      }
    },
    onDisconnect: () => {
      console.log("[DigitalTwin] Disconnected from WebSocket");
    },
    autoReconnect: true,
  });

  // Handle area selection
  const handleSelectArea = useCallback(
    (areaId: string) => {
      setSelectedArea(areaId);
      subscribe(areaId);
    },
    [subscribe]
  );

  // Handle phase change
  const handleSetPhase = useCallback(
    async (phase: number) => {
      try {
        // Send command via WebSocket
        sendCommand({ type: "setPhase", phase });

        // Also send via HTTP API as backup
        await fetch(`${API_URL}/api/command/phase`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ phase }),
        });

        console.log(`[DigitalTwin] Set phase to ${phase}`);
      } catch (error) {
        console.error("[DigitalTwin] Error setting phase:", error);
      }
    },
    [sendCommand]
  );

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800">
      {/* Header */}
      <header className="bg-white dark:bg-gray-800 shadow-md">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
                🚦 GreenWave Digital Twin
              </h1>
              <p className="mt-1 text-sm text-gray-600 dark:text-gray-400">
                Hệ thống giám sát và điều khiển giao thông thông minh
              </p>
            </div>
            <div className="flex items-center gap-3">
              <div
                className={`px-4 py-2 rounded-full text-sm font-medium ${
                  isConnected
                    ? "bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400"
                    : "bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400"
                }`}
              >
                {isConnected ? "● Đang kết nối" : "○ Mất kết nối"}
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="space-y-6">
          {/* Area Selector */}
          <AreaSelector
            areas={AREAS}
            selectedArea={selectedArea}
            onSelectArea={handleSelectArea}
          />

          {/* Map and Stats Grid */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Map - Takes 2 columns */}
            <div className="lg:col-span-2">
              <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-4">
                <h2 className="text-lg font-semibold mb-4 text-gray-800 dark:text-gray-100">
                  🗺️ Bản đồ Giao thông - {currentArea.name}
                </h2>
                <TrafficMap
                  center={currentArea.center}
                  bounds={currentArea.bounds}
                  vehicles={simulationState?.vehicles || []}
                  trafficLights={simulationState?.trafficLights || []}
                  lockView={true}
                />
              </div>
            </div>

            {/* Stats - Takes 1 column */}
            <div className="space-y-6">
              <TrafficStats
                trafficFlow={simulationState?.trafficFlow || null}
                airQuality={simulationState?.airQuality || null}
                reward={simulationState?.reward}
                isConnected={isConnected}
              />
            </div>
          </div>

          {/* Control Panel */}
          <TrafficControl
            onSetPhase={handleSetPhase}
            currentPhase={simulationState?.trafficFlow?.phase || 0}
            disabled={!isConnected}
          />

          {/* Debug Info (Development only) */}
          {import.meta.env.DEV && (
            <div className="bg-gray-800 text-green-400 rounded-lg p-4 font-mono text-xs">
              <div className="font-bold mb-2">🔧 Debug Info:</div>
              <pre className="overflow-auto max-h-40">
                {JSON.stringify(simulationState, null, 2)}
              </pre>
            </div>
          )}
        </div>
      </main>

      {/* Footer */}
      <footer className="mt-12 bg-white dark:bg-gray-800 shadow-md">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <p className="text-center text-sm text-gray-600 dark:text-gray-400">
            © 2025 GreenWave Traffic Control System | OLP 2025
          </p>
        </div>
      </footer>
    </div>
  );
};
