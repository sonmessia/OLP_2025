import React from "react";
import { TrendingUp, TrendingDown } from "lucide-react";

interface StatCardProps {
  label: string;
  value: string | number;
  unit?: string;
  trend?: {
    value: number;
    direction: "up" | "down";
  };
  status?: "success" | "warning" | "error" | "info";
}

export const StatCard: React.FC<StatCardProps> = ({
  label,
  value,
  unit,
  trend,
  status = "info",
}) => {
  const getStatusColor = () => {
    switch (status) {
      case "success":
        return "border-green-200 bg-green-50/50";
      case "warning":
        return "border-amber-200 bg-amber-50/50";
      case "error":
        return "border-red-200 bg-red-50/50";
      default:
        return "border-gray-200 bg-white";
    }
  };

  return (
    <div className={`stat-card ${getStatusColor()}`}>
      <div className="stat-label">{label}</div>
      <div className="flex items-baseline gap-2 mt-2">
        <span className="stat-value">{value}</span>
        {unit && (
          <span className="text-sm font-medium text-gray-500">{unit}</span>
        )}
      </div>
      {trend && (
        <div className={`stat-trend ${trend.direction}`}>
          {trend.direction === "up" ? (
            <TrendingUp size={14} />
          ) : (
            <TrendingDown size={14} />
          )}
          <span>{Math.abs(trend.value)}%</span>
          <span className="text-gray-400">so với trước</span>
        </div>
      )}
    </div>
  );
};
