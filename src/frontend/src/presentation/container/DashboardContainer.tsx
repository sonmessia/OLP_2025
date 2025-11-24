// src/presentation/containers/DashboardContainer.tsx
import React, { useState, useEffect } from "react";
import { useSensors } from "../hooks/useSensors";
import { MapView } from "../components/feature/MapView";

import type { NotificationModel } from "../../domain/models/NotificationModel";
import type { SensorModel } from "../../domain/models/SenSorModel";
import { SensorType } from "../../domain/models/SenSorModel";
import { RefreshCw } from "lucide-react";
import { AirQualityDetailPanel } from "../components/feature/AirQualityDetailPanel";
import { NotificationPanel } from "../components/feature/NotificationPanel";
import { WaterQualityDetailPanel } from "../components/feature/WaterQualityDetailPanel";

export const DashboardContainer: React.FC = () => {
  const {
    sensors,
    selectedSensor,
    loading,
    error,
    handleRefresh,
    selectSensor,
    dismissError,
  } = useSensors();

  const [notifications, setNotifications] = useState<NotificationModel[]>([]);

  // Handle errors with notifications
  useEffect(() => {
    if (error) {
      const notification: NotificationModel = {
        id: `error-${Date.now()}`,
        type: "error",
        message: error,
        timestamp: new Date(),
      };
      setNotifications((prev) => [...prev, notification]);
      dismissError();
    }
  }, [error, dismissError]);

  const handleSensorClick = (sensor: SensorModel) => {
    selectSensor(sensor);
  };

  const handleCloseDetail = () => {
    selectSensor(null);
  };

  const onRefresh = async () => {
    const notification: NotificationModel = {
      id: `info-${Date.now()}`,
      type: "info",
      message: "Đang làm mới dữ liệu...",
      timestamp: new Date(),
    };
    setNotifications((prev) => [...prev, notification]);

    const result = await handleRefresh();

    if (result.success) {
      const successNotif: NotificationModel = {
        id: `success-${Date.now()}`,
        type: "success",
        message: "Dữ liệu đã được cập nhật thành công",
        timestamp: new Date(),
      };
      setNotifications((prev) => [...prev, successNotif]);
    }
  };

  const handleDismissNotification = (id: string) => {
    setNotifications((prev) => prev.filter((n) => n.id !== id));
  };

  return (
    <div className="relative w-screen h-screen overflow-hidden">
      {/* Header */}
      <div className="absolute top-0 left-0 right-0 z-30 bg-white shadow-md">
        <div className="px-6 py-4 flex items-center justify-between">
          <h1 className="text-2xl font-bold text-gray-800">
            Giám sát Chất lượng Môi trường
          </h1>
          <button
            onClick={onRefresh}
            disabled={loading}
            className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            <RefreshCw className={`w-4 h-4 ${loading ? "animate-spin" : ""}`} />
            <span>Làm mới</span>
          </button>
        </div>
      </div>

      {/* Map */}
      <div className="absolute inset-0 pt-[72px]">
        <MapView sensors={sensors} onSensorClick={handleSensorClick} />
      </div>

      {/* Notifications */}
      <NotificationPanel
        notifications={notifications}
        onDismiss={handleDismissNotification}
      />

      {/* Detail Panels */}
      {selectedSensor && selectedSensor.type === SensorType.AIR_QUALITY && (
        <AirQualityDetailPanel
          sensor={selectedSensor}
          onClose={handleCloseDetail}
        />
      )}

      {selectedSensor && selectedSensor.type === SensorType.WATER_QUALITY && (
        <WaterQualityDetailPanel
          sensor={selectedSensor}
          onClose={handleCloseDetail}
        />
      )}

      {/* Loading Overlay */}
      {loading && (
        <div className="absolute inset-0 bg-black/20 flex items-center justify-center z-50 pointer-events-none">
          <div className="bg-white px-6 py-4 rounded-lg shadow-xl flex items-center gap-3">
            <RefreshCw className="w-5 h-5 animate-spin text-blue-600" />
            <span className="font-semibold">Đang tải dữ liệu...</span>
          </div>
        </div>
      )}

      {/* Stats Bar */}
      <div className="absolute bottom-6 right-6 bg-white rounded-lg shadow-lg p-4 z-10">
        <div className="text-sm space-y-1">
          <div className="flex items-center justify-between gap-4">
            <span className="text-gray-600">Tổng số cảm biến:</span>
            <span className="font-bold text-blue-600">{sensors.length}</span>
          </div>
          <div className="flex items-center justify-between gap-4">
            <span className="text-gray-600">Không khí:</span>
            <span className="font-semibold">
              {sensors.filter((s) => s.type === SensorType.AIR_QUALITY).length}
            </span>
          </div>
          <div className="flex items-center justify-between gap-4">
            <span className="text-gray-600">Nước:</span>
            <span className="font-semibold">
              {
                sensors.filter((s) => s.type === SensorType.WATER_QUALITY)
                  .length
              }
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};
