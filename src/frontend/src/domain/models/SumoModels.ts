// Domain Models - SUMO Traffic Simulation
// Tuân thủ Clean Architecture: không phụ thuộc vào framework cụ thể

/**
 * Traffic Light Signal State
 */
export interface TrafficLightSignal {
  index: number;
  state: string;
  color: "green" | "yellow" | "red" | "off";
}

/**
 * Traffic Light Information
 */
export interface TrafficLight {
  id: string;
  currentPhase: number;
  phaseDuration: number;
  timeUntilSwitch: number;
  isMain: boolean;
  lights: TrafficLightSignal[];
}

/**
 * SUMO Simulation State
 */
export interface SumoSimulationState {
  simulationTime: number;
  vehicleCount: number;
  avgSpeed: number;
  avgOccupancy: number;
  currentPhase: string;
  loadedVehicles: number;
  departedVehicles: number;
  arrivedVehicles: number;
  queueLength: number;
  waitingTime: number;
  trafficLights: TrafficLight[];
  totalTrafficLights: number;
}

/**
 * SUMO Connection Status
 */
export enum SumoConnectionStatus {
  CONNECTED = "CONNECTED",
  DISCONNECTED = "DISCONNECTED",
  CONNECTING = "CONNECTING",
  ERROR = "ERROR",
}

/**
 * SUMO Status
 */
export interface SumoStatus {
  connected: boolean;
  running?: boolean;
  scenario?: string;
  description?: string;
  tlsId?: string;
  port?: number;
  connectionStatus: SumoConnectionStatus;
}

/**
 * Scenario Information
 */
export interface ScenarioInfo {
  id: string;
  name: string;
  description: string;
  configFile: string;
}

/**
 * AI Control Status
 */
export enum AIControlStatus {
  ENABLED = "ENABLED",
  DISABLED = "DISABLED",
  INITIALIZING = "INITIALIZING",
  ERROR = "ERROR",
}

/**
 * AI Control State
 */
export interface AIControlState {
  status: AIControlStatus;
  numTrafficLights: number;
  algorithm: string;
  features: string[];
  actionCount: number;
  lastDecisionTime?: Date;
}

/**
 * AI Decision
 */
export interface AIDecision {
  tlsId: string;
  action: "switch" | "hold";
  fromPhase: number;
  toPhase: number;
  priorityScore?: number;
  reason?: string;
}

/**
 * AI Step Result
 */
export interface AIStepResult {
  simulationTime: number;
  decisions: AIDecision[];
  totalSwitches: number;
  totalHolds: number;
}

/**
 * SUMO Dashboard State
 * Tổng hợp tất cả thông tin cho dashboard
 */
export interface SumoDashboardState {
  status: SumoStatus;
  simulationState: SumoSimulationState | null;
  aiControlState: AIControlState | null;
  scenarios: ScenarioInfo[];
  lastUpdated: Date;
}

/**
 * SUMO Configuration
 */
export interface SumoConfiguration {
  scenario: string;
  gui: boolean;
  port: number;
}

/**
 * Performance Metrics
 */
export interface PerformanceMetrics {
  avgReward: number;
  avgSpeed: number;
  avgWaitingTime: number;
  throughput: number;
  timestamp: Date;
}

/**
 * Comparison Data
 */
export interface ComparisonData {
  algorithm: string;
  avgReward: number;
  avgSpeed: number;
  waitingTime: number;
  throughput: number;
}

// Factory methods for creating SUMO models
export class SumoModelFactory {
  static createDefaultStatus(): SumoStatus {
    return {
      connected: false,
      connectionStatus: SumoConnectionStatus.DISCONNECTED,
    };
  }

  static createDefaultAIControlState(): AIControlState {
    return {
      status: AIControlStatus.DISABLED,
      numTrafficLights: 0,
      algorithm: "",
      features: [],
      actionCount: 0,
    };
  }

  static createDefaultDashboardState(): SumoDashboardState {
    return {
      status: this.createDefaultStatus(),
      simulationState: null,
      aiControlState: null,
      scenarios: [],
      lastUpdated: new Date(),
    };
  }

  static createConfiguration(
    scenario: string,
    gui: boolean = false,
    port: number = 8813
  ): SumoConfiguration {
    return {
      scenario,
      gui,
      port,
    };
  }
}

// Validation utilities
export class SumoValidator {
  static validateScenario(scenario: string): boolean {
    const validScenarios = ["Nga4ThuDuc", "NguyenThaiSon", "QuangTrung"];
    return validScenarios.includes(scenario);
  }

  static validatePort(port: number): boolean {
    return port >= 1024 && port <= 65535;
  }

  static isConnected(status: SumoStatus): boolean {
    return (
      status.connected &&
      status.connectionStatus === SumoConnectionStatus.CONNECTED
    );
  }

  static isAIEnabled(aiState: AIControlState | null): boolean {
    return aiState?.status === AIControlStatus.ENABLED;
  }
}
