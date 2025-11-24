import React from "react";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ChartOptions,
} from "chart.js";
import { Bar } from "react-chartjs-2";

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

interface VehicleDensityChartProps {
  data: {
    lanes: string[];
    density: number[];
  };
}

export const VehicleDensityChart: React.FC<VehicleDensityChartProps> = ({
  data,
}) => {
  const options: ChartOptions<"bar"> = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: false,
      },
      tooltip: {
        backgroundColor: "rgba(255, 255, 255, 0.95)",
        titleColor: "#111827",
        bodyColor: "#6b7280",
        borderColor: "#e5e7eb",
        borderWidth: 1,
        padding: 12,
        boxPadding: 6,
        font: {
          family: "Inter",
        },
        callbacks: {
          label: (context) => {
            return `Mật độ: ${context.parsed.y} xe/km`;
          },
        },
      },
    },
    scales: {
      x: {
        grid: {
          display: false,
        },
        ticks: {
          font: {
            family: "Inter",
            size: 11,
          },
          color: "#9ca3af",
        },
      },
      y: {
        beginAtZero: true,
        grid: {
          color: "#f3f4f6",
        },
        ticks: {
          font: {
            family: "Inter",
            size: 11,
          },
          color: "#9ca3af",
        },
      },
    },
    animation: {
      duration: 750,
      easing: "easeInOutQuart",
    },
  };

  const chartData = {
    labels: data.lanes,
    datasets: [
      {
        label: "Mật độ xe",
        data: data.density,
        backgroundColor: (context: any) => {
          const value = context.parsed.y;
          if (value > 80) return "rgba(239, 68, 68, 0.8)"; // Red - High density
          if (value > 50) return "rgba(245, 158, 11, 0.8)"; // Amber - Medium density
          return "rgba(34, 197, 94, 0.8)"; // Green - Low density
        },
        borderColor: (context: any) => {
          const value = context.parsed.y;
          if (value > 80) return "#ef4444";
          if (value > 50) return "#f59e0b";
          return "#22c55e";
        },
        borderWidth: 2,
        borderRadius: 6,
        borderSkipped: false,
      },
    ],
  };

  return (
    <div className="chart-container">
      <Bar options={options} data={chartData} />
    </div>
  );
};
