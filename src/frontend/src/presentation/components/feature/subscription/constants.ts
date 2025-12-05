export const AIR_QUALITY_ATTRIBUTES = [
  { value: "airQualityIndex", labelKey: "subscription:attributes.aqi" },
  { value: "pm25", labelKey: "subscription:attributes.pm25" },
  { value: "pm10", labelKey: "subscription:attributes.pm10" },
  { value: "co", labelKey: "subscription:attributes.co" },
  { value: "no2", labelKey: "subscription:attributes.no2" },
  { value: "o3", labelKey: "subscription:attributes.o3" },
  { value: "temperature", labelKey: "subscription:attributes.temperature" },
  { value: "relativeHumidity", labelKey: "subscription:attributes.humidity" },
  { value: "windSpeed", labelKey: "subscription:attributes.windSpeed" },
];

export const TRAFFIC_FLOW_ATTRIBUTES = [
  { value: "vehicleCount", labelKey: "subscription:attributes.vehicleCount" },
  { value: "avgSpeed", labelKey: "subscription:attributes.avgSpeed" },
  { value: "queues", labelKey: "subscription:attributes.queues" },
];

export const OPERATORS = [
  { value: "==", labelKey: "subscription:operators.equals" },
  { value: "!=", labelKey: "subscription:operators.notEquals" },
  { value: ">", labelKey: "subscription:operators.greaterThan" },
  { value: "<", labelKey: "subscription:operators.lessThan" },
  { value: ">=", labelKey: "subscription:operators.greaterThanOrEqual" },
  { value: "<=", labelKey: "subscription:operators.lessThanOrEqual" },
];
