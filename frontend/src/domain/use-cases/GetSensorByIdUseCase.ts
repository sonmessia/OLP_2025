import type { SensorModel } from "../models/SenSorModel";
import type { ISensorRepository } from "../repositories/ISensorRepository";

export class GetSensorByIdUseCase {
  constructor(private repository: ISensorRepository) {}

  async execute(id: string): Promise<SensorModel | null> {
    try {
      return await this.repository.getSensorById(id);
    } catch (error) {
      throw new Error(
        "Failed to fetch sensor details: " + (error as Error).message
      );
    }
  }
}
