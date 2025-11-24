import React, { useEffect, useRef } from "react";
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
  ChartOptions,
} from "chart.js";
import { Line } from "react-chartjs-2";

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

interface TrafficFlowChartProps {
  data: {
    timestamps: string[];
    vehicleCount: number[];
    avgSpeed: number[];
  };
}

export const TrafficFlowChart: React.FC<TrafficFlowChartProps> = ({ data }) => {
  const chartRef = useRef<ChartJS<"line">>(null);

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
        labels: {
          usePointStyle: true,
          padding: 15,
          font: {
            family: "Inter",
            size: 12,
            weight: "500",
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
        usePointStyle: true,
        font: {
          family: "Inter",
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
    labels: data.timestamps,
    datasets: [
      {
        label: "Số lượng xe",
        data: data.vehicleCount,
        borderColor: "#22c55e",
        backgroundColor: "rgba(34, 197, 94, 0.1)",
        borderWidth: 2,
        fill: true,
        tension: 0.4,
        pointRadius: 3,
        pointHoverRadius: 6,
        pointBackgroundColor: "#22c55e",
        pointBorderColor: "#fff",
        pointBorderWidth: 2,
      },
      {
        label: "Tốc độ TB (km/h)",
        data: data.avgSpeed,
        borderColor: "#3b82f6",
        backgroundColor: "rgba(59, 130, 246, 0.1)",
        borderWidth: 2,
        fill: true,
        tension: 0.4,
        pointRadius: 3,
        pointHoverRadius: 6,
        pointBackgroundColor: "#3b82f6",
        pointBorderColor: "#fff",
        pointBorderWidth: 2,
      },
    ],
  };

  useEffect(() => {
    // Update chart when data changes
    if (chartRef.current) {
      chartRef.current.update("none");
    }
  }, [data]);

  return (
    <div className="chart-container">
      <Line ref={chartRef} options={options} data={chartData} />
    </div>
  );
};
