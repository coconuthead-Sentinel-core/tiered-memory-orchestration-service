# System Design

## Metadata
- System: Sentinel Forge Cognitive AI Orchestration Platform
- Version: 2026-04-22 review release
- Owner: Shannon Brian Kelley
- Date: 2026-04-22

## Architecture Overview
Sentinel Forge is a Python and FastAPI system that layers adaptive cognition, symbolic interpretation, and operational runtime endpoints over a locally verifiable service core.

The design is optimized for:
- local deterministic validation
- clear architecture review
- low-friction extension of lenses and symbolic routing

## Layer Definitions
| Layer | Name | Responsibility |
|---|---|---|
| L1 | API surface | expose HTTP and WebSocket endpoints through FastAPI |
| L2 | Orchestration | coordinate chat, lens routing, symbolic reactions, and memory zoning |
| L3 | Runtime service | manage Quantum Nexus state, jobs, profiles, and operational metrics |
| L4 | Persistence and assets | provide JSON and optional Cosmos-backed state plus glyph seed data |

## Module Boundaries
| Module | File(s) | Responsibility |
|---|---|---|
| App bootstrap | `backend/main.py` | assemble the FastAPI application and routers |
| HTTP API | `backend/api.py` | expose status, chat, cognition, glyph, dashboard, and operations routes |
| WebSocket API | `backend/ws_api.py` | expose sync, cognitive, and metrics streams |
| Orchestrator | `backend/services/cognitive_orchestrator.py` | handle lenses, entropy zoning, and symbolic reactions |
| Runtime service | `backend/service.py` | manage QNF pools, jobs, threads, metrics, and profile state |
| Symbolic system | `backend/services/glyph_processor.py`, `glyph_parser.py`, `glyph_event_bridge.py` | interpret glyphs and publish events |
| Memory system | `backend/services/memory_zones.py` | classify content into active, pattern, and crystal zones |
| Event transport | `backend/eventbus.py` | in-process publish and subscribe support |

## Key Data Structures
- zoned note records for three-zone memory classification
- symbolic metadata and glyph matches for symbolic processing
- service metrics and profile payloads for operational views
- request and response models in `backend/schemas.py`

## Workflows
- HTTP request to orchestrator: request enters `backend/api.py`, reaches the shared orchestrator, is lens-adjusted, and returns a response payload
- raw event listener: EventBus events reach the orchestrator listener, are interpreted by glyph logic, and can trigger follow-on actions
- metrics stream: runtime and cognition events are filtered and forwarded to WebSocket consumers

## Failure Modes
| Failure | Detection | Recovery |
|---|---|---|
| Route drift between docs and code | validation review or API tests fail | refresh docs and generated OpenAPI in the same change set |
| Missing cloud credentials | Azure-backed flows unavailable | run in mock mode for local validation |
| Event listener regression | API completion tests fail | repair start or stop behavior on the shared orchestrator |
| Historical docs confusion | reviewers find conflicting paperwork | route active readers through `docs/README.md` and keep old material under `docs/archive/` |
