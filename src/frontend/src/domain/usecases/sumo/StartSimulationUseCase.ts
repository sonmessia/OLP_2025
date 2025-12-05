import type { ISumoRepository } from "../../repositories/ISumoRepository";
import type { SumoConfiguration, SumoStatus } from "../../models/SumoModels";

export class StartSimulationUseCase {
  constructor(private sumoRepository: ISumoRepository) {}

  async execute(config: SumoConfiguration): Promise<SumoStatus> {
    return this.sumoRepository.startSimulation(config);
  }
}
