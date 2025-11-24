import React, { useState, useCallback, useMemo } from "react";
import { TrafficMap } from "../components/feature/TrafficMap";
import { AreaSelector } from "../components/feature/AreaSelector";
import { TrafficControl } from "../components/feature/TrafficControl";
import { StatCard } from "../components/feature/StatCard";
import {
  TrafficFlowChart,
  VehicleDensityChart,
  TrafficPhaseChart,
} from "../components/feature/charts";
import { useWebSocket } from "../hooks/useWebSocket";
import type {
  Area,
  SimulationState,
} from "../../domain/models/simulation.types";

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

  // Historical data for charts
  const [historicalData, setHistoricalData] = useState<{
    timestamps: string[];
    vehicleCount: number[];
    avgSpeed: number[];
  }>({
    timestamps: [],
    vehicleCount: [],
    avgSpeed: [],
  });

  const currentArea = AREAS.find((a) => a.id === selectedArea) || AREAS[0];

  // WebSocket connection
  const { isConnected, sendCommand, subscribe } = useWebSocket({
    url: WS_URL,
    onMessage: (data: SimulationState) => {
      setSimulationState(data);

      // Update historical data for charts
      setHistoricalData((prev) => {
        const now = new Date().toLocaleTimeString("vi-VN", {
          hour: "2-digit",
          minute: "2-digit",
        });
        const maxDataPoints = 20;

        return {
          timestamps: [...prev.timestamps, now].slice(-maxDataPoints),
          vehicleCount: [
            ...prev.vehicleCount,
            data.vehicles?.length || 0,
          ].slice(-maxDataPoints),
          avgSpeed: [
            ...prev.avgSpeed,
            (data.trafficFlow as any)?.avgSpeed || 0,
          ].slice(-maxDataPoints),
        };
      });
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
      // Reset historical data when changing area
      setHistoricalData({
        timestamps: [],
        vehicleCount: [],
        avgSpeed: [],
      });
    },
    [subscribe]
  );

  // Handle phase change
  const handleSetPhase = useCallback(
    async (phase: number) => {
      try {
        // Send command via WebSocket
        sendCommand({ phase } as any);

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

  // Calculate statistics
  const stats = useMemo(() => {
    if (!simulationState) {
      return {
        totalVehicles: 0,
        avgSpeed: 0,
        avgWaitingTime: 0,
        co2Emission: 0,
      };
    }

    const totalVehicles = simulationState.vehicles?.length || 0;
    const avgSpeed = (simulationState.trafficFlow as any)?.avgSpeed || 0;
    const avgWaitingTime =
      (simulationState.trafficFlow as any)?.avgWaitingTime || 0;
    const co2Emission = (simulationState.airQuality as any)?.co2 || 0;

    return {
      totalVehicles,
      avgSpeed,
      avgWaitingTime,
      co2Emission,
    };
  }, [simulationState]);

  // Mock data for density chart
  const densityData = useMemo(
    () => ({
      lanes: ["Làn 1", "Làn 2", "Làn 3", "Làn 4"],
      density: [
        Math.floor(Math.random() * 100),
        Math.floor(Math.random() * 100),
        Math.floor(Math.random() * 100),
        Math.floor(Math.random() * 100),
      ],
    }),
    []
  );

  // Mock data for phase chart
  const phaseData = useMemo(
    () => ({
      phases: ["Pha 1", "Pha 2", "Pha 3", "Pha 4"],
      durations: [30, 25, 35, 20],
    }),
    []
  );

  return (
    <div
      className="min-h-screen"
      style={{ backgroundColor: "var(--color-surface)" }}
    >
      {/* Header */}
      <header
        style={{
          backgroundColor: "var(--color-background)",
          borderBottom: "1px solid var(--color-border)",
          boxShadow: "var(--shadow-sm)",
        }}
      >
        <div className="max-w-[1600px] mx-auto px-6 py-5">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-gradient">
                Thống Kê Giao Thông
              </h1>
              <p
                className="mt-1 text-sm"
                style={{ color: "var(--color-text-secondary)" }}
              >
                Hệ thống giám sát và quản lý giao thông thông minh
              </p>
            </div>
            <div className="flex items-center gap-3">
              <div
                className={`badge ${
                  isConnected ? "badge-success" : "badge-error"
                }`}
              >
                <span className={isConnected ? "animate-pulse" : ""}>●</span>
                {isConnected ? "Đang kết nối" : "Mất kết nối"}
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-[1600px] mx-auto px-6 py-6">
        <div className="space-y-6">
          {/* Area Selector */}
          <AreaSelector
            areas={AREAS}
            selectedArea={selectedArea}
            onSelectArea={handleSelectArea}
          />

          {/* Statistics Cards */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <StatCard
              label="Tổng số xe"
              value={stats.totalVehicles}
              unit="xe"
              status={stats.totalVehicles > 50 ? "warning" : "success"}
              trend={{
                value: 12,
                direction: "up",
              }}
            />
            <StatCard
              label="Tốc độ trung bình"
              value={stats.avgSpeed.toFixed(1)}
              unit="km/h"
              status={stats.avgSpeed < 20 ? "error" : "success"}
              trend={{
                value: 5,
                direction: "down",
              }}
            />
            <StatCard
              label="Thời gian chờ TB"
              value={stats.avgWaitingTime.toFixed(1)}
              unit="giây"
              status={stats.avgWaitingTime > 30 ? "warning" : "success"}
              trend={{
                value: 8,
                direction: "up",
              }}
            />
            <StatCard
              label="Lượng CO₂"
              value={stats.co2Emission.toFixed(2)}
              unit="mg/m³"
              status={stats.co2Emission > 100 ? "error" : "success"}
              trend={{
                value: 3,
                direction: "down",
              }}
            />
          </div>

          {/* Main Grid */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Left Column - Map */}
            <div className="lg:col-span-2 space-y-6">
              {/* Map Card */}
              <div className="card">
                <div className="card-header">
                  <h2
                    className="text-base font-semibold"
                    style={{ color: "var(--color-text-primary)" }}
                  >
                    Bản đồ Giao thông - {currentArea.name}
                  </h2>
                </div>
                <div className="card-body">
                  <TrafficMap
                    center={currentArea.center}
                    bounds={currentArea.bounds}
                    vehicles={simulationState?.vehicles || []}
                    trafficLights={simulationState?.trafficLights || []}
                    lockView={true}
                  />
                </div>
              </div>

              {/* Traffic Flow Chart */}
              <div className="card">
                <div className="card-header">
                  <h2
                    className="text-base font-semibold"
                    style={{ color: "var(--color-text-primary)" }}
                  >
                    Lưu lượng Giao thông Theo Thời gian
                  </h2>
                </div>
                <div className="card-body">
                  <TrafficFlowChart data={historicalData} />
                </div>
              </div>
            </div>

            {/* Right Column - Charts & Controls */}
            <div className="space-y-6">
              {/* Vehicle Density Chart */}
              <div className="card">
                <div className="card-header">
                  <h2
                    className="text-base font-semibold"
                    style={{ color: "var(--color-text-primary)" }}
                  >
                    Mật độ Xe Theo Làn
                  </h2>
                </div>
                <div className="card-body">
                  <VehicleDensityChart data={densityData} />
                </div>
              </div>

              {/* Traffic Phase Chart */}
              <div className="card">
                <div className="card-header">
                  <h2
                    className="text-base font-semibold"
                    style={{ color: "var(--color-text-primary)" }}
                  >
                    Phân bổ Thời gian Pha
                  </h2>
                </div>
                <div className="card-body">
                  <TrafficPhaseChart
                    data={phaseData}
                    currentPhase={
                      (simulationState?.trafficFlow as any)?.phase || 0
                    }
                  />
                </div>
              </div>

              {/* Control Panel */}
              <div className="card">
                <div className="card-header">
                  <h2
                    className="text-base font-semibold"
                    style={{ color: "var(--color-text-primary)" }}
                  >
                    Điều khiển Đèn tín hiệu
                  </h2>
                </div>
                <div className="card-body">
                  <TrafficControl
                    onSetPhase={handleSetPhase}
                    currentPhase={
                      (simulationState?.trafficFlow as any)?.phase || 0
                    }
                    disabled={!isConnected}
                  />
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer
        style={{
          backgroundColor: "var(--color-background)",
          borderTop: "1px solid var(--color-border)",
          marginTop: "3rem",
        }}
      >
        <div className="max-w-[1600px] mx-auto px-6 py-4">
          <p
            className="text-center text-sm"
            style={{ color: "var(--color-text-secondary)" }}
          >
            © 2025 Hệ thống Quản lý Giao thông Thông minh | OLP 2025
          </p>
        </div>
      </footer>
    </div>
  );
};
