// Copyright (c) 2025 Green Wave Team
// 
// This software is released under the MIT License.
// https://opensource.org/licenses/MIT

/**
 * Traffic simulation data types for frontend
 */

export interface VehicleData {
  id: string;
  lat: number;
  lon: number;
  angle: number;
  speed: number;
  type?: string;
}

export interface TrafficLightState {
  id: string;
  state: string;
  phase: number;
  program: string;
}

export interface TrafficFlowData {
  queues: number[];
  phase: number;
  timestamp: number;
}

export interface AirQualityData {
  pm25: number;
  timestamp: number;
}

export interface SimulationState {
  vehicles: VehicleData[];
  trafficLights: TrafficLightState[];
  trafficFlow: TrafficFlowData;
  airQuality: AirQualityData;
  reward?: number;
}

export interface AreaBounds {
  name: string;
  bounds: [[number, number], [number, number]];
  center: [number, number];
  tlsId: string;
}

export type WebSocketMessage =
  | {
      type: "simulation_update";
      data: SimulationState;
      timestamp: number;
    }
  | {
      type: "command";
      data: { command: string; params?: Record<string, unknown> };
      timestamp: number;
    }
  | {
      type: "error";
      data: { message: string; code?: string };
      timestamp: number;
    }
  | {
      type: "connection";
      data: { status: "connected" | "disconnected"; clientId?: string };
      timestamp: number;
    };

export interface Area {
  id: string;
  name: string;
  bounds: [[number, number], [number, number]];
  center: [number, number];
  tlsId: string;
}
