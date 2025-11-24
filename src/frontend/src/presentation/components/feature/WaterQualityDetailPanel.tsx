import React from "react";
import { Droplet, X, MapPin } from "lucide-react";
import {
  getWaterQualityColor,
  getWaterQualityText,
} from "../../utils/SensorHelpers";
import type { WaterQualityObservedModel } from "../../../domain/models/WaterQualityObservedModel";

interface WaterQualityDetailPanelProps {
  sensor: WaterQualityObservedModel;
  onClose: () => void;
}

export const WaterQualityDetailPanel: React.FC<
  WaterQualityDetailPanelProps
> = ({ sensor, onClose }) => {
  const color = getWaterQualityColor(sensor.waterQualityLevel);
  const levelText = getWaterQualityText(sensor.waterQualityLevel);

  return (
    <div className="fixed top-4 right-4 z-40 w-96 bg-white rounded-lg shadow-2xl overflow-hidden">
      <div className="p-4 bg-cyan-600 text-white flex items-center justify-between">
        <div className="flex items-center gap-3">
          <Droplet className="w-6 h-6" />
          <h3 className="font-bold text-lg">Chất lượng nước</h3>
        </div>
        <button onClick={onClose} className="hover:bg-white/20 p-1 rounded">
          <X className="w-5 h-5" />
        </button>
      </div>

      <div className="p-4 space-y-4">
        <div>
          <p className="text-sm text-gray-600 mb-1">Địa điểm</p>
          <p className="font-semibold flex items-center gap-2">
            <MapPin className="w-4 h-4 text-gray-500" />
            {sensor.areaServed || "Không rõ"}
          </p>
        </div>

        <div>
          <p className="text-sm text-gray-600 mb-2">Mức độ chất lượng</p>
          <span
            className="inline-flex items-center px-3 py-1 rounded-full text-sm font-semibold text-white"
            style={{ backgroundColor: color }}
          >
            {levelText}
          </span>
        </div>

        <div className="grid grid-cols-2 gap-3">
          {sensor.pH !== undefined && (
            <div className="bg-gray-50 p-3 rounded">
              <p className="text-xs text-gray-600">pH</p>
              <p className="text-xl font-bold text-cyan-600">
                {sensor.pH.toFixed(1)}
              </p>
            </div>
          )}
          {sensor.dissolvedOxygen !== undefined && (
            <div className="bg-gray-50 p-3 rounded">
              <p className="text-xs text-gray-600">DO</p>
              <p className="font-semibold">
                {sensor.dissolvedOxygen.toFixed(1)} mg/L
              </p>
            </div>
          )}
          {sensor.turbidity !== undefined && (
            <div className="bg-gray-50 p-3 rounded">
              <p className="text-xs text-gray-600">Độ đục</p>
              <p className="font-semibold">{sensor.turbidity.toFixed(1)} NTU</p>
            </div>
          )}
          {sensor.temperature !== undefined && (
            <div className="bg-gray-50 p-3 rounded">
              <p className="text-xs text-gray-600">Nhiệt độ</p>
              <p className="font-semibold">{sensor.temperature.toFixed(1)}°C</p>
            </div>
          )}
          {sensor.conductivity !== undefined && (
            <div className="bg-gray-50 p-3 rounded col-span-2">
              <p className="text-xs text-gray-600">Độ dẫn điện</p>
              <p className="font-semibold">
                {sensor.conductivity.toFixed(0)} µS/cm
              </p>
            </div>
          )}
          {sensor.bod !== undefined && (
            <div className="bg-gray-50 p-3 rounded">
              <p className="text-xs text-gray-600">BOD</p>
              <p className="font-semibold">{sensor.bod.toFixed(1)} mg/L</p>
            </div>
          )}
          {sensor.cod !== undefined && (
            <div className="bg-gray-50 p-3 rounded">
              <p className="text-xs text-gray-600">COD</p>
              <p className="font-semibold">{sensor.cod.toFixed(1)} mg/L</p>
            </div>
          )}
        </div>

        <div className="pt-3 border-t border-gray-200">
          <p className="text-xs text-gray-500">
            Cập nhật:{" "}
            {sensor.dateObserved?.toLocaleString("vi-VN") || "Không rõ"}
          </p>
        </div>
      </div>
    </div>
  );
};
