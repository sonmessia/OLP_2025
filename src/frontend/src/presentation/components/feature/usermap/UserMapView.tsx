import React, { useEffect, useState } from "react";
import {
  MapContainer,
  TileLayer,
  Marker,
  Popup,
  Circle,
  useMap,
  useMapEvents,
} from "react-leaflet";
import L from "leaflet";
import { Locate, Navigation } from "lucide-react";
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

// Component to handle map interactions and logic
const MapController: React.FC<{
  searchQuery: string;
  onLocationSelect: (location: LocationModel) => void;
}> = ({ searchQuery, onLocationSelect }) => {
  const map = useMap();
  const [userLocation, setUserLocation] = useState<L.LatLng | null>(null);
  const [userAccuracy, setUserAccuracy] = useState<number | null>(null);
  const [isFollowing, setIsFollowing] = useState(true);
  const [lastUpdate, setLastUpdate] = useState<Date | null>(null);
  const [speed, setSpeed] = useState<number | null>(null);

  // Handle map clicks
  useMapEvents({
    click(e) {
      const location: LocationModel = {
        type: GeoJSONType.Point,
        coordinates: [e.latlng.lng, e.latlng.lat],
      };
      onLocationSelect(location);
    },
    dragstart() {
      // Stop following if user manually drags the map
      setIsFollowing(false);
    },
  });

  // Locate user on mount with realtime watching using native Geolocation API
  useEffect(() => {
    let watchId: number | null = null;

    if ("geolocation" in navigator) {
      watchId = navigator.geolocation.watchPosition(
        (position) => {
          const { latitude, longitude, accuracy, speed } = position.coords;
          const latlng = new L.LatLng(latitude, longitude);

          setUserLocation(latlng);
          setUserAccuracy(accuracy);
          setLastUpdate(new Date());
          setSpeed(speed);

          // Only auto-center if we are in "following" mode
          if (isFollowing) {
            map.setView(latlng, map.getZoom() < 16 ? 16 : map.getZoom(), {
              animate: true,
            });
          }
        },
        (error) => {
          console.warn("Location error:", error.message);
        },
        {
          enableHighAccuracy: true,
          timeout: 10000,
          maximumAge: 0,
        }
      );
    }

    // Cleanup function to stop watching when component unmounts
    return () => {
      if (watchId !== null) {
        navigator.geolocation.clearWatch(watchId);
      }
    };
  }, [map, isFollowing]);

  // Handle search
  useEffect(() => {
    if (!searchQuery) return;

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
          const latLng = new L.LatLng(lat, lng);

          map.setView(latLng, 15);
          setIsFollowing(false); // Stop following user when searching

          const location: LocationModel = {
            type: GeoJSONType.Point,
            coordinates: [lng, lat],
          };
          onLocationSelect(location);

          // Add a temporary popup
          L.popup()
            .setLatLng(latLng)
            .setContent(`<p class="font-bold">${result.display_name}</p>`)
            .openOn(map);
        }
      } catch (error) {
        console.error("Search error:", error);
      }
    };

    const timeoutId = setTimeout(searchLocation, 500);
    return () => clearTimeout(timeoutId);
  }, [searchQuery, map, onLocationSelect]);

  const handleLocateClick = () => {
    setIsFollowing(true);
    if (userLocation) {
      map.flyTo(userLocation, 16);
    }
  };

  return (
    <>
      {userLocation && (
        <>
          <Marker
            position={userLocation}
            icon={L.divIcon({
              html: `
                <div style="
                  background-color: #3B82F6;
                  width: 16px;
                  height: 16px;
                  border-radius: 50%;
                  border: 2px solid white;
                  box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.3);
                "></div>
              `,
              className: "user-location-marker",
              iconSize: [24, 24],
              iconAnchor: [12, 12],
            })}
          >
            <Popup>Bạn đang ở đây</Popup>
          </Marker>
          {userAccuracy && (
            <Circle
              center={userLocation}
              radius={userAccuracy}
              pathOptions={{
                fillColor: "#3B82F6",
                fillOpacity: 0.1,
                stroke: false,
              }}
            />
          )}
        </>
      )}

      {/* Real-time Location Info Panel */}
      {userLocation && (
        <div className="absolute top-4 left-4 z-[1000] bg-white dark:bg-gray-800 rounded-lg shadow-lg p-3 min-w-[250px]">
          <h3 className="text-sm font-bold text-gray-900 dark:text-white mb-2 flex items-center gap-2">
            <Navigation className="w-4 h-4 text-blue-500" />
            Vị trí của bạn
          </h3>
          <div className="space-y-1 text-xs text-gray-600 dark:text-gray-300">
            <div className="flex justify-between">
              <span className="font-medium">Vĩ độ:</span>
              <span className="font-mono">{userLocation.lat.toFixed(6)}°</span>
            </div>
            <div className="flex justify-between">
              <span className="font-medium">Kinh độ:</span>
              <span className="font-mono">{userLocation.lng.toFixed(6)}°</span>
            </div>
            {userAccuracy && (
              <div className="flex justify-between">
                <span className="font-medium">Độ chính xác:</span>
                <span className="font-mono">±{Math.round(userAccuracy)}m</span>
              </div>
            )}
            {speed !== null && speed > 0 && (
              <div className="flex justify-between">
                <span className="font-medium">Tốc độ:</span>
                <span className="font-mono">
                  {(speed * 3.6).toFixed(1)} km/h
                </span>
              </div>
            )}
            {lastUpdate && (
              <div className="flex justify-between pt-1 border-t border-gray-200 dark:border-gray-700">
                <span className="font-medium">Cập nhật:</span>
                <span className="font-mono">
                  {lastUpdate.toLocaleTimeString("vi-VN")}
                </span>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Locate Me Button */}
      <div className="absolute bottom-24 right-4 z-[1000]">
        <button
          onClick={handleLocateClick}
          className={`p-2 rounded-full shadow-lg transition-colors ${
            isFollowing
              ? "bg-blue-500 text-white hover:bg-blue-600"
              : "bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700"
          }`}
          title={isFollowing ? "Đang theo dõi vị trí" : "Vị trí của tôi"}
        >
          {isFollowing ? (
            <Navigation className="w-6 h-6" />
          ) : (
            <Locate className="w-6 h-6" />
          )}
        </button>
      </div>
    </>
  );
};

export const UserMapView: React.FC<UserMapViewProps> = ({
  isDarkMode,
  airQualityData,
  onLocationSelect,
  searchQuery,
}) => {
  const tileUrl = isDarkMode
    ? "https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
    : "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png";

  return (
    <div className="w-full h-full">
      <MapContainer
        center={[10.8231, 106.6297]} // Default to HCMC
        zoom={12}
        className="w-full h-full"
        zoomControl={false} // We can add custom zoom control if needed, or set to true
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>'
          url={tileUrl}
          subdomains="abcd"
          maxZoom={19}
        />

        <MapController
          searchQuery={searchQuery}
          onLocationSelect={(loc) => onLocationSelect(loc)}
        />

        {/* Heatmap Circles */}
        {airQualityData.map((item) => {
          if (!item.location || !item.airQualityIndex) return null;
          const [lng, lat] = item.location.coordinates;
          const intensity = Math.min(item.airQualityIndex / 200, 1);
          const radius = 1000 + intensity * 2000;

          let color = "#10B981"; // Green
          if (intensity > 0.75) color = "#D9232F"; // Red
          else if (intensity > 0.5) color = "#FBBF24"; // Yellow

          return (
            <Circle
              key={`heat-${item.id}`}
              center={[lat, lng]}
              radius={radius}
              pathOptions={{
                fillColor: color,
                fillOpacity: 0.2 + intensity * 0.1,
                stroke: false,
              }}
            />
          );
        })}

        {/* Air Quality Markers */}
        {airQualityData.map((data) => {
          if (!data.location) return null;
          const [lng, lat] = data.location.coordinates;

          return (
            <Marker
              key={data.id}
              position={[lat, lng]}
              icon={getAQIIcon(data.airQualityIndex || 0)}
              eventHandlers={{
                click: () => onLocationSelect(data.location!, data),
              }}
            >
              <Popup className="custom-popup">
                <div className="p-2 min-w-[200px]">
                  <h3 className="font-bold text-lg mb-2">
                    {data.areaServed || "Vị trí"}
                  </h3>
                  <div className="space-y-1 text-sm">
                    <p>
                      <strong>AQI:</strong> {data.airQualityIndex || "N/A"}
                    </p>
                    <p>
                      <strong>PM2.5:</strong> {data.pm25 || "N/A"} μg/m³
                    </p>
                    <p>
                      <strong>PM10:</strong> {data.pm10 || "N/A"} μg/m³
                    </p>
                    <p>
                      <strong>Nhiệt độ:</strong> {data.temperature || "N/A"}°C
                    </p>
                    <p>
                      <strong>Độ ẩm:</strong>{" "}
                      {data.relativeHumidity
                        ? Math.round(data.relativeHumidity * 100)
                        : "N/A"}
                      %
                    </p>
                  </div>
                </div>
              </Popup>
            </Marker>
          );
        })}
      </MapContainer>
    </div>
  );
};
