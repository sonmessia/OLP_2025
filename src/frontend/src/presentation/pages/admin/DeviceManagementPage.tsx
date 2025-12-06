// Copyright (c) 2025 Green Wave Team
// 
// This software is released under the MIT License.
// https://opensource.org/licenses/MIT

import React, { useState, useEffect } from "react";
import { useTranslation } from "react-i18next";
import {
  DeviceType,
  DeviceStatus,
  DeviceFactory,
} from "../../../domain/models/DeviceModels";
import type { DeviceModel } from "../../../domain/models/DeviceModels";
import { DashboardHeader } from "../../components/feature/dashboard/DashboardHeader";
import {
  FilterBar,
  DeviceCard,
  DeviceWizard,
} from "../../components/feature/devices";
import { Plus, Map, WifiOff } from "lucide-react";

interface DeviceFilters {
  deviceType?: DeviceType;
  status?: DeviceStatus;
  district?: string;
  search?: string;
}

export const DeviceManagementPage: React.FC = () => {
  const { t } = useTranslation(["devices", "common"]);

  // Initialize dark mode from localStorage or system preference
  const getInitialDarkMode = () => {
    if (typeof window !== "undefined") {
      const stored = localStorage.getItem("darkMode");
      if (stored !== null) {
        return stored === "true";
      }
      return window.matchMedia("(prefers-color-scheme: dark)").matches;
    }
    return false;
  };

  const [isDarkMode, setIsDarkMode] = useState(getInitialDarkMode);
  const [devices, setDevices] = useState<DeviceModel[]>([]);
  const [filteredDevices, setFilteredDevices] = useState<DeviceModel[]>([]);
  const [filters, setFilters] = useState<DeviceFilters>({});
  const [loading, setLoading] = useState(true);
  const [isWizardOpen, setIsWizardOpen] = useState(false);
  const [editingDevice, setEditingDevice] = useState<DeviceModel | undefined>();

  // Apply dark mode class on mount and change
  useEffect(() => {
    if (isDarkMode) {
      document.documentElement.classList.add("dark");
    } else {
      document.documentElement.classList.remove("dark");
    }
  }, [isDarkMode]);

  const handleThemeToggle = () => {
    const newDarkMode = !isDarkMode;
    setIsDarkMode(newDarkMode);
    localStorage.setItem("darkMode", newDarkMode.toString());
  };

  // Mock data for demonstration
  useEffect(() => {
    const mockDevices: DeviceModel[] = [
      DeviceFactory.createTrafficCamera({
        id: "1",
        name: "Camera Ngã 4 Hàng Xanh",
        serialNumber: "SN-2024-CAM-001",
        manufacturer: "Bosch",
        location: {
          latitude: 10.8231,
          longitude: 106.6297,
          description: "Cột đèn số 5, hướng về Quận 1",
        },
        status: DeviceStatus.ONLINE,
        httpConfig: {
          ipAddress: "192.168.1.105",
          apiEndpoint: "/api/v1/stream",
        },
        lastDataReceived: new Date(),
        createdAt: new Date("2024-01-15"),
        updatedAt: new Date(),
      }),
      DeviceFactory.createAirQualitySensor({
        id: "2",
        name: "Trạm quan trắc không khí Quận 1",
        serialNumber: "SN-2024-AQ-002",
        manufacturer: "Honeywell",
        location: {
          latitude: 10.815,
          longitude: 106.63,
          description: "Trụ sở UBND Quận 1",
        },
        status: DeviceStatus.ONLINE,
        mqttConfig: {
          topicSubscribe: "hcm/q1/airquality/data",
          brokerUrl: "mqtt://broker.hivemq.com",
          port: 1883,
        },
        lastDataReceived: new Date(),
        createdAt: new Date("2024-02-01"),
        updatedAt: new Date(),
      }),
      DeviceFactory.createSmartLight({
        id: "3",
        name: "Đèn thông minh Ngã Tư Thủ Đức",
        serialNumber: "SN-2024-LIGHT-003",
        manufacturer: "Philips",
        location: {
          latitude: 10.85,
          longitude: 106.75,
          description: "Ngã Tư Thủ Đức",
        },
        status: DeviceStatus.MAINTENANCE,
        mqttConfig: {
          topicSubscribe: "hcm/thuduc/light/data",
          topicPublish: "hcm/thuduc/light/cmd",
        },
        lastDataReceived: new Date(Date.now() - 3600000),
        createdAt: new Date("2024-01-20"),
        updatedAt: new Date(),
      }),
    ];

    setDevices(mockDevices);
    setLoading(false);
  }, []);

  // Filter devices based on current filters
  useEffect(() => {
    let filtered = devices;

    if (filters.search) {
      filtered = filtered.filter(
        (device) =>
          device.name.toLowerCase().includes(filters.search!.toLowerCase()) ||
          device.serialNumber
            .toLowerCase()
            .includes(filters.search!.toLowerCase()) ||
          device.location.description
            ?.toLowerCase()
            .includes(filters.search!.toLowerCase())
      );
    }

    if (filters.deviceType) {
      filtered = filtered.filter(
        (device) => device.type === filters.deviceType
      );
    }

    if (filters.status) {
      filtered = filtered.filter((device) => device.status === filters.status);
    }

    if (filters.district) {
      // Simple district matching based on location description
      filtered = filtered.filter((device) => {
        const description = device.location.description?.toLowerCase() || "";
        return description.includes(
          filters.district!.replace("quan", "quận").replace("thuduc", "thủ đức")
        );
      });
    }

    setFilteredDevices(filtered);
  }, [devices, filters]);

  const handleAddDevice = () => {
    setEditingDevice(undefined);
    setIsWizardOpen(true);
  };

  const handleEditDevice = (device: DeviceModel) => {
    setEditingDevice(device);
    setIsWizardOpen(true);
  };

  const handleViewLogs = (device: DeviceModel) => {
    // TODO: Navigate to device logs page
    console.log("View logs for device:", device.name);
  };

  const handleRestartDevice = (device: DeviceModel) => {
    // TODO: Implement device restart
    console.log("Restart device:", device.name);
  };

  const handleDeviceSubmit = (device: DeviceModel) => {
    if (editingDevice) {
      // Update existing device
      setDevices((prev) => prev.map((d) => (d.id === device.id ? device : d)));
    } else {
      // Add new device
      setDevices((prev) => [...prev, device]);
    }
    setIsWizardOpen(false);
    setEditingDevice(undefined);
  };

  // Calculate statistics
  const stats = {
    total: devices.length,
    online: devices.filter((d) => d.status === DeviceStatus.ONLINE).length,
    offline: devices.filter((d) => d.status === DeviceStatus.OFFLINE).length,
    maintenance: devices.filter((d) => d.status === DeviceStatus.MAINTENANCE)
      .length,
    error: devices.filter((d) => d.status === DeviceStatus.ERROR).length,
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900 flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-500"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 transition-colors duration-300">
      <DashboardHeader
        onThemeToggle={handleThemeToggle}
        isDarkMode={isDarkMode}
      />

      <div className="container mx-auto px-6 py-8">
        {/* Page Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h1 className="text-4xl font-bold text-text-main mb-2">
                {t("devices:management.title")}
              </h1>
              <p className="text-lg text-text-muted">
                {t("devices:management.subtitle")}
              </p>
            </div>
            <button
              onClick={handleAddDevice}
              className="flex items-center gap-3 px-6 py-4 rounded-2xl font-medium text-white transition-all duration-300 transform hover:scale-105 hover:shadow-xl"
              style={{
                background:
                  "linear-gradient(135deg, var(--color-greenwave-primary-light) 0%, var(--color-greenwave-primary-dark) 100%)",
                boxShadow: "0 8px 32px rgba(16, 124, 65, 0.3)",
              }}
            >
              <Plus className="w-6 h-6" />
              {t("devices:management.addNew")}
            </button>
          </div>

          {/* Statistics Cards */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-6 mb-8">
            <div className="glass-card p-6 rounded-2xl text-center bg-white/50 dark:bg-gray-800/50">
              <div className="text-3xl font-bold text-text-main mb-2">
                {stats.total}
              </div>
              <div className="text-sm text-text-muted">
                {t("devices:management.total")}
              </div>
            </div>

            <div className="glass-card p-6 rounded-2xl text-center bg-green-50/50 dark:bg-green-900/20 border-green-200 dark:border-green-800">
              <div className="flex items-center justify-center gap-2 mb-2">
                <div className="w-3 h-3 rounded-full bg-green-500"></div>
                <div className="text-3xl font-bold text-green-600 dark:text-green-400">
                  {stats.online}
                </div>
              </div>
              <div className="text-sm text-text-muted">
                {t("devices:status.online")}
              </div>
            </div>

            <div className="glass-card p-6 rounded-2xl text-center bg-red-50/50 dark:bg-red-900/20 border-red-200 dark:border-red-800">
              <div className="flex items-center justify-center gap-2 mb-2">
                <div className="w-3 h-3 rounded-full bg-red-500"></div>
                <div className="text-3xl font-bold text-red-600 dark:text-red-400">
                  {stats.offline}
                </div>
              </div>
              <div className="text-sm text-text-muted">
                {t("devices:status.offline")}
              </div>
            </div>

            <div className="glass-card p-6 rounded-2xl text-center bg-yellow-50/50 dark:bg-yellow-900/20 border-yellow-200 dark:border-yellow-800">
              <div className="flex items-center justify-center gap-2 mb-2">
                <div className="w-3 h-3 rounded-full bg-yellow-500"></div>
                <div className="text-3xl font-bold text-yellow-600 dark:text-yellow-400">
                  {stats.maintenance}
                </div>
              </div>
              <div className="text-sm text-text-muted">
                {t("devices:status.maintenance")}
              </div>
            </div>

            <div className="glass-card p-6 rounded-2xl text-center bg-red-50/50 dark:bg-red-900/20 border-red-200 dark:border-red-800">
              <div className="flex items-center justify-center gap-2 mb-2">
                <div className="w-3 h-3 rounded-full bg-red-600"></div>
                <div className="text-3xl font-bold text-red-700 dark:text-red-500">
                  {stats.error}
                </div>
              </div>
              <div className="text-sm text-text-muted">
                {t("devices:status.error")}
              </div>
            </div>
          </div>
        </div>

        {/* Filter Bar */}
        <FilterBar
          filters={filters}
          onFiltersChange={setFilters}
          onAddDevice={handleAddDevice}
          loading={loading}
        />

        {/* Results Summary */}
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center gap-4">
            <h2 className="text-xl font-semibold text-text-main">
              {t("devices:management.listTitle")} ({filteredDevices.length})
            </h2>
            {Object.keys(filters).length > 0 && (
              <span className="text-sm text-text-muted">
                {t("devices:management.filtering")}
              </span>
            )}
          </div>

          <div className="flex items-center gap-3">
            <button className="flex items-center gap-2 px-4 py-2 rounded-lg border border-greenwave-primary-light/20 bg-greenwave-accent-light/50 dark:bg-greenwave-accent-dark/50 text-text-main hover:bg-greenwave-accent-light/70 transition-colors">
              <Map className="w-4 h-4" />
              {t("devices:management.viewMap")}
            </button>
          </div>
        </div>

        {/* Device Grid */}
        {filteredDevices.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {filteredDevices.map((device) => (
              <DeviceCard
                key={device.id}
                device={device}
                onEdit={handleEditDevice}
                onViewLogs={handleViewLogs}
                onRestart={handleRestartDevice}
              />
            ))}
          </div>
        ) : (
          <div className="text-center py-16">
            <div className="glass-card p-12 rounded-3xl max-w-md mx-auto bg-white/5 dark:bg-white/5">
              <div className="w-20 h-20 mx-auto mb-6 rounded-full bg-gray-100 dark:bg-gray-800 flex items-center justify-center">
                <WifiOff className="w-10 h-10 text-gray-400" />
              </div>
              <h3 className="text-xl font-semibold text-text-main mb-2">
                {t("devices:management.notFound")}
              </h3>
              <p className="text-text-muted mb-6">
                {Object.keys(filters).length > 0
                  ? t("devices:management.adjustFilter")
                  : t("devices:management.noDevices")}
              </p>
              {Object.keys(filters).length > 0 ? (
                <button
                  onClick={() => setFilters({})}
                  className="px-6 py-3 rounded-lg border border-gray-300 dark:border-gray-600 text-text-main hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
                >
                  {t("devices:management.clearFilters")}
                </button>
              ) : (
                <button
                  onClick={handleAddDevice}
                  className="px-6 py-3 rounded-lg font-medium text-white transition-colors"
                  style={{
                    background:
                      "linear-gradient(135deg, var(--color-greenwave-primary-light) 0%, var(--color-greenwave-primary-dark) 100%)",
                  }}
                >
                  {t("devices:management.addFirst")}
                </button>
              )}
            </div>
          </div>
        )}
      </div>

      {/* Device Wizard Modal */}
      <DeviceWizard
        isOpen={isWizardOpen}
        onClose={() => {
          setIsWizardOpen(false);
          setEditingDevice(undefined);
        }}
        onSubmit={handleDeviceSubmit}
        editingDevice={editingDevice}
      />
    </div>
  );
};
