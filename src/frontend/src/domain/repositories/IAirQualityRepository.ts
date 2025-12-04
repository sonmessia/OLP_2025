import type { AirQualityObservedModel } from "../models/AirQualityObservedModel";

export interface IAirQualityRepository {
  getAll(): Promise<AirQualityObservedModel[]>;
  getById(id: string): Promise<AirQualityObservedModel>;
}
