import React from "react";
import { useTranslation } from "react-i18next";
import type { TFunction } from "i18next";
import {
  DeviceStatus,
  DeviceType,
  type DeviceModel,
} from "../../../../domain/models/DeviceModels";
import {
  Camera,
  Wind,
  Cpu,
  Wifi,
  WifiOff,
  AlertCircle,
  Edit,
  Activity,
  Power,
} from "lucide-react";

const DEVICE_STATUS_KEYS = {
  [DeviceStatus.ONLINE]: "devices:status.online",
  [DeviceStatus.OFFLINE]: "devices:status.offline",
  [DeviceStatus.MAINTENANCE]: "devices:status.maintenance",
  [DeviceStatus.ERROR]: "devices:status.error",
} as const;

interface DeviceCardProps {
  device: DeviceModel;
  onEdit: (device: DeviceModel) => void;
  onViewLogs: (device: DeviceModel) => void;
  onRestart: (device: DeviceModel) => void;
}

const getDeviceIcon = (type: DeviceType) => {
  switch (type) {
    case DeviceType.TRAFFIC_CAM:
      return Camera;
    case DeviceType.AIR_QUALITY_SENSOR:
      return Wind;
    default:
      return Cpu;
  }
};

const getStatusColor = (status: DeviceStatus) => {
  switch (status) {
    case DeviceStatus.ONLINE:
      return "text-green-700 bg-green-100 dark:text-green-300 dark:bg-green-900/30";
    case DeviceStatus.OFFLINE:
      return "text-red-700 bg-red-100 dark:text-red-300 dark:bg-red-900/30";
    case DeviceStatus.MAINTENANCE:
      return "text-yellow-700 bg-yellow-100 dark:text-yellow-300 dark:bg-yellow-900/30";
    case DeviceStatus.ERROR:
      return "text-red-700 bg-red-100 dark:text-red-300 dark:bg-red-900/30";
    default:
      return "text-gray-700 bg-gray-100 dark:text-gray-300 dark:bg-gray-900/30";
  }
};

const getQuickStats = (
  device: DeviceModel,
  t: TFunction<["devices", "common"]>
) => {
  // Mock data - trong thực tế sẽ lấy từ device stats
  switch (device.type) {
    case DeviceType.TRAFFIC_CAM:
      return {
        value: "35 xe/phút",
        label: t("devices:quickStats.trafficFlow"),
      };
    case DeviceType.AIR_QUALITY_SENSOR:
      return { value: "AQI: 82", label: t("devices:quickStats.aqiIndex") };
    default:
      return {
        value: t("devices:quickStats.activity"),
        label: t("devices:quickStats.activity"),
      };
  }
};

