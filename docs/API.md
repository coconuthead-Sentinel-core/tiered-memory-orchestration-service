# API Contract

## Status
- Project: Sentinel Forge Cognitive AI Orchestration Platform
- Document state: active human-readable contract
- Owner: Shannon Brian Kelley
- Review date: 2026-04-22

## Scope
This document captures the current HTTP and WebSocket contract for the repository review release. The generated machine-readable schema lives at `docs/engineering-build/openapi/openapi.generated.json`.

## HTTP Endpoint Groups
| Group | Key Paths | Purpose | Auth | Notes |
|---|---|---|---|---|
| Core health and ops | `/api/status`, `/api/metrics`, `/api/metrics/prom`, `/api/healthz`, `/api/readyz`, `/api/config`, `/api/version`, `/api/ops` | runtime status, metrics, probes, config view, ops dashboard | None by default | `metrics/prom` emits Prometheus-style text |
| Chat and notes | `/api/chat`, `/api/notes`, `/api/notes/upsert` | chat completions and repository note persistence | None by default | `chat` uses the shared cognitive orchestrator |
| Cognitive control | `/api/cognitive/status`, `/api/cognitive/metrics`, `/api/task/orchestrate/start`, `/api/task/orchestrate/stop` | cognitive core status and raw-event listener control | None by default | orchestration start/stop now operate on the shared orchestrator |
| Cognition pipeline | `/api/cog/status`, `/api/cog/process`, `/api/cog/rules`, `/api/cog/memory`, `/api/cog/prime`, `/api/cog/suggest`, `/api/cog/threads`, `/api/cog/stats`, `/api/cog/seeds`, `/api/cog/matrix` | symbolic rules, memory state, threads, seeds, and cognition statistics | None by default | request and response models live in `backend/schemas.py` |
| Glyph and sync | `/api/glyphs/pack`, `/api/glyphs/interpret`, `/api/glyphs/validate`, `/api/glyphs/boot`, `/api/activate/{preset}`, `/api/sync/update`, `/api/sync/snapshot`, `/api/sync/trinode` | symbolic routing, boot sequence, preset activation, and tri-node synchronization | None by default | sync payloads are typed in `backend/schemas.py` |
| Platform service | `/api/process`, `/api/pools`, `/api/teardown`, `/api/rebuild`, `/api/stress`, `/api/jobs/{job_id}`, `/api/state`, `/api/state/save`, `/api/upgrade/plan`, `/api/upgrade/apply`, `/api/triage/tuner`, `/api/sentinel/profile`, `/api/sentinel/init` | QNF runtime operations, jobs, persistence, tuning, and profile management | None by default | stress jobs support sync and async execution |
| Dashboard views | `/api/dashboard`, `/api/dashboard/metrics`, `/api/dashboard/activity`, `/api/dashboard/sentinel`, `/api/dashboard/nexus`, `/api/dashboard/nexus-metrics` | HTML dashboards plus JSON feeds | None by default | `/api/dashboard/metrics` is the canonical aggregated metrics feed |

## WebSocket Endpoints
| Path | Purpose | Event Types | Auth | Notes |
|---|---|---|---|---|
| `/ws/sync` | compatibility pass-through stream of EventBus traffic | arbitrary EventBus payloads | API key when configured | no initial state snapshot |
| `/ws/cognitive` | cognitive and symbolic stream with initial state snapshot | cognitive, symbolic, and glyph events | API key when configured | sends `cognitive.state` immediately after connect |
| `/ws/metrics` | event-driven metrics stream | `metrics.initial_state`, `zone.classified`, `zone.transition` | API key when configured | filters to metrics-relevant cognitive events |

## Schemas And Contract Sources
- Typed request and response models: `backend/schemas.py`
- Executable route source: `backend/api.py` and `backend/ws_api.py`
- OpenAPI export script: `scripts/export_openapi.py`
- Example payloads: `docs/API_EXAMPLES.md`

## Validation Rules
- Error model: FastAPI JSON errors for validation failures and `HTTPException` responses for operational failures.
- Authentication model:
  - WebSockets enforce `X-API-Key` header or `api_key` query parameter when `QNF_API_KEY` or `QNF_REQUIRE_API_KEY` is configured.
  - HTTP endpoints are currently open by default unless route-specific guards are added in future hardening work.
- Versioning rule: the contract is versioned by the repository state on `main`; generated OpenAPI should be refreshed in the same change set as endpoint changes.
