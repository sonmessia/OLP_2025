import React, { useState, useEffect } from "react";
import type { PollutionHotspot } from "../../../../domain/models/DashboardModel";
import { Settings, Zap, Save } from "lucide-react";

interface ManualControlPanelProps {
  selectedSensor: PollutionHotspot | null;
}

export const ManualControlPanel: React.FC<ManualControlPanelProps> = ({
  selectedSensor,
}) => {
  const [greenLight, setGreenLight] = useState(30);
  const [yellowLight, setYellowLight] = useState(3);
  const [redLight, setRedLight] = useState(25);
  const [isApplying, setIsApplying] = useState(false);

  // Reset form when sensor changes
  useEffect(() => {
    if (selectedSensor) {
      // In a real app, we would fetch the current configuration for this sensor
      // For now, we'll just reset to defaults or random values to simulate fetching
      setGreenLight(30);
      setYellowLight(3);
      setRedLight(25);
    }
  }, [selectedSensor]);

  const handleApply = () => {
    if (!selectedSensor) return;
    setIsApplying(true);
    // Simulate API call
    setTimeout(() => {
      setIsApplying(false);
      alert(`Đã cập nhật cấu hình cho ${selectedSensor.name}`);
    }, 1000);
  };

  const handleImmediateSwitch = () => {
    if (!selectedSensor) return;
    // Simulate immediate command
    alert(`Đã gửi lệnh chuyển đèn ngay lập tức cho ${selectedSensor.name}`);
  };

  if (!selectedSensor) {
    return (
      <div className="bg-white dark:bg-gray-800 rounded-xl border-2 border-gray-200 dark:border-gray-700 p-6 h-full flex flex-col items-center justify-center text-center">
        <div className="w-16 h-16 bg-gray-100 dark:bg-gray-700 rounded-full flex items-center justify-center mb-4">
          <Settings className="w-8 h-8 text-gray-400" />
        </div>
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
          Chưa chọn thiết bị
        </h3>
        <p className="text-gray-500 dark:text-gray-400 max-w-xs">
          Vui lòng chọn một điểm giám sát trên bản đồ để truy cập bảng điều
          khiển thủ công.
        </p>
      </div>
    );
  }

  return (
    <div className="bg-white dark:bg-gray-800 rounded-xl border-2 border-gray-200 dark:border-gray-700 p-4 h-full flex flex-col">
      <div className="flex items-center justify-between mb-4 pb-4 border-b border-gray-100 dark:border-gray-700">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
            <Settings className="w-5 h-5 text-blue-600 dark:text-blue-400" />
          </div>
          <div>
            <h3 className="font-bold text-gray-900 dark:text-white">
              Điều khiển thủ công
            </h3>
            <p className="text-xs text-gray-500 dark:text-gray-400">
              {selectedSensor.name}
            </p>
          </div>
        </div>
        <div className="px-2 py-1 bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-400 text-xs font-medium rounded-full flex items-center gap-1">
          <span className="w-1.5 h-1.5 bg-green-500 rounded-full animate-pulse"></span>
          Online
        </div>
      </div>

      <div className="flex-1 space-y-4 overflow-y-auto">
        {/* Traffic Light Timing Configuration */}
        <div className="space-y-3">
          <h4 className="text-sm font-semibold text-gray-700 dark:text-gray-300 flex items-center gap-2">
            <ClockIcon className="w-4 h-4" />
            Cấu hình thời gian (giây)
          </h4>

          <div className="grid grid-cols-3 gap-3">
            <div className="space-y-1">
              <label className="text-xs font-medium text-green-600 dark:text-green-400">
                Đèn Xanh
              </label>
              <input
                type="number"
                value={greenLight}
                onChange={(e) => setGreenLight(Number(e.target.value))}
                className="w-full px-3 py-2 border border-gray-200 dark:border-gray-600 rounded-lg bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-green-500 outline-none transition-all"
              />
            </div>
            <div className="space-y-1">
              <label className="text-xs font-medium text-yellow-600 dark:text-yellow-400">
                Đèn Vàng
              </label>
              <input
                type="number"
                value={yellowLight}
                onChange={(e) => setYellowLight(Number(e.target.value))}
                className="w-full px-3 py-2 border border-gray-200 dark:border-gray-600 rounded-lg bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-yellow-500 outline-none transition-all"
              />
            </div>
            <div className="space-y-1">
              <label className="text-xs font-medium text-red-600 dark:text-red-400">
                Đèn Đỏ
              </label>
              <input
                type="number"
                value={redLight}
                onChange={(e) => setRedLight(Number(e.target.value))}
                className="w-full px-3 py-2 border border-gray-200 dark:border-gray-600 rounded-lg bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-red-500 outline-none transition-all"
              />
            </div>
          </div>
        </div>

        {/* Current Status Info */}
        <div className="p-3 bg-gray-50 dark:bg-gray-700/50 rounded-lg border border-gray-100 dark:border-gray-700">
          <h4 className="text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase mb-2">
            Thông tin cảm biến
          </h4>
          <div className="grid grid-cols-2 gap-2 text-sm">
            <div className="flex justify-between">
              <span className="text-gray-600 dark:text-gray-400">PM2.5:</span>
              <span className="font-medium text-gray-900 dark:text-white">
                {selectedSensor.pm25} μg/m³
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600 dark:text-gray-400">AQI:</span>
              <span className="font-medium text-gray-900 dark:text-white">
                {selectedSensor.aqi}
              </span>
            </div>
          </div>
        </div>
      </div>

      <div className="mt-4 pt-4 border-t border-gray-100 dark:border-gray-700 grid grid-cols-2 gap-3">
        <button
          onClick={handleApply}
          disabled={isApplying}
          className="flex items-center justify-center gap-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {isApplying ? (
            <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
          ) : (
            <Save className="w-4 h-4" />
          )}
          Lưu cấu hình
        </button>
        <button
          onClick={handleImmediateSwitch}
          className="flex items-center justify-center gap-2 px-4 py-2 bg-amber-500 hover:bg-amber-600 text-white rounded-lg font-medium transition-colors"
        >
          <Zap className="w-4 h-4" />
          Chuyển đèn ngay
        </button>
      </div>
    </div>
  );
};

// Helper icon
const ClockIcon = ({ className }: { className?: string }) => (
  <svg
    className={className}
    fill="none"
    stroke="currentColor"
    viewBox="0 0 24 24"
  >
    <path
      strokeLinecap="round"
      strokeLinejoin="round"
      strokeWidth={2}
      d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
    />
  </svg>
);
