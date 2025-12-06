// Copyright (c) 2025 Green Wave Team
// 
// This software is released under the MIT License.
// https://opensource.org/licenses/MIT

import type { AirQualityObservedDto } from "../dtos/AirQualityDTOs";
import type { AirQualityObservedModel } from "../../domain/models/AirQualityObservedModel";
import { GeoJSONType } from "../../domain/models/CommonModels";
import { SensorType } from "../../domain/models/SenSorModel";

export class AirQualityMapper {
  static toDomain(dto: AirQualityObservedDto): AirQualityObservedModel {
    return {
      id: dto.id,
      type: SensorType.AIR_QUALITY,
      dateObserved: dto.dateObserved ? new Date(dto.dateObserved) : undefined,
      location:
        dto.location && dto.location.type === "Point"
          ? {
              type: GeoJSONType.Point,
              coordinates: dto.location.coordinates as [number, number],
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
    };
  }

  static toDto(model: AirQualityObservedModel): AirQualityObservedDto {
    return {
      id: model.id,
      type: model.type,
      dateObserved: model.dateObserved?.toISOString(),
      location: model.location
        ? {
            type: model.location.type,
            coordinates: model.location.coordinates,
          }
        : undefined,
      airQualityIndex: model.airQualityIndex,
      airQualityLevel: model.airQualityLevel,
      areaServed: model.areaServed,
      co: model.co,
      no2: model.no2,
      o3: model.o3,
      pm10: model.pm10,
      pm25: model.pm25,
      temperature: model.temperature,
      relativeHumidity: model.relativeHumidity,
      windDirection: model.windDirection,
      windSpeed: model.windSpeed,
    };
  }
}
