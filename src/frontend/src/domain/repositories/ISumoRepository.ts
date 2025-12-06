// Copyright (c) 2025 Green Wave Team
// 
// This software is released under the MIT License.
// https://opensource.org/licenses/MIT

import type {
  SumoStatus,
  SumoConfiguration,
  SumoSimulationState,
  ScenarioInfo,
  AIControlState,
  AIStepResult,
} from "../models/SumoModels";

export interface ISumoRepository {
  getStatus(): Promise<SumoStatus>;
  startSimulation(config: SumoConfiguration): Promise<SumoStatus>;
  getState(): Promise<SumoSimulationState>;
  executeStep(): Promise<SumoSimulationState>;
  stopSimulation(): Promise<void>;
  getScenarios(): Promise<ScenarioInfo[]>;
  enableAIControl(): Promise<AIControlState>;
  executeAIStep(): Promise<AIStepResult>;
  disableAIControl(): Promise<void>;
}
