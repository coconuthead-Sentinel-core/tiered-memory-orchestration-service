# Sentinel Forge Architecture

## Status
- Project: Sentinel Forge Cognitive AI Orchestration Platform
- Document state: active architecture summary
- Owner: Shannon Brian Kelley
- Last updated: 2026-04-22

## Purpose
This file is the high-level architecture summary for the current repository release. It complements the detailed engineering-build paperwork in `docs/engineering-build/`.

## System Summary
- Problem being solved: provide a FastAPI-based orchestration layer that adapts output formatting to different cognitive styles while preserving deterministic local development and testability.
- Primary users: developers, reviewers, neurodivergent-oriented product stakeholders, and technical evaluators reviewing symbolic and lens-based orchestration.
- Primary runtime surfaces: HTTP API, WebSocket streams, dashboard views, evaluation scripts, and local verification tooling.
- Non-goals for this release: public cloud deployment, multi-tenant production hosting, and Apple-platform application delivery.

## Architecture Snapshot
- Application entry points:
  - `backend/main.py` for FastAPI app wiring
  - `backend/api.py` for REST endpoints
  - `backend/ws_api.py` for WebSocket endpoints
  - `scripts/smoke_test.py` and `scripts/export_openapi.py` for verification and contract export
- Core services:
  - `backend/service.py` wraps the Quantum Nexus runtime, jobs, event stream, profile, seeds, threads, and platform metrics
  - `backend/services/cognitive_orchestrator.py` adds lens transformation, symbolic processing, entropy zoning, and raw-event reactions
  - `backend/services/glyph_processor.py`, `glyph_parser.py`, and `glyph_event_bridge.py` handle symbolic recognition and event publication
  - `backend/services/memory_zones.py` provides three-zone entropy classification
- Data and state:
  - in-memory QNF service state
  - `backend/storage.py` JSON persistence
  - optional Cosmos DB persistence via `backend/infrastructure/cosmos_repo.py`
  - glyph seed definitions in `data/glyphs_pack.json`
- External integrations:
  - optional Azure OpenAI and Azure Cosmos DB
  - none required for local validation in mock mode

## Runtime Model
- HTTP requests enter through `backend/api.py`.
- Chat and symbolic flows are handled by the shared `_orchestrator` instance.
- Platform operations and thread/state management are handled by the shared `service` instance.
- Real-time updates are distributed over the in-process `backend/eventbus.py` and exposed through `/ws/sync`, `/ws/cognitive`, and `/ws/metrics`.

## Operating Constraints
- Runtime constraints:
  - the validated release scope is local development and review, not public cloud hosting
  - mock mode must continue to work without Azure credentials
- Security constraints:
  - WebSocket API key enforcement is available through `backend/security.py`
  - HTTP authentication is not universally enforced in the current release and should be treated as an explicit future hardening area, not an implicit control
- Documentation constraints:
  - architecture, API, SDLC, review, and compliance paperwork must agree with the current `main` branch
  - previously filled historical paperwork is archived under `docs/archive/`

## Linked Detailed Paperwork
- Engineering build suite: `docs/engineering-build/README.md`
- SDLC packet: `docs/sdlc/README.md`
- API contract: `docs/API.md`
- Review packet: `docs/HR_REVIEW_PACKET.md`
- iOS compliance packet: `docs/compliance/ios/README.md`
