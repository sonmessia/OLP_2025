import React, { useEffect, useRef } from "react";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import type {
  VehicleData,
  TrafficLightState,
} from "../../../domain/models/simulation.types";

interface TrafficMapProps {
  center: [number, number];
  bounds: [[number, number], [number, number]];
  vehicles: VehicleData[];
  trafficLights: TrafficLightState[];
  lockView?: boolean;
}

export const TrafficMap: React.FC<TrafficMapProps> = ({
  center,
  bounds,
  vehicles,
  trafficLights,
  lockView = true,
}) => {
  const mapRef = useRef<L.Map | null>(null);
  const mapContainerRef = useRef<HTMLDivElement>(null);
  const vehicleMarkersRef = useRef<Map<string, L.Marker>>(new Map());
  const trafficLightMarkersRef = useRef<Map<string, L.CircleMarker>>(new Map());

  // Initialize map
  useEffect(() => {
    if (!mapContainerRef.current || mapRef.current) return;

    // Create map
    const map = L.map(mapContainerRef.current, {
      center,
      zoom: 16,
      zoomControl: !lockView,
      dragging: !lockView,
      touchZoom: !lockView,
      scrollWheelZoom: !lockView,
      doubleClickZoom: !lockView,
      boxZoom: !lockView,
      keyboard: !lockView,
    });

    // Add OpenStreetMap tiles
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      attribution: "© OpenStreetMap contributors",
      maxZoom: 19,
    }).addTo(map);

    // Fit to bounds
    map.fitBounds(bounds);

    mapRef.current = map;

    return () => {
      map.remove();
      mapRef.current = null;
    };
  }, [center, bounds, lockView]);

  // Update vehicles
  useEffect(() => {
    if (!mapRef.current) return;

    const map = mapRef.current;
    const currentVehicleIds = new Set(vehicles.map((v) => v.id));

    // Remove vehicles that no longer exist
    vehicleMarkersRef.current.forEach((marker, id) => {
      if (!currentVehicleIds.has(id)) {
        marker.remove();
        vehicleMarkersRef.current.delete(id);
      }
    });

    // Update or create vehicle markers
    vehicles.forEach((vehicle) => {
      const existingMarker = vehicleMarkersRef.current.get(vehicle.id);

      if (existingMarker) {
        // Update position and rotation
        existingMarker.setLatLng([vehicle.lat, vehicle.lon]);
        const icon = existingMarker.getIcon() as L.DivIcon;
        const newIcon = L.divIcon({
          className: "vehicle-marker",
          html: `<div style="transform: rotate(${vehicle.angle}deg);">🚗</div>`,
          iconSize: [30, 30],
          iconAnchor: [15, 15],
        });
        existingMarker.setIcon(newIcon);
      } else {
        // Create new marker
        const icon = L.divIcon({
          className: "vehicle-marker",
          html: `<div style="transform: rotate(${vehicle.angle}deg);">🚗</div>`,
          iconSize: [30, 30],
          iconAnchor: [15, 15],
        });

        const marker = L.marker([vehicle.lat, vehicle.lon], { icon })
          .bindPopup(
            `
            <strong>Vehicle ${vehicle.id}</strong><br/>
            Speed: ${vehicle.speed.toFixed(1)} m/s<br/>
            Angle: ${vehicle.angle.toFixed(0)}°
          `
          )
          .addTo(map);

        vehicleMarkersRef.current.set(vehicle.id, marker);
      }
    });
  }, [vehicles]);

  // Update traffic lights
  useEffect(() => {
    if (!mapRef.current) return;

    const map = mapRef.current;

    trafficLights.forEach((tl) => {
      const existingMarker = trafficLightMarkersRef.current.get(tl.id);

      // Determine color based on state
      const getColor = (state: string): string => {
        if (state.includes("G") || state.includes("g")) return "#10b981"; // green
        if (state.includes("r")) return "#ef4444"; // red
        if (state.includes("y")) return "#f59e0b"; // yellow
        return "#6b7280"; // gray
      };

      const color = getColor(tl.state);

      if (existingMarker) {
        // Update color
        existingMarker.setStyle({ fillColor: color, color });
      } else {
        // Create new traffic light marker
        // Note: You'll need to provide actual coordinates for traffic lights
        // For now, we'll place them near the center
        const marker = L.circleMarker(center, {
          radius: 8,
          fillColor: color,
          color,
          weight: 2,
          opacity: 1,
          fillOpacity: 0.8,
        })
          .bindPopup(
            `
            <strong>Traffic Light ${tl.id}</strong><br/>
            Phase: ${tl.phase}<br/>
            State: ${tl.state}
          `
          )
          .addTo(map);

        trafficLightMarkersRef.current.set(tl.id, marker);
      }
    });
  }, [trafficLights, center]);

  return (
    <div
      ref={mapContainerRef}
      className="w-full h-full rounded-lg overflow-hidden shadow-lg"
      style={{ minHeight: "500px" }}
    />
  );
};
