import React from "react";
import { useAppSelector } from "../../../../data/redux/hooks";
import { Activity, Car, Gauge, Users } from "lucide-react";
import { MetricCard } from "./components/MetricCard";
import { useTranslation } from "react-i18next";

export const TrafficMetrics: React.FC = () => {
  const { simulationState } = useAppSelector((state) => state.sumo);
  const { t } = useTranslation("sumo");

  const metrics = [
    {
      label: t("metrics.avgSpeed"),
      value: simulationState?.avgSpeed.toFixed(1) || "0.0",
      unit: "km/h",
      color: "blue",
      icon: Gauge,
      trend: simulationState
        ? simulationState.avgSpeed > 30
          ? ("up" as const)
          : ("down" as const)
        : null,
    },
    {
      label: t("metrics.vehicles"),
      value: simulationState?.vehicleCount || 0,
      unit: t("metrics.active"),
      color: "green",
      icon: Car,
      trend: null,
    },
    {
      label: t("metrics.occupancy"),
      value: simulationState ? Math.round(simulationState.avgOccupancy) : 0,
      unit: "%",
      color: "yellow",
      icon: Activity,
      trend: simulationState
        ? simulationState.avgOccupancy < 50
          ? ("up" as const)
          : ("down" as const)
        : null,
    },
    {
      label: t("metrics.queue"),
      value: simulationState?.queueLength || 0,
      unit: t("chart.vehicles"),
      color: "red",
      icon: Users,
      trend: simulationState
        ? simulationState.queueLength < 10
          ? ("up" as const)
          : ("down" as const)
        : null,
    },
  ];

  return (
    <div className="glass-card rounded-xl p-6 shadow-xl">
      <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-6">
        {t("metrics.title")}
      </h2>

      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        {metrics.map((metric, index) => (
          <MetricCard key={index} {...metric} />
        ))}
      </div>

      {/* Occupancy Progress Bar */}
      {simulationState && (
        <div className="mt-6">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
              {t("metrics.roadOccupancy")}
            </span>
            <span className="text-sm font-bold text-gray-900 dark:text-white">
              {Math.round(simulationState.avgOccupancy)}%
            </span>
          </div>
          <div className="w-full h-3 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
            <div
              className="h-full eco-gradient-primary transition-all duration-500 ease-out
                         flex items-center justify-center"
              style={{
                width: `${Math.min(simulationState.avgOccupancy, 100)}%`,
              }}
            />
          </div>
        </div>
      )}

      {/* Additional Stats */}
      {simulationState && (
        <div className="mt-6 pt-6 border-t border-gray-200 dark:border-gray-700">
          <div className="grid grid-cols-3 gap-4 text-center">
            <div>
              <p className="text-xs text-gray-600 dark:text-gray-400 mb-1">
                {t("metrics.loaded")}
              </p>
              <p className="text-lg font-bold text-gray-900 dark:text-white">
                {simulationState.loadedVehicles}
              </p>
            </div>
            <div>
              <p className="text-xs text-gray-600 dark:text-gray-400 mb-1">
                {t("metrics.departed")}
              </p>
              <p className="text-lg font-bold text-gray-900 dark:text-white">
                {simulationState.departedVehicles}
              </p>
            </div>
            <div>
              <p className="text-xs text-gray-600 dark:text-gray-400 mb-1">
                {t("metrics.arrived")}
              </p>
              <p className="text-lg font-bold text-emerald-600 dark:text-emerald-400">
                {simulationState.arrivedVehicles}
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Waiting Time */}
      {simulationState && (
        <div className="mt-4 p-3 bg-gradient-to-r from-orange-50 to-red-50 dark:from-orange-900/20 dark:to-red-900/20 rounded-lg border-l-4 border-orange-500">
          <div className="flex items-center justify-between">
            <span className="text-sm font-medium text-orange-800 dark:text-orange-200">
              {t("metrics.waitingTime")}
            </span>
            <span className="text-lg font-bold text-orange-900 dark:text-orange-100">
              {simulationState.waitingTime.toFixed(1)}s
            </span>
          </div>
        </div>
      )}
    </div>
  );
};
