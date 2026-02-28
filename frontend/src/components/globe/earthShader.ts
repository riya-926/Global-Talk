import * as THREE from 'three';

/** Vertex shader: pass normal and UV */
export const earthVertexShader = /* glsl */ `
  varying vec2 vUv;
  varying vec3 vNormal;

  void main() {
    vUv = uv;
    vNormal = normalize(normalMatrix * normal);
    gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
  }
`;

/** Fragment shader: blend day and night textures by sun direction */
export const earthFragmentShader = /* glsl */ `
  uniform sampler2D dayMap;
  uniform sampler2D nightMap;
  uniform vec3 sunDirection;

  varying vec2 vUv;
  varying vec3 vNormal;

  void main() {
    vec3 N = normalize(vNormal);
    float NdotL = dot(N, sunDirection);
    float blend = smoothstep(-0.08, 0.12, NdotL);

    vec4 dayColor = texture2D(dayMap, vUv);
    vec4 nightColor = texture2D(nightMap, vUv);
    gl_FragColor = mix(nightColor, dayColor, blend);
  }
`;

export interface EarthShaderUniforms {
  dayMap: { value: THREE.Texture | null };
  nightMap: { value: THREE.Texture | null };
  sunDirection: { value: THREE.Vector3 };
}

export function createEarthShaderUniforms(): EarthShaderUniforms {
  return {
    dayMap: { value: null as THREE.Texture | null },
    nightMap: { value: null as THREE.Texture | null },
    sunDirection: { value: new THREE.Vector3(1, 0, 0) },
  };
}
