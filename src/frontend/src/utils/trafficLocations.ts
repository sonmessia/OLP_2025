export interface TrafficLocation {
  id: string; // Matches the scenario ID in SumoModels
  nameKey: string; // Translation key for the name
  descriptionKey: string; // Translation key for the description
  coordinates: [number, number]; // [lat, lon] - Leaflet prefers [lat, lon], GeoJSON is [lon, lat]
}

export const TRAFFIC_LOCATIONS: TrafficLocation[] = [
  {
    id: "Nga4ThuDuc",
    nameKey: "locations.nga4ThuDuc",
    descriptionKey: "locations.description.thuDucCrossroads",
    coordinates: [10.849067, 106.7741],
  },
  {
    id: "NguyenThaiSon",
    nameKey: "locations.nguyenThaiSon",
    descriptionKey: "locations.description.nguyenThaiSonRoundabout",
    coordinates: [10.8168, 106.6785], // Near Gia Dinh Park / Nguyen Thai Son
  },
  {
    id: "QuangTrung",
    nameKey: "locations.quangTrung",
    descriptionKey: "locations.description.quangTrungIntersection",
    coordinates: [10.813955, 106.678668], // The main 6-way intersection
  },
];

// Helper function to get localized traffic locations
export const getLocalizedTrafficLocations = (t: (key: string) => string): Array<Omit<TrafficLocation, 'nameKey' | 'descriptionKey'> & {name: string, description: string}> => {
  return TRAFFIC_LOCATIONS.map(location => ({
    id: location.id,
    name: t(location.nameKey),
    description: t(location.descriptionKey),
    coordinates: location.coordinates
  }));
};
