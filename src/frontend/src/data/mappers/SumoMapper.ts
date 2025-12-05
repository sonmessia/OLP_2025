// Mapper - Convert between DTOs and Domain Models
// Tuân thủ Clean Architecture: chuyển đổi dữ liệu giữa các layer

import type {
  TrafficLightSignalDTO,
  TrafficLightDTO,
  SumoStateResponseDTO,
  SumoStatusResponseDTO,
  AIControlResponseDTO,
  AIDecisionDTO,
  AIStepResponseDTO,
  ScenarioInfoDTO,
} from "../dtos/SumoDTOs";

import {
  SumoConnectionStatus,
  AIControlStatus,
} from "../../domain/models/SumoModels";

import type {
  TrafficLightSignal,
  TrafficLight,
  SumoSimulationState,
  SumoStatus,
  ScenarioInfo,
  AIControlState,
  AIDecision,
  AIStepResult,
} from "../../domain/models/SumoModels";

/**
 * SUMO Mapper Class
 */
export class SumoMapper {
  /**
   * Map Traffic Light Signal DTO to Domain Model
   */
  static mapTrafficLightSignal(dto: TrafficLightSignalDTO): TrafficLightSignal {
    return {
      index: dto.index,
      state: dto.state,
      color: this.normalizeColor(dto.color),
    };
  }

  /**
   * Map Traffic Light DTO to Domain Model
   */
  static mapTrafficLight(dto: TrafficLightDTO): TrafficLight {
    return {
      id: dto.id,
      currentPhase: dto.current_phase,
      phaseDuration: dto.phase_duration,
      timeUntilSwitch: dto.time_until_switch,
      isMain: dto.is_main,
      lights: dto.lights.map((light) => this.mapTrafficLightSignal(light)),
    };
  }

  /**
   * Map SUMO State DTO to Domain Model
   */
  static mapSumoState(dto: SumoStateResponseDTO): SumoSimulationState {
    return {
      simulationTime: dto.simulation_time,
      vehicleCount: dto.vehicle_count,
      avgSpeed: dto.avg_speed,
      avgOccupancy: dto.avg_occupancy,
      currentPhase: dto.current_phase,
      loadedVehicles: dto.loaded_vehicles,
      departedVehicles: dto.departed_vehicles,
      arrivedVehicles: dto.arrived_vehicles,
      queueLength: dto.queue_length,
      waitingTime: dto.waiting_time,
      trafficLights: dto.traffic_lights.map((tl) => this.mapTrafficLight(tl)),
      totalTrafficLights: dto.total_traffic_lights,
    };
  }

  /**
   * Map SUMO Status DTO to Domain Model
   */
  static mapSumoStatus(dto: SumoStatusResponseDTO): SumoStatus {
    return {
      connected: dto.connected,
      running: dto.running,
      scenario: dto.scenario,
      description: dto.description,
      tlsId: dto.tls_id,
      port: dto.port,
      connectionStatus: this.mapConnectionStatus(dto.connected),
    };
  }

  /**
   * Map AI Control Response DTO to Domain Model
   */
  static mapAIControlState(dto: AIControlResponseDTO): AIControlState {
    return {
      status: this.mapAIControlStatus(dto.status),
      numTrafficLights: dto.num_traffic_lights,
      algorithm: dto.algorithm,
      features: dto.features,
      actionCount: 0,
      lastDecisionTime: new Date(),
    };
  }

  /**
   * Map AI Decision DTO to Domain Model
   */
  /**
   * Map AI Decision DTO to Domain Model
   */
  static mapAIDecision(dto: AIDecisionDTO): AIDecision {
    const action =
      dto.action === "switch" || dto.action === "hold" ? dto.action : "hold";

    return {
      tlsId: dto.tls_id,
      action: action,
      fromPhase: dto.from_phase,
      toPhase: dto.to_phase,
      priorityScore: dto.priority_score,
      reason: dto.reason,
    };
  }

  /**
   * Map AI Step Response DTO to Domain Model
   */
  static mapAIStepResult(dto: AIStepResponseDTO): AIStepResult {
    return {
      simulationTime: dto.simulation_time,
      decisions: dto.decisions.map((d) => this.mapAIDecision(d)),
      totalSwitches: dto.total_switches,
      totalHolds: dto.total_holds,
    };
  }

  /**
   * Map Scenario Info DTO to Domain Model
   */
  static mapScenarioInfo(dto: ScenarioInfoDTO): ScenarioInfo {
    return {
      id: dto.id,
      name: dto.name,
      description: dto.description,
      configFile: dto.config_file,
    };
  }

  /**
   * Helper: Normalize color string
   */
  private static normalizeColor(
    color: string
  ): "green" | "yellow" | "red" | "off" {
    const normalized = color.toLowerCase();
    if (normalized === "green" || normalized === "g") return "green";
    if (normalized === "yellow" || normalized === "y") return "yellow";
    if (normalized === "red" || normalized === "r") return "red";
    return "off";
  }

  /**
   * Helper: Map connection status
   */
  private static mapConnectionStatus(connected: boolean): SumoConnectionStatus {
    return connected
      ? SumoConnectionStatus.CONNECTED
      : SumoConnectionStatus.DISCONNECTED;
  }

  /**
   * Helper: Map AI control status
   */
  private static mapAIControlStatus(status: string): AIControlStatus {
    const upperStatus = status.toUpperCase();
    if (upperStatus === "SUCCESS" || upperStatus === "ENABLED") {
      return AIControlStatus.ENABLED;
    }
    if (upperStatus === "INITIALIZING") {
      return AIControlStatus.INITIALIZING;
    }
    if (upperStatus === "ERROR") {
      return AIControlStatus.ERROR;
    }
    return AIControlStatus.DISABLED;
  }
}

/**
 * Reverse Mapper - Domain Model to DTO (for requests)
 */
export class SumoReverseMapper {
  /**
   * Map Domain Configuration to Start Request DTO
   */
  static mapStartRequest(
    scenario: string,
    gui: boolean = false,
    port: number = 8813
  ) {
    return {
      scenario,
      gui,
      port,
    };
  }
}
