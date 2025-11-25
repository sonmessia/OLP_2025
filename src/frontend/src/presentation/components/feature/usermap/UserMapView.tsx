import React, { useEffect, useRef } from "react";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import type { AirQualityObservedModel } from "../../../../domain/models/AirQualityObservedModel";
import type { LocationModel } from "../../../../domain/models/CommonModels";
import { GeoJSONType } from "../../../../domain/models/CommonModels";

interface UserMapViewProps {
  isDarkMode: boolean;
  airQualityData: AirQualityObservedModel[];
  selectedLocation: LocationModel | null;
  onLocationSelect: (
    location: LocationModel,
    airQuality?: AirQualityObservedModel
  ) => void;
  searchQuery: string;
}

// Custom icons for different AQI levels
const getAQIIcon = (aqi: number): L.DivIcon => {
  let color = "#10B981"; // Green for good
  if (aqi > 150) color = "#D9232F"; // Red for hazardous
  else if (aqi > 100) color = "#F59E0B"; // Orange for unhealthy
  else if (aqi > 50) color = "#FBBF24"; // Yellow for moderate

  return L.divIcon({
    html: `
      <div style="
        background-color: ${color};
        width: 24px;
        height: 24px;
        border-radius: 50%;
        border: 3px solid white;
        box-shadow: 0 2px 6px rgba(0,0,0,0.3);
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: bold;
        font-size: 10px;
      ">
        ${aqi}
      </div>
    `,
    className: "custom-aqi-marker",
    iconSize: [30, 30],
    iconAnchor: [15, 15],
  });
};

