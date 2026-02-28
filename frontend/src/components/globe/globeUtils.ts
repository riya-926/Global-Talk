import * as THREE from 'three';

/**
 * Convert latitude/longitude (degrees) to a 3D position on a sphere.
 * Lat: -90 (south) to 90 (north). Lon: -180 (west) to 180 (east).
 * Y-up: (0,1,0) is north pole; equator in XZ plane.
 */
export function latLonToVector3(
  lat: number,
  lon: number,
  radius: number,
  target = new THREE.Vector3()
): THREE.Vector3 {
  const phi = ((90 - lat) * Math.PI) / 180;
  const theta = ((lon + 180) * Math.PI) / 180;
  target.set(
    -radius * Math.sin(phi) * Math.cos(theta),
    radius * Math.cos(phi),
    radius * Math.sin(phi) * Math.sin(theta)
  );
  return target;
}

/**
 * Compute sun direction in world space (unit vector from Earth center toward the sun).
 * Approximates sun position from UTC date/time for a believable terminator.
 * Uses simplified solar position: declination from day-of-year, hour angle from UTC hour.
 */
export function getSunDirection(date: Date): THREE.Vector3 {
  const utc = date.getTime() + date.getTimezoneOffset() * 60 * 1000;
  const d = new Date(utc);
  const dayOfYear =
    (Date.UTC(d.getUTCFullYear(), d.getUTCMonth(), d.getUTCDate()) -
      Date.UTC(d.getUTCFullYear(), 0, 0)) /
    (24 * 60 * 60 * 1000);
  const hour = d.getUTCHours() + d.getUTCMinutes() / 60 + d.getUTCSeconds() / 3600;

  // Solar declination (approx): -23.44° to +23.44°
  const declination =
    (23.44 * Math.PI) / 180 * Math.sin((2 * Math.PI * (dayOfYear - 81)) / 365);
  // Solar longitude: noon at Greenwich = 0; 15° per hour
  const lonRad = ((hour - 12) * 15 * Math.PI) / 180;

  // Sun position (unit sphere): lat = 90 - declination, lon = lonRad
  const phi = Math.PI / 2 - declination;
  const theta = lonRad;
  // Direction FROM earth TO sun (for lighting: light comes from this direction)
  return new THREE.Vector3(
    Math.sin(phi) * Math.cos(theta),
    Math.cos(phi),
    -Math.sin(phi) * Math.sin(theta)
  );
}
