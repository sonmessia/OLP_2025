import { LocationType, type LocationModel } from "./CommonModels";
import type { SensorType } from "./SenSorModel";

export interface WaterQualityObservedModel {
  id: string;
  type: SensorType.WATER_QUALITY;
  dateObserved?: Date;
  location?: LocationModel;

  // Water Quality Parameters
  pH?: number;
  dissolvedOxygen?: number; // DO (mg/L)
  turbidity?: number; // NTU
  temperature?: number;
  conductivity?: number; // µS/cm
  tss?: number; // Total Suspended Solids
  bod?: number; // Biochemical Oxygen Demand
  cod?: number; // Chemical Oxygen Demand
  nh4?: number; // Ammonium

  // Quality Level (custom field)
  waterQualityLevel?: "excellent" | "good" | "moderate" | "poor" | "very_poor";
  areaServed?: string;
  typeofLocation?: LocationType;
}
