import React, { useEffect, useRef, useState } from "react";
import * as maptilersdk from "@maptiler/sdk";
import "@maptiler/sdk/dist/maptiler-sdk.css";
import {
  MapPin,
  Layers,
  Navigation,
  Search,
  ZoomIn,
  ZoomOut,
} from "lucide-react";
import { MAPTILER_API_KEY } from "../config/maptilerConfig";

maptilersdk.config.apiKey = MAPTILER_API_KEY;

const MapTilerApp: React.FC = () => {
  const mapContainer = useRef<HTMLDivElement>(null);
  const map = useRef<maptilersdk.Map | null>(null);
  const [mapStyle, setMapStyle] = useState<string>("streets-v2");
  const [searchQuery, setSearchQuery] = useState<string>("");
  const [markers, setMarkers] = useState<maptilersdk.Marker[]>([]);

  useEffect(() => {
    if (map.current) return;

    if (mapContainer.current) {
      maptilersdk.config.apiKey = MAPTILER_API_KEY;

      map.current = new maptilersdk.Map({
        container: mapContainer.current,
        style:
          maptilersdk.MapStyle[
            mapStyle
              .toUpperCase()
              .replace("-", "_") as keyof typeof maptilersdk.MapStyle
          ],
        center: [106.6297, 10.8231], // Ho Chi Minh City
        zoom: 8,
        navigationControl: false,
      });

      // Add default marker at center
      const marker = new maptilersdk.Marker({ color: "#ef4444" })
        .setLngLat([106.6297, 10.8231])
        .setPopup(
          new maptilersdk.Popup().setHTML(
            '<h3 class="font-bold">Hồ Chí Minh</h3><p>Vị trí mặc định</p>'
          )
        )
        .addTo(map.current);

      setMarkers([marker]);

      // Click event to add markers
      map.current.on("click", (e) => {
        if (map.current) {
          const newMarker = new maptilersdk.Marker({ color: "#3b82f6" })
            .setLngLat([e.lngLat.lng, e.lngLat.lat])
            .setPopup(
              new maptilersdk.Popup().setHTML(
                `<div class="p-2">
                  <p class="text-sm"><strong>Kinh độ:</strong> ${e.lngLat.lng.toFixed(
                    4
                  )}</p>
                  <p class="text-sm"><strong>Vĩ độ:</strong> ${e.lngLat.lat.toFixed(
                    4
                  )}</p>
                </div>`
              )
            )
            .addTo(map.current);

          setMarkers((prev) => [...prev, newMarker]);
        }
      });
    }
  }, []);

  useEffect(() => {
    if (map.current) {
      map.current.setStyle(
        maptilersdk.MapStyle[
          mapStyle
            .toUpperCase()
            .replace("-", "_") as keyof typeof maptilersdk.MapStyle
        ]
      );
    }
  }, [mapStyle]);

  const handleSearch = async () => {
    if (!searchQuery.trim()) return;

    try {
      const response = await fetch(
        `https://api.maptiler.com/geocoding/${encodeURIComponent(
          searchQuery
        )}.json?key=${MAPTILER_API_KEY}`
      );
      const data = await response.json();

      if (data.features && data.features.length > 0) {
        const [lng, lat] = data.features[0].center;

        if (map.current) {
          map.current.flyTo({
            center: [lng, lat],
            zoom: 14,
            duration: 2000,
          });

          const searchMarker = new maptilersdk.Marker({ color: "#10b981" })
            .setLngLat([lng, lat])
            .setPopup(
              new maptilersdk.Popup().setHTML(
                `<div class="p-2">
                  <h3 class="font-bold">${data.features[0].place_name}</h3>
                </div>`
              )
            )
            .addTo(map.current);

          setMarkers((prev) => [...prev, searchMarker]);
        }
      }
    } catch (error) {
      console.error("Search error:", error);
    }
  };

  const clearMarkers = () => {
    markers.forEach((marker) => marker.remove());
    setMarkers([]);
  };

  const zoomIn = () => {
    if (map.current) {
      map.current.zoomIn();
    }
  };

  const zoomOut = () => {
    if (map.current) {
      map.current.zoomOut();
    }
  };

  const resetView = () => {
    if (map.current) {
      map.current.flyTo({
        center: [106.6297, 10.8231],
        zoom: 12,
        duration: 1500,
      });
    }
  };

  return (
    <div className="relative w-full h-screen bg-gray-900">
      {/* Header */}
      <div className="absolute top-0 left-0 right-0 z-10 bg-gradient-to-b from-gray-900/90 to-transparent p-4">
        <div className="max-w-7xl mx-auto">
          <h1 className="text-2xl font-bold text-white mb-4 flex items-center gap-2">
            <MapPin className="w-6 h-6" />
            MapTiler Interactive Map
          </h1>

          {/* Search Bar */}
          <div className="flex gap-2">
            <div className="flex-1 flex gap-2 bg-white rounded-lg shadow-lg p-2">
              <Search className="w-5 h-5 text-gray-400 my-auto" />
              <input
                type="text"
                placeholder="Tìm kiếm địa điểm..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                onKeyPress={(e) => e.key === "Enter" && handleSearch()}
                className="flex-1 outline-none text-gray-800"
              />
              <button
                onClick={handleSearch}
                className="px-4 py-1 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors"
              >
                Tìm
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Map Container */}
      <div ref={mapContainer} className="w-full h-full" />

      {/* Control Panel */}
      <div className="absolute top-32 right-4 z-10 bg-white rounded-lg shadow-lg p-3 space-y-2">
        <button
          onClick={zoomIn}
          className="w-full p-2 hover:bg-gray-100 rounded transition-colors"
          title="Phóng to"
        >
          <ZoomIn className="w-5 h-5 mx-auto" />
        </button>
        <button
          onClick={zoomOut}
          className="w-full p-2 hover:bg-gray-100 rounded transition-colors"
          title="Thu nhỏ"
        >
          <ZoomOut className="w-5 h-5 mx-auto" />
        </button>
        <button
          onClick={resetView}
          className="w-full p-2 hover:bg-gray-100 rounded transition-colors"
          title="Về vị trí mặc định"
        >
          <Navigation className="w-5 h-5 mx-auto" />
        </button>
      </div>

      {/* Style Selector */}
      <div className="absolute bottom-4 left-4 z-10 bg-white rounded-lg shadow-lg p-4">
        <div className="flex items-center gap-2 mb-3">
          <Layers className="w-5 h-5" />
          <h3 className="font-semibold">Kiểu bản đồ</h3>
        </div>
        <div className="space-y-2">
          {["streets-v2", "satellite", "hybrid", "topo-v2", "winter-v2"].map(
            (style) => (
              <button
                key={style}
                onClick={() => setMapStyle(style)}
                className={`w-full px-4 py-2 rounded transition-colors text-left ${
                  mapStyle === style
                    ? "bg-blue-500 text-white"
                    : "bg-gray-100 hover:bg-gray-200 text-gray-800"
                }`}
              >
                {style.split("-")[0].charAt(0).toUpperCase() +
                  style.split("-")[0].slice(1)}
              </button>
            )
          )}
        </div>
      </div>

      {/* Marker Count */}
      <div className="absolute bottom-4 right-4 z-10 bg-white rounded-lg shadow-lg p-4">
        <div className="flex items-center justify-between gap-4">
          <div>
            <p className="text-sm text-gray-600">Số điểm đánh dấu</p>
            <p className="text-2xl font-bold text-blue-500">{markers.length}</p>
          </div>
          {markers.length > 0 && (
            <button
              onClick={clearMarkers}
              className="px-3 py-1 bg-red-500 text-white rounded hover:bg-red-600 transition-colors text-sm"
            >
              Xóa tất cả
            </button>
          )}
        </div>
      </div>

      {/* Instructions */}
      <div className="absolute bottom-20 right-4 z-10 bg-blue-500 text-white rounded-lg shadow-lg p-3 max-w-xs">
        <p className="text-sm">
          💡 <strong>Mẹo:</strong> Click vào bản đồ để thêm điểm đánh dấu!
        </p>
      </div>
    </div>
  );
};

export default MapTilerApp;
