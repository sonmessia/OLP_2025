import React, { useState, useEffect } from "react";
import { DashboardHeader } from "../components/feature/dashboard/DashboardHeader";
import { KPICard } from "../components/feature/dashboard/KPICard";
import { MonitoringChart } from "../components/feature/dashboard/MonitoringChart";
import { RewardChart } from "../components/feature/dashboard/RewardChart";
import { PollutionMap } from "../components/feature/dashboard/PollutionMap";
import { AlertPanel } from "../components/feature/dashboard/AlertPanel";
import type {
  DashboardStateModel,
  KPICardModel,
  MonitoringDataPoint,
  RewardDataPoint,
  PollutionHotspot,
  AlertLog,
  InterventionAction,
} from "../../domain/models/DashboardModel";

// Mock data generator (will be replaced with real API calls)
const generateMockData = (): DashboardStateModel => {
  const now = new Date();
  const timePoints = Array.from({ length: 20 }, (_, i) => {
    const time = new Date(now.getTime() - (19 - i) * 5 * 60 * 1000);
    return time.toISOString();
  });

  const kpis: KPICardModel[] = [
    {
      id: "1",
      title: "Thời gian chờ TB",
      value: 45,
      unit: "giây",
      trend: "down",
      trendValue: -12,
      icon: "Clock",
      color: "blue",
    },
    {
      id: "2",
      title: "PM2.5 TB",
      value: 35,
      unit: "μg/m³",
      trend: "down",
      trendValue: -8,
      icon: "Leaf",
      color: "green",
    },
    {
      id: "3",
      title: "Số xe qua nút",
      value: 1248,
      unit: "xe/h",
      trend: "up",
      trendValue: 5,
      icon: "Car",
      color: "yellow",
    },
    {
      id: "4",
      title: "Điểm AI",
      value: 87,
      unit: "%",
      trend: "up",
      trendValue: 3,
      icon: "Brain",
      color: "blue",
    },
  ];

  const monitoringData: MonitoringDataPoint[] = timePoints.map(
    (time, index) => ({
      timestamp: time,
      avgWaitingTime: 40 + Math.sin(index / 3) * 15 + Math.random() * 5,
      pm25Level: 30 + Math.cos(index / 4) * 20 + Math.random() * 8,
    })
  );

  const rewardData: RewardDataPoint[] = timePoints.map((time) => ({
    timestamp: time,
    trafficReward: 40 + Math.random() * 20,
    environmentReward: 30 + Math.random() * 25,
  }));

  const pollutionHotspots: PollutionHotspot[] = [
    {
      id: "1",
      name: "Ngã Tư Thủ Đức",
      latitude: 10.8505,
      longitude: 106.7718,
      pm25: 45.2,
      aqi: 85,
      severity: "medium",
    },
    {
      id: "2",
      name: "Ngã Tư Hàng Xanh",
      latitude: 10.7997,
      longitude: 106.7012,
      pm25: 62.8,
      aqi: 112,
      severity: "high",
    },
    {
      id: "3",
      name: "Cầu Sài Gòn",
      latitude: 10.7626,
      longitude: 106.6989,
      pm25: 28.5,
      aqi: 48,
      severity: "low",
    },
  ];

  const alerts: AlertLog[] = [
    {
      id: "1",
      timestamp: new Date(now.getTime() - 10 * 60 * 1000).toISOString(),
      type: "warning",
      message: "PM2.5 vượt ngưỡng 50 μg/m³",
      location: "Ngã Tư Hàng Xanh",
      resolved: false,
    },
    {
      id: "2",
      timestamp: new Date(now.getTime() - 25 * 60 * 1000).toISOString(),
      type: "info",
      message: "Lưu lượng xe tăng cao",
      location: "Ngã Tư Thủ Đức",
      resolved: true,
    },
    {
      id: "2",
      timestamp: new Date(now.getTime() - 25 * 60 * 1000).toISOString(),
      type: "info",
      message: "Lưu lượng xe tăng cao",
      location: "Ngã Tư Thủ Đức",
      resolved: true,
    },
    {
      id: "2",
      timestamp: new Date(now.getTime() - 25 * 60 * 1000).toISOString(),
      type: "info",
      message: "Lưu lượng xe tăng cao",
      location: "Ngã Tư Thủ Đức",
      resolved: true,
    },
  ];

  const interventions: InterventionAction[] = [
    {
      id: "1",
      timestamp: new Date(now.getTime() - 5 * 60 * 1000).toISOString(),
      action: "Tăng thời gian đèn xanh hướng Đông-Tây",
      target: "Ngã Tư Hàng Xanh",
      status: "in-progress",
      aiTriggered: true,
    },
    {
      id: "1",
      timestamp: new Date(now.getTime() - 5 * 60 * 1000).toISOString(),
      action: "Tăng thời gian đèn xanh hướng Đông-Tây",
      target: "Ngã Tư Hàng Xanh",
      status: "in-progress",
      aiTriggered: true,
    },
    {
      id: "1",
      timestamp: new Date(now.getTime() - 5 * 60 * 1000).toISOString(),
      action: "Tăng thời gian đèn xanh hướng Đông-Tây",
      target: "Ngã Tư Hàng Xanh",
      status: "in-progress",
      aiTriggered: true,
    },
    {
      id: "2",
      timestamp: new Date(now.getTime() - 15 * 60 * 1000).toISOString(),
      action: "Giảm PM2.5 bằng điều chỉnh pha",
      target: "Ngã Tư Thủ Đức",
      status: "completed",
      aiTriggered: true,
    },
    {
      id: "3",
      timestamp: new Date(now.getTime() - 30 * 60 * 1000).toISOString(),
      action: "Cân bằng lưu lượng",
      target: "Cầu Sài Gòn",
      status: "completed",
      aiTriggered: false,
    },
  ];

  return {
    kpis,
    monitoringData,
    rewardData,
    pollutionHotspots,
    alerts,
    interventions,
    lastUpdated: now.toISOString(),
  };
};

