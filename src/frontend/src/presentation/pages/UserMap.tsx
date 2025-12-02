import React, { useState, useEffect } from "react";
import { UserMapHeader } from "../components/feature/usermap/UserMapHeader";
import { UserMapView } from "../components/feature/usermap/UserMapView";
import { HealthInsightPanel } from "../components/feature/usermap/HealthInsightPanel";
import { AQIGauge } from "../components/feature/usermap/AQIGauge";
import type { AirQualityObservedModel } from "../../domain/models/AirQualityObservedModel";
import type { LocationModel } from "../../domain/models/CommonModels";
import { GeoJSONType } from "../../domain/models/CommonModels";

// Mock data for demonstration
const generateMockAirQualityData = (): AirQualityObservedModel[] => [
  {
    id: "1",
    type: "AirQualityObserved" as any,
    dateObserved: new Date(),
    location: {
      type: GeoJSONType.Point,
      coordinates: [106.7012, 10.7997], // [longitude, latitude] - Ngã Tư Hàng Xanh
    },
    airQualityIndex: 45,
    airQualityLevel: "Tốt",
    areaServed: "Ngã Tư Hàng Xanh, Quận 1",
    pm25: 12.5,
    pm10: 20.3,
    co: 0.4,
    no2: 25.8,
    o3: 35.2,
    temperature: 28.5,
    relativeHumidity: 0.75,
    windSpeed: 3.2,
    windDirection: 45.0,
  },
  {
    id: "2",
    type: "AirQualityObserved" as any,
    dateObserved: new Date(),
    location: {
      type: GeoJSONType.Point,
      coordinates: [106.7718, 10.8505], // Ngã Tư Thủ Đức
    },
    airQualityIndex: 85,
    airQualityLevel: "Kém",
    areaServed: "Ngã Tư Thủ Đức, TP. Thủ Đức",
    pm25: 35.8,
    pm10: 45.2,
    co: 0.8,
    no2: 42.1,
    o3: 28.9,
    temperature: 30.2,
    relativeHumidity: 0.68,
    windSpeed: 2.1,
    windDirection: 90.0,
  },
  {
    id: "3",
    type: "AirQualityObserved" as any,
    dateObserved: new Date(),
    location: {
      type: GeoJSONType.Point,
      coordinates: [106.6989, 10.7626], // Cầu Sài Gòn
    },
    airQualityIndex: 165,
    airQualityLevel: "Nguy hại",
    areaServed: "Cầu Sài Gòn, Bình Thạnh",
    pm25: 75.3,
    pm10: 95.7,
    co: 1.2,
    no2: 68.4,
    o3: 45.8,
    temperature: 31.1,
    relativeHumidity: 0.62,
    windSpeed: 1.8,
    windDirection: 180.0,
  },
];

export const UserMap: React.FC = () => {
  const [isDarkMode, setIsDarkMode] = useState(false);
  const [selectedLocation, setSelectedLocation] =
    useState<LocationModel | null>(null);
  const [selectedAirQuality, setSelectedAirQuality] =
    useState<AirQualityObservedModel | null>(null);
  const [searchQuery, setSearchQuery] = useState("");
  const [airQualityData] = useState<AirQualityObservedModel[]>(
    generateMockAirQualityData()
  );

  // Initialize dark mode
  useEffect(() => {
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

    setIsDarkMode(getInitialDarkMode());
  }, []);

  // Apply dark mode class
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

  const handleLocationSelect = (
    location: LocationModel,
    airQuality?: AirQualityObservedModel
  ) => {
    setSelectedLocation(location);
    setSelectedAirQuality(airQuality || null);
  };

  const handleSearch = (query: string) => {
    setSearchQuery(query);
    // Search functionality will be implemented in the search component
  };

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 relative">
      {/* Header */}
      <UserMapHeader
        onThemeToggle={handleThemeToggle}
        isDarkMode={isDarkMode}
        onSearch={handleSearch}
        searchQuery={searchQuery}
      />

      {/* Main Content */}
      <div className="relative h-[calc(100vh-72px)]">
        {/* Map View */}
        <UserMapView
          isDarkMode={isDarkMode}
          airQualityData={airQualityData}
          selectedLocation={selectedLocation}
          onLocationSelect={handleLocationSelect}
          searchQuery={searchQuery}
        />

        {/* AQI Gauge - Fixed Position */}
        <div className="absolute bottom-6 left-4 z-[1000]">
          <AQIGauge
            value={selectedAirQuality?.airQualityIndex || 50}
            isDarkMode={isDarkMode}
          />
        </div>

        {/* Health Insight Panel - Fixed Position */}
        {selectedAirQuality && (
          <div className="absolute top-4 right-4 z-[1000] w-80">
            <HealthInsightPanel
              airQuality={selectedAirQuality}
              isDarkMode={isDarkMode}
            />
          </div>
        )}
      </div>
    </div>
  );
};
