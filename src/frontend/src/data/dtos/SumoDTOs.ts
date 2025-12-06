// Copyright (c) 2025 Green Wave Team
// 
// This software is released under the MIT License.
// https://opensource.org/licenses/MIT

// Data Transfer Objects - Raw data from SUMO API
// Tuân thủ Clean Architecture: định nghĩa chính xác cấu trúc dữ liệu từ server

/**
 * Traffic Light Signal DTO
 */
export interface TrafficLightSignalDTO {
  index: number;
  state: string;
  color: string;
}

/**
 * Traffic Light DTO
 */
export interface TrafficLightDTO {
  id: string;
  current_phase: number;
  phase_duration: number;
  time_until_switch: number;
  is_main: boolean;
  lights: TrafficLightSignalDTO[];
}

/**
 * SUMO State Response DTO
 */
export interface SumoStateResponseDTO {
  simulation_time: number;
  vehicle_count: number;
  avg_speed: number;
  avg_occupancy: number;
  current_phase: string;
  loaded_vehicles: number;
  departed_vehicles: number;
  arrived_vehicles: number;
  queue_length: number;
  waiting_time: number;
  traffic_lights: TrafficLightDTO[];
  total_traffic_lights: number;
}

/**
 * SUMO Status Response DTO
 */
export interface SumoStatusResponseDTO {
  connected: boolean;
  running?: boolean;
  scenario?: string;
  description?: string;
  tls_id?: string;
  port?: number;
}

/**
 * SUMO Start Request DTO
 */
export interface SumoStartRequestDTO {
  scenario: string;
  gui?: boolean;
  port?: number;
}

/**
 * SUMO Start Response DTO
 */
export interface SumoStartResponseDTO {
  status: string;
  message: string;
  description: string;
  tls_id: string;
  scenario: string;
  initial_state?: SumoStateResponseDTO;
}

/**
 * SUMO Step Response DTO
 */
export interface SumoStepResponseDTO {
  time: number;
  state: SumoStateResponseDTO;
  step_count?: number;
}

/**
 * AI Control Response DTO
 */
export interface AIControlResponseDTO {
  status: string;
  message: string;
  num_traffic_lights: number;
  algorithm: string;
  features: string[];
}

/**
 * AI Decision DTO
 */
export interface AIDecisionDTO {
  tls_id: string;
  action: string;
  from_phase: number;
  to_phase: number;
  priority_score?: number;
  reason?: string;
}

/**
 * AI Step Response DTO
 */
export interface AIStepResponseDTO {
  simulation_time: number;
  decisions: AIDecisionDTO[];
  total_switches: number;
  total_holds: number;
}

/**
 * Scenario Info DTO
 */
export interface ScenarioInfoDTO {
  id: string;
  name: string;
  description: string;
  config_file: string;
}

/**
 * Generic Response DTO
 */
export interface GenericResponseDTO {
  status: string;
  message: string;
}

/**
 * Error Response DTO
 */
export interface SumoErrorResponseDTO {
  detail: string;
  error?: string;
  status_code?: number;
}
