// Copyright (c) 2025 Green Wave Team
// 
// This software is released under the MIT License.
// https://opensource.org/licenses/MIT

import React, { useState, useEffect } from "react";
import { useTranslation } from "react-i18next";
import { useAppDispatch, useAppSelector } from "../../../data/redux/hooks";
import { fetchSumoStatus, fetchSumoState } from "../../../data/redux/sumoSlice";
import { DashboardHeader } from "../../components/feature/dashboard/DashboardHeader";
import { SumoControlPanel } from "../../components/feature/sumo/SumoControlPanel";
import { TrafficMetrics } from "../../components/feature/sumo/TrafficMetrics";
import { TrafficLightsDisplay } from "../../components/feature/sumo/TrafficLightsDisplay";
import { AIControlPanel } from "../../components/feature/sumo/AIControlPanel";
import { SystemLogs } from "../../components/feature/sumo/SystemLogs";
import { TrafficFlowChart } from "../../components/feature/sumo/TrafficFlowChart";
import { SimulationControlPanel } from "../../components/feature/sumo/SimulationControlPanel";

export const ControlTrafficPage: React.FC = () => {
  const dispatch = useAppDispatch();
  const { status, isSimulationRunning } = useAppSelector((state) => state.sumo);
  const { t } = useTranslation(["traffic", "common"]);

  // Initialize dark mode from localStorage or system preference
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
    t("traffic:logs.initSuccess"),
    t("traffic:logs.waitingConnection"),
  ]);

  // Apply dark mode class on mount
  useEffect(() => {
    if (isDarkMode) {
      document.documentElement.classList.add("dark");
    } else {
      document.documentElement.classList.remove("dark");
    }
  }, [isDarkMode]);

  // Initialize data on component mount
  useEffect(() => {
    // Initial fetch of SUMO status
    const initializeData = async () => {
      try {
        await dispatch(fetchSumoStatus()).unwrap();
        addLog(t("traffic:logs.sumoInitSuccess"));
      } catch (error) {
        addLog(t("traffic:logs.sumoInitFailed", { error }));
      }
    };

    initializeData();

    // Poll status every 5 seconds
    const statusInterval = setInterval(() => {
      dispatch(fetchSumoStatus());
    }, 5000);

    return () => clearInterval(statusInterval);
  }, [dispatch, t]);

  // Fetch SUMO state when simulation is running
  useEffect(() => {
    if (status.connected && isSimulationRunning) {
      // Fetch state every 1 second
      const stateInterval = setInterval(() => {
        dispatch(fetchSumoState());
      }, 1000);

      return () => clearInterval(stateInterval);
    }
  }, [status.connected, isSimulationRunning, dispatch]);

  const handleThemeToggle = () => {
    const newDarkMode = !isDarkMode;
    setIsDarkMode(newDarkMode);
    localStorage.setItem("darkMode", newDarkMode.toString());
  };

  const addLog = (message: string) => {
    setSystemLogs((prev) => [...prev, message]);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800">
      <DashboardHeader
        onThemeToggle={handleThemeToggle}
        isDarkMode={isDarkMode}
      />

      <main className="p-4 max-w-[1920px] mx-auto">
        {/* Main Layout: Left Sidebar (1/4) + Right Content (3/4) */}
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6 mb-4">
          {/* Left Sidebar - Controls & Logs (1/4) */}
          <div className="lg:col-span-1 space-y-6">
            {/* SUMO Control Panel */}
            <SumoControlPanel onLog={addLog} />

            {/* Simulation Control Panel */}
            <SimulationControlPanel onLog={addLog} />
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
            {t("traffic:footer.systemName")}
          </p>
          <p className="text-xs text-gray-400 dark:text-gray-500 mt-1">
            {t("traffic:footer.poweredBy")}
          </p>
        </div>
      </main>
    </div>
  );
};
