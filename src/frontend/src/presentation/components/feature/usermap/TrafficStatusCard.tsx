// Copyright (c) 2025 Green Wave Team
// 
// This software is released under the MIT License.
// https://opensource.org/licenses/MIT

import React from "react";
import { Gauge, Clock, Activity, Car } from "lucide-react";
import { useTranslation } from "react-i18next";

interface TrafficStatusCardProps {
  avgSpeed: number;
  vehicleCount: number;
  waitingTime: number;
  lastUpdated: Date;
  isDarkMode: boolean;
}

export const TrafficStatusCard: React.FC<TrafficStatusCardProps> = ({
  avgSpeed,
  vehicleCount,
  waitingTime,
  lastUpdated,
  isDarkMode,
}) => {
  const { t } = useTranslation("traffic");
  const textColor = isDarkMode ? "text-white" : "text-gray-800";

  return (
    <div
      className={`glass-card ${textColor} rounded-xl shadow-lg p-4 transition-all duration-300`}
    >
      <div className="flex items-center justify-between mb-4">
        <h3 className="font-bold text-lg flex items-center gap-2">
          <Activity className="text-blue-500" />
          {t("statusCard.title")}
        </h3>
        <span
          className={`text-xs font-medium px-2 py-1 rounded-full ${
            isDarkMode ? "bg-gray-700" : "bg-gray-100"
          }`}
        >
          {t("statusCard.live")}
        </span>
      </div>

      <div className="grid grid-cols-3 gap-4">
        {/* Average Speed */}
        <div className="flex flex-col gap-1">
          <div className="flex items-center gap-2 text-sm opacity-80">
            <Gauge className="text-blue-500" />
            <span className="text-xs">{t("statusCard.avgSpeed")}</span>
          </div>
          <div className="text-xl font-bold">
            {avgSpeed.toFixed(1)}{" "}
            <span className="text-xs font-normal">km/h</span>
          </div>
        </div>

        {/* Vehicle Count */}
        <div className="flex flex-col gap-1">
          <div className="flex items-center gap-2 text-sm opacity-80">
            <Car className="text-orange-500" />
            <span className="text-xs">{t("statusCard.vehicleCount")}</span>
          </div>
          <div className="text-xl font-bold">
            {vehicleCount.toFixed(0)}{" "}
            <span className="text-xs font-normal">vehs</span>
          </div>
        </div>

        {/* Waiting Time */}
        <div className="flex flex-col gap-1 col-span-1">
          <div className="flex items-center gap-2 text-sm opacity-80">
            <Clock className="text-red-500" />
            <span className="text-xs">{t("statusCard.waitingTime")}</span>
          </div>
          <div className="text-xl font-bold">
            {waitingTime.toFixed(0)}{" "}
            <span className="text-xs font-normal">s</span>
          </div>
        </div>
      </div>

      {/* Last Updated */}
      <div className="mt-4 pt-2 border-t border-gray-200 dark:border-gray-700 text-xs text-right opacity-60">
        {t("statusCard.updated")}: {lastUpdated.toLocaleTimeString()}
      </div>
    </div>
  );
};
