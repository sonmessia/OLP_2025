export interface TrafficLocation {
  id: string; // Matches the scenario ID in SumoModels
  name: string;
  coordinates: [number, number]; // [lat, lon] - Leaflet prefers [lat, lon], GeoJSON is [lon, lat]
  description: string;
}

export const TRAFFIC_LOCATIONS: TrafficLocation[] = [
  {
    id: "Nga4ThuDuc",
    name: "Ngã 4 Thủ Đức",
    coordinates: [10.849067, 106.7741],
    description: "Giao lộ Xa Lộ Hà Nội - Võ Văn Ngân",
  },
  {
    id: "NguyenThaiSon",
    name: "Vòng Xoay Nguyễn Thái Sơn",
    coordinates: [10.8168, 106.6785], // Near Gia Dinh Park / Nguyen Thai Son
    description: "Vòng xoay Nguyễn Thái Sơn - Nguyễn Kiệm",
  },
  {
    id: "QuangTrung",
    name: "Ngã 5 Chuồng Chó (Quang Trung)",
    coordinates: [10.813955, 106.678668], // The main 6-way intersection
    description: "Giao lộ Quang Trung - Nguyễn Oanh - Nguyễn Kiệm",
  },
];
