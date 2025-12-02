import React from "react";
import { TrendingUp, TrendingDown, type LucideIcon } from "lucide-react";

interface MetricCardProps {
  label: string;
  value: string | number;
  unit: string;
  color: string;
  icon: LucideIcon;
  trend: "up" | "down" | null;
}

export const MetricCard: React.FC<MetricCardProps> = ({
  label,
  value,
  unit,
  color,
  icon: Icon,
  trend,
}) => {
  const getColorClasses = (color: string) => {
    const colors = {
      blue: "from-blue-500 to-cyan-500",
      green: "from-emerald-500 to-green-600",
      yellow: "from-yellow-500 to-orange-500",
      red: "from-red-500 to-pink-500",
    };
    return colors[color as keyof typeof colors] || colors.blue;
  };

  const getIconBgColor = (color: string) => {
    const colors = {
      blue: "bg-blue-100 dark:bg-blue-900/30",
      green: "bg-emerald-100 dark:bg-emerald-900/30",
      yellow: "bg-yellow-100 dark:bg-yellow-900/30",
      red: "bg-red-100 dark:bg-red-900/30",
    };
    return colors[color as keyof typeof colors] || colors.blue;
  };

  return (
    <div
      className="relative overflow-hidden rounded-lg bg-white dark:bg-gray-800 p-4 
                 border border-gray-200 dark:border-gray-700 hover:shadow-lg transition-all duration-300
                 hover:scale-105"
    >
      {/* Background Gradient */}
      <div
        className={`absolute inset-0 bg-gradient-to-br ${getColorClasses(
          color
        )} opacity-5`}
      />

      <div className="relative">
        <div className="flex items-center justify-between mb-3">
          <div className={`p-2 rounded-lg ${getIconBgColor(color)}`}>
            <Icon
              className={`w-5 h-5 text-${color}-600 dark:text-${color}-400`}
            />
          </div>
          {trend && (
            <div
              className={`flex items-center ${
                trend === "up" ? "text-emerald-500" : "text-red-500"
              }`}
            >
              {trend === "up" ? (
                <TrendingUp className="w-4 h-4" />
              ) : (
                <TrendingDown className="w-4 h-4" />
              )}
            </div>
          )}
        </div>

        <div className="space-y-1">
          <p className="text-xs text-gray-600 dark:text-gray-400 font-medium">
            {label}
          </p>
          <div className="flex items-baseline gap-1">
            <span className="text-2xl font-bold text-gray-900 dark:text-white">
              {value}
            </span>
            <span className="text-xs text-gray-500 dark:text-gray-400">
              {unit}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};
