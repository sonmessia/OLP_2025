import React, { useMemo } from "react";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";
import type { ChartData, ChartOptions } from "chart.js";
import { Bar } from "react-chartjs-2";
import type { RewardDataPoint } from "../../../../domain/models/DashboardModel";
import { TrendingUp, Leaf, Car, Activity } from "lucide-react";

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

interface RewardChartProps {
  data: RewardDataPoint[];
  isDarkMode?: boolean;
}

export const RewardChart: React.FC<RewardChartProps> = ({
  data,
  isDarkMode = false,
}) => {
  // Detect dark mode from document if not provided
  const darkMode =
    isDarkMode || document.documentElement.classList.contains("dark");

  // Calculate statistics
  const stats = useMemo(() => {
    if (data.length === 0)
      return { avgTraffic: 0, avgEnv: 0, lastTotal: 0, trend: 0 };

    const totalTraffic = data.reduce((sum, p) => sum + p.trafficReward, 0);
    const totalEnv = data.reduce((sum, p) => sum + p.environmentReward, 0);
    const avgTraffic = totalTraffic / data.length;
    const avgEnv = totalEnv / data.length;

    const lastPoint = data[data.length - 1];
    const lastTotal = lastPoint.trafficReward + lastPoint.environmentReward;

    // Simple trend: compare last point total to average total
    const avgTotal = avgTraffic + avgEnv;
    const trend = ((lastTotal - avgTotal) / avgTotal) * 100;

    return {
      avgTraffic,
      avgEnv,
      lastTotal,
      trend,
    };
  }, [data]);

  const labels = data.map((point) => {
    const date = new Date(point.timestamp);
    return date.toLocaleTimeString("vi-VN", {
      hour: "2-digit",
      minute: "2-digit",
    });
  });

  const chartData: ChartData<"bar"> = {
    labels,
    datasets: [
      {
        label: "Giao thông",
        data: data.map((point) => point.trafficReward),
        backgroundColor: "#3B82F6", // Blue-500
        hoverBackgroundColor: "#2563EB", // Blue-600
        borderRadius: 4,
        barPercentage: 0.6,
        categoryPercentage: 0.8,
      },
      {
        label: "Môi trường",
        data: data.map((point) => point.environmentReward),
        backgroundColor: "#10B981", // Emerald-500
        hoverBackgroundColor: "#059669", // Emerald-600
        borderRadius: 4,
        barPercentage: 0.6,
        categoryPercentage: 0.8,
      },
    ],
  };

  const options: ChartOptions<"bar"> = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: "top",
        align: "end",
        labels: {
          usePointStyle: true,
          pointStyle: "circle",
          padding: 20,
          font: {
            size: 11,
            family: "'Inter', sans-serif",
            weight: 500,
          },
          color: darkMode ? "#9CA3AF" : "#6B7280", // Gray-400 : Gray-500
        },
      },
      title: {
        display: false, // We use custom header
      },
      tooltip: {
        backgroundColor: darkMode ? "#1F2937" : "#FFFFFF",
        titleColor: darkMode ? "#F3F4F6" : "#111827",
        bodyColor: darkMode ? "#D1D5DB" : "#4B5563",
        borderColor: darkMode ? "#374151" : "#E5E7EB",
        borderWidth: 1,
        padding: 12,
        boxPadding: 4,
        usePointStyle: true,
        callbacks: {
          label: function (context) {
            let label = context.dataset.label || "";
            if (label) {
              label += ": ";
            }
            if (context.parsed.y !== null) {
              label += context.parsed.y.toFixed(2);
            }
            return label;
          },
        },
      },
    },
    scales: {
      x: {
        stacked: true,
        grid: {
          display: false,
        },
        ticks: {
          color: darkMode ? "#9CA3AF" : "#9CA3AF",
          font: {
            size: 10,
          },
          maxRotation: 0,
          autoSkip: true,
          maxTicksLimit: 6,
        },
        border: {
          display: false,
        },
      },
      y: {
        stacked: true,
        grid: {
          color: darkMode
            ? "rgba(75, 85, 99, 0.2)"
            : "rgba(229, 231, 235, 0.5)",
          drawTicks: false,
        },
        ticks: {
          color: darkMode ? "#9CA3AF" : "#9CA3AF",
          font: {
            size: 10,
          },
          padding: 10,
        },
        border: {
          display: false,
          dash: [4, 4],
        },
      },
    },
    interaction: {
      mode: "index",
      intersect: false,
    },
  };

  return (
    <div className="bg-white dark:bg-gray-800 rounded-2xl border border-gray-100 dark:border-gray-700 px-2 py-4 h-full shadow-sm flex flex-col">
      {/* Header Section */}
      <div className="flex flex-col mb-4">
        <div className="flex items-center justify-between mb-2">
          <div>
            <h3 className="text-lg font-bold text-gray-900 dark:text-white flex items-center gap-2">
              <Activity className="w-5 h-5 text-indigo-500" />
              Hiệu Suất AI
            </h3>
            <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
              Phân bổ điểm thưởng Giao thông & Môi trường
            </p>
          </div>
          <div className="flex items-center gap-2 px-3 py-1 rounded-full bg-green-50 dark:bg-green-900/20 border border-green-100 dark:border-green-900/30">
            <TrendingUp className="w-4 h-4 text-green-600 dark:text-green-400" />
            <span className="text-xs font-medium text-green-700 dark:text-green-300">
              {stats.trend > 0 ? "+" : ""}
              {stats.trend.toFixed(1)}% vs TB
            </span>
          </div>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-3 gap-4">
          <div className="p-2 rounded-xl bg-blue-50 dark:bg-blue-900/10 border border-blue-100 dark:border-blue-800/30">
            <div className="flex items-center gap-2 mb-1">
              <Car className="w-4 h-4 text-blue-600 dark:text-blue-400" />
              <span className="text-xs font-medium text-blue-700 dark:text-blue-300">
                Giao thông (TB)
              </span>
            </div>
            <p className="text-md font-bold text-blue-900 dark:text-blue-100">
              {stats.avgTraffic.toFixed(2)}
            </p>
          </div>

          <div className="p-3 rounded-xl bg-emerald-50 dark:bg-emerald-900/10 border border-emerald-100 dark:border-emerald-800/30">
            <div className="flex items-center gap-2 mb-1">
              <Leaf className="w-4 h-4 text-emerald-600 dark:text-emerald-400" />
              <span className="text-xs font-medium text-emerald-700 dark:text-emerald-300">
                Môi trường (TB)
              </span>
            </div>
            <p className="text-md font-bold text-emerald-900 dark:text-emerald-100">
              {stats.avgEnv.toFixed(2)}
            </p>
          </div>

          <div className="p-3 rounded-xl bg-purple-50 dark:bg-purple-900/10 border border-purple-100 dark:border-purple-800/30">
            <div className="flex items-center gap-2 mb-1">
              <Activity className="w-4 h-4 text-purple-600 dark:text-purple-400" />
              <span className="text-xs font-medium text-purple-700 dark:text-purple-300">
                Tổng điểm (Mới nhất)
              </span>
            </div>
            <p className="text-md font-bold text-purple-900 dark:text-purple-100">
              {stats.lastTotal.toFixed(2)}
            </p>
          </div>
        </div>
      </div>

      {/* Chart Section */}
      <div className="flex-1 min-h-[200px] w-full">
        <Bar data={chartData} options={options} />
      </div>
    </div>
  );
};
