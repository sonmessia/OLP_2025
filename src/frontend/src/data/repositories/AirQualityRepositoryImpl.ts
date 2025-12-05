import type { IAirQualityRepository } from "../../domain/repositories/IAirQualityRepository";
import type { AirQualityObservedModel } from "../../domain/models/AirQualityObservedModel";
import { airQualityApi } from "../../api/airQualityApi";
import { AirQualityMapper } from "../mappers/AirQualityMapper";

export class AirQualityRepositoryImpl implements IAirQualityRepository {
  async getAll(): Promise<AirQualityObservedModel[]> {
    const dtos = await airQualityApi.getAll();
    console.log(dtos);
    if (typeof dtos === "number") {
      return []; // Handle the case where API might return a number (count)
    }
    return dtos.map((dto) => AirQualityMapper.toDomain(dto));
  }

  async getById(id: string): Promise<AirQualityObservedModel> {
    const dto = await airQualityApi.getById(id);
    return AirQualityMapper.toDomain(dto);
  }
}
