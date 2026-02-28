export interface CityMarker {
  id: string;
  name: string;
  lat: number;
  lon: number;
}

/** Purple "signal" marker locations: US East, Canada, Midwest, California, India, Europe */
export const CITY_MARKERS: CityMarker[] = [
  { id: 'nyc', name: 'New York', lat: 40.7128, lon: -74.006 },
  { id: 'dc', name: 'Washington, D.C.', lat: 38.9072, lon: -77.0369 },
  { id: 'boston', name: 'Boston', lat: 42.3601, lon: -71.0589 },
  { id: 'toronto', name: 'Toronto', lat: 43.6532, lon: -79.3832 },
  { id: 'montreal', name: 'Montreal', lat: 45.5017, lon: -73.5673 },
  { id: 'chicago', name: 'Chicago', lat: 41.8781, lon: -87.6298 },
  { id: 'sf', name: 'San Francisco', lat: 37.7749, lon: -122.4194 },
  { id: 'la', name: 'Los Angeles', lat: 34.0522, lon: -118.2437 },
  { id: 'newdelhi', name: 'New Delhi', lat: 28.6139, lon: 77.209 },
  { id: 'hyderabad', name: 'Hyderabad', lat: 17.385, lon: 78.4867 },
  { id: 'london', name: 'London', lat: 51.5074, lon: -0.1278 },
  { id: 'paris', name: 'Paris', lat: 48.8566, lon: 2.3522 },
  { id: 'berlin', name: 'Berlin', lat: 52.52, lon: 13.405 },
];