export const DeviceCard: React.FC<DeviceCardProps> = ({
  device,
  onEdit,
  onViewLogs,
  onRestart,
}) => {
  const { t } = useTranslation(["devices", "common"]);
  const Icon = getDeviceIcon(device.type);
  const statusColor = getStatusColor(device.status);
  const quickStats = getQuickStats(device, t);

  const formatLastSeen = (date?: Date) => {
    if (!date) return t("devices:noData");

    const now = new Date();
    const diff = now.getTime() - date.getTime();
    const minutes = Math.floor(diff / 60000);

    if (minutes < 1) return t("devices:justNow");
    if (minutes < 60) return t("devices:minutesAgo", { count: minutes });

    const hours = Math.floor(minutes / 60);
    if (hours < 24) return t("devices:hoursAgo", { count: hours });

    const days = Math.floor(hours / 24);
    return t("devices:daysAgo", { count: days });
  };

  return (
    <div className="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-2xl p-6 shadow-sm hover:shadow-md transition-all duration-300 cursor-pointer group">
      {/* Header with Icon and Status */}
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center gap-3">
          <div
            className={`p-3 rounded-lg transition-transform group-hover:scale-110 ${
              device.type === DeviceType.TRAFFIC_CAM
                ? "bg-blue-100 dark:bg-blue-900/30"
                : device.type === DeviceType.AIR_QUALITY_SENSOR
                ? "bg-green-100 dark:bg-green-900/30"
                : "bg-purple-100 dark:bg-purple-900/30"
            }`}
          >
            <Icon
              className={`w-6 h-6 ${
                device.type === DeviceType.TRAFFIC_CAM
                  ? "text-blue-600 dark:text-blue-400"
                  : device.type === DeviceType.AIR_QUALITY_SENSOR
                  ? "text-green-600 dark:text-green-400"
                  : "text-purple-600 dark:text-purple-400"
              }`}
            />
          </div>

          <div>
            <h3 className="font-semibold text-gray-900 dark:text-white text-lg group-hover:text-greenwave-primary-light transition-colors">
              {device.name}
            </h3>
            <p className="text-sm text-gray-500 dark:text-gray-400">
              {device.manufacturer || t("devices:unknown")} •{" "}
              {device.serialNumber}
            </p>
          </div>
        </div>

        {/* Status Indicator */}
        <div
          className={`flex items-center gap-2 px-3 py-1 rounded-full text-xs font-medium ${statusColor}`}
        >
          <div
            className={`w-2 h-2 rounded-full ${
              device.status === DeviceStatus.ONLINE ? "animate-pulse" : ""
            }`}
          />
          {t(DEVICE_STATUS_KEYS[device.status])}
        </div>
      </div>

      {/* Location */}
      <div className="mb-4 p-3 rounded-lg bg-gray-50 dark:bg-gray-700/50">
        <p className="text-sm text-gray-500 dark:text-gray-400 mb-1">
          {t("common:location")}:
        </p>
        <p className="text-sm text-gray-900 dark:text-white font-medium">
          {device.location.description ||
            `${device.location.latitude.toFixed(
              4
            )}, ${device.location.longitude.toFixed(4)}`}
        </p>
      </div>

      {/* Quick Stats */}
      <div className="mb-4">
        <div className="flex items-center justify-between p-3 rounded-lg bg-green-50 dark:bg-green-900/20 border border-green-100 dark:border-green-800/30">
          <div>
            <p className="text-xs text-gray-500 dark:text-gray-400">
              {quickStats.label}
            </p>
            <p className="text-lg font-bold text-gray-900 dark:text-white">
              {quickStats.value}
            </p>
          </div>
          <Activity className="w-5 h-5 text-green-600 dark:text-green-400" />
        </div>
      </div>

      {/* Last Seen */}
      <div className="mb-4 text-sm text-gray-500 dark:text-gray-400">
        <div className="flex items-center gap-2">
          {device.status === DeviceStatus.ONLINE ? (
            <Wifi className="w-4 h-4 text-green-500" />
          ) : (
            <WifiOff className="w-4 h-4 text-red-500" />
          )}
          <span>
            {t("devices:lastUpdate")}: {formatLastSeen(device.lastDataReceived)}
          </span>
        </div>
      </div>

      {/* Action Buttons */}
      <div className="flex gap-2">
        <button
          onClick={(e) => {
            e.stopPropagation();
            onEdit(device);
          }}
          className="flex-1 flex items-center justify-center gap-2 px-3 py-2 rounded-lg bg-blue-50 dark:bg-blue-900/20 text-blue-600 dark:text-blue-400 hover:bg-blue-100 dark:hover:bg-blue-900/40 transition-colors text-sm font-medium"
        >
          <Edit className="w-4 h-4" />
          {t("common:edit")}
        </button>

        <button
          onClick={(e) => {
            e.stopPropagation();
            onViewLogs(device);
          }}
          className="flex-1 flex items-center justify-center gap-2 px-3 py-2 rounded-lg bg-gray-50 dark:bg-gray-700/50 text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors text-sm font-medium"
        >
          <Activity className="w-4 h-4" />
          {t("devices:logs")}
        </button>

        <button
          onClick={(e) => {
            e.stopPropagation();
            onRestart(device);
          }}
          className="flex items-center justify-center px-3 py-2 rounded-lg bg-green-50 dark:bg-green-900/20 text-green-600 dark:text-green-400 hover:bg-green-100 dark:hover:bg-green-900/40 transition-colors"
          title={t("devices:restart")}
        >
          <Power className="w-4 h-4" />
        </button>
      </div>

      {/* Alert Indicator */}
      {device.status === DeviceStatus.ERROR && (
        <div className="mt-4 p-3 rounded-lg bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800">
          <div className="flex items-center gap-2 text-red-600 dark:text-red-400">
            <AlertCircle className="w-4 h-4" />
            <span className="text-sm font-medium">
              {t("devices:needsAttention")}
            </span>
          </div>
        </div>
      )}
    </div>
  );
};
