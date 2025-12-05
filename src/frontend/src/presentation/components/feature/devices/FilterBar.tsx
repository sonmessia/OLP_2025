import React from "react";
import {
  DeviceType,
  DeviceStatus,
} from "../../../../domain/models/DeviceModels";
import { Filter, Search, Plus } from "lucide-react";

interface DeviceFilters {
  deviceType?: DeviceType;
  status?: DeviceStatus;
  district?: string;
  search?: string;
}

interface FilterBarProps {
  filters: DeviceFilters;
  onFiltersChange: (filters: DeviceFilters) => void;
  onAddDevice: () => void;
  loading?: boolean;
}

const deviceTypes = [
  { value: "", label: "Tất cả thiết bị", icon: Filter },
  { value: DeviceType.TRAFFIC_CAM, label: "Camera Giao thông" },
  { value: DeviceType.AIR_QUALITY_SENSOR, label: "Cảm biến Không khí" },
  { value: DeviceType.SMART_LIGHT, label: "Đèn thông minh" },
  { value: DeviceType.INDUCTIVE_LOOP, label: "Cảm biến từ" },
  { value: DeviceType.RADAR_SENSOR, label: "Radar Sensor" },
];

const deviceStatuses = [
  { value: "", label: "Tất cả trạng thái" },
  { value: DeviceStatus.ONLINE, label: "Online" },
  { value: DeviceStatus.OFFLINE, label: "Offline" },
  { value: DeviceStatus.MAINTENANCE, label: "Bảo trì" },
  { value: DeviceStatus.ERROR, label: "Lỗi" },
];

const districts = [
  { value: "", label: "Tất cả quận" },
  { value: "quan1", label: "Quận 1" },
  { value: "quan3", label: "Quận 3" },
  { value: "quan5", label: "Quận 5" },
  { value: "quan7", label: "Quận 7" },
  { value: "binhthanh", label: "Quận Bình Thạnh" },
  { value: "phunhuan", label: "Quận Phú Nhuận" },
  { value: "thuduc", label: "Thủ Đức" },
];

export const FilterBar: React.FC<FilterBarProps> = ({
  filters,
  onFiltersChange,
  onAddDevice,
  loading = false,
}) => {
  const handleFilterChange = (key: keyof DeviceFilters, value: string) => {
    const newFilters = { ...filters };
    if (value === "") {
      delete newFilters[key];
    } else {
      newFilters[key] = value as any;
    }
    onFiltersChange(newFilters);
  };

  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    handleFilterChange("search", e.target.value);
  };

  const hasActiveFilters = Object.keys(filters).length > 0;

  return (
    <div className="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-2xl p-6 mb-8 shadow-sm">
      <div className="flex flex-col lg:flex-row gap-6">
        {/* Search and Add Device */}
        <div className="flex-1 flex flex-col sm:flex-row gap-4">
          {/* Search Input */}
          <div className="relative flex-1">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
            <input
              type="text"
              placeholder="Tìm kiếm thiết bị, địa chỉ..."
              value={filters.search || ""}
              onChange={handleSearchChange}
              className="w-full pl-10 pr-4 py-3 rounded-lg border border-gray-200 dark:border-gray-600 bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-greenwave-primary-light focus:border-transparent transition-all"
            />
          </div>

          {/* Add Device Button */}
          <button
            onClick={onAddDevice}
            disabled={loading}
            className="flex items-center justify-center gap-2 px-6 py-3 rounded-lg font-medium text-white transition-all duration-300 transform hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed"
            style={{
              background:
                "linear-gradient(135deg, var(--color-greenwave-primary-light) 0%, var(--color-greenwave-primary-dark) 100%)",
              boxShadow: "0 4px 15px rgba(16, 124, 65, 0.3)",
            }}
          >
            <Plus className="w-5 h-5" />
            Thêm Thiết bị
          </button>
        </div>

        {/* Filters */}
        <div className="flex flex-col sm:flex-row gap-4">
          {/* Device Type Filter */}
          <select
            value={filters.deviceType || ""}
            onChange={(e) => handleFilterChange("deviceType", e.target.value)}
            className="px-4 py-3 rounded-lg border border-gray-200 dark:border-gray-600 bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-greenwave-primary-light focus:border-transparent transition-all"
          >
            {deviceTypes.map((type) => (
              <option key={type.value} value={type.value}>
                {type.label}
              </option>
            ))}
          </select>

          {/* Status Filter */}
          <select
            value={filters.status || ""}
            onChange={(e) => handleFilterChange("status", e.target.value)}
            className="px-4 py-3 rounded-lg border border-gray-200 dark:border-gray-600 bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-greenwave-primary-light focus:border-transparent transition-all"
          >
            {deviceStatuses.map((status) => (
              <option key={status.value} value={status.value}>
                {status.label}
              </option>
            ))}
          </select>

          {/* District Filter */}
          <select
            value={filters.district || ""}
            onChange={(e) => handleFilterChange("district", e.target.value)}
            className="px-4 py-3 rounded-lg border border-gray-200 dark:border-gray-600 bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-greenwave-primary-light focus:border-transparent transition-all"
          >
            {districts.map((district) => (
              <option key={district.value} value={district.value}>
                {district.label}
              </option>
            ))}
          </select>

          {/* Clear Filters */}
          {hasActiveFilters && (
            <button
              onClick={() => onFiltersChange({})}
              className="px-4 py-3 rounded-lg border border-red-200 dark:border-red-800 bg-red-50 dark:bg-red-900/20 text-red-600 dark:text-red-400 hover:bg-red-100 dark:hover:bg-red-900/30 transition-colors"
            >
              Xóa bộ lọc
            </button>
          )}
        </div>
      </div>

      {/* Active Filters Display */}
      {hasActiveFilters && (
        <div className="mt-4 flex flex-wrap gap-2">
          {Object.entries(filters).map(([key, value]) => {
            if (!value) return null;

            let displayValue = value;
            if (key === "deviceType") {
              const type = deviceTypes.find((t) => t.value === value);
              displayValue = type?.label || value;
            } else if (key === "status") {
              const status = deviceStatuses.find((s) => s.value === value);
              displayValue = status?.label || value;
            } else if (key === "district") {
              const district = districts.find((d) => d.value === value);
              displayValue = district?.label || value;
            }

            return (
              <div
                key={key}
                className="inline-flex items-center gap-2 px-3 py-1 rounded-full text-sm bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-300 border border-green-200 dark:border-green-800"
              >
                <span className="font-medium capitalize">{key}:</span>
                <span>{displayValue}</span>
                <button
                  onClick={() =>
                    handleFilterChange(key as keyof DeviceFilters, "")
                  }
                  className="ml-1 hover:text-red-500 transition-colors"
                >
                  ×
                </button>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};
