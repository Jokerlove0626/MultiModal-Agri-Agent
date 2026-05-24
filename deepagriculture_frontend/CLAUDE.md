# CLAUDE.md — DeepAgriculture / 智农大夫 Frontend

## Project overview

智农大夫 (Agri-Doctor) is an AI-powered agricultural pest & disease diagnostic platform. The backend (FastAPI) serves trained models for multimodal diagnosis (image + text), knowledge graph reasoning (GraphRAG), and national pest monitoring data. This repo is the **Vue 3 frontend**.

## Commands

```bash
npm run dev       # Start Vite dev server (default http://localhost:5173)
npm run build     # Production build
npm run preview   # Preview production build
```

Backend expected at `http://127.0.0.1:8000` (override via `VITE_API_BASE_URL` / `VITE_API_URL` env vars).

## Tech stack

| Layer | Choice |
|---|---|
| Framework | Vue 3 (Composition API, `<script setup>`) |
| Build | Vite 8 |
| Router | Vue Router 4 (history mode) |
| Charts | ECharts 6 (map + force-graph) |
| HTTP | Axios (graph API) + native `fetch` (chat API with SSE streaming) |
| Markdown | `marked` + `dompurify` (XSS-safe AI output rendering) |
| Icons | Material Symbols (font, outlined) |
| CSS | Tailwind CSS (CDN, no build pipeline — see note below) |
| Fonts | Space Grotesk (headlines), Inter (body) via Google Fonts |
| State | **No Pinia/Vuex** — all state is local `ref()`/`computed()` + `localStorage` for session ID |

### Important: CDN Tailwind

Tailwind is loaded via `<script>` CDN in `index.html` — there is **no** `tailwind.config.js`, `postcss.config.js`, or CSS build pipeline. The config is inline in `<script id="tailwind-config">`. This means:
- No class purging — all utility classes ship to production
- Custom theme tokens (colors, fonts, shadows, background patterns) are defined in the inline config
- Custom CSS lives in `<style>` blocks inside `.vue` files (global styles in `App.vue`, scoped styles in each component)

## Routes

| Path | View | Description |
|---|---|---|
| `/` | `home.vue` | Landing page (hero, features, timeline, FAQ, CTA) |
| `/chat` | `chat.vue` | AI diagnostic chat (text + image, SSE streaming) |
| `/graph` | `graph.vue` | Interactive knowledge graph (ECharts force-directed) |
| `/monitor` | `monitor.vue` | National pest outbreak map (ECharts GeoJSON China) |
| `/knowledge` | `knowledge.vue` | Stub — `<h1>` only, not yet implemented |

## Layout system

Two distinct layouts:

1. **Marketing layout** (/, /graph, /monitor, /knowledge): `TopNav` component at top (sticky, glassmorphic on scroll) + `<router-view>` content below.
2. **Chat layout** (/chat): TopNav is **hidden** — chat has its own full-height layout with left sidebar (brand + nav + "New Diagnosis" button) and main chat area.

## API layer (`src/services/`)

- **`chatApi.js`**: 4 functions using native `fetch` — `postChat`, `postChatStream` (SSE), `postIdentify` (FormData upload), `postIdentifyStream` (SSE). All include `session_id`, `province`, `city` in payload.
- **`graphApi.js`**: 1 function using axios — `getGraphData(diseaseName, limit)` → `GET /api/graph/visualize`.

Streaming uses `AbortController` + manual SSE parsing from `ReadableStream`.

## Design language

- **Theme**: "The Living Laboratory" — agricultural green meets tech/scientific aesthetic
- **Color**: Material Design 3 green tonal palette (`#2E7D32` primary, `#f1f8e9` background)
- **Key patterns**: Glassmorphism (`.glass-card`), scroll-reveal animations, SVG animated graph lines, pulsing node animations, staggered text reveal
- **Background**: Fixed `tech-grid` pattern (40px green grid lines at 30% opacity) on all pages
- **Typography**: Space Grotesk for headlines, Inter for body — both from Google Fonts
- **Transitions**: Damping cubic-bezier (`0.25, 1, 0.5, 1`) throughout

## Key architectural notes

- No shared state management — session ID persisted in `localStorage` under key `deepagriculture.session_id`
- Chat uses browser geolocation (reverse-geocoded via OSM Nominatim) to send province/city with every request
- Legacy static HTML prototypes exist in `public/chat/` and `public/home.html` — not used at runtime
- Favicon is a leaf icon at `public/favicon.ico`
