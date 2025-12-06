// Copyright (c) 2025 Green Wave Team
// 
// This software is released under the MIT License.
// https://opensource.org/licenses/MIT

import React, { useState, useEffect } from "react";
import { useTranslation } from "react-i18next";
import { useSelector } from "react-redux";
import { useAppDispatch, useAppSelector } from "../../../data/redux/hooks";
import {
  startSimulation,
  fetchSumoStatus,
  fetchSumoState,
} from "../../../data/redux/sumoSlice";
import { SumoModelFactory } from "../../../domain/models/SumoModels";
import type { RootState } from "../../../data/redux/store";
import { UserRole } from "../../../domain/models/AuthModels";
import { DashboardHeader } from "../../components/feature/dashboard/DashboardHeader";
import { AreaControlPanel } from "../../components/feature/area/AreaControlPanel";
import { AreaMapView } from "../../components/feature/area/AreaMapView";
import { TrafficMetrics } from "../../components/feature/sumo/TrafficMetrics";
import { TrafficLightsDisplay } from "../../components/feature/sumo/TrafficLightsDisplay";
import { AIControlPanel } from "../../components/feature/sumo/AIControlPanel";
import { SystemLogs } from "../../components/feature/sumo/SystemLogs";
import { TrafficFlowChart } from "../../components/feature/sumo/TrafficFlowChart";

import { TRAFFIC_LOCATIONS } from "../../../utils/trafficLocations";

// Coordinate mapping for areas derived from TRAFFIC_LOCATIONS
const AREA_COORDINATES: Record<string, { lat: number; lng: number }> =
  TRAFFIC_LOCATIONS.reduce(
    (acc, loc) => {
      acc[loc.id] = { lat: loc.coordinates[0], lng: loc.coordinates[1] };
      return acc;
    },
    {
      // Default fallback
      default: { lat: 10.8231, lng: 106.6297 },
    } as Record<string, { lat: number; lng: number }>
  );

const AreaManagerPage: React.FC = () => {
  const dispatch = useAppDispatch();
  const { user } = useSelector((state: RootState) => state.auth);
  const { status, isSimulationRunning } = useAppSelector((state) => state.sumo);
  const { t } = useTranslation(["areaControl", "common", "user"]);

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

  const [isDarkMode, setIsDarkMode] = useState(getInitialDarkMode);
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

  const handleThemeToggle = () => {
    const newDarkMode = !isDarkMode;
    setIsDarkMode(newDarkMode);
    localStorage.setItem("darkMode", newDarkMode.toString());
  };

  const addLog = (message: string) => {
    setSystemLogs((prev) => [...prev, message]);
  };

  // Initialize data
  useEffect(() => {
    const initializeData = async () => {
      try {
        await dispatch(fetchSumoStatus()).unwrap();
        addLog(t("areaControl:messages.logs.connectedSuccess"));
      } catch (error) {
        addLog(t("areaControl:messages.logs.connectError", { error }));
      }
    };

    initializeData();

    const statusInterval = setInterval(() => {
      dispatch(fetchSumoStatus());
    }, 5000);

    return () => clearInterval(statusInterval);
  }, [dispatch, t]);

  // Fetch SUMO state when simulation is running
  useEffect(() => {
    // Check if the running scenario matches the user's area
    const userScenarioId = TRAFFIC_LOCATIONS.find(
      (loc) => loc.id === user?.areaName
    )?.id;

    if (status.connected && isSimulationRunning) {
      if (
        userScenarioId &&
        status.scenario &&
        status.scenario !== userScenarioId
      ) {
        // Mismatch detected: Stop the wrong simulation
        console.warn(
          `Mismatch: Running scenario ${status.scenario} but user area is ${userScenarioId}. Stopping...`
        );
        addLog(
          t("areaControl:messages.logs.scenarioMismatch", {
            scenario: status.scenario,
          })
        );
        // Do NOT fetch state
        return;
      }

      // Only fetch state if scenario matches
      const stateInterval = setInterval(() => {
        dispatch(fetchSumoState());
      }, 1000);

      return () => clearInterval(stateInterval);
    } else if (status.connected && !isSimulationRunning && user?.areaName) {
      // Auto-start simulation for the user's area if connected but not running
      if (userScenarioId) {
        // Debounce auto-start to avoid rapid firing on mount
        const timer = setTimeout(() => {
          addLog(
            t("areaControl:messages.logs.autoStart", { area: user.areaName })
          );
          const config = SumoModelFactory.createConfiguration(
            userScenarioId,
            false, // No GUI by default for auto-start
            8813
          );
          dispatch(startSimulation(config));
        }, 1000);
        return () => clearTimeout(timer);
      }
    }
  }, [
    status.connected,
    isSimulationRunning,
    dispatch,
    status.scenario,
    user?.areaName,
    t,
  ]);

  if (!user || user.role !== UserRole.AREA_MANAGER) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900">
        <div className="text-center">
          <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">
            {t("areaControl:messages.accessDenied")}
          </h1>
          <p className="text-lg text-gray-600 dark:text-gray-400">
            {t("areaControl:messages.noPermission")}
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800">
      <DashboardHeader
        onThemeToggle={handleThemeToggle}
        isDarkMode={isDarkMode}
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
                areaName={user.areaName || t("areaControl:messages.yourArea")}
                isDarkMode={isDarkMode}
              />
            </div>

            <AreaControlPanel
              areaName={user.areaName || t("user:area" as any)}
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
            {t("areaControl:messages.footer", { area: user.areaName })}
          </p>
        </div>
      </main>
    </div>
  );
};

export default AreaManagerPage;
