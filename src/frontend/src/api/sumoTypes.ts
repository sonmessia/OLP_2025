// Copyright (c) 2025 Green Wave Team
// 
// This software is released under the MIT License.
// https://opensource.org/licenses/MIT

/**
 * SUMO API Types
 * Types for SUMO traffic simulation API
 */

// Traffic Light Signal State
export interface TrafficLightSignal {
  index: number;
  state: string;
  color: "green" | "yellow" | "red" | "off";
}

// Traffic Light Information
export interface TrafficLight {
  id: string;
  current_phase: number;
  phase_duration: number;
  time_until_switch: number;
  is_main: boolean;
  lights: TrafficLightSignal[];
}

// SUMO Simulation State
export interface SumoState {
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
  traffic_lights: TrafficLight[];
  total_traffic_lights: number;
}

// SUMO Status Response
export interface SumoStatus {
  connected: boolean;
  running?: boolean;
  scenario?: string;
  description?: string;
  tls_id?: string;
  port?: number;
}

// SUMO Start Request
export interface SumoStartRequest {
  scenario: string;
  gui?: boolean;
  port?: number;
}

// SUMO Start Response
export interface SumoStartResponse {
  status: string;
  message: string;
  description: string;
  tls_id: string;
  scenario: string;
  initial_state?: SumoState;
}

// SUMO Step Response
export interface SumoStepResponse {
  time: number;
  state: SumoState;
  step_count?: number;
}

// AI Control Response
export interface AIControlResponse {
  status: string;
  message: string;
  num_traffic_lights: number;
  algorithm: string;
  features: string[];
}

// AI Decision
export interface AIDecision {
  tls_id: string;
  action: "switch" | "hold";
  from_phase: number;
  to_phase: number;
  priority_score?: number;
  reason?: string;
}

// AI Step Response
export interface AIStepResponse {
  simulation_time: number;
  decisions: AIDecision[];
  total_switches: number;
  total_holds: number;
}

// Scenario Information
export interface ScenarioInfo {
  id: string;
  name: string;
  description: string;
  config_file: string;
}

// Error Response
export interface SumoErrorResponse {
  detail: string;
  error?: string;
}
