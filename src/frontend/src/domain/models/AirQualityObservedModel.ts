import { LocationType, type LocationModel } from "./CommonModels";
import type { SensorType } from "./SenSorModel";

// Mô hình Miền (Domain Model) cho AirQualityObserved
// Loại bỏ các trường kỹ thuật (id, dateCreated, owner, v.v.) và các trường Optional không cần thiết
export interface AirQualityObservedModel {
  // Thuộc tính cốt lõi (Bắt buộc hoặc cần thiết trong miền logic)
  id: string; // Giả định id là bắt buộc sau khi được truy xuất từ API
  type: SensorType.AIR_QUALITY;
  dateObserved?: Date; // Dùng Date thay vì AwareDatetime
  location?: LocationModel;

  // Thuộc tính Chất lượng Không khí
  airQualityIndex?: number;
  airQualityLevel?: string;
  areaServed?: string;

  // Các chất gây ô nhiễm
  co?: number; // Carbon Monoxide
  no2?: number; // Nitrogen dioxide
  o3?: number; // Ozone
  pm10?: number;
  pm25?: number;

  // Thông tin thêm
  temperature?: number;
  relativeHumidity?: number; // 0.0 đến 1.0
  windDirection?: number; // -180.0 đến 180.0
  windSpeed?: number;
  typeofLocation?: LocationType;
}
