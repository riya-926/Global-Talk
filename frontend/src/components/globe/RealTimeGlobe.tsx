import React, {
  useRef,
  useMemo,
  useState,
  useEffect,
  useCallback,
  Suspense,
} from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, Html } from '@react-three/drei';
import * as THREE from 'three';
import { latLonToVector3 } from './globeUtils';
import { EARTH_TEXTURE_URLS, EARTH_TEXTURE_CDN } from './textureUrls';
import { CITY_MARKERS } from './cityMarkers';

const EARTH_RADIUS = 1;
const AUTO_ROTATE_SPEED = 0.06;
const MARKER_RADIUS = 0.028;
const MARKER_PULSE_SPEED = 0.8;

function loadTexture(url: string): Promise<THREE.Texture> {
  return new Promise((resolve, reject) => {
    const loader = new THREE.TextureLoader();
    loader.load(
      url,
      (tex) => {
        tex.colorSpace = THREE.SRGBColorSpace;
        tex.wrapS = tex.wrapT = THREE.RepeatWrapping;
        tex.minFilter = THREE.LinearFilter;
        tex.magFilter = THREE.LinearFilter;
        tex.anisotropy = 1;
        tex.generateMipmaps = false;
        // Zoom out texture so more ocean is visible, continents less dominant
        tex.repeat.set(1.38, 1.38);
        tex.offset.set(0.115, 0.115);
        resolve(tex);
      },
      undefined,
      reject
    );
  });
}

async function loadDayTexture(): Promise<THREE.Texture> {
  const local = EARTH_TEXTURE_URLS.day;
  const cdn = EARTH_TEXTURE_CDN.day;
  try {
    return await loadTexture(local);
  } catch {
    return loadTexture(cdn);
  }
}

interface EarthSphereProps {
  dayTexture: THREE.Texture | null;
}

function EarthSphere({ dayTexture }: EarthSphereProps) {
  const geometry = useMemo(() => new THREE.SphereGeometry(EARTH_RADIUS, 48, 48), []);

  if (!dayTexture) return null;

  return (
    <mesh geometry={geometry}>
      <meshStandardMaterial
        map={dayTexture}
        color={0xd4e8f7}
        side={THREE.FrontSide}
        metalness={0.02}
        roughness={0.9}
      />
    </mesh>
  );
}

function CityMarker({
  lat,
  lon,
  name,
  pulseOffset,
}: {
  lat: number;
  lon: number;
  name: string;
  pulseOffset: number;
}) {
  const meshRef = useRef<THREE.Mesh>(null);
  const [hovered, setHovered] = useState(false);

  const position = useMemo(() => {
    const v = latLonToVector3(lat, lon, EARTH_RADIUS + 0.02);
    return [v.x, v.y, v.z] as [number, number, number];
  }, [lat, lon]);

  useFrame((state) => {
    const mat = meshRef.current?.material as THREE.MeshBasicMaterial | undefined;
    if (!mat?.emissive) return;
    const t = state.clock.elapsedTime * MARKER_PULSE_SPEED + pulseOffset;
    mat.emissiveIntensity = 0.45 + 0.2 * Math.sin(t);
  });

  return (
    <group position={position}>
      <mesh
        ref={meshRef}
        onPointerOver={(e) => {
          e.stopPropagation();
          setHovered(true);
          document.body.style.cursor = 'pointer';
        }}
        onPointerOut={() => {
          setHovered(false);
          document.body.style.cursor = 'default';
        }}
      >
        <sphereGeometry args={[MARKER_RADIUS, 12, 12]} />
        <meshBasicMaterial
          color="#a78bfa"
          emissive="#7c3aed"
          emissiveIntensity={0.5}
          transparent
          opacity={0.9}
        />
      </mesh>
      {hovered && (
        <Html center distanceFactor={2} style={{ pointerEvents: 'none' }}>
          <span className="globe-marker-tooltip">{name}</span>
        </Html>
      )}
    </group>
  );
}

function GlobeScene({
  dayTexture,
  onCreated,
}: {
  dayTexture: THREE.Texture | null;
  onCreated?: () => void;
}) {
  const groupRef = useRef<THREE.Group>(null);

  useFrame((_state, delta) => {
    if (groupRef.current) {
      groupRef.current.rotation.y += AUTO_ROTATE_SPEED * delta;
    }
  });

  useEffect(() => {
    onCreated?.();
  }, [onCreated]);

  return (
    <>
      <ambientLight intensity={0.52} />
      <directionalLight position={[4, 3, 4]} intensity={0.5} />
      <group ref={groupRef}>
        <EarthSphere dayTexture={dayTexture} />
        {CITY_MARKERS.map((city, i) => (
          <CityMarker
            key={city.id}
            lat={city.lat}
            lon={city.lon}
            name={city.name}
            pulseOffset={i * 0.5}
          />
        ))}
      </group>
      <OrbitControls
        enableZoom={false}
        minPolarAngle={Math.PI / 3}
        maxPolarAngle={Math.PI - Math.PI / 3}
        enablePan={false}
        rotateSpeed={0.4}
      />
    </>
  );
}

function GlobeFallback() {
  return (
    <div className="globe-fallback">
      <img
        src="/textures/earth-day.jpg"
        alt="Earth"
        onError={(e) => {
          (e.target as HTMLImageElement).src =
            'https://threejs.org/examples/textures/planets/earth_atmos_2048.jpg';
        }}
      />
    </div>
  );
}

export function RealTimeGlobe() {
  const [dayTex, setDayTex] = useState<THREE.Texture | null>(null);
  const [webglOk, setWebglOk] = useState<boolean | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);

  useEffect(() => {
    let cancelled = false;
    const canvas = document.createElement('canvas');
    const gl = canvas.getContext('webgl2') || canvas.getContext('webgl');
    setWebglOk(!!gl);
    if (!gl) {
      setLoading(false);
      setError(true);
      return;
    }

    loadDayTexture()
      .then((day) => {
        if (!cancelled) {
          setDayTex(day);
          setError(false);
        } else {
          day.dispose();
        }
      })
      .catch(() => {
        if (!cancelled) setError(true);
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });

    return () => {
      cancelled = true;
    };
  }, []);

  const handleCreated = useCallback(() => {
    setLoading(false);
  }, []);

  if (error || webglOk === false) {
    return <GlobeFallback />;
  }

  const textureReady = !!dayTex;

  return (
    <div className="real-time-globe" style={{ width: '100%', height: '100%', minHeight: 320 }}>
      {loading && !textureReady && (
        <div className="globe-loading">Loading globe…</div>
      )}
      {textureReady && (
        <Canvas
          gl={{ antialias: true, alpha: true, powerPreference: 'high-performance' }}
          camera={{ position: [0, 0, 4.8], fov: 42 }}
          onCreated={({ gl }) => {
            gl.setClearColor(0x000000, 0);
          }}
        >
          <Suspense fallback={null}>
            <GlobeScene dayTexture={dayTex} onCreated={handleCreated} />
          </Suspense>
        </Canvas>
      )}
    </div>
  );
}
