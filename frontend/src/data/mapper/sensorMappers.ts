// src/data/mappers/sensorMappers.ts
import type {
  SensorDTO,
  AirQualityDTO,
  WaterQualityDTO,
} from "../../api/sensorApiClient";
import type { SensorModel } from "../../domain/models/SenSorModel";
import type { AirQualityObservedModel } from "../../domain/models/AirQualityObservedModel";
import type { WaterQualityObservedModel } from "../../domain/models/WaterQualityObservedModel";
import {
  AirQualityType,
  WaterQualityType,
  GeoJSONType,
  LocationType,
} from "../../domain/models/CommonModels";

export class SensorMappers {
  static dtoToModel(dto: SensorDTO): SensorModel {
    if (dto.type === "AirQualityObserved") {
      return this.airQualityDtoToModel(dto as AirQualityDTO);
    } else {
      return this.waterQualityDtoToModel(dto as WaterQualityDTO);
    }
  }

  static dtoArrayToModelArray(dtos: SensorDTO[]): SensorModel[] {
    return dtos.map((dto) => this.dtoToModel(dto));
  }

  private static airQualityDtoToModel(
    dto: AirQualityDTO
  ): AirQualityObservedModel {
    return {
      id: dto.id,
      type: AirQualityType.AirQualityObserved,
      dateObserved: dto.dateObserved ? new Date(dto.dateObserved) : undefined,
      location: dto.location
        ? {
            type: GeoJSONType.Point,
            coordinates: dto.location.coordinates,
          }
        : undefined,
      airQualityIndex: dto.airQualityIndex,
      airQualityLevel: dto.airQualityLevel,
      areaServed: dto.areaServed,
      co: dto.co,
      no2: dto.no2,
      o3: dto.o3,
      pm10: dto.pm10,
      pm25: dto.pm25,
      temperature: dto.temperature,
      relativeHumidity: dto.relativeHumidity,
      windDirection: dto.windDirection,
      windSpeed: dto.windSpeed,
      typeofLocation:
        dto.typeofLocation === "indoor"
          ? LocationType.indoor
          : LocationType.outdoor,
    };
  }

  private static waterQualityDtoToModel(
    dto: WaterQualityDTO
  ): WaterQualityObservedModel {
    return {
      id: dto.id,
      type: WaterQualityType.WaterQualityObserved,
      dateObserved: dto.dateObserved ? new Date(dto.dateObserved) : undefined,
      location: dto.location
        ? {
            type: GeoJSONType.Point,
            coordinates: dto.location.coordinates,
          }
        : undefined,
      pH: dto.pH,
      dissolvedOxygen: dto.dissolvedOxygen,
      turbidity: dto.turbidity,
      temperature: dto.temperature,
      conductivity: dto.conductivity,
      tss: dto.tss,
      bod: dto.bod,
      cod: dto.cod,
      nh4: dto.nh4,
      waterQualityLevel: dto.waterQualityLevel,
      areaServed: dto.areaServed,
      typeofLocation:
        dto.typeofLocation === "indoor"
          ? LocationType.indoor
          : LocationType.outdoor,
    };
  }

  // Model to DTO (for POST/PUT operations)
  static modelToDto(model: SensorModel): SensorDTO {
    if (model.type === AirQualityType.AirQualityObserved) {
      return this.airQualityModelToDto(model as AirQualityObservedModel);
    } else {
      return this.waterQualityModelToDto(model as WaterQualityObservedModel);
    }
  }

  private static airQualityModelToDto(
    model: AirQualityObservedModel
  ): AirQualityDTO {
    return {
      id: model.id,
      type: "AirQualityObserved",
      dateObserved: model.dateObserved?.toISOString() || "",
      location: model.location
        ? {
            type: "Point",
            coordinates: model.location.coordinates,
          }
        : undefined,
      airQualityIndex: model.airQualityIndex,
      airQualityLevel: model.airQualityLevel,
      areaServed: model.areaServed,
      pm25: model.pm25,
      pm10: model.pm10,
      co: model.co,
      no2: model.no2,
      o3: model.o3,
      temperature: model.temperature,
      relativeHumidity: model.relativeHumidity,
      windSpeed: model.windSpeed,
      windDirection: model.windDirection,
      typeofLocation: model.typeofLocation,
    };
  }

  private static waterQualityModelToDto(
    model: WaterQualityObservedModel
  ): WaterQualityDTO {
    return {
      id: model.id,
      type: "WaterQualityObserved",
      dateObserved: model.dateObserved?.toISOString() || "",
      location: model.location
        ? {
            type: "Point",
            coordinates: model.location.coordinates,
          }
        : undefined,
      pH: model.pH,
      dissolvedOxygen: model.dissolvedOxygen,
      turbidity: model.turbidity,
      temperature: model.temperature,
      conductivity: model.conductivity,
      tss: model.tss,
      bod: model.bod,
      cod: model.cod,
      nh4: model.nh4,
      waterQualityLevel: model.waterQualityLevel,
      areaServed: model.areaServed,
      typeofLocation: model.typeofLocation,
    };
  }
}
