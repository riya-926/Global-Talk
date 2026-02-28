/**
 * Earth texture URLs. Prefer local /public/textures/ for performance and offline.
 * Fallback to CDN if local load fails.
 */
const BASE = typeof window !== 'undefined' ? '' : '';

export const EARTH_TEXTURE_URLS = {
  /** Daytime diffuse (albedo) - continents and oceans */
  day: `${BASE}/textures/earth-day.jpg`,
  /** Night lights (cities) - used on dark side */
  night: `${BASE}/textures/earth-night.jpg`,
  /** Normal/bump for surface detail */
  normal: `${BASE}/textures/earth-normal.jpg`,
} as const;

/** CDN fallbacks (use if local textures are missing) */
export const EARTH_TEXTURE_CDN = {
  day: 'https://threejs.org/examples/textures/planets/earth_atmos_2048.jpg',
  night: 'https://unpkg.com/three-globe@2.24.3/example/img/earth-night.jpg',
  normal: 'https://threejs.org/examples/textures/planets/earth_normal_2048.jpg',
} as const;
