import type { AirQualityObservedDto } from "../data/dtos/AirQualityDTOs";

// Helper to generate deterministic random numbers based on a seed
// This ensures that for the same seed, we get the same "random" number
const seededRandom = (seed: number) => {
  const x = Math.sin(seed++) * 10000;
  return x - Math.floor(x);
};

export const generateMockAirQualityData = (): AirQualityObservedDto[] => {
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

  const getAQILevel = (aqi: number) => {
    if (aqi <= 50) return "Good";
    if (aqi <= 100) return "Moderate";
    if (aqi <= 150) return "Unhealthy for Sensitive Groups";
    if (aqi <= 200) return "Unhealthy";
    if (aqi <= 300) return "Very Unhealthy";
    return "Hazardous";
  };

  const locations = [
    {
      id: "urn:ngsi-ld:AirQualityObserved:ThuDuc:Crossroads",
      name: "Ngã Tư Thủ Đức",
      area: "TP. Thủ Đức, TP.HCM",
      coords: [106.7718, 10.8505],
      baseAQI: 110,
    },
    {
      id: "urn:ngsi-ld:AirQualityObserved:GoVap:QuangTrung",
      name: "Ngã 5 Quang Trung",
      area: "Gò Vấp, TP.HCM",
      coords: [106.6816, 10.822], // Tọa độ xấp xỉ Ngã 5 Chuồng Chó (Quang Trung)
      baseAQI: 145,
    },
    {
      id: "urn:ngsi-ld:AirQualityObserved:HCMC:D1",
      name: "Quận 1 - Trung tâm",
      area: "Quận 1, TP.HCM",
      coords: [106.7009, 10.7769],
      baseAQI: 85,
    },
    {
      id: "urn:ngsi-ld:AirQualityObserved:Hanoi:BaDinh",
      name: "Ba Đình - Hà Nội",
      area: "Ba Đình, Hà Nội",
      coords: [105.8342, 21.0278],
      baseAQI: 160,
    },
    {
      id: "urn:ngsi-ld:AirQualityObserved:DaNang:HaiChau",
      name: "Hải Châu - Đà Nẵng",
      area: "Hải Châu, Đà Nẵng",
      coords: [108.2208, 16.0544],
      baseAQI: 45,
    },
  ];

  return locations.map((loc) => {
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
      airQualityLevel: getAQILevel(aqi),
      areaServed: loc.area,
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
