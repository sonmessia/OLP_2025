import type { ChartOptions, ChartData, ScriptableContext } from "chart.js";

export interface DataPoint {
  timestamp: string;
  vehicleCount: number;
  avgSpeed: number;
}

// import type { TFunction } from "i18next";
export const getChartOptions = (
  isDarkMode: boolean,
  t: any
): ChartOptions<"line"> => {
  return {
    responsive: true,
    maintainAspectRatio: false,
    interaction: {
      mode: "index",
      intersect: false,
    },
    plugins: {
      legend: {
        display: true,
        position: "top",
        align: "end",
        labels: {
          color: isDarkMode ? "#e0e0e0" : "#374151",
          font: {
            size: 13,
            weight: "bold",
            family: "system-ui, -apple-system, sans-serif",
          },
          padding: 16,
          usePointStyle: true,
          pointStyle: "circle",
          boxWidth: 8,
          boxHeight: 8,
        },
      },
      title: {
        display: false,
      },
      tooltip: {
        enabled: true,
        backgroundColor: isDarkMode
          ? "rgba(17, 24, 39, 0.95)"
          : "rgba(255, 255, 255, 0.95)",
        titleColor: isDarkMode ? "#f3f4f6" : "#111827",
        bodyColor: isDarkMode ? "#e5e7eb" : "#374151",
        borderColor: isDarkMode
          ? "rgba(75, 85, 99, 0.5)"
          : "rgba(209, 213, 219, 0.5)",
        borderWidth: 1,
        padding: 12,
        cornerRadius: 8,
        displayColors: true,
        boxWidth: 12,
        boxHeight: 12,
        boxPadding: 6,
        titleFont: {
          size: 13,
          weight: "bold",
        },
        bodyFont: {
          size: 12,
          weight: "normal",
        },
        callbacks: {
          title: function (context: any[]) {
            return `${t("sumo:chart.time")} ${context[0].label}`;
          },
          label: function (context: any) {
            let label = context.dataset.label || "";
            if (label) {
              label += ": ";
            }
            if (context.parsed.y !== null) {
              if (context.datasetIndex === 0) {
                label += `${context.parsed.y} ${t("sumo:chart.vehicles")}`;
              } else {
                label += `${context.parsed.y.toFixed(1)} km/h`;
              }
            }
            return label;
          },
        },
      },
    },
    scales: {
      x: {
        display: true,
        grid: {
          display: true,
          color: isDarkMode
            ? "rgba(75, 85, 99, 0.2)"
            : "rgba(229, 231, 235, 0.8)",
          lineWidth: 1,
        },
        ticks: {
          color: isDarkMode ? "#9ca3af" : "#6b7280",
          maxRotation: 0,
          minRotation: 0,
          font: {
            size: 11,
            weight: "normal",
          },
          padding: 8,
          autoSkip: true,
          maxTicksLimit: 10,
        },
        border: {
          display: false,
        },
      },
      y: {
        type: "linear",
        display: true,
        position: "left",
        title: {
          display: true,
          text: t("sumo:chart.vehicleCount"),
          color: isDarkMode ? "#10b981" : "#107c41",
          font: {
            size: 13,
            weight: "bold",
          },
          padding: { top: 0, bottom: 8 },
        },
        grid: {
          color: isDarkMode
            ? "rgba(75, 85, 99, 0.15)"
            : "rgba(229, 231, 235, 0.6)",
          lineWidth: 1,
        },
        ticks: {
          color: isDarkMode ? "#10b981" : "#107c41",
          font: {
            size: 12,
            weight: "bold",
          },
          padding: 8,
          callback: function (value: any) {
            return value;
          },
        },
        beginAtZero: true,
        max: 200,
        border: {
          display: false,
        },
      },
      y1: {
        type: "linear",
        display: true,
        position: "right",
        title: {
          display: true,
          text: t("sumo:chart.speedUnit"),
          color: isDarkMode ? "#60a5fa" : "#3b82f6",
          font: {
            size: 13,
            weight: "bold",
          },
          padding: { top: 0, bottom: 8 },
        },
        grid: {
          drawOnChartArea: false,
        },
        ticks: {
          color: isDarkMode ? "#60a5fa" : "#3b82f6",
          font: {
            size: 12,
            weight: "bold",
          },
          padding: 8,
          callback: function (value: any) {
            return value;
          },
        },
        beginAtZero: true,
        max: 100,
        border: {
          display: false,
        },
      },
    },
  };
};

export const getChartData = (
  dataHistory: DataPoint[],
  t: any
): ChartData<"line"> => {
  return {
    labels: dataHistory.map((d) => d.timestamp),
    datasets: [
      {
        label: t("sumo:chart.vehicleCount"),
        data: dataHistory.map((d) => d.vehicleCount),
        borderColor: "#107c41",
        backgroundColor: (context: ScriptableContext<"line">) => {
          const ctx = context.chart.ctx;
          const gradient = ctx.createLinearGradient(0, 0, 0, 300);
          gradient.addColorStop(0, "rgba(16, 124, 65, 0.3)");
          gradient.addColorStop(1, "rgba(16, 124, 65, 0.0)");
          return gradient;
        },
        borderWidth: 3,
        tension: 0.4,
        fill: true,
        yAxisID: "y",
        pointRadius: 4,
        pointHoverRadius: 6,
        pointBackgroundColor: "#107c41",
        pointBorderColor: "#fff",
        pointBorderWidth: 2,
        pointHoverBackgroundColor: "#107c41",
        pointHoverBorderColor: "#fff",
        pointHoverBorderWidth: 3,
      },
      {
        label: t("sumo:chart.avgSpeed"),
        data: dataHistory.map((d) => d.avgSpeed),
        borderColor: "#3b82f6",
        backgroundColor: (context: ScriptableContext<"line">) => {
          const ctx = context.chart.ctx;
          const gradient = ctx.createLinearGradient(0, 0, 0, 300);
          gradient.addColorStop(0, "rgba(59, 130, 246, 0.3)");
          gradient.addColorStop(1, "rgba(59, 130, 246, 0.0)");
          return gradient;
        },
        borderWidth: 3,
        tension: 0.4,
        fill: true,
        yAxisID: "y1",
        pointRadius: 4,
        pointHoverRadius: 6,
        pointBackgroundColor: "#3b82f6",
        pointBorderColor: "#fff",
        pointBorderWidth: 2,
        pointHoverBackgroundColor: "#3b82f6",
        pointHoverBorderColor: "#fff",
        pointHoverBorderWidth: 3,
      },
    ],
  };
};
