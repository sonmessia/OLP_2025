// Copyright (c) 2025 Green Wave Team
// 
// This software is released under the MIT License.
// https://opensource.org/licenses/MIT

import React from "react";
import { useTranslation } from "react-i18next";
import { type TFunction } from "i18next";
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend,
  type ChartOptions,
} from "chart.js";
import { Doughnut } from "react-chartjs-2";
import { Leaf, Cloud, Wind, AlertTriangle } from "lucide-react";

// Register Chart.js components
ChartJS.register(ArcElement, Tooltip, Legend);

interface AQIGaugeProps {
  value: number;
  isDarkMode: boolean;
  size?: number; // Default size for the gauge
}

const getAQIState = (value: number, t: TFunction<"aqi">) => {
  if (value <= 50) {
    return {
      color: "#10B981", // Green-500
      label: t("good"),
      description: t("descriptions.good"),
      Icon: Leaf,
      bgClass: "bg-green-100 dark:bg-green-900/30",
      textClass: "text-green-600 dark:text-green-400",
    };
  }
  if (value <= 100) {
    return {
      color: "#FBBF24", // Yellow-400
      label: t("moderate"),
      description: t("descriptions.moderate"),
      Icon: Cloud,
      bgClass: "bg-yellow-100 dark:bg-yellow-900/30",
      textClass: "text-yellow-600 dark:text-yellow-400",
    };
  }
  if (value <= 150) {
    return {
      color: "#F97316", // Orange-500
      label: t("unhealthy"),
      description: t("descriptions.unhealthy"),
      Icon: Wind,
      bgClass: "bg-orange-100 dark:bg-orange-900/30",
      textClass: "text-orange-600 dark:text-orange-400",
    };
  }
  return {
    color: "#EF4444", // Red-500
    label: t("hazardous"),
    description: t("descriptions.hazardous"),
    Icon: AlertTriangle,
    bgClass: "bg-red-100 dark:bg-red-900/30",
    textClass: "text-red-600 dark:text-red-400",
  };
};

export const AQIGauge: React.FC<AQIGaugeProps> = ({
  value,
  isDarkMode,
  size = 140,
}) => {
  const { t } = useTranslation("aqi");
  const { color, label, description, Icon, bgClass, textClass } = getAQIState(
    value,
    t
  );

  // Data for the half-doughnut gauge
  const data = {
    datasets: [
      {
        data: [value, Math.max(0, 300 - value)], // AQI max is typically 300+
        backgroundColor: [color, isDarkMode ? "#374151" : "#E5E7EB"], // Gray-700 : Gray-200
        borderWidth: 0,
        circumference: 180, // Half circle
        rotation: 270, // Start from top
        cutout: "80%", // Thinner donut
        borderRadius: 20,
      },
    ],
  };

  // Chart options
  const options: ChartOptions<"doughnut"> = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: false,
      },
      tooltip: {
        enabled: false,
      },
    },
    cutout: "75%",
    circumference: 180,
    rotation: 270,
  };

  return (
    <div
      className={`
      relative flex flex-col items-center justify-center
      glass-card rounded-2xl shadow-xl p-3
      transition-all duration-300
    `}
    >
      <h3 className="hidden md:block text-xs font-semibold text-gray-400 dark:text-gray-500 md:mb-2 uppercase tracking-widest">
        {t("title")}
      </h3>

      <div
        className="relative md:mb-1"
        style={{ width: size, height: size / 1.8 }}
      >
        <Doughnut data={data} options={options} />

        {/* Center Content */}
        <div className="absolute inset-0 flex flex-col items-center justify-end pb-0">
          <Icon
            className={`hidden md:block w-5 h-5 ${textClass}`}
            strokeWidth={2.5}
          />
          <span
            className={`text-xl md:text-3xl font-black ${textClass} tracking-tight leading-none`}
          >
            {value}
          </span>
        </div>
      </div>

      <div
        className={`mt-1 px-4 py-1 rounded-full ${bgClass} transition-colors duration-300`}
      >
        <span className={`text-sm font-bold ${textClass}`}>{label}</span>
      </div>

      <p className="hidden md:block text-[10px] text-gray-400 dark:text-gray-500 mt-2 font-medium text-center max-w-[120px]">
        {description}
      </p>
    </div>
  );
};
