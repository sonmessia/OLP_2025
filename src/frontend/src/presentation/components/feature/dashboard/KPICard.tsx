// Copyright (c) 2025 Green Wave Team
// 
// This software is released under the MIT License.
// https://opensource.org/licenses/MIT

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
  kpi?: KPICardModel;
  title?: string;
  metrics?: Array<{
    label: string;
    value: string;
    unit?: string;
  }>;
  showProgress?: boolean;
  progressValue?: number;
  progressColor?: string;
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

export const KPICard: React.FC<KPICardProps> = ({
  kpi,
  title,
  metrics,
  showProgress,
  progressValue,
  progressColor = "bg-blue-500",
}) => {
  // Handle metrics array mode (for Air Quality Dashboard)
  if (metrics) {
    return (
      <div
        className={`rounded-lg border p-4 transition-all hover:shadow-md ${colorClasses.blue}`}
      >
        <div className="flex flex-col">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
            {title}
          </h3>

          <div className="space-y-3">
            {metrics.map((metric, index) => (
              <div key={index} className="flex items-baseline justify-between">
                <span className="text-sm text-gray-600 dark:text-gray-400">
                  {metric.label}
                </span>
                <div className="flex items-baseline gap-1">
                  <span className="text-xl font-bold text-gray-900 dark:text-white">
                    {metric.value}
                  </span>
                  {metric.unit && (
                    <span className="text-sm text-gray-600 dark:text-gray-400">
                      {metric.unit}
                    </span>
                  )}
                </div>
              </div>
            ))}
          </div>

          {showProgress && progressValue !== undefined && (
            <div className="mt-4">
              <div className="w-full bg-gray-200 rounded-full h-2 overflow-hidden">
                <div
                  className={`h-full transition-all duration-300 ${progressColor}`}
                  style={{ width: `${Math.min(progressValue, 100)}%` }}
                />
              </div>
            </div>
          )}
        </div>
      </div>
    );
  }

  // Handle single KPI mode (original functionality)
  if (!kpi) {
    return null;
  }

  const getTrendIcon = () => {
    switch (kpi.trend) {
      case "up":
        return <TrendingUp className="w-3 h-3" />;
      case "down":
        return <TrendingDown className="w-3 h-3" />;
      default:
        return <Minus className="w-3 h-3" />;
    }
  };

  const IconComponent = iconComponents[kpi.icon] || Clock;

  return (
    <div
      className={`rounded-lg border p-3 transition-all hover:shadow-md ${
        colorClasses[kpi.color]
      }`}
    >
      <div className="flex items-start justify-between">
        <div className="flex-1 min-w-0">
          <p className="text-xs font-semibold text-gray-600 dark:text-gray-400 truncate">
            {kpi.title}
          </p>
          <div className="flex items-baseline gap-1.5 mt-1">
            <h3 className="text-xl font-bold text-gray-900 dark:text-white leading-none">
              {kpi.value.toLocaleString()}
            </h3>
            <span className="text-xs text-gray-500 dark:text-gray-400">
              {kpi.unit}
            </span>
          </div>
        </div>
        <div
          className={`flex items-center gap-1 mt-1.5 ${
            iconColorClasses[kpi.color]
          }`}
        >
          {getTrendIcon()}
          <span className="text-xs font-medium">
            {kpi.trendValue > 0 ? "+" : ""}
            {kpi.trendValue}%
          </span>
        </div>
        <div
          className={`p-2 rounded-md bg-white/60 dark:bg-black/20 ml-3 ${
            iconColorClasses[kpi.color]
          }`}
        >
          <IconComponent className="w-5 h-5" />
        </div>
      </div>
    </div>
  );
};
