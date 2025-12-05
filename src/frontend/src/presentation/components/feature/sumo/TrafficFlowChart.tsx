import React, { useEffect, useRef } from "react";
import { Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler,
} from "chart.js";
import { useAppSelector } from "../../../../data/redux/hooks";
import { Activity, TrendingUp, Gauge } from "lucide-react";
import {
  type DataPoint,
  getChartData,
  getChartOptions,
} from "./components/TrafficChartConfig";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
);

export const TrafficFlowChart: React.FC = () => {
  const { simulationState } = useAppSelector((state) => state.sumo);
  const dataHistoryRef = useRef<DataPoint[]>([]);
  const maxDataPoints = 20;

  // Initialize with placeholder data
  useEffect(() => {
    if (dataHistoryRef.current.length === 0) {
      const placeholderData: DataPoint[] = Array.from(
        { length: maxDataPoints },
        (_, i) => ({
          timestamp: `T-${maxDataPoints - i}`,
          vehicleCount: 0,
          avgSpeed: 0,
        })
      );
      dataHistoryRef.current = placeholderData;
    }
  }, []);

  // Update data history when simulation state changes
  useEffect(() => {
    if (simulationState) {
      const now = new Date();
      const timestamp = now.toLocaleTimeString("vi-VN", {
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit",
      });

      const newDataPoint: DataPoint = {
        timestamp,
        vehicleCount: simulationState.vehicleCount,
        avgSpeed: simulationState.avgSpeed,
      };

      dataHistoryRef.current = [...dataHistoryRef.current, newDataPoint].slice(
        -maxDataPoints
      );
    }
  }, [simulationState]);

  const isDarkMode = document.documentElement.classList.contains("dark");

  const chartData = getChartData(dataHistoryRef.current);
  const options = getChartOptions(isDarkMode);

  const hasRealData = dataHistoryRef.current.some(
    (d) => d.vehicleCount > 0 || d.avgSpeed > 0
  );
  const latestData = dataHistoryRef.current[dataHistoryRef.current.length - 1];

  return (
    <div className="glass-card rounded-xl p-6 shadow-xl">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-3">
          <Activity className="w-6 h-6 text-emerald-600 dark:text-emerald-400" />
          <h2 className="text-xl font-bold text-gray-900 dark:text-white">
            Real-time Traffic Flow
          </h2>
        </div>

        {/* Live Stats */}
        {hasRealData && (
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2 px-3 py-1.5 bg-emerald-50 dark:bg-emerald-900/20 rounded-lg">
              <TrendingUp className="w-4 h-4 text-emerald-600 dark:text-emerald-400" />
              <span className="text-sm font-bold text-emerald-900 dark:text-emerald-100">
                {latestData.vehicleCount}
              </span>
              <span className="text-xs text-emerald-600 dark:text-emerald-400">
                vehicles
              </span>
            </div>
            <div className="flex items-center gap-2 px-3 py-1.5 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
              <Gauge className="w-4 h-4 text-blue-600 dark:text-blue-400" />
              <span className="text-sm font-bold text-blue-900 dark:text-blue-100">
                {latestData.avgSpeed.toFixed(1)}
              </span>
              <span className="text-xs text-blue-600 dark:text-blue-400">
                km/h
              </span>
            </div>
          </div>
        )}
      </div>

      <div className="h-80 relative">
        <Line data={chartData} options={options} />

        {/* Overlay message when no real data */}
        {!hasRealData && (
          <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
            <div
              className="bg-white/95 dark:bg-gray-800/95 backdrop-blur-sm px-6 py-4 rounded-xl 
                          border-2 border-dashed border-gray-300 dark:border-gray-600 shadow-lg"
            >
              <div className="flex items-center gap-3">
                <Activity className="w-5 h-5 text-emerald-600 dark:text-emerald-400 animate-pulse" />
                <div>
                  <p className="text-sm font-semibold text-gray-900 dark:text-white mb-1">
                    Chart Ready
                  </p>
                  <p className="text-xs text-gray-600 dark:text-gray-400">
                    Start SUMO, then enable AI control
                  </p>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Chart Info Footer */}
      <div className="mt-4 pt-4 border-t border-gray-200 dark:border-gray-700">
        <div className="flex items-center justify-between text-xs">
          <div className="flex items-center gap-4 text-gray-500 dark:text-gray-400">
            <span className="font-medium">
              {dataHistoryRef.current.length} data points
            </span>
            {hasRealData && (
              <span className="flex items-center gap-1">
                <span className="w-2 h-2 bg-emerald-500 rounded-full animate-pulse" />
                Live updating
              </span>
            )}
          </div>

          {hasRealData && (
            <div className="flex items-center gap-4">
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 rounded-full bg-[#107c41]" />
                <span className="text-gray-700 dark:text-gray-300 font-medium">
                  Vehicles
                </span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 rounded-full bg-[#3b82f6]" />
                <span className="text-gray-700 dark:text-gray-300 font-medium">
                  Speed
                </span>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
