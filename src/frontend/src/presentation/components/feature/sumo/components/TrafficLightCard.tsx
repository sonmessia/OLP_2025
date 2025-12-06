// Copyright (c) 2025 Green Wave Team
// 
// This software is released under the MIT License.
// https://opensource.org/licenses/MIT

import React from "react";
import { useTranslation } from "react-i18next";
import { Star, Clock } from "lucide-react";
import type { TrafficLight } from "../../../../../domain/models/SumoModels";

interface TrafficLightCardProps {
  tls: TrafficLight;
}

export const TrafficLightCard: React.FC<TrafficLightCardProps> = ({ tls }) => {
  const { t } = useTranslation("sumo");

  const getLightColor = (color: string) => {
    const colors = {
      green: "bg-emerald-500 shadow-lg shadow-emerald-500/50",
      yellow: "bg-yellow-500 shadow-lg shadow-yellow-500/50",
      red: "bg-red-500 shadow-lg shadow-red-500/50",
      off: "bg-gray-300 dark:bg-gray-600",
    };
    return colors[color as keyof typeof colors] || colors.off;
  };

  const getCountdownColor = (timeUntilSwitch: number) => {
    if (timeUntilSwitch < 5) return "bg-red-500 animate-pulse";
    if (timeUntilSwitch < 10) return "bg-yellow-500";
    return "bg-blue-500";
  };

  const isMain = tls.isMain;

  return (
    <div
      className={`relative p-4 rounded-lg border-l-4 transition-all duration-300 hover:shadow-lg max-h-[300px]
        ${
          isMain
            ? "bg-emerald-50 dark:bg-emerald-900/20 border-emerald-500"
            : "bg-gray-50 dark:bg-gray-800/50 border-blue-500"
        }`}
    >
      {/* Header */}
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-2">
          {isMain && (
            <Star className="w-4 h-4 text-emerald-600 dark:text-emerald-400 fill-current" />
          )}
          <span className="font-bold text-gray-900 dark:text-white text-sm">
            {tls.id}
          </span>
        </div>
        <div
          className={`flex items-center gap-1 px-3 py-1 rounded-full text-white text-xs font-bold ${getCountdownColor(
            tls.timeUntilSwitch
          )}`}
        >
          <Clock className="w-3 h-3" />
          {tls.timeUntilSwitch.toFixed(1)}s
        </div>
      </div>

      {/* Signal Lights */}
      <div className="flex gap-1 mb-3 flex-wrap">
        {tls.lights.map((light, index) => (
          <div
            key={index}
            className={`w-5 h-5 rounded-full border-2 border-gray-300 dark:border-gray-600 
                       ${getLightColor(light.color)} 
                       transition-all duration-300`}
            title={`${t("trafficLight.signal")} ${light.index}: ${light.state}`}
          />
        ))}
      </div>

      {/* Info */}
      <div className="text-xs text-gray-600 dark:text-gray-400 flex items-center gap-2 flex-wrap">
        <span className="bg-gray-200 dark:bg-gray-700 px-2 py-1 rounded">
          {t("trafficLight.phase")} {tls.currentPhase}
        </span>
        <span className="bg-gray-200 dark:bg-gray-700 px-2 py-1 rounded">
          {tls.phaseDuration.toFixed(1)}s
        </span>
        {isMain && (
          <span className="bg-emerald-100 dark:bg-emerald-900/30 text-emerald-700 dark:text-emerald-300 px-2 py-1 rounded font-semibold">
            {t("trafficLight.mainControl")}
          </span>
        )}
      </div>
    </div>
  );
};
