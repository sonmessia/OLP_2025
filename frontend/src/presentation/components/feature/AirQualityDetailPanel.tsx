import React from "react";
import { Wind, X, MapPin } from "lucide-react";
import {
  getAirQualityColor,
  getAirQualityText,
} from "../../utils/SensorHelpers";
import type { AirQualityObservedModel } from "../../../domain/models/AirQualityObservedModel";

interface AirQualityDetailPanelProps {
  sensor: AirQualityObservedModel;
  onClose: () => void;
}

export const AirQualityDetailPanel: React.FC<AirQualityDetailPanelProps> = ({
  sensor,
  onClose,
}) => {
  const color = getAirQualityColor(sensor.airQualityLevel || "");
  const levelText = getAirQualityText(sensor.airQualityLevel);

  return (
    <div className="fixed top-4 right-4 z-40 w-96 bg-white rounded-lg shadow-2xl overflow-hidden">
      <div className="p-4 bg-blue-600 text-white flex items-center justify-between">
        <div className="flex items-center gap-3">
          <Wind className="w-6 h-6" />
          <h3 className="font-bold text-lg">Chất lượng không khí</h3>
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

        <div className="bg-gray-50 p-3 rounded">
          <p className="text-xs text-gray-600">Chỉ số AQI</p>
          <p className="text-2xl font-bold text-blue-600">
            {sensor.airQualityIndex || "N/A"}
          </p>
        </div>

        <div className="grid grid-cols-2 gap-3">
          {sensor.pm25 !== undefined && (
            <div className="bg-gray-50 p-3 rounded">
              <p className="text-xs text-gray-600">PM2.5</p>
              <p className="font-semibold">{sensor.pm25.toFixed(1)} µg/m³</p>
            </div>
          )}
          {sensor.pm10 !== undefined && (
            <div className="bg-gray-50 p-3 rounded">
              <p className="text-xs text-gray-600">PM10</p>
              <p className="font-semibold">{sensor.pm10.toFixed(1)} µg/m³</p>
            </div>
          )}
          {sensor.co !== undefined && (
            <div className="bg-gray-50 p-3 rounded">
              <p className="text-xs text-gray-600">CO</p>
              <p className="font-semibold">{sensor.co.toFixed(1)} ppm</p>
            </div>
          )}
          {sensor.no2 !== undefined && (
            <div className="bg-gray-50 p-3 rounded">
              <p className="text-xs text-gray-600">NO₂</p>
              <p className="font-semibold">{sensor.no2.toFixed(1)} ppb</p>
            </div>
          )}
          {sensor.o3 !== undefined && (
            <div className="bg-gray-50 p-3 rounded">
              <p className="text-xs text-gray-600">O₃</p>
              <p className="font-semibold">{sensor.o3.toFixed(1)} ppb</p>
            </div>
          )}
          {sensor.temperature !== undefined && (
            <div className="bg-gray-50 p-3 rounded">
              <p className="text-xs text-gray-600">Nhiệt độ</p>
              <p className="font-semibold">{sensor.temperature.toFixed(1)}°C</p>
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
