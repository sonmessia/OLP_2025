import React from "react";
import type {
  TrafficFlowData,
  AirQualityData,
} from "../../../domain/models/simulation.types";

interface TrafficStatsProps {
  trafficFlow: TrafficFlowData | null;
  airQuality: AirQualityData | null;
  reward?: number;
  isConnected: boolean;
}

export const TrafficStats: React.FC<TrafficStatsProps> = ({
  trafficFlow,
  airQuality,
  reward,
  isConnected,
}) => {
  const getPhaseColor = (phase: number): string => {
    switch (phase) {
      case 0:
        return "text-green-600 dark:text-green-400";
      case 1:
        return "text-blue-600 dark:text-blue-400";
      case 2:
        return "text-yellow-600 dark:text-yellow-400";
      default:
        return "text-gray-600 dark:text-gray-400";
    }
  };

  const getPM25Status = (pm25: number): { text: string; color: string } => {
    if (pm25 < 12) return { text: "Tốt", color: "text-green-600" };
    if (pm25 < 35.4) return { text: "Trung bình", color: "text-yellow-600" };
    if (pm25 < 55.4) return { text: "Kém", color: "text-orange-600" };
    return { text: "Xấu", color: "text-red-600" };
  };

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-semibold text-gray-800 dark:text-gray-100">
          📊 Thống Kê Giao Thông
        </h2>
        <div className="flex items-center gap-2">
          <div
            className={`w-3 h-3 rounded-full ${
              isConnected ? "bg-green-500 animate-pulse" : "bg-red-500"
            }`}
          />
          <span className="text-sm text-gray-600 dark:text-gray-400">
            {isConnected ? "Đang kết nối" : "Mất kết nối"}
          </span>
        </div>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {/* Queue 0 */}
        <div className="bg-gradient-to-br from-blue-50 to-blue-100 dark:from-blue-900/20 dark:to-blue-800/20 rounded-lg p-4">
          <div className="text-xs font-medium text-blue-600 dark:text-blue-400 mb-1">
            Hàng đợi Đông-Tây
          </div>
          <div className="text-2xl font-bold text-blue-700 dark:text-blue-300">
            {trafficFlow?.queues[0] ?? 0}
          </div>
          <div className="text-xs text-blue-600/70 dark:text-blue-400/70 mt-1">
            xe
          </div>
        </div>

        {/* Queue 1 */}
        <div className="bg-gradient-to-br from-purple-50 to-purple-100 dark:from-purple-900/20 dark:to-purple-800/20 rounded-lg p-4">
          <div className="text-xs font-medium text-purple-600 dark:text-purple-400 mb-1">
            Hàng đợi Bắc-Nam
          </div>
          <div className="text-2xl font-bold text-purple-700 dark:text-purple-300">
            {trafficFlow?.queues[1] ?? 0}
          </div>
          <div className="text-xs text-purple-600/70 dark:text-purple-400/70 mt-1">
            xe
          </div>
        </div>

        {/* Phase */}
        <div className="bg-gradient-to-br from-green-50 to-green-100 dark:from-green-900/20 dark:to-green-800/20 rounded-lg p-4">
          <div className="text-xs font-medium text-green-600 dark:text-green-400 mb-1">
            Pha đèn hiện tại
          </div>
          <div
            className={`text-2xl font-bold ${getPhaseColor(
              trafficFlow?.phase ?? 0
            )}`}
          >
            {trafficFlow?.phase ?? 0}
          </div>
          <div className="text-xs text-green-600/70 dark:text-green-400/70 mt-1">
            {trafficFlow?.phase === 0 ? "Đông-Tây" : "Bắc-Nam"}
          </div>
        </div>

        {/* PM2.5 */}
        <div className="bg-gradient-to-br from-orange-50 to-orange-100 dark:from-orange-900/20 dark:to-orange-800/20 rounded-lg p-4">
          <div className="text-xs font-medium text-orange-600 dark:text-orange-400 mb-1">
            Chất lượng không khí
          </div>
          <div className="text-2xl font-bold text-orange-700 dark:text-orange-300">
            {airQuality?.pm25.toFixed(1) ?? "0.0"}
          </div>
          <div
            className={`text-xs font-medium mt-1 ${
              getPM25Status(airQuality?.pm25 ?? 0).color
            }`}
          >
            {getPM25Status(airQuality?.pm25 ?? 0).text}
          </div>
        </div>
      </div>

      {/* Reward */}
      {reward !== undefined && (
        <div className="mt-4 bg-gradient-to-r from-indigo-50 to-purple-50 dark:from-indigo-900/20 dark:to-purple-900/20 rounded-lg p-4">
          <div className="flex items-center justify-between">
            <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
              AI Reward Score
            </span>
            <span
              className={`text-xl font-bold ${
                reward >= 0 ? "text-green-600" : "text-red-600"
              }`}
            >
              {reward.toFixed(2)}
            </span>
          </div>
          <div className="mt-2 h-2 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
            <div
              className={`h-full transition-all duration-300 ${
                reward >= 0 ? "bg-green-500" : "bg-red-500"
              }`}
              style={{ width: `${Math.min(Math.abs(reward) * 10, 100)}%` }}
            />
          </div>
        </div>
      )}
    </div>
  );
};
