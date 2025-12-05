// src/api/sumoApi.ts

import axiosInstance from "../app/config/axiosConfig";
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
 * SUMO API Client
 * API client for SUMO traffic simulation backend
 */
export class SumoApiClient {
  /**
   * Get SUMO connection status
   * @returns Promise with SUMO status information
   */
  async getSumoStatus(): Promise<SumoStatusResponseDTO> {
    try {
      const response = await axiosInstance.get<SumoStatusResponseDTO>(
        "/sumo/status"
      );
      return response.data;
    } catch (error: unknown) {
      console.error("Error fetching SUMO status:", error);
      throw error;
    }
  }

  /**
   * Start SUMO simulation
   * @param request - SUMO start configuration
   * @returns Promise with start response
   */
  async startSumoSimulation(
    request: SumoStartRequestDTO
  ): Promise<SumoStartResponseDTO> {
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
  }

  /**
   * Get current SUMO simulation state
   * @returns Promise with current simulation state
   */
  async getSumoState(): Promise<SumoStateResponseDTO> {
    try {
      const response = await axiosInstance.get<SumoStateResponseDTO>(
        "/sumo/state"
      );
      return response.data;
    } catch (error: unknown) {
      console.error("Error fetching SUMO state:", error);
      throw error;
    }
  }

  /**
   * Execute one simulation step
   * @returns Promise with step response
   */
  async executeSumoStep(): Promise<SumoStepResponseDTO> {
    try {
      const response = await axiosInstance.post<SumoStepResponseDTO>(
        "/sumo/step"
      );
      return response.data;
    } catch (error: unknown) {
      console.error("Error executing SUMO step:", error);
      throw error;
    }
  }

  /**
   * Stop SUMO simulation
   * @returns Promise with stop confirmation
   */
  async stopSumoSimulation(): Promise<{
    status: string;
    message: string;
  }> {
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
  }

  /**
   * Get available scenarios
   * @returns Promise with list of available scenarios
   */
  async getSumoScenarios(): Promise<ScenarioInfoDTO[]> {
    try {
      const response = await axiosInstance.get<ScenarioInfoDTO[]>(
        "/sumo/scenarios"
      );
      return response.data;
    } catch (error: unknown) {
      console.error("Error fetching SUMO scenarios:", error);
      throw error;
    }
  }

  /**
   * Enable AI traffic control
   * @returns Promise with AI control status
   */
  async enableAIControl(): Promise<AIControlResponseDTO> {
    try {
      const response = await axiosInstance.post<AIControlResponseDTO>(
        "/sumo/ai-control"
      );
      return response.data;
    } catch (error: unknown) {
      console.error("Error enabling AI control:", error);
      throw error;
    }
  }

  /**
   * Execute one AI control step
   * @returns Promise with AI decisions
   */
  async executeAIStep(): Promise<AIStepResponseDTO> {
    try {
      const response = await axiosInstance.post<AIStepResponseDTO>(
        "/sumo/ai-step"
      );
      return response.data;
    } catch (error: unknown) {
      console.error("Error executing AI step:", error);
      throw error;
    }
  }

  /**
   * Disable AI traffic control
   * @returns Promise with disable confirmation
   */
  async disableAIControl(): Promise<{
    status: string;
    message: string;
  }> {
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
  }
}

export const sumoApi = new SumoApiClient();
export default sumoApi;
