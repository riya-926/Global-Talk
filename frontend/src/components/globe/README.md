# Real-Time 3D Globe Hero

## Run

- From repo root: `npm run dev` (or run the frontend dev server).
- Open the app; the homepage hero section shows the globe.

## Textures

Place these in **`frontend/public/textures/`** for best performance and offline use:

| File            | Description |
|-----------------|-------------|
| `earth-day.jpg` | Daytime albedo (continents/oceans). Use 2K or 4K. |
| `earth-night.jpg` | Night lights (cities). Same size as day. |
| `earth-normal.jpg` | Optional; normal map not used in current shader. |

If local files are missing, the app uses CDN fallbacks (see `textureUrls.ts`). If the night texture fails, a dark fallback is used.

## Behaviour

- **Day/night**: Sun direction is computed from current UTC and updated every 10s; the terminator moves in real time.
- **Rotation**: Globe auto-rotates; drag to orbit (OrbitControls). Zoom disabled.
- **Markers**: Purple blinking markers at fixed cities; hover shows tooltip.

## WebGL fallback

If WebGL is unavailable or fails, a static Earth image is shown instead.
