import React from "react";
import { useTranslation } from "react-i18next";
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
import type { ChartOptions, ScriptableContext } from "chart.js";
import { Line } from "react-chartjs-2";
import type { MonitoringDataPoint } from "../../../../domain/models/DashboardModel";

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

interface MonitoringChartProps {
  data: MonitoringDataPoint[];
  isDarkMode?: boolean;
}

export const MonitoringChart: React.FC<MonitoringChartProps> = ({
  data,
  isDarkMode = false,
}) => {
  const { t, i18n } = useTranslation(["monitoring"]);
  // Detect dark mode from document if not provided
  const darkMode =
    isDarkMode || document.documentElement.classList.contains("dark");

  // Calculate stats
  const latest = data[data.length - 1] || { avgWaitingTime: 0, pm25Level: 0 };
  const avgWait = Math.round(
    data.reduce((acc, curr) => acc + curr.avgWaitingTime, 0) /
      (data.length || 1)
  );
  const avgPM25 =
    Math.round(
      (data.reduce((acc, curr) => acc + curr.pm25Level, 0) /
        (data.length || 1)) *
        10
    ) / 10;

  const labels = data.map((point) => {
    const date = new Date(point.timestamp);
    return date.toLocaleTimeString(i18n.language === "en" ? "en-US" : "vi-VN", {
      hour: "2-digit",
      minute: "2-digit",
    });
  });

  const chartData = {
    labels,
    datasets: [
      {
        label: t("waitingTime"),
        data: data.map((point) => point.avgWaitingTime),
        borderColor: "#3B82F6", // Blue-500
        backgroundColor: (context: ScriptableContext<"line">) => {
          const ctx = context.chart.ctx;
          const gradient = ctx.createLinearGradient(0, 0, 0, 300);
          gradient.addColorStop(0, "rgba(59, 130, 246, 0.2)");
          gradient.addColorStop(1, "rgba(59, 130, 246, 0.0)");
          return gradient;
        },
        yAxisID: "y-axis-1",
        tension: 0.4,
        fill: true,
        pointRadius: 0,
        pointHoverRadius: 6,
        pointBackgroundColor: "#3B82F6",
        borderWidth: 2,
      },
      {
        label: t("pm25"),
        data: data.map((point) => point.pm25Level),
        borderColor: "#10B981", // Emerald-500
        backgroundColor: (context: ScriptableContext<"line">) => {
          const ctx = context.chart.ctx;
          const gradient = ctx.createLinearGradient(0, 0, 0, 300);
          gradient.addColorStop(0, "rgba(16, 185, 129, 0.2)");
          gradient.addColorStop(1, "rgba(16, 185, 129, 0.0)");
          return gradient;
        },
        yAxisID: "y-axis-2",
        tension: 0.4,
        fill: true,
        pointRadius: 0,
        pointHoverRadius: 6,
        pointBackgroundColor: "#10B981",
        borderWidth: 2,
      },
    ],
  };

  const options: ChartOptions<"line"> = {
    responsive: true,
    maintainAspectRatio: false,
    interaction: {
      mode: "index" as const,
      intersect: false,
    },
    plugins: {
      legend: {
        position: "top" as const,
        align: "end",
        labels: {
          usePointStyle: true,
          boxWidth: 8,
          boxHeight: 8,
          padding: 20,
          font: {
            size: 11,
            weight: 500,
            family: "'Inter', sans-serif",
          },
          color: darkMode ? "#9CA3AF" : "#6B7280", // Gray-400 : Gray-500
        },
      },
      title: {
        display: false, // Hide default title
      },
      tooltip: {
        backgroundColor: darkMode
          ? "rgba(17, 24, 39, 0.95)"
          : "rgba(255, 255, 255, 0.95)",
        titleColor: darkMode ? "#F9FAFB" : "#111827",
        bodyColor: darkMode ? "#D1D5DB" : "#4B5563",
        borderColor: darkMode ? "#374151" : "#E5E7EB",
        borderWidth: 1,
        padding: 10,
        boxPadding: 4,
        usePointStyle: true,
        titleFont: {
          size: 13,
          weight: "bold",
        },
        bodyFont: {
          size: 12,
        },
        callbacks: {
          label: function (context) {
            let label = context.dataset.label || "";
            if (label) {
              label += ": ";
            }
            if (context.parsed.y !== null) {
              label += context.parsed.y.toFixed(1);
            }
            return label;
          },
        },
      },
    },
    scales: {
      "y-axis-1": {
        type: "linear" as const,
        display: true,
        position: "left" as const,
        title: {
          display: false, // Hide axis title for cleaner look
        },
        ticks: {
          color: darkMode ? "#9CA3AF" : "#6B7280",
          font: { size: 10 },
          maxTicksLimit: 6,
        },
        grid: {
          color: darkMode ? "rgba(75, 85, 99, 0.1)" : "rgba(0, 0, 0, 0.03)",
          drawTicks: false,
        },
        border: { display: false },
      },
      "y-axis-2": {
        type: "linear" as const,
        display: true,
        position: "right" as const,
        title: {
          display: false,
        },
        ticks: {
          color: darkMode ? "#9CA3AF" : "#6B7280",
          font: { size: 10 },
          maxTicksLimit: 6,
        },
        grid: {
          drawOnChartArea: false, // Only show grid for left axis
          drawTicks: false,
        },
        border: { display: false },
      },
      x: {
        ticks: {
          color: darkMode ? "#9CA3AF" : "#6B7280",
          font: { size: 10 },
          maxTicksLimit: 8,
        },
        grid: {
          display: false, // Hide vertical grid lines
        },
        border: { display: false },
      },
    },
  };

  return (
    <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 p-5 h-full flex flex-col shadow-sm">
      {/* Custom Header with Stats */}
      <div className="mb-2 flex flex-col sm:flex-row sm:items-end justify-between gap-4">
        <div>
          <h3 className="text-base font-bold text-gray-900 dark:text-white flex items-center gap-2">
            <span className="w-1 h-4 bg-blue-500 rounded-full"></span>
            {t("realTimeMonitoring")}
          </h3>
          <p className="text-xs text-gray-500 dark:text-gray-400 mt-1 ml-3">
            {t("updateInterval")}
          </p>
        </div>

        <div className="flex items-center gap-6">
          {/* Traffic Stat */}
          <div className="text-right">
            <p className="text-[10px] uppercase tracking-wider text-gray-500 dark:text-gray-400 font-semibold mb-0.5">
              {t("waitingTimeLabel")}
            </p>
            <div className="flex items-baseline justify-end gap-2">
              <span className="text-2xl font-bold text-gray-900 dark:text-white">
                {Math.round(latest.avgWaitingTime)}
                <span className="text-sm font-normal text-gray-500 ml-0.5">
                  {t("secondsAbbr")}
                </span>
              </span>
              <span className="text-xs font-medium text-blue-600 dark:text-blue-400 bg-blue-50 dark:bg-blue-900/30 px-1.5 py-0.5 rounded">
                {t("averageAbbr")} {avgWait}
              </span>
            </div>
          </div>

          {/* Environment Stat */}
          <div className="text-right border-l border-gray-200 dark:border-gray-700 pl-6">
            <p className="text-[10px] uppercase tracking-wider text-gray-500 dark:text-gray-400 font-semibold mb-0.5">
              PM2.5
            </p>
            <div className="flex items-baseline justify-end gap-2">
              <span className="text-2xl font-bold text-gray-900 dark:text-white">
                {latest.pm25Level.toFixed(1)}
                <span className="text-sm font-normal text-gray-500 ml-0.5">
                  {t("microgramAbbr")}
                </span>
              </span>
              <span
                className={`text-xs font-medium px-1.5 py-0.5 rounded ${
                  latest.pm25Level > 50
                    ? "text-red-600 bg-red-50 dark:text-red-400 dark:bg-red-900/30"
                    : "text-emerald-600 bg-emerald-50 dark:text-emerald-400 dark:bg-emerald-900/30"
                }`}
              >
                {t("averageAbbr")} {avgPM25}
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Chart Area */}
      <div className="flex-1 min-h-0 w-full">
        <Line data={chartData} options={options} />
      </div>
    </div>
  );
};
