// Copyright (c) 2025 Green Wave Team
// 
// This software is released under the MIT License.
// https://opensource.org/licenses/MIT

import type { ISumoRepository } from "../../repositories/ISumoRepository";
import type { SumoStatus } from "../../models/SumoModels";

export class GetSumoStatusUseCase {
  constructor(private sumoRepository: ISumoRepository) {}

  async execute(): Promise<SumoStatus> {
    return this.sumoRepository.getStatus();
  }
}
