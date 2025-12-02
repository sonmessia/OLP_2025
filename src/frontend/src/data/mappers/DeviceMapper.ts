import {
  DeviceType,
  ConnectionProtocol,
  DeviceStatus,
  type MQTTConfig,
  type HTTPConfig,
  type AlertThreshold,
  type DeviceModel,
} from "../../domain/models/DeviceModels";

import type {
  DeviceResponseDTO,
  CreateDeviceRequestDTO,
  UpdateDeviceRequestDTO,
} from "../dtos/DeviceDTOs";

export class DeviceMapper {
  static fromDTO(dto: DeviceResponseDTO): DeviceModel {
    return {
      id: dto.id,
      name: dto.device_name,
      type: this.parseDeviceType(dto.device_type),
      manufacturer: dto.manufacturer,
      serialNumber: dto.serial_number,
      installDate: dto.install_date ? new Date(dto.install_date) : undefined,
      protocol: this.parseProtocol(dto.protocol),
      mqttConfig: this.buildMQTTConfig(dto),
      httpConfig: this.buildHTTPConfig(dto),
      location: {
        latitude: dto.latitude,
        longitude: dto.longitude,
        description: dto.location_desc,
      },
      updateInterval: dto.update_interval,
      status: this.parseStatus(dto.status),
      isActive: dto.active_status,
      alertThreshold: this.parseAlertThreshold(dto.alert_threshold),
      createdAt: new Date(dto.created_at),
      updatedAt: new Date(dto.updated_at),
      lastDataReceived: dto.last_data_received
        ? new Date(dto.last_data_received)
        : undefined,
    };
  }

  static toDTO(model: DeviceModel): CreateDeviceRequestDTO {
    return {
      device_name: model.name,
      device_type: model.type,
      manufacturer: model.manufacturer,
      serial_number: model.serialNumber,
      install_date: model.installDate?.toISOString(),
      protocol: model.protocol,
      mqtt_broker_url: model.mqttConfig?.brokerUrl,
      mqtt_port: model.mqttConfig?.port,
      mqtt_topic_sub: model.mqttConfig?.topicSubscribe,
      mqtt_topic_pub: model.mqttConfig?.topicPublish,
      auth_username: model.mqttConfig?.username,
      auth_password: model.mqttConfig?.password,
      ip_address: model.httpConfig?.ipAddress,
      api_endpoint: model.httpConfig?.apiEndpoint,
      rtsp_url: model.httpConfig?.rtspUrl,
      latitude: model.location.latitude,
      longitude: model.location.longitude,
      location_desc: model.location.description,
      update_interval: model.updateInterval,
      active_status: model.isActive,
      alert_threshold: model.alertThreshold
        ? JSON.stringify(model.alertThreshold)
        : undefined,
    };
  }

  static toUpdateDTO(model: DeviceModel): UpdateDeviceRequestDTO {
    return {
      id: model.id,
      ...this.toDTO(model),
    };
  }

  private static parseDeviceType(type: string): DeviceType {
    switch (type) {
      case "TRAFFIC_CAM":
        return DeviceType.TRAFFIC_CAM;
      case "INDUCTIVE_LOOP":
        return DeviceType.INDUCTIVE_LOOP;
      case "RADAR_SENSOR":
        return DeviceType.RADAR_SENSOR;
      case "SMART_LIGHT":
        return DeviceType.SMART_LIGHT;
      case "AIR_QUALITY_SENSOR":
        return DeviceType.AIR_QUALITY_SENSOR;
      default:
        return DeviceType.TRAFFIC_CAM;
    }
  }

  private static parseProtocol(protocol: string): ConnectionProtocol {
    switch (protocol) {
      case "MQTT":
        return ConnectionProtocol.MQTT;
      case "HTTP":
        return ConnectionProtocol.HTTP;
      case "RTSP":
        return ConnectionProtocol.RTSP;
      case "MODBUS_TCP":
        return ConnectionProtocol.MODBUS_TCP;
      case "LORAWAN":
        return ConnectionProtocol.LORAWAN;
      case "COAP":
        return ConnectionProtocol.COAP;
      default:
        return ConnectionProtocol.HTTP;
    }
  }

  private static parseStatus(status: string): DeviceStatus {
    switch (status) {
      case "ONLINE":
        return DeviceStatus.ONLINE;
      case "OFFLINE":
        return DeviceStatus.OFFLINE;
      case "MAINTENANCE":
        return DeviceStatus.MAINTENANCE;
      case "ERROR":
        return DeviceStatus.ERROR;
      default:
        return DeviceStatus.OFFLINE;
    }
  }

  private static buildMQTTConfig(
    dto: DeviceResponseDTO
  ): MQTTConfig | undefined {
    if (!dto.mqtt_topic_sub) return undefined;

    return {
      brokerUrl: dto.mqtt_broker_url,
      port: dto.mqtt_port,
      topicSubscribe: dto.mqtt_topic_sub,
      topicPublish: dto.mqtt_topic_pub,
      username: dto.auth_username,
      password: dto.auth_password,
    };
  }

  private static buildHTTPConfig(
    dto: DeviceResponseDTO
  ): HTTPConfig | undefined {
    if (!dto.ip_address) return undefined;

    return {
      ipAddress: dto.ip_address,
      apiEndpoint: dto.api_endpoint || "/api/v1",
      rtspUrl: dto.rtsp_url,
    };
  }

  private static parseAlertThreshold(
    thresholdStr?: string
  ): AlertThreshold | undefined {
    if (!thresholdStr) return undefined;

    try {
      return JSON.parse(thresholdStr) as AlertThreshold;
    } catch {
      return undefined;
    }
  }
}
