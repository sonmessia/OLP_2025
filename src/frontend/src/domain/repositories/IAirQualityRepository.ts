// Copyright (c) 2025 Green Wave Team
// 
// This software is released under the MIT License.
// https://opensource.org/licenses/MIT

import type { AirQualityObservedModel } from "../models/AirQualityObservedModel";

export interface IAirQualityRepository {
  getAll(): Promise<AirQualityObservedModel[]>;
  getById(id: string): Promise<AirQualityObservedModel>;
}
