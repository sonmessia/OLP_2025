// Data Transfer Objects - Raw data from API
// Tuân thủ Clean Architecture: định nghĩa chính xác cấu trúc dữ liệu từ server

export interface DeviceResponseDTO {
  id: string;
  device_name: string;
  device_type: string;
  manufacturer?: string;
  serial_number: string;
  install_date?: string; // ISO string
  protocol: string;
  mqtt_broker_url?: string;
  mqtt_port?: number;
  mqtt_topic_sub?: string;
  mqtt_topic_pub?: string;
  auth_username?: string;
  auth_password?: string; // encrypted
  ip_address?: string;
  api_endpoint?: string;
  rtsp_url?: string;
  latitude: number;
  longitude: number;
  location_desc?: string;
  update_interval: number;
  active_status: boolean;
  alert_threshold?: string; // JSON string
  status: string;
  created_at: string; // ISO string
  updated_at: string; // ISO string
  last_data_received?: string; // ISO string
}

export interface CreateDeviceRequestDTO {
  device_name: string;
  device_type: string;
  manufacturer?: string;
  serial_number: string;
  install_date?: string;
  protocol: string;
  // MQTT fields
  mqtt_broker_url?: string;
  mqtt_port?: number;
  mqtt_topic_sub?: string;
  mqtt_topic_pub?: string;
  auth_username?: string;
  auth_password?: string;
  // HTTP fields
  ip_address?: string;
  api_endpoint?: string;
  rtsp_url?: string;
  // Location
  latitude: number;
  longitude: number;
  location_desc?: string;
  // Settings
  update_interval: number;
  active_status: boolean;
  alert_threshold?: string;
}

export interface UpdateDeviceRequestDTO extends Partial<CreateDeviceRequestDTO> {
  id: string;
}

export interface DeviceListResponseDTO {
  devices: DeviceResponseDTO[];
  total: number;
  page: number;
  limit: number;
}

export interface ConnectionTestRequestDTO {
  device_id: string;
  protocol: string;
  mqtt_config?: {
    broker_url: string;
    port: number;
    topic: string;
    username?: string;
    password?: string;
  };
  http_config?: {
    ip_address: string;
    api_endpoint: string;
  };
}

export interface ConnectionTestResponseDTO {
  success: boolean;
  message: string;
  response_time?: number; // ms
  error_details?: string;
}

export interface DeviceStatsResponseDTO {
  device_id: string;
  last_seen: string;
  data_points: number;
  errors: number;
  uptime: number;
}

export interface DeviceFilterDTO {
  device_type?: string;
  status?: string;
  district?: string;
  page?: number;
  limit?: number;
  search?: string;
}