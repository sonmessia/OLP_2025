import type { AirQualityObservedModel } from "./AirQualityObservedModel";
import type { WaterQualityObservedModel } from "./WaterQualityObservedModel";

export type SensorModel = AirQualityObservedModel | WaterQualityObservedModel;

export enum SensorType {
  AIR_QUALITY = "AirQualityObserved",
  WATER_QUALITY = "WaterQualityObserved",
}
