// Copyright (c) 2025 Green Wave Team
// 
// This software is released under the MIT License.
// https://opensource.org/licenses/MIT

import type { ISumoRepository } from "../../domain/repositories/ISumoRepository";
import type {
  SumoStatus,
  SumoConfiguration,
  SumoSimulationState,
  ScenarioInfo,
  AIControlState,
  AIStepResult,
} from "../../domain/models/SumoModels";
import { sumoApi } from "../../api/sumoApi";
import { SumoMapper, SumoReverseMapper } from "../mappers/SumoMapper";

export class SumoRepositoryImpl implements ISumoRepository {
  async getStatus(): Promise<SumoStatus> {
    const dto = await sumoApi.getSumoStatus();
    return SumoMapper.mapSumoStatus(dto);
  }

  async startSimulation(config: SumoConfiguration): Promise<SumoStatus> {
    const requestDto = SumoReverseMapper.mapStartRequest(
      config.scenario,
      config.gui,
      config.port
    );
    await sumoApi.startSumoSimulation(requestDto);
    // The start response contains status info, but we might want to fetch full status or map what we have.
    // The SumoStartResponseDTO has status, message, etc.
    // Let's assume we return a basic status or fetch it again.
    // For now, let's map what we can or fetch status.
    // The interface expects SumoStatus.
    // Let's fetch status to be sure.
    return this.getStatus();
  }

  async getState(): Promise<SumoSimulationState> {
    const dto = await sumoApi.getSumoState();
    return SumoMapper.mapSumoState(dto);
  }

  async executeStep(): Promise<SumoSimulationState> {
    const dto = await sumoApi.executeSumoStep();
    return SumoMapper.mapSumoState(dto.state);
  }

  async stopSimulation(): Promise<void> {
    await sumoApi.stopSumoSimulation();
  }

  async getScenarios(): Promise<ScenarioInfo[]> {
    const dtos = await sumoApi.getSumoScenarios();
    return dtos.map((dto) => SumoMapper.mapScenarioInfo(dto));
  }

  async enableAIControl(): Promise<AIControlState> {
    const dto = await sumoApi.enableAIControl();
    return SumoMapper.mapAIControlState(dto);
  }

  async executeAIStep(): Promise<AIStepResult> {
    const dto = await sumoApi.executeAIStep();
    return SumoMapper.mapAIStepResult(dto);
  }

  async disableAIControl(): Promise<void> {
    await sumoApi.disableAIControl();
  }
}
