// Copyright (c) 2025 Green Wave Team
// 
// This software is released under the MIT License.
// https://opensource.org/licenses/MIT

import type { AirQualityObservedDto } from "../data/dtos/AirQualityDTOs";

// Helper to generate deterministic random numbers based on a seed
// This ensures that for the same seed, we get the same "random" number
const seededRandom = (seed: number) => {
  const x = Math.sin(seed++) * 10000;
  return x - Math.floor(x);
};

export interface MockLocation {
  id: string;
  nameKey: string;
  areaKey: string;
  coords: [number, number];
  baseAQI: number;
}

const LOCATIONS: MockLocation[] = [
  {
    id: "urn:ngsi-ld:AirQualityObserved:ThuDuc:Crossroads",
    nameKey: "locations.thuDucCrossroads",
    areaKey: "locations.thuDucCity, locations.hcmc",
    coords: [106.7718, 10.8505],
    baseAQI: 110,
  },
  {
    id: "urn:ngsi-ld:AirQualityObserved:GoVap:QuangTrung",
    nameKey: "locations.goVapQuangTrung",
    areaKey: "locations.goVapQuangTrung, locations.hcmc",
    coords: [106.6816, 10.822], // Tọa độ xấp xỉ Ngã 5 Chuồng Chó (Quang Trung)
    baseAQI: 145,
  },
  {
    id: "urn:ngsi-ld:AirQualityObserved:HCMC:D1",
    nameKey: "locations.d1Center",
    areaKey: "locations.d1Center, locations.hcmc",
    coords: [106.7009, 10.7769],
    baseAQI: 85,
  },
  {
    id: "urn:ngsi-ld:AirQualityObserved:Hanoi:BaDinh",
    nameKey: "locations.baDinhHanoi",
    areaKey: "locations.baDinhHanoi, locations.hanoi",
    coords: [105.8342, 21.0278],
    baseAQI: 160,
  },
  {
    id: "urn:ngsi-ld:AirQualityObserved:DaNang:HaiChau",
    nameKey: "locations.haiChauDaNang",
    areaKey: "locations.haiChauDaNang, locations.danang",
    coords: [108.2208, 16.0544],
    baseAQI: 45,
  },
];

export const generateMockAirQualityData = (t?: (key: string) => string): AirQualityObservedDto[] => {
  // Create a time slot that changes every 10 seconds
  // Date.now() is in ms. /1000 -> seconds. /10 -> 10s blocks.
  const timeSlot = Math.floor(Date.now() / 10000);

  const getFluctuatedValue = (
    baseValue: number,
    variance: number,
    id: string
  ) => {
    // Use timeSlot + id char code sum as seed to ensure stability within 10s but variety between items
    const idSum = id
      .split("")
      .reduce((acc, char) => acc + char.charCodeAt(0), 0);
    const seed = timeSlot + idSum;
    const rand = seededRandom(seed); // 0..1
    const fluctuation = (rand - 0.5) * 2 * variance; // -variance .. +variance
    return Number((baseValue + fluctuation).toFixed(1));
  };

  const getAQILevel = (aqi: number, t?: (key: string) => string) => {
    if (!t) {
      // Fallback to English if no translation function provided
      if (aqi <= 50) return "Good";
      if (aqi <= 100) return "Moderate";
      if (aqi <= 150) return "Unhealthy for Sensitive Groups";
      if (aqi <= 200) return "Unhealthy";
      if (aqi <= 300) return "Very Unhealthy";
      return "Hazardous";
    }

    if (aqi <= 50) return t("aqi.good");
    if (aqi <= 100) return t("aqi.moderate");
    if (aqi <= 150) return t("aqi.unhealthyForSensitive");
    if (aqi <= 200) return t("aqi.unhealthy");
    if (aqi <= 300) return t("aqi.veryUnhealthy");
    return t("aqi.hazardous");
  };

  const getLocalizedString = (key: string, fallback: string): string => {
    if (!t) return fallback;
    return key.includes(",")
      ? key.split(", ").map(k => t(k)).join(", ")
      : t(key);
  };

  return LOCATIONS.map((loc) => {
    const aqi = Math.max(
      0,
      Math.round(getFluctuatedValue(loc.baseAQI, 20, loc.id))
    );

    return {
      id: loc.id,
      type: "AirQualityObserved",
      dateObserved: new Date().toISOString(),
      location: {
        type: "Point",
        coordinates: loc.coords,
      },
      airQualityIndex: aqi,
      airQualityLevel: getAQILevel(aqi, t),
      areaServed: getLocalizedString(loc.areaKey, "Unknown Area"),
      co: Math.max(0, getFluctuatedValue(5, 2, loc.id)),
      no2: Math.max(0, getFluctuatedValue(40, 10, loc.id)),
      o3: Math.max(0, getFluctuatedValue(25, 10, loc.id)),
      pm10: Math.max(0, getFluctuatedValue(aqi * 0.6, 15, loc.id)),
      pm25: Math.max(0, getFluctuatedValue(aqi * 0.4, 10, loc.id)),
      temperature: getFluctuatedValue(32, 2, loc.id),
      relativeHumidity: Math.min(
        1,
        Math.max(0, getFluctuatedValue(0.7, 0.1, loc.id))
      ),
      windSpeed: Math.max(0, getFluctuatedValue(3, 2, loc.id)),
      windDirection:
        Math.abs(Math.round(getFluctuatedValue(180, 180, loc.id))) % 360,
      typeofLocation: "outdoor",
    };
  });
};