export const ManagerDashboard: React.FC = () => {
  // Initialize dark mode from localStorage or system preference
  const getInitialDarkMode = () => {
    if (typeof window !== 'undefined') {
      const stored = localStorage.getItem('darkMode');
      if (stored !== null) {
        return stored === 'true';
      }
      return window.matchMedia('(prefers-color-scheme: dark)').matches;
    }
    return false;
  };

  const [isDarkMode, setIsDarkMode] = useState(getInitialDarkMode);
  const [dashboardData, setDashboardData] = useState<DashboardStateModel>(
    generateMockData()
  );

  // Apply dark mode class on mount
  useEffect(() => {
    if (isDarkMode) {
      document.documentElement.classList.add("dark");
    } else {
      document.documentElement.classList.remove("dark");
    }
  }, [isDarkMode]);

  // Simulate real-time updates
  useEffect(() => {
    const interval = setInterval(() => {
      setDashboardData(generateMockData());
    }, 30000); // Update every 30 seconds

    return () => clearInterval(interval);
  }, []);

  const handleThemeToggle = () => {
    const newDarkMode = !isDarkMode;
    setIsDarkMode(newDarkMode);
    localStorage.setItem('darkMode', newDarkMode.toString());
  };

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <DashboardHeader
        onThemeToggle={handleThemeToggle}
        isDarkMode={isDarkMode}
      />

      <main className="p-4">
        {/* KPI Cards - Top Row (20% Height) */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 md:gap-6 gap-2 md:mb-4 mb-2">
          {dashboardData.kpis.map((kpi) => (
            <KPICard key={kpi.id} kpi={kpi} />
          ))}
        </div>

        {/* Bottom Row (40% Height) */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
          {/* Pollution Map - 65% */}
          <div className="lg:col-span-2 h-[500px]">
            <PollutionMap hotspots={dashboardData.pollutionHotspots} />
          </div>

          {/* Alert Panel - 35% */}
          <div className="h-[500px]">
            <AlertPanel
              alerts={dashboardData.alerts}
              interventions={dashboardData.interventions}
            />
          </div>
        </div>

        {/* Middle Row (40% Height) */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
          {/* Main Monitoring Chart - 65% */}
          <div className="lg:col-span-2 h-96">
            <MonitoringChart
              data={dashboardData.monitoringData}
              isDarkMode={isDarkMode}
            />
          </div>

          {/* Reward Chart - 35% */}
          <div className="h-96">
            <RewardChart
              data={dashboardData.rewardData}
              isDarkMode={isDarkMode}
            />
          </div>
        </div>

        {/* Last Updated */}
        <div className="mt-6 text-center">
          <p className="text-sm text-gray-500 dark:text-gray-400">
            Cập nhật lần cuối:{" "}
            {new Date(dashboardData.lastUpdated).toLocaleString("vi-VN")}
          </p>
        </div>
      </main>
    </div>
  );
};
