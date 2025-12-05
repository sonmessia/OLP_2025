export interface AirQualityObservedDto {
  id: string;
  type: string;
  dateObserved?: string;
  location?: {
    type: string;
    coordinates: number[];
  };
  airQualityIndex?: number;
  airQualityLevel?: string;
  areaServed?: string;
  co?: number;
  no2?: number;
  o3?: number;
  pm10?: number;
  pm25?: number;
  temperature?: number;
  relativeHumidity?: number;
  windDirection?: number;
  windSpeed?: number;
  typeofLocation?: string;
}
