// Copyright (c) 2025 Green Wave Team
// 
// This software is released under the MIT License.
// https://opensource.org/licenses/MIT

// Các Enums chung
export enum GeoJSONType {
  Point = "Point",
  LineString = "LineString",
  Polygon = "Polygon",
  MultiPoint = "MultiPoint",
  MultiLineString = "MultiLineString",
  MultiPolygon = "MultiPolygon",
}

export enum AirQualityType {
  AirQualityObserved = "AirQualityObserved",
}

export enum CarbonFootprintType {
  CarbonFootprint = "CarbonFootprint",
}

export enum WaterQualityType {
  WaterQualityObserved = "WaterQualityObserved",
}

export enum LocationType {
  indoor = "indoor",
  outdoor = "outdoor",
}

// GeoJSON Models (Sử dụng interface đơn giản hơn)
export interface GeoJSONPointModel {
  type: GeoJSONType.Point;
  coordinates: [number, number]; // [longitude, latitude]
  bbox?: number[];
}

// Đối với các loại GeoJSON phức tạp hơn, có thể thêm vào đây:
// export interface GeoJSONLineStringModel { ... }

export type LocationModel = GeoJSONPointModel; // Giả sử chỉ sử dụng Point cho đơn giản

// Address Model
export interface AddressModel {
  addressCountry?: string;
  addressLocality?: string;
  addressRegion?: string;
  district?: string;
  postOfficeBoxNumber?: string;
  postalCode?: string;
  streetAddress?: string;
  streetNr?: string;
}
