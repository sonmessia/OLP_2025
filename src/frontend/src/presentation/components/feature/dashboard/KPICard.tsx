import React from "react";
import type { KPICardModel } from "../../../../domain/models/DashboardModel";
import {
  TrendingUp,
  TrendingDown,
  Minus,
  Clock,
  Leaf,
  Car,
  Brain,
} from "lucide-react";

interface KPICardProps {
  kpi: KPICardModel;
}

const colorClasses = {
  green:
    "bg-emerald-50 dark:bg-emerald-900/20 border-emerald-200 dark:border-emerald-800",
  blue: "bg-blue-50 dark:bg-blue-900/20 border-blue-200 dark:border-blue-800",
  yellow:
    "bg-yellow-50 dark:bg-yellow-900/20 border-yellow-200 dark:border-yellow-800",
  red: "bg-red-50 dark:bg-red-900/20 border-red-200 dark:border-red-800",
};

const iconColorClasses = {
  green: "text-emerald-600 dark:text-emerald-400",
  blue: "text-blue-600 dark:text-blue-400",
  yellow: "text-yellow-600 dark:text-yellow-400",
  red: "text-red-600 dark:text-red-400",
};

// Icon mapping
const iconComponents: Record<
  string,
  React.ComponentType<{ className?: string }>
> = {
  Clock,
  Leaf,
  Car,
  Brain,
};

export const KPICard: React.FC<KPICardProps> = ({ kpi }) => {
  const getTrendIcon = () => {
    switch (kpi.trend) {
      case "up":
        return <TrendingUp className="w-4 h-4" />;
      case "down":
        return <TrendingDown className="w-4 h-4" />;
      default:
        return <Minus className="w-4 h-4" />;
    }
  };

  const getTrendColor = () => {
    if (kpi.trend === "up") return "text-green-600 dark:text-green-400";
    if (kpi.trend === "down") return "text-red-600 dark:text-red-400";
    return "text-gray-600 dark:text-gray-400";
  };

  const IconComponent = iconComponents[kpi.icon] || Clock;

  return (
    <div
      className={`rounded-xl border-2 p-2 md:px-6 md:py-2 transition-all hover:shadow-lg ${
        colorClasses[kpi.color]
      }`}
    >
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <p className="text-sm font-medium text-gray-600 dark:text-gray-400 mb-1">
            {kpi.title}
          </p>
          <div className="flex items-baseline gap-2">
            <h3 className="text-2xl font-bold text-gray-900 dark:text-white">
              {kpi.value.toLocaleString()}
            </h3>
            <span className="text-sm text-gray-500 dark:text-gray-400">
              {kpi.unit}
            </span>
          </div>
          <div className={`flex items-center gap-1 mt-2 ${getTrendColor()}`}>
            {getTrendIcon()}
            <span className="text-sm font-medium">
              {kpi.trendValue > 0 ? "+" : ""}
              {kpi.trendValue}%
            </span>
          </div>
        </div>
        <div
          className={`p-3 rounded-lg bg-white/50 dark:bg-black/20 ${
            iconColorClasses[kpi.color]
          }`}
        >
          <IconComponent className="w-6 h-6" />
        </div>
      </div>
    </div>
  );
};
