// src/presentation/components/MapView.tsx
import React, { useEffect, useRef, useState } from "react";
import maplibregl from "maplibre-gl";
import "maplibre-gl/dist/maplibre-gl.css";
import {
  SensorType,
  type SensorModel,
} from "../../../domain/models/SenSorModel";
import {
  getAirQualityColor,
  getWaterQualityColor,
} from "../../utils/SensorHelpers";
import { MAPTILER_API_KEY } from "../../../app/config/maptilerConfig";

interface MapViewProps {
  sensors: SensorModel[];
  onSensorClick: (sensor: SensorModel) => void;
}

const MAPTILER_KEY = MAPTILER_API_KEY;

export const MapView: React.FC<MapViewProps> = ({ sensors, onSensorClick }) => {
  const mapContainer = useRef<HTMLDivElement>(null);
  const map = useRef<maplibregl.Map | null>(null);
  const markers = useRef<maplibregl.Marker[]>([]);
  const [mapLoaded, setMapLoaded] = useState(false);

  // Initialize map
  useEffect(() => {
    if (!mapContainer.current || map.current) return;

    map.current = new maplibregl.Map({
      container: mapContainer.current,
      style: `https://api.maptiler.com/maps/streets-v2/style.json?key=${MAPTILER_KEY}`,
      center: [106.6297, 10.8231],
      zoom: 11,
    });

    map.current.on("load", () => {
      setMapLoaded(true);
    });

    return () => {
      markers.current.forEach((marker) => marker.remove());
      map.current?.remove();
      map.current = null;
    };
  }, []);

  // Update markers when sensors change
  useEffect(() => {
    if (!map.current || !mapLoaded) return;

    markers.current.forEach((marker) => marker.remove());
    markers.current = [];

    sensors.forEach((sensor) => {
      if (!sensor.location) return;

      const [lng, lat] = sensor.location.coordinates;

      let markerColor = "#6b7280";
      if (sensor.type === SensorType.AIR_QUALITY) {
        const airSensor = sensor;
        markerColor = getAirQualityColor(airSensor.airQualityLevel || "");
      } else if (sensor.type === SensorType.WATER_QUALITY) {
        const waterSensor = sensor;
        markerColor = getWaterQualityColor(waterSensor.waterQualityLevel);
      }

      const el = document.createElement("div");
      el.className = "custom-marker";
      el.style.width = "24px";
      el.style.height = "24px";
      el.style.borderRadius = "50%";
      el.style.backgroundColor = markerColor;
      el.style.border = "3px solid white";
      el.style.boxShadow = "0 2px 4px rgba(0,0,0,0.3)";
      el.style.cursor = "pointer";
      el.style.transition = "transform 0.2s";

      el.addEventListener("mouseenter", () => {
        el.style.transform = "scale(1.3)";
      });

      el.addEventListener("mouseleave", () => {
        el.style.transform = "scale(1)";
      });

      el.addEventListener("click", () => {
        onSensorClick(sensor);
      });

      const marker = new maplibregl.Marker({ element: el })
        .setLngLat([lng, lat])
        .addTo(map.current!);

      markers.current.push(marker);
    });
  }, [sensors, mapLoaded, onSensorClick]);

  return (
    <div className="relative w-full h-full">
      <div ref={mapContainer} className="w-full h-full" />

      <div className="absolute bottom-6 left-6 bg-white rounded-lg shadow-lg p-4 z-10">
        <h4 className="font-semibold text-sm mb-2">Chất lượng môi trường</h4>
        <div className="space-y-1 text-xs">
          <div className="flex items-center gap-2">
            <div
              className="w-4 h-4 rounded-full"
              style={{ backgroundColor: "#10b981" }}
            ></div>
            <span>Tốt</span>
          </div>
          <div className="flex items-center gap-2">
            <div
              className="w-4 h-4 rounded-full"
              style={{ backgroundColor: "#f59e0b" }}
            ></div>
            <span>Trung bình</span>
          </div>
          <div className="flex items-center gap-2">
            <div
              className="w-4 h-4 rounded-full"
              style={{ backgroundColor: "#ef4444" }}
            ></div>
            <span>Không tốt</span>
          </div>
          <div className="flex items-center gap-2">
            <div
              className="w-4 h-4 rounded-full"
              style={{ backgroundColor: "#991b1b" }}
            ></div>
            <span>Nguy hại</span>
          </div>
        </div>
      </div>
    </div>
  );
};
