/**
 * SUMO API Client
 * API client for SUMO traffic simulation backend
 */

import axiosInstance from "./axiosConfig";
import type {
  SumoStatusResponseDTO,
  SumoStartRequestDTO,
  SumoStartResponseDTO,
  SumoStateResponseDTO,
  SumoStepResponseDTO,
  AIControlResponseDTO,
  AIStepResponseDTO,
  ScenarioInfoDTO,
} from "../data/dtos/SumoDTOs";

/**
 * Get SUMO connection status
 * @returns Promise with SUMO status information
 */
export const getSumoStatus = async (): Promise<SumoStatusResponseDTO> => {
  try {
    const response = await axiosInstance.get<SumoStatusResponseDTO>(
      "/sumo/status"
    );
    return response.data;
  } catch (error: unknown) {
    console.error("Error fetching SUMO status:", error);
    throw error;
  }
};

/**
 * Start SUMO simulation
 * @param request - SUMO start configuration
 * @returns Promise with start response
 */
export const startSumoSimulation = async (
  request: SumoStartRequestDTO
): Promise<SumoStartResponseDTO> => {
  try {
    const response = await axiosInstance.post<SumoStartResponseDTO>(
      "/sumo/start",
      request
    );
    return response.data;
  } catch (error: unknown) {
    console.error("Error starting SUMO simulation:", error);
    throw error;
  }
};

/**
 * Get current SUMO simulation state
 * @returns Promise with current simulation state
 */
export const getSumoState = async (): Promise<SumoStateResponseDTO> => {
  try {
    const response = await axiosInstance.get<SumoStateResponseDTO>(
      "/sumo/state"
    );
    return response.data;
  } catch (error: unknown) {
    console.error("Error fetching SUMO state:", error);
    throw error;
  }
};

/**
 * Execute one simulation step
 * @returns Promise with step response
 */
export const executeSumoStep = async (): Promise<SumoStepResponseDTO> => {
  try {
    const response = await axiosInstance.post<SumoStepResponseDTO>(
      "/sumo/step"
    );
    return response.data;
  } catch (error: unknown) {
    console.error("Error executing SUMO step:", error);
    throw error;
  }
};

/**
 * Stop SUMO simulation
 * @returns Promise with stop confirmation
 */
export const stopSumoSimulation = async (): Promise<{
  status: string;
  message: string;
}> => {
  try {
    const response = await axiosInstance.post<{
      status: string;
      message: string;
    }>("/sumo/stop");
    return response.data;
  } catch (error: unknown) {
    console.error("Error stopping SUMO simulation:", error);
    throw error;
  }
};

/**
 * Get available scenarios
 * @returns Promise with list of available scenarios
 */
export const getSumoScenarios = async (): Promise<ScenarioInfoDTO[]> => {
  try {
    const response = await axiosInstance.get<ScenarioInfoDTO[]>(
      "/sumo/scenarios"
    );
    return response.data;
  } catch (error: unknown) {
    console.error("Error fetching SUMO scenarios:", error);
    throw error;
  }
};

/**
 * Enable AI traffic control
 * @returns Promise with AI control status
 */
export const enableAIControl = async (): Promise<AIControlResponseDTO> => {
  try {
    const response = await axiosInstance.post<AIControlResponseDTO>(
      "/sumo/ai-control"
    );
    return response.data;
  } catch (error: unknown) {
    console.error("Error enabling AI control:", error);
    throw error;
  }
};

/**
 * Execute one AI control step
 * @returns Promise with AI decisions
 */
export const executeAIStep = async (): Promise<AIStepResponseDTO> => {
  try {
    const response = await axiosInstance.post<AIStepResponseDTO>(
      "/sumo/ai-step"
    );
    return response.data;
  } catch (error: unknown) {
    console.error("Error executing AI step:", error);
    throw error;
  }
};

/**
 * Disable AI traffic control
 * @returns Promise with disable confirmation
 */
export const disableAIControl = async (): Promise<{
  status: string;
  message: string;
}> => {
  try {
    const response = await axiosInstance.post<{
      status: string;
      message: string;
    }>("/sumo/ai-disable");
    return response.data;
  } catch (error: unknown) {
    console.error("Error disabling AI control:", error);
    throw error;
  }
};

// Export all SUMO API functions as a single object
export const sumoApi = {
  getSumoStatus,
  startSumoSimulation,
  getSumoState,
  executeSumoStep,
  stopSumoSimulation,
  getSumoScenarios,
  enableAIControl,
  executeAIStep,
  disableAIControl,
};

export default sumoApi;
