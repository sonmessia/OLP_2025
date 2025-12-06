// Copyright (c) 2025 Green Wave Team
// 
// This software is released under the MIT License.
// https://opensource.org/licenses/MIT

import React from "react";
import { useTranslation } from "react-i18next";
import type {
  AlertLog,
  InterventionAction,
} from "../../../../domain/models/DashboardModel";
import {
  AlertTriangle,
  AlertCircle,
  Info,
  CheckCircle,
  Clock,
  Play,
} from "lucide-react";

interface AlertPanelProps {
  alerts: AlertLog[];
  interventions: InterventionAction[];
}

const alertIcons = {
  warning: <AlertTriangle className="w-5 h-5 text-yellow-600" />,
  critical: <AlertCircle className="w-5 h-5 text-red-600" />,
  info: <Info className="w-5 h-5 text-blue-600" />,
};

const statusIcons = {
  pending: <Clock className="w-4 h-4 text-gray-500" />,
  "in-progress": <Play className="w-4 h-4 text-blue-500" />,
  completed: <CheckCircle className="w-4 h-4 text-green-500" />,
};

export const AlertPanel: React.FC<AlertPanelProps> = ({
  alerts,
  interventions,
}) => {
  const { t, i18n } = useTranslation(["alerts"]);

  const formatTime = (timestamp: string) => {
    const date = new Date(timestamp);
    return date.toLocaleTimeString(i18n.language === "en" ? "en-US" : "vi-VN", {
      hour: "2-digit",
      minute: "2-digit",
    });
  };

  const getStatusLabel = (status: string) => {
    const key = status === "in-progress" ? "inProgress" : status;
    // @ts-expect-error - dynamic key
    return t(`status.${key}`) as string;
  };

  return (
    <div className="bg-white dark:bg-gray-800 rounded-xl border-2 border-gray-200 dark:border-gray-700 p-3 h-full flex flex-col overflow-hidden">
      {/* Alerts Section */}
      <div className="mb-4 flex-shrink-0">
        <h3 className="text-base font-bold text-gray-900 dark:text-white mb-3 flex items-center gap-2">
          <AlertTriangle className="w-4 h-4" />
          {t("title")}
        </h3>
        <div className="space-y-2 max-h-32 overflow-y-auto pr-1">
          {alerts.length === 0 ? (
            <p className="text-xs text-gray-500 dark:text-gray-400 italic">
              {t("noAlerts")}
            </p>
          ) : (
            alerts.slice(0, 3).map((alert) => (
              <div
                key={alert.id}
                className={`p-2 rounded-lg border-l-4 ${
                  alert.type === "critical"
                    ? "bg-red-50 dark:bg-red-900/20 border-red-500"
                    : alert.type === "warning"
                    ? "bg-yellow-50 dark:bg-yellow-900/20 border-yellow-500"
                    : "bg-blue-50 dark:bg-blue-900/20 border-blue-500"
                } ${alert.resolved ? "opacity-50" : ""}`}
              >
                <div className="flex items-start gap-2">
                  <div className="flex-shrink-0 mt-0.5">
                    {alertIcons[alert.type]}
                  </div>
                  <div className="flex-1 min-w-0 overflow-hidden">
                    <p className="text-xs font-medium text-gray-900 dark:text-white truncate">
                      {alert.message}
                    </p>
                    <div className="flex items-center gap-1.5 mt-1 flex-wrap">
                      <span className="text-xs text-gray-500 dark:text-gray-400">
                        {formatTime(alert.timestamp)}
                      </span>
                      {alert.location && (
                        <>
                          <span className="text-xs text-gray-400">•</span>
                          <span className="text-xs text-gray-500 dark:text-gray-400 truncate">
                            {alert.location}
                          </span>
                        </>
                      )}
                    </div>
                  </div>
                  {alert.resolved && (
                    <CheckCircle className="w-4 h-4 text-green-500 flex-shrink-0" />
                  )}
                </div>
              </div>
            ))
          )}
        </div>
      </div>

      {/* Interventions Section */}
      <div className="flex-1 min-h-0 flex flex-col">
        <h3 className="text-base font-bold text-gray-900 dark:text-white mb-3 flex items-center gap-2 flex-shrink-0">
          <Play className="w-4 h-4" />
          {t("aiIntervention")}
        </h3>
        <div className="space-y-2 overflow-y-auto pr-1 flex-1">
          {interventions.length === 0 ? (
            <p className="text-xs text-gray-500 dark:text-gray-400 italic">
              {t("noIntervention")}
            </p>
          ) : (
            interventions.slice(0, 10).map((intervention) => (
              <div
                key={intervention.id}
                className="p-2 rounded-lg bg-gray-50 dark:bg-gray-700/50 border border-gray-200 dark:border-gray-600"
              >
                <div className="flex items-start gap-2">
                  <div className="flex-1 min-w-0 overflow-hidden">
                    <p className="text-xs font-medium text-gray-900 dark:text-white break-words">
                      {intervention.action}
                    </p>
                    <div className="flex items-center gap-1.5 mt-1 flex-wrap">
                      <span className="text-xs text-gray-500 dark:text-gray-400 truncate">
                        {intervention.target}
                      </span>
                      <span className="text-xs text-gray-400">•</span>
                      <span className="text-xs text-gray-500 dark:text-gray-400">
                        {formatTime(intervention.timestamp)}
                      </span>
                    </div>
                  </div>
                  <div className="flex flex-col items-end gap-1 flex-shrink-0">
                    {intervention.aiTriggered && (
                      <span className="px-1.5 py-0.5 text-xs font-medium bg-purple-100 dark:bg-purple-900/30 text-purple-700 dark:text-purple-300 rounded">
                        {t("aiTag")}
                      </span>
                    )}
                    <div className="flex items-center gap-1">
                      {statusIcons[intervention.status]}
                      <span className="text-xs text-gray-600 dark:text-gray-400 whitespace-nowrap">
                        {getStatusLabel(intervention.status)}
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
};
