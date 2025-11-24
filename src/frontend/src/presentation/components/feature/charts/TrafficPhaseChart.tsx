import React from "react";
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from "chart.js";
import type { ChartOptions } from "chart.js";
import { Doughnut } from "react-chartjs-2";

ChartJS.register(ArcElement, Tooltip, Legend);

interface TrafficPhaseChartProps {
  data: {
    phases: string[];
    durations: number[];
  };
  currentPhase?: number;
}

export const TrafficPhaseChart: React.FC<TrafficPhaseChartProps> = ({
  data,
  currentPhase = 0,
}) => {
  const options: ChartOptions<"doughnut"> = {
    responsive: true,
    maintainAspectRatio: false,
    cutout: "70%",
    plugins: {
      legend: {
        position: "bottom" as const,
        labels: {
          usePointStyle: true,
          padding: 15,
          font: {
            family: "Inter",
            size: 12,
            weight: 500,
          },
          generateLabels: (chart) => {
            const data = chart.data;
            if (data.labels && data.datasets.length) {
              return data.labels.map((label, i) => {
                const dataset = data.datasets[0];
                const value = dataset.data[i];
                const isActive = i === currentPhase;

                // Safely extract background colors as string array
                const bgColors: string[] = Array.isArray(
                  dataset.backgroundColor
                )
                  ? (dataset.backgroundColor as string[])
                  : [];

                return {
                  text: `${label}: ${value}s ${isActive ? "●" : ""}`,
                  fillStyle: bgColors[i] || "#000000",
                  hidden: false,
                  index: i,
                  fontColor: isActive ? "#22c55e" : "#6b7280",
                };
              });
            }
            return [];
          },
        },
      },
      tooltip: {
        backgroundColor: "rgba(255, 255, 255, 0.95)",
        titleColor: "#111827",
        bodyColor: "#6b7280",
        borderColor: "#e5e7eb",
        borderWidth: 1,
        padding: 12,
        boxPadding: 6,
        bodyFont: {
          family: "Inter",
        },
        titleFont: {
          family: "Inter",
        },
        callbacks: {
          label: (context) => {
            return `Thời gian: ${context.parsed} giây`;
          },
        },
      },
    },
    animation: {
      animateRotate: true,
      animateScale: true,
    },
  };

  const chartData = {
    labels: data.phases,
    datasets: [
      {
        label: "Thời gian pha",
        data: data.durations,
        backgroundColor: [
          "rgba(34, 197, 94, 0.8)", // Green
          "rgba(245, 158, 11, 0.8)", // Amber
          "rgba(239, 68, 68, 0.8)", // Red
          "rgba(59, 130, 246, 0.8)", // Blue
        ],
        borderColor: ["#22c55e", "#f59e0b", "#ef4444", "#3b82f6"],
        borderWidth: 2,
      },
    ],
  };

  return (
    <div className="chart-container" style={{ maxHeight: "300px" }}>
      <Doughnut options={options} data={chartData} />
    </div>
  );
};
