// src/api/sensorApiClient.ts
// Raw HTTP calls - No business logic here

export interface AirQualityDTO {
  id: string;
  type: string;
  dateObserved: string;
  location?: {
    type: string;
    coordinates: [number, number];
  };
  airQualityIndex?: number;
  airQualityLevel?: string;
  areaServed?: string;
  pm25?: number;
  pm10?: number;
  co?: number;
  no2?: number;
  o3?: number;
  temperature?: number;
  relativeHumidity?: number;
  windDirection?: number;
  windSpeed?: number;
  typeofLocation?: string;
}

export interface WaterQualityDTO {
  id: string;
  type: string;
  dateObserved: string;
  location?: {
    type: string;
    coordinates: [number, number];
  };
  pH?: number;
  dissolvedOxygen?: number;
  turbidity?: number;
  temperature?: number;
  conductivity?: number;
  tss?: number;
  bod?: number;
  cod?: number;
  nh4?: number;
  waterQualityLevel?: "excellent" | "good" | "moderate" | "poor" | "very_poor";
  areaServed?: string;
  typeofLocation?: string;
}

export type SensorDTO = AirQualityDTO | WaterQualityDTO;

class SensorApiClient {
  private baseUrl: string = "/api"; // Replace with actual API URL

  async fetchAllSensors(): Promise<SensorDTO[]> {
    // Simulated API call - Replace with real fetch/axios
    return new Promise((resolve, reject) => {
      setTimeout(() => {
        // Simulate 10% error rate
        if (Math.random() < 0.1) {
          reject(new Error("Network connection failed"));
          return;
        }

        resolve(this.getMockData());
      }, 500);
    });
  }

  async fetchSensorById(id: string): Promise<SensorDTO | null> {
    return new Promise((resolve, reject) => {
      setTimeout(() => {
        const allSensors = this.getMockData();
        const sensor = allSensors.find((s) => s.id === id);
        resolve(sensor || null);
      }, 300);
    });
  }

  async refreshSensors(): Promise<SensorDTO[]> {
    return new Promise((resolve) => {
      setTimeout(() => {
        const mockData = this.getMockData().map((sensor) => {
          if (sensor.type === "AirQualityObserved") {
            return {
              ...sensor,
              dateObserved: new Date().toISOString(),
              airQualityIndex: Math.floor(Math.random() * 300),
              pm25: Math.random() * 100,
              temperature: 28 + Math.random() * 6,
            };
          } else {
            return {
              ...sensor,
              dateObserved: new Date().toISOString(),
              pH: 6 + Math.random() * 2,
              dissolvedOxygen: 2 + Math.random() * 6,
              temperature: 26 + Math.random() * 4,
            };
          }
        });
        resolve(mockData);
      }, 800);
    });
  }

  private getMockData(): SensorDTO[] {
    const airQualityData: AirQualityDTO[] = [
      {
        id: "air-sensor-001",
        type: "AirQualityObserved",
        dateObserved: new Date().toISOString(),
        location: {
          type: "Point",
          coordinates: [106.6297, 10.8231],
        },
        airQualityIndex: 156,
        airQualityLevel: "Unhealthy",
        areaServed: "Quận 1, TP. Hồ Chí Minh",
        pm25: 85.5,
        pm10: 120.3,
        co: 1.2,
        no2: 45.3,
        o3: 78.9,
        temperature: 32,
        relativeHumidity: 0.75,
        windSpeed: 12.5,
        windDirection: 135,
        typeofLocation: "outdoor",
      },
      {
        id: "air-sensor-002",
        type: "AirQualityObserved",
        dateObserved: new Date().toISOString(),
        location: {
          type: "Point",
          coordinates: [106.7009, 10.7769],
        },
        airQualityIndex: 45,
        airQualityLevel: "Good",
        areaServed: "Quận Bình Thạnh, TP. Hồ Chí Minh",
        pm25: 12.5,
        pm10: 25.3,
        co: 0.4,
        no2: 15.3,
        o3: 45.9,
        temperature: 30,
        relativeHumidity: 0.7,
        windSpeed: 8.2,
        windDirection: 90,
        typeofLocation: "outdoor",
      },
      {
        id: "air-sensor-003",
        type: "AirQualityObserved",
        dateObserved: new Date().toISOString(),
        location: {
          type: "Point",
          coordinates: [106.7718, 10.8505],
        },
        airQualityIndex: 95,
        airQualityLevel: "Moderate",
        areaServed: "Quận Thủ Đức, TP. Hồ Chí Minh",
        pm25: 35.5,
        pm10: 65.3,
        co: 0.8,
        no2: 28.3,
        o3: 62.9,
        temperature: 31,
        relativeHumidity: 0.72,
        windSpeed: 10.1,
        windDirection: 180,
        typeofLocation: "outdoor",
      },
    ];

    const waterQualityData: WaterQualityDTO[] = [
      {
        id: "water-sensor-001",
        type: "WaterQualityObserved",
        dateObserved: new Date().toISOString(),
        location: {
          type: "Point",
          coordinates: [106.6438, 10.8142],
        },
        areaServed: "Sông Sài Gòn - Quận 1",
        pH: 6.8,
        dissolvedOxygen: 5.2,
        turbidity: 25.5,
        temperature: 28,
        conductivity: 450,
        tss: 35,
        bod: 12,
        cod: 28,
        nh4: 0.8,
        waterQualityLevel: "moderate",
        typeofLocation: "outdoor",
      },
      {
        id: "water-sensor-002",
        type: "WaterQualityObserved",
        dateObserved: new Date().toISOString(),
        location: {
          type: "Point",
          coordinates: [106.6912, 10.7895],
        },
        areaServed: "Kênh Nhiêu Lộc - Quận 3",
        pH: 5.5,
        dissolvedOxygen: 2.1,
        turbidity: 85.5,
        temperature: 29,
        conductivity: 780,
        tss: 125,
        bod: 45,
        cod: 98,
        nh4: 3.2,
        waterQualityLevel: "poor",
        typeofLocation: "outdoor",
      },
      {
        id: "water-sensor-003",
        type: "WaterQualityObserved",
        dateObserved: new Date().toISOString(),
        location: {
          type: "Point",
          coordinates: [106.66, 10.76],
        },
        areaServed: "Kênh Tân Hóa - Lò Gốm - Quận 6",
        pH: 7.2,
        dissolvedOxygen: 6.5,
        turbidity: 15.2,
        temperature: 27,
        conductivity: 380,
        tss: 18,
        bod: 8,
        cod: 18,
        nh4: 0.5,
        waterQualityLevel: "good",
        typeofLocation: "outdoor",
      },
    ];

    return [...airQualityData, ...waterQualityData];
  }
}

export const sensorApiClient = new SensorApiClient();
