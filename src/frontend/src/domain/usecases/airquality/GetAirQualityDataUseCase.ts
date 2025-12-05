import type { IAirQualityRepository } from "../../repositories/IAirQualityRepository";
import type { AirQualityObservedModel } from "../../models/AirQualityObservedModel";

export class GetAirQualityDataUseCase {
  constructor(private repository: IAirQualityRepository) {}

  async execute(): Promise<AirQualityObservedModel[]> {
    return await this.repository.getAll();
  }
}
