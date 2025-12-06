// Copyright (c) 2025 Green Wave Team
// 
// This software is released under the MIT License.
// https://opensource.org/licenses/MIT

// Domain Models - Thiết bị IoT
// Tuân thủ Clean Architecture: không phụ thuộc vào framework cụ thể

export enum DeviceType {
  TRAFFIC_CAM = "TRAFFIC_CAM",
  INDUCTIVE_LOOP = "INDUCTIVE_LOOP",
  RADAR_SENSOR = "RADAR_SENSOR",
  SMART_LIGHT = "SMART_LIGHT",
  AIR_QUALITY_SENSOR = "AIR_QUALITY_SENSOR",
}

export enum ConnectionProtocol {
  MQTT = "MQTT",
  HTTP = "HTTP",
  RTSP = "RTSP",
  MODBUS_TCP = "MODBUS_TCP",
  LORAWAN = "LORAWAN",
  COAP = "COAP",
}

export enum DeviceStatus {
  ONLINE = "ONLINE",
  OFFLINE = "OFFLINE",
  MAINTENANCE = "MAINTENANCE",
  ERROR = "ERROR",
}

export interface Geolocation {
  latitude: number;
  longitude: number;
  description?: string;
}

export interface MQTTConfig {
  brokerUrl?: string;
  port?: number;
  topicSubscribe: string;
  topicPublish?: string;
  username?: string;
  password?: string;
}

export interface HTTPConfig {
  ipAddress: string;
  apiEndpoint?: string;
  rtspUrl?: string;
}

export interface AlertThreshold {
  pm25?: number;
  pm10?: number;
  co?: number;
  no2?: number;
  temperature?: { min: number; max: number };
  humidity?: { min: number; max: number };
  trafficVolume?: { min: number; max: number };
}

export interface DeviceModel {
  // General Information
  id: string;
  name: string;
  type: DeviceType;
  manufacturer?: string;
  serialNumber: string;
  installDate?: Date;

  // Connection Configuration
  protocol: ConnectionProtocol;
  mqttConfig?: MQTTConfig;
  httpConfig?: HTTPConfig;

  // Location
  location: Geolocation;

  // Operational Settings
  updateInterval: number; // seconds
  status: DeviceStatus;
  isActive: boolean;
  alertThreshold?: AlertThreshold;

  // Metadata
  createdAt: Date;
  updatedAt: Date;
  lastDataReceived?: Date;
}

export interface DeviceStats {
  deviceId: string;
  lastSeen: Date;
  dataPoints: number;
  errors: number;
  uptime: number; // percentage
}

// Factory methods for creating devices
export class DeviceFactory {
  static createTrafficCamera(data: Partial<DeviceModel>): DeviceModel {
    return {
      id: data.id || "",
      name: data.name || "",
      type: DeviceType.TRAFFIC_CAM,
      manufacturer: data.manufacturer,
      serialNumber: data.serialNumber || "",
      installDate: data.installDate,
      protocol: data.protocol || ConnectionProtocol.RTSP,
      httpConfig: data.httpConfig,
      location: data.location || { latitude: 0, longitude: 0 },
      updateInterval: data.updateInterval || 30,
      status: DeviceStatus.OFFLINE,
      isActive: data.isActive ?? true,
      createdAt: data.createdAt || new Date(),
      updatedAt: data.updatedAt || new Date(),
      ...data,
    };
  }

  static createAirQualitySensor(data: Partial<DeviceModel>): DeviceModel {
    return {
      id: data.id || "",
      name: data.name || "",
      type: DeviceType.AIR_QUALITY_SENSOR,
      manufacturer: data.manufacturer,
      serialNumber: data.serialNumber || "",
      installDate: data.installDate,
      protocol: data.protocol || ConnectionProtocol.MQTT,
      mqttConfig: data.mqttConfig,
      location: data.location || { latitude: 0, longitude: 0 },
      updateInterval: data.updateInterval || 60,
      status: DeviceStatus.OFFLINE,
      isActive: data.isActive ?? true,
      alertThreshold: data.alertThreshold,
      createdAt: data.createdAt || new Date(),
      updatedAt: data.updatedAt || new Date(),
      ...data,
    };
  }

  static createSmartLight(data: Partial<DeviceModel>): DeviceModel {
    return {
      id: data.id || "",
      name: data.name || "",
      type: DeviceType.SMART_LIGHT,
      manufacturer: data.manufacturer,
      serialNumber: data.serialNumber || "",
      installDate: data.installDate,
      protocol: data.protocol || ConnectionProtocol.MQTT,
      mqttConfig: data.mqttConfig,
      location: data.location || { latitude: 0, longitude: 0 },
      updateInterval: data.updateInterval || 10,
      status: DeviceStatus.OFFLINE,
      isActive: data.isActive ?? true,
      createdAt: data.createdAt || new Date(),
      updatedAt: data.updatedAt || new Date(),
      ...data,
    };
  }
}

// Validation utilities
export class DeviceValidator {
  static validateLocation(location: Geolocation): boolean {
    return (
      location.latitude >= -90 &&
      location.latitude <= 90 &&
      location.longitude >= -180 &&
      location.longitude <= 180
    );
  }

  static validateMQTTConfig(config: MQTTConfig): boolean {
    return !!(config.topicSubscribe && config.topicSubscribe.length > 0);
  }

  static validateHTTPConfig(config: HTTPConfig): boolean {
    const ipRegex =
      /^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/;
    const isIpValid = ipRegex.test(config.ipAddress);
    const isApiEndpointValid =
      config.apiEndpoint === undefined || config.apiEndpoint.length > 0;
    return isIpValid && isApiEndpointValid;
  }

  static validateSerialNumber(serial: string): boolean {
    return serial.length >= 3 && serial.length <= 50;
  }
}
