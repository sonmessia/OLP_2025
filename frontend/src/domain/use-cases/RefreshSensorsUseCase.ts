import type { SensorModel } from "../models/SenSorModel";
import type { ISensorRepository } from "../repositories/ISensorRepository";

export class RefreshSensorsUseCase {
  constructor(private repository: ISensorRepository) {}

  async execute(): Promise<SensorModel[]> {
    try {
      return await this.repository.refreshSensors();
    } catch (error) {
      throw new Error("Failed to refresh sensors: " + (error as Error).message);
    }
  }
}
