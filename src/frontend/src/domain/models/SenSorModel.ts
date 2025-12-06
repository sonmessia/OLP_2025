// Copyright (c) 2025 Green Wave Team
// 
// This software is released under the MIT License.
// https://opensource.org/licenses/MIT

import type { AirQualityObservedModel } from "./AirQualityObservedModel";
import type { WaterQualityObservedModel } from "./WaterQualityObservedModel";

export type SensorModel = AirQualityObservedModel | WaterQualityObservedModel;

export enum SensorType {
  AIR_QUALITY = "AirQualityObserved",
  WATER_QUALITY = "WaterQualityObserved",
}
