import React, { useState, useEffect } from "react";
import { useSelector } from "react-redux";
import { useAppDispatch, useAppSelector } from "../../../data/redux/hooks";
import { fetchSumoStatus, fetchSumoState } from "../../../data/redux/sumoSlice";
import type { RootState } from "../../../data/redux/store";
import { UserRole } from "../../../domain/models/AuthModels";
import AuthHeader from "../../components/common/AuthHeader";
import { AreaControlPanel } from "../../components/feature/area/AreaControlPanel";
import { AreaMapView } from "../../components/feature/area/AreaMapView";
import { TrafficMetrics } from "../../components/feature/sumo/TrafficMetrics";
import { TrafficLightsDisplay } from "../../components/feature/sumo/TrafficLightsDisplay";
import { AIControlPanel } from "../../components/feature/sumo/AIControlPanel";
import { SystemLogs } from "../../components/feature/sumo/SystemLogs";
import { TrafficFlowChart } from "../../components/feature/sumo/TrafficFlowChart";

// Coordinate mapping for areas
const AREA_COORDINATES: Record<string, { lat: number; lng: number }> = {
  "Ngã 4 Thủ Đức": { lat: 10.8505, lng: 106.7718 },
  "Ngã 4 Hàng Xanh": { lat: 10.7997, lng: 106.7012 },
  "Cầu Sài Gòn": { lat: 10.7938, lng: 106.7215 },
  // Default fallback
  default: { lat: 10.8231, lng: 106.6297 },
};

const AreaManagerPage: React.FC = () => {
  const dispatch = useAppDispatch();
  const { user } = useSelector((state: RootState) => state.auth);
  const { status, isSimulationRunning } = useAppSelector((state) => state.sumo);

  // Initialize dark mode
  const getInitialDarkMode = () => {
    if (typeof window !== "undefined") {
      const stored = localStorage.getItem("darkMode");
      if (stored !== null) {
        return stored === "true";
      }
      return window.matchMedia("(prefers-color-scheme: dark)").matches;
    }
    return false;
  };

  const [isDarkMode] = useState(getInitialDarkMode);
  const [systemLogs, setSystemLogs] = useState<string[]>([
    "System initialized successfully",
    "Waiting for connection...",
  ]);

  // Get coordinates for user's area
  const areaCoords =
    user?.areaName && AREA_COORDINATES[user.areaName]
      ? AREA_COORDINATES[user.areaName]
      : AREA_COORDINATES["default"];

  // Apply dark mode class
  useEffect(() => {
    if (isDarkMode) {
      document.documentElement.classList.add("dark");
    } else {
      document.documentElement.classList.remove("dark");
    }
  }, [isDarkMode]);

  // Initialize data
  useEffect(() => {
    const initializeData = async () => {
      try {
        await dispatch(fetchSumoStatus()).unwrap();
        addLog("📡 Kết nối tới máy chủ thành công");
      } catch (error) {
        addLog(`⚠️ Không thể kết nối tới máy chủ: ${error}`);
      }
    };

    initializeData();

    const statusInterval = setInterval(() => {
      dispatch(fetchSumoStatus());
    }, 5000);

    return () => clearInterval(statusInterval);
  }, [dispatch]);

  // Fetch SUMO state when simulation is running
  useEffect(() => {
    if (status.connected && isSimulationRunning) {
      const stateInterval = setInterval(() => {
        dispatch(fetchSumoState());
      }, 1000);

      return () => clearInterval(stateInterval);
    }
  }, [status.connected, isSimulationRunning, dispatch]);

  const addLog = (message: string) => {
    setSystemLogs((prev) => [...prev, message]);
  };

  if (!user || user.role !== UserRole.AREA_MANAGER) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900">
        <div className="text-center">
          <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">
            Truy cập bị từ chối
          </h1>
          <p className="text-lg text-gray-600 dark:text-gray-400">
            Bạn không có quyền truy cập trang này
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800">
      <AuthHeader
        title={`Quản lý khu vực: ${user.areaName || "Chưa xác định"}`}
      />

      <main className="p-4 max-w-[1920px] mx-auto">
        {/* Main Layout: Left Sidebar (1/4) + Right Content (3/4) */}
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6 mb-4">
          {/* Left Sidebar - Map & Controls (1/4) */}
          <div className="lg:col-span-1 space-y-6">
            {/* Map View - Always show first */}
            <div className="glass-card rounded-xl p-1 shadow-xl h-[300px] overflow-hidden relative">
              <AreaMapView
                latitude={areaCoords.lat}
                longitude={areaCoords.lng}
                areaName={user.areaName || "Khu vực của bạn"}
                isDarkMode={isDarkMode}
              />
            </div>

            {/* Area Control Panel */}
            <AreaControlPanel
              areaName={user.areaName || "Khu vực"}
              onLog={addLog}
            />
          </div>

          {/* Right Content Area (3/4) */}
          <div className="lg:col-span-3 space-y-6">
            {/* Top Row: Traffic Metrics */}
            <TrafficMetrics />

            {/* Middle Row: Traffic Lights & AI Control */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              {/* Traffic Lights Display */}
              <div className="lg:col-span-2">
                <TrafficLightsDisplay />
              </div>

              {/* AI Control Panel */}
              <div className="lg:col-span-1">
                <AIControlPanel onLog={addLog} />
              </div>
            </div>

            {/* Bottom Row: Traffic Flow Chart */}
            <TrafficFlowChart />
          </div>
        </div>

        {/* System Logs */}
        <div className="mb-4">
          <SystemLogs logs={systemLogs} maxLogs={20} />
        </div>

        {/* Footer Info */}
        <div className="mt-6 text-center">
          <p className="text-sm text-gray-500 dark:text-gray-400">
            Hệ thống quản lý giao thông thông minh - Khu vực {user.areaName}
          </p>
        </div>
      </main>
    </div>
  );
};

export default AreaManagerPage;
