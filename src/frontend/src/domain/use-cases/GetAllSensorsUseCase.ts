import type { SensorModel } from "../models/SenSorModel";
import type { ISensorRepository } from "../repositories/ISensorRepository";

export class GetAllSensorsUseCase {
  constructor(private repository: ISensorRepository) {}

  async execute(): Promise<SensorModel[]> {
    try {
      return await this.repository.getAllSensors();
    } catch (error) {
      throw new Error("Failed to fetch sensors: " + (error as Error).message);
    }
  }
}
