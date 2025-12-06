import React, { useState, useEffect, useRef } from "react";
import { useTranslation } from "react-i18next";
import {
  MapContainer,
  TileLayer,
  CircleMarker,
  Popup,
  useMap,
} from "react-leaflet";
import type { PollutionHotspot } from "../../../../domain/models/DashboardModel";
import "leaflet/dist/leaflet.css";

interface PollutionMapProps {
  hotspots: PollutionHotspot[];
}

interface NominatimResult {
  place_id: number;
  display_name: string;
  lat: string;
  lon: string;
  boundingbox: [string, string, string, string];
}

const severityColors = {
  low: "#10B981",
  medium: "#FBBF24",
  high: "#F59E0B",
  critical: "#D9232F",
};

// Component to handle map navigation
const MapController: React.FC<{
  center: [number, number] | null;
  zoom: number;
}> = ({ center, zoom }) => {
  const map = useMap();

  useEffect(() => {
    if (center) {
      map.flyTo(center, zoom, {
        duration: 1.5,
      });
    }
  }, [center, zoom, map]);

  return null;
};

export const PollutionMap: React.FC<
  PollutionMapProps & { onHotspotSelect?: (hotspot: PollutionHotspot) => void }
> = ({ hotspots, onHotspotSelect }) => {
  const { t } = useTranslation(["maps"]);
  // Default center (Ho Chi Minh City)
  const defaultCenter: [number, number] = [10.8231, 106.6297];
  const center: [number, number] =
    hotspots.length > 0
      ? [hotspots[0].latitude, hotspots[0].longitude]
      : defaultCenter;

  // Search states
  const [searchQuery, setSearchQuery] = useState("");
  const [searchResults, setSearchResults] = useState<NominatimResult[]>([]);
  const [isSearching, setIsSearching] = useState(false);
  const [showResults, setShowResults] = useState(false);
  const [mapCenter, setMapCenter] = useState<[number, number] | null>(null);
  const [mapZoom, setMapZoom] = useState(13);
  const searchTimeoutRef = useRef<number | null>(null);

  // Debounced search effect
  useEffect(() => {
    // Clear previous timeout
    if (searchTimeoutRef.current) {
      clearTimeout(searchTimeoutRef.current);
    }

    // Don't search if query is too short
    if (searchQuery.trim().length < 3) {
      setSearchResults([]);
      setShowResults(false);
      return;
    }

    // Set a new timeout for search
    searchTimeoutRef.current = setTimeout(() => {
      performSearch(searchQuery);
    }, 500); // Debounce delay: 500ms

    // Cleanup
    return () => {
      if (searchTimeoutRef.current) {
        clearTimeout(searchTimeoutRef.current);
      }
    };
  }, [searchQuery]);

  // Function to perform search using Nominatim API
  const performSearch = async (query: string) => {
    setIsSearching(true);
    try {
      const response = await fetch(
        `https://nominatim.openstreetmap.org/search?` +
          new URLSearchParams({
            q: query,
            format: "json",
            limit: "5",
            countrycodes: "vn", // Limit to Vietnam
            addressdetails: "1",
          })
      );

      if (!response.ok) {
        throw new Error("Search failed");
      }

      const data: NominatimResult[] = await response.json();
      setSearchResults(data);
      setShowResults(true);
    } catch (error) {
      console.error("Search error:", error);
      setSearchResults([]);
    } finally {
      setIsSearching(false);
    }
  };

  // Handle location selection
  const handleLocationSelect = (result: NominatimResult) => {
    const lat = parseFloat(result.lat);
    const lon = parseFloat(result.lon);

    setMapCenter([lat, lon]);
    setMapZoom(15); // Zoom in when selecting a location
    setShowResults(false);
    setSearchQuery(result.display_name);
  };

  return (
    <div className="bg-white dark:bg-gray-800 rounded-xl border-2 border-gray-200 dark:border-gray-700 p-3 h-full">
      {/* Search Box */}
      <div className="relative mb-3">
        <div className="relative">
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            onFocus={() => searchResults.length > 0 && setShowResults(true)}
            placeholder={t("searchPlaceholder")}
            className="w-full px-4 py-2 pl-10 pr-10 text-sm border-2 border-gray-300 dark:border-gray-600 rounded-lg 
                     bg-white dark:bg-gray-700 text-gray-900 dark:text-white
                     focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent
                     placeholder-gray-400 dark:placeholder-gray-500"
          />
          {/* Search Icon */}
          <svg
            className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
            />
          </svg>

          {/* Loading Spinner */}
          {isSearching && (
            <div className="absolute right-3 top-1/2 transform -translate-y-1/2">
              <div className="animate-spin rounded-full h-4 w-4 border-2 border-green-500 border-t-transparent"></div>
            </div>
          )}

          {/* Clear Button */}
          {searchQuery && !isSearching && (
            <button
              onClick={() => {
                setSearchQuery("");
                setSearchResults([]);
                setShowResults(false);
              }}
              className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
            >
              <svg
                className="w-4 h-4"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M6 18L18 6M6 6l12 12"
                />
              </svg>
            </button>
          )}
        </div>

        {/* Search Results Dropdown */}
        {showResults && searchResults.length > 0 && (
          <div className="absolute z-50 w-full mt-1 bg-white dark:bg-gray-700 border-2 border-gray-200 dark:border-gray-600 rounded-lg shadow-lg max-h-60 overflow-y-auto">
            {searchResults.map((result) => (
              <button
                key={result.place_id}
                onClick={() => handleLocationSelect(result)}
                className="w-full px-4 py-3 text-left hover:bg-gray-100 dark:hover:bg-gray-600 
                         border-b border-gray-200 dark:border-gray-600 last:border-b-0
                         transition-colors duration-150"
              >
                <div className="flex items-start">
                  <svg
                    className="w-5 h-5 text-green-500 mr-2 mt-0.5 flex-shrink-0"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"
                    />
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"
                    />
                  </svg>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-gray-900 dark:text-white truncate">
                      {result.display_name}
                    </p>
                  </div>
                </div>
              </button>
            ))}
          </div>
        )}

        {/* No Results Message */}
        {showResults &&
          searchResults.length === 0 &&
          !isSearching &&
          searchQuery.length >= 3 && (
            <div className="absolute z-50 w-full mt-1 bg-white dark:bg-gray-700 border-2 border-gray-200 dark:border-gray-600 rounded-lg shadow-lg p-4">
              <p className="text-sm text-gray-500 dark:text-gray-400 text-center">
                {t("noResults", { query: searchQuery })}
              </p>
            </div>
          )}
      </div>

      <div className="h-[calc(100%-3rem)] rounded-lg overflow-hidden">
        <MapContainer
          center={center}
          zoom={13}
          style={{ height: "100%", width: "100%" }}
          className="z-0"
        >
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />

          {/* Map Controller for navigation */}
          <MapController center={mapCenter} zoom={mapZoom} />

          {hotspots.map((hotspot) => (
            <CircleMarker
              key={hotspot.id}
              center={[hotspot.latitude, hotspot.longitude]}
              radius={15}
              fillColor={severityColors[hotspot.severity]}
              color="#fff"
              weight={2}
              opacity={1}
              fillOpacity={0.7}
              eventHandlers={{
                click: () => onHotspotSelect?.(hotspot),
              }}
            >
              <Popup>
                <div className="p-2">
                  <h4 className="font-bold text-gray-900 mb-2">
                    {hotspot.name}
                  </h4>
                  <div className="space-y-1 text-sm">
                    <p>
                      <span className="font-medium">{t("pm25")}</span>{" "}
                      {hotspot.pm25.toFixed(1)} μg/m³
                    </p>
                    <p>
                      <span className="font-medium">{t("aqi")}</span>{" "}
                      {hotspot.aqi}
                    </p>
                    <p>
                      <span className="font-medium">{t("severityLabel")}</span>{" "}
                      <span
                        className="font-semibold"
                        style={{ color: severityColors[hotspot.severity] }}
                      >
                        {t(`severity.${hotspot.severity}`)}
                      </span>
                    </p>
                  </div>
                </div>
              </Popup>
            </CircleMarker>
          ))}
        </MapContainer>
      </div>
    </div>
  );
};