export const UserMapView: React.FC<UserMapViewProps> = ({
  isDarkMode,
  airQualityData,
  onLocationSelect,
  searchQuery,
}) => {
  const mapRef = useRef<HTMLDivElement>(null);
  const mapRefInstance = useRef<L.Map | null>(null);
  const markersRef = useRef<L.Layer[]>([]);
  const heatLayerRef = useRef<L.Layer | null>(null);

  // Initialize map
  useEffect(() => {
    if (!mapRef.current || mapRefInstance.current) return;

    // Initialize map centered on Ho Chi Minh City
    const map = L.map(mapRef.current, {
      center: [10.8231, 106.6297], // HCMC coordinates
      zoom: 12,
      zoomControl: true,
    });

    // Add tile layer based on theme
    const tileUrl = isDarkMode
      ? "https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
      : "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png";

    const tileLayer = L.tileLayer(tileUrl, {
      attribution:
        '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
      subdomains: "abcd",
      maxZoom: 19,
    });

    tileLayer.addTo(map);
    mapRefInstance.current = map;

    // Add click handler for map
    map.on("click", (e: L.LeafletMouseEvent) => {
      const location: LocationModel = {
        type: GeoJSONType.Point,
        coordinates: [e.latlng.lng, e.latlng.lat],
      };
      onLocationSelect(location);
    });

    return () => {
      if (mapRefInstance.current) {
        mapRefInstance.current.remove();
        mapRefInstance.current = null;
      }
    };
  }, []);

  // Update tile layer when theme changes
  useEffect(() => {
    if (!mapRefInstance.current) return;

    const map = mapRefInstance.current;

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

    const tileLayer = L.tileLayer(tileUrl, {
      attribution:
        '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
      subdomains: "abcd",
      maxZoom: 19,
    });

    tileLayer.addTo(map);
  }, [isDarkMode]);

  // Create heatmap layer
  const createHeatmapLayer = (data: AirQualityObservedModel[]): L.Layer => {
    const heatData: [number, number, number][] = data
      .filter((item) => item.location && item.airQualityIndex)
      .map((item) => [
        item.location!.coordinates[1], // latitude
        item.location!.coordinates[0], // longitude
        Math.min(item.airQualityIndex! / 200, 1), // intensity (normalized)
      ]);

    // Create a simple circle-based heatmap since we don't have leaflet.heat
    const heatGroup = L.layerGroup();

    heatData.forEach(([lat, lng, intensity]) => {
      const radius = 1000 + intensity * 2000; // 1-3km radius
      let color = "rgba(16, 185, 129, "; // Green
      if (intensity > 0.75) color = "rgba(217, 35, 47, "; // Red
      else if (intensity > 0.5) color = "rgba(251, 191, 36, "; // Yellow

      const circle = L.circle([lat, lng], {
        radius: radius,
        fillColor: color + intensity * 0.3 + ")",
        fillOpacity: 0.3,
        stroke: false,
      });

      heatGroup.addLayer(circle);
    });

    return heatGroup;
  };

  // Update air quality markers and heatmap
  useEffect(() => {
    if (!mapRefInstance.current) return;

    const map = mapRefInstance.current;

    // Clear existing markers
    markersRef.current.forEach((marker) => {
      map.removeLayer(marker);
    });
    markersRef.current = [];

    // Remove existing heatmap
    if (heatLayerRef.current) {
      map.removeLayer(heatLayerRef.current);
    }

    // Add new heatmap layer
    heatLayerRef.current = createHeatmapLayer(airQualityData);
    heatLayerRef.current.addTo(map);

    // Add markers for air quality data points
    airQualityData.forEach((data) => {
      if (!data.location) return;

      const [lng, lat] = data.location.coordinates;
      const marker = L.marker([lat, lng], {
        icon: getAQIIcon(data.airQualityIndex || 0),
      });

      // Create popup content
      const popupContent = `
        <div class="p-3 min-w-[200px]">
          <h3 class="font-bold text-lg mb-2">${data.areaServed || "Vị trí"}</h3>
          <div class="space-y-1">
            <p><strong>AQI:</strong> ${data.airQualityIndex || "N/A"}</p>
            <p><strong>PM2.5:</strong> ${data.pm25 || "N/A"} μg/m³</p>
            <p><strong>PM10:</strong> ${data.pm10 || "N/A"} μg/m³</p>
            <p><strong>Nhiệt độ:</strong> ${data.temperature || "N/A"}°C</p>
            <p><strong>Độ ẩm:</strong> ${
              data.relativeHumidity
                ? Math.round(data.relativeHumidity * 100)
                : "N/A"
            }%</p>
          </div>
        </div>
      `;

      marker.bindPopup(popupContent);

      // Add click handler
      marker.on("click", () => {
        onLocationSelect(data.location!, data);
      });

      marker.addTo(map);
      markersRef.current.push(marker);
    });

    // Fit map to show all markers
    if (markersRef.current.length > 0 && map) {
      const group = L.featureGroup(markersRef.current);
      map.fitBounds(group.getBounds().pad(0.1));
    }
  }, [airQualityData, onLocationSelect]);

  // Handle search
  useEffect(() => {
    if (!searchQuery || !mapRefInstance.current) return;

    const searchLocation = async () => {
      try {
        const response = await fetch(
          `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(
            searchQuery
          )}&limit=1`
        );
        const data = await response.json();

        if (data && data.length > 0) {
          const result = data[0];
          const lat = parseFloat(result.lat);
          const lng = parseFloat(result.lon);

          const map = mapRefInstance.current;
          if (map) {
            map.setView([lat, lng], 15);
          }

          const location: LocationModel = {
            type: GeoJSONType.Point,
            coordinates: [lng, lat],
          };

          onLocationSelect(location);

          // Add a temporary marker for searched location
          const searchMarker = L.marker([lat, lng], {
            icon: L.divIcon({
              html: `
                <div style="
                  background-color: #3B82F6;
                  width: 30px;
                  height: 30px;
                  border-radius: 50%;
                  border: 3px solid white;
                  box-shadow: 0 2px 6px rgba(0,0,0,0.3);
                  display: flex;
                  align-items: center;
                  justify-content: center;
                  color: white;
                ">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <circle cx="11" cy="11" r="8" />
                    <path d="m21 21-4.3-4.3" />
                  </svg>
                </div>
              `,
              className: "search-marker",
              iconSize: [36, 36],
              iconAnchor: [18, 18],
            }),
          });

          if (map) {
            searchMarker.addTo(map);
          }
          markersRef.current.push(searchMarker);

          // Show popup with location info
          searchMarker
            .bindPopup(
              `
            <div class="p-2">
              <p class="font-bold">${result.display_name}</p>
            </div>
          `
            )
            .openPopup();
        }
      } catch (error) {
        console.error("Search error:", error);
      }
    };

    const timeoutId = setTimeout(searchLocation, 500); // Debounce search
    return () => clearTimeout(timeoutId);
  }, [searchQuery, onLocationSelect]);

  return (
    <div className="relative w-full h-full">
      <div ref={mapRef} className="w-full h-full" />
    </div>
  );
};
