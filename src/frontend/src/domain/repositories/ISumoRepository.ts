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
