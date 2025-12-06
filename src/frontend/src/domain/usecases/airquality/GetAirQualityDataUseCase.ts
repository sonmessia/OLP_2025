// Copyright (c) 2025 Green Wave Team
// 
// This software is released under the MIT License.
// https://opensource.org/licenses/MIT

import type { IAirQualityRepository } from "../../repositories/IAirQualityRepository";
import type { AirQualityObservedModel } from "../../models/AirQualityObservedModel";

export class GetAirQualityDataUseCase {
  constructor(private repository: IAirQualityRepository) {}

  async execute(): Promise<AirQualityObservedModel[]> {
    return await this.repository.getAll();
  }
}
