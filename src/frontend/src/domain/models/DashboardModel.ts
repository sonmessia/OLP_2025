// Domain Models for Manager Dashboard

/**
 * KPI (Key Performance Indicator) Card Data
 */
export interface KPICardModel {
  id: string;
  title: string;
  value: number;
  unit: string;
  trend: "up" | "down" | "stable";
  trendValue: number; // Percentage change
  icon: string;
  color: "green" | "blue" | "yellow" | "red";
}

/**
 * Multi-objective Monitoring Chart Data Point
 */
export interface MonitoringDataPoint {
  timestamp: string; // ISO 8601 format
  avgWaitingTime: number; // seconds
  pm25Level: number; // μg/m³
}

/**
 * AI Reward Distribution Data Point
 */
export interface RewardDataPoint {
  timestamp: string;
  trafficReward: number;
  environmentReward: number;
}

/**
 * Pollution Hotspot on Map
 */
export interface PollutionHotspot {
  id: string;
  name: string;
  latitude: number;
  longitude: number;
  pm25: number;
  aqi: number;
  severity: "low" | "medium" | "high" | "critical";
}

/**
 * Alert/Warning Log Entry
 */
export interface AlertLog {
  id: string;
  timestamp: string;
  type: "warning" | "critical" | "info";
  message: string;
  location?: string;
  resolved: boolean;
}

/**
 * Intervention Action Item
 */
export interface InterventionAction {
  id: string;
  timestamp: string;
  action: string;
  target: string; // e.g., "Intersection A"
  status: "pending" | "in-progress" | "completed";
  aiTriggered: boolean;
}

/**
 * Dashboard State Model (Complete state for Manager Dashboard)
 */
export interface DashboardStateModel {
  kpis: KPICardModel[];
  monitoringData: MonitoringDataPoint[];
  rewardData: RewardDataPoint[];
  pollutionHotspots: PollutionHotspot[];
  alerts: AlertLog[];
  interventions: InterventionAction[];
  lastUpdated: string;
}
