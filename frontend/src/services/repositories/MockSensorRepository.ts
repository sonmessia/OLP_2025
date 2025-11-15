import type { AirQualityObservedModel } from "../../domain/models/AirQualityObservedModel";
import {
  AirQualityType,
  WaterQualityType,
  GeoJSONType,
  LocationType,
} from "../../domain/models/CommonModels";
import type { SensorModel } from "../../domain/models/SenSorModel";
import type { WaterQualityObservedModel } from "../../domain/models/WaterQualityObservedModel";
import type { ISensorRepository } from "../../domain/repositories/ISensorRepository";

export class MockSensorRepository implements ISensorRepository {
  private mockAirQualityData: AirQualityObservedModel[] = [
    {
      id: "air-sensor-001",
      type: AirQualityType.AirQualityObserved,
      dateObserved: new Date(),
      location: {
        type: GeoJSONType.Point,
        coordinates: [106.6297, 10.8231], // [lng, lat] - Quận 1, TP.HCM
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
      typeofLocation: LocationType.outdoor,
    },
    {
      id: "air-sensor-002",
      type: AirQualityType.AirQualityObserved,
      dateObserved: new Date(),
      location: {
        type: GeoJSONType.Point,
        coordinates: [106.7009, 10.7769], // Quận Bình Thạnh
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
      typeofLocation: LocationType.outdoor,
    },
    {
      id: "air-sensor-003",
      type: AirQualityType.AirQualityObserved,
      dateObserved: new Date(),
      location: {
        type: GeoJSONType.Point,
        coordinates: [106.7718, 10.8505], // Quận Thủ Đức
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
      typeofLocation: LocationType.outdoor,
    },
  ];

  private mockWaterQualityData: WaterQualityObservedModel[] = [
    {
      id: "water-sensor-001",
      type: WaterQualityType.WaterQualityObserved,
      dateObserved: new Date(),
      location: {
        type: GeoJSONType.Point,
        coordinates: [106.6438, 10.8142], // Sông Sài Gòn, Quận 1
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
      typeofLocation: LocationType.outdoor,
    },
    {
      id: "water-sensor-002",
      type: WaterQualityType.WaterQualityObserved,
      dateObserved: new Date(),
      location: {
        type: GeoJSONType.Point,
        coordinates: [106.6912, 10.7895], // Kênh Nhiêu Lộc, Quận 3
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
      typeofLocation: LocationType.outdoor,
    },
    {
      id: "water-sensor-003",
      type: WaterQualityType.WaterQualityObserved,
      dateObserved: new Date(),
      location: {
        type: GeoJSONType.Point,
        coordinates: [106.66, 10.76], // Kênh Tân Hóa - Lò Gốm
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
      typeofLocation: LocationType.outdoor,
    },
  ];

  async getAllSensors(): Promise<SensorModel[]> {
    // Simulate API delay
    await new Promise((resolve) => setTimeout(resolve, 500));

    // Simulate random error (10% chance)
    if (Math.random() < 0.1) {
      throw new Error("Network connection failed");
    }

    return [...this.mockAirQualityData, ...this.mockWaterQualityData];
  }

  async getSensorById(id: string): Promise<SensorModel | null> {
    await new Promise((resolve) => setTimeout(resolve, 300));

    const allSensors = [
      ...this.mockAirQualityData,
      ...this.mockWaterQualityData,
    ];
    return allSensors.find((sensor) => sensor.id === id) || null;
  }

  async refreshSensors(): Promise<SensorModel[]> {
    await new Promise((resolve) => setTimeout(resolve, 800));

    // Simulate data update with random values
    const updatedAirData = this.mockAirQualityData.map((sensor) => ({
      ...sensor,
      dateObserved: new Date(),
      airQualityIndex: Math.floor(Math.random() * 300),
      pm25: Math.random() * 100,
      temperature: 28 + Math.random() * 6,
    }));

    const updatedWaterData = this.mockWaterQualityData.map((sensor) => ({
      ...sensor,
      dateObserved: new Date(),
      pH: 6 + Math.random() * 2,
      dissolvedOxygen: 2 + Math.random() * 6,
      temperature: 26 + Math.random() * 4,
    }));

    return [...updatedAirData, ...updatedWaterData];
  }
}
