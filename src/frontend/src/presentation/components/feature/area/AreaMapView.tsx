// Copyright (c) 2025 Green Wave Team
// 
// This software is released under the MIT License.
// https://opensource.org/licenses/MIT

import React, { useEffect, useRef } from "react";
import L from "leaflet";
import "leaflet/dist/leaflet.css";

interface AreaMapViewProps {
  latitude: number;
  longitude: number;
  areaName: string;
  isDarkMode: boolean;
}

export const AreaMapView: React.FC<AreaMapViewProps> = ({
  latitude,
  longitude,
  areaName,
  isDarkMode,
}) => {
  const mapRef = useRef<HTMLDivElement>(null);
  const mapRefInstance = useRef<L.Map | null>(null);
  const markerRef = useRef<L.Marker | null>(null);

  // Initialize map
  useEffect(() => {
    if (!mapRef.current || mapRefInstance.current) return;

    const map = L.map(mapRef.current, {
      center: [latitude, longitude],
      zoom: 16,
      zoomControl: true,
    });

    mapRefInstance.current = map;

    return () => {
      if (mapRefInstance.current) {
        mapRefInstance.current.remove();
        mapRefInstance.current = null;
      }
    };
  }, [latitude, longitude]);

  // Update tile layer and view
  useEffect(() => {
    if (!mapRefInstance.current) return;

    const map = mapRefInstance.current;

    // Update view
    map.setView([latitude, longitude], 16);

    // Remove existing tile layers
    map.eachLayer((layer) => {
      if (layer instanceof L.TileLayer) {
        map.removeLayer(layer);
      }
    });

    // Add new tile layer
    const tileUrl = isDarkMode
      ? "https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
      : "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png";

    L.tileLayer(tileUrl, {
      attribution:
        '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
      maxZoom: 19,
    }).addTo(map);

    // Update marker
    if (markerRef.current) {
      map.removeLayer(markerRef.current);
    }

    const customIcon = L.divIcon({
      html: `
        <div style="
          background-color: #10B981;
          width: 24px;
          height: 24px;
          border-radius: 50%;
          border: 3px solid white;
          box-shadow: 0 2px 6px rgba(0,0,0,0.3);
          display: flex;
          align-items: center;
          justify-content: center;
        ">
          <div style="width: 8px; height: 8px; background-color: white; border-radius: 50%;"></div>
        </div>
      `,
      className: "custom-area-marker",
      iconSize: [24, 24],
      iconAnchor: [12, 12],
    });

    markerRef.current = L.marker([latitude, longitude], { icon: customIcon })
      .addTo(map)
      .bindPopup(`<b>${areaName}</b>`)
      .openPopup();
  }, [latitude, longitude, areaName, isDarkMode]);

  return <div ref={mapRef} className="w-full h-full rounded-xl z-0" />;
};
