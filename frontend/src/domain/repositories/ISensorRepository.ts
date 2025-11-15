import type { SensorModel } from "../models/SenSorModel";

export interface ISensorRepository {
  getAllSensors(): Promise<SensorModel[]>;
  getSensorById(id: string): Promise<SensorModel | null>;
  refreshSensors(): Promise<SensorModel[]>;
}
