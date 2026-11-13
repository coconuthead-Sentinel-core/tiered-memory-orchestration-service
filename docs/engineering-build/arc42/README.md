# arc42 Summary

## Metadata
- System: Sentinel Forge Cognitive AI Orchestration Platform
- Document state: completed summary
- Version: main branch review release
- Authors: Shannon Brian Kelley with Codex assistance
- Date: 2026-04-22

## 1. Introduction And Goals
- Sentinel Forge provides a review-ready FastAPI platform for chat orchestration, symbolic routing, cognitive lenses, state streaming, and supporting operational views.
- Quality goals:
  - Deterministic local validation in mock mode
  - Clear separation between route layer, orchestration layer, and runtime service layer
  - Review-friendly documentation that matches the current repository state
- Stakeholders:
  - Project owner: wants a portfolio-grade repository with readable architecture and working validation
  - Technical reviewer: wants testable routes, coherent docs, and low ambiguity about runtime scope
  - Future contributor: wants clear entry points, branching policy, and contract references

## 2. Constraints
- Technical constraints:
  - Python/FastAPI implementation on Windows-friendly local development
  - Optional Azure services cannot be required for baseline verification
  - Existing QNF runtime and symbolic modules remain part of the codebase
- Organizational constraints:
  - Single-owner repository with AI-assisted implementation support
  - `main` is the canonical release branch for the current review release
- Regulatory and compliance constraints:
  - iOS compliance paperwork must explicitly record non-applicability when no iOS target exists
  - AI governance documentation must distinguish advisory behavior from autonomous decisioning

## 3. Context And Scope
- Business context:
  - The system is a reviewable orchestration platform and portfolio artifact.
  - It is not positioned in this release as a public SaaS deployment.
- Technical context:
  - Inbound interfaces: HTTP endpoints, WebSocket endpoints, local scripts, dashboard templates
  - Outbound interfaces: optional Azure OpenAI, optional Cosmos DB, local filesystem persistence
  - Formats: JSON, WebSocket JSON events, Prometheus text, Markdown documentation

## 4. Solution Strategy
- Use FastAPI for route definition and schema generation.
- Use a shared `service` object for QNF runtime operations and a shared `_orchestrator` for chat, lens, and symbolic behavior.
- Preserve local-first execution by defaulting to mock-capable flows.
- Export human-readable and machine-readable API documentation from the running app.

## 5. Building Block View
- Level 1:
  - API layer: `backend/api.py`, `backend/ws_api.py`
  - Application bootstrap: `backend/main.py`
  - Runtime service layer: `backend/service.py`
  - Orchestration layer: `backend/services/cognitive_orchestrator.py`
  - Persistence layer: `backend/storage.py`, `backend/infrastructure/cosmos_repo.py`
- Level 2:
  - Cognitive services: lenses, glyph processor, glyph parser, firewall, memory zones
  - Platform services: jobs, profile, threads, seeds, metrics, event queue
  - Dashboard layer: HTML templates and JSON endpoints
- Level 3:
  - EventBus as the in-process async coordination surface
  - ThreeZoneMemory as the entropy classifier
  - GlyphProcessor as the symbolic matcher

## 6. Runtime View
- Scenario: chat request
  1. Client posts to `/api/chat`.
  2. `_orchestrator` records input and applies entropy and lens-aware processing.
  3. The adapter path produces a response or falls back to Quantum Nexus processing.
  4. Memory zone and symbolic metadata are attached and events may be published.
- Scenario: dashboard metrics
  1. Client requests `/api/dashboard/metrics`.
  2. The route aggregates `service.metrics()`, `service.status()`, and cognition stats.
  3. The response returns normalized health, performance, and cognition blocks.

## 7. Deployment View
- Local review deployment:
  - Python virtual environment
  - FastAPI application via `uvicorn backend.main:app`
  - Optional Docker packaging through `Dockerfile` and `docker-compose.yml`
- Network boundaries:
  - Browser or API client to FastAPI
  - FastAPI to optional Azure services
  - FastAPI to local filesystem persistence

## 8. Crosscutting Concepts
- Security: configurable WebSocket API key enforcement, documented disclosure path, no cloud dependency required for local verification
- Observability: status and metrics endpoints, Prometheus-style metrics, event history, dashboard feeds
- Configuration: environment-variable driven runtime with mock-mode support
- Data management: JSONStore and optional Cosmos repository
- Error handling: FastAPI validation, defensive adapter fallback, mock persistence fallback for note writes

## 9. Architectural Decisions
- `0001`: keep active paperwork in-repo and archive prior filled packets
- `0002`: use adapter-first orchestration with mock-safe fallback
- `0003`: keep the async contract internal through EventBus and WebSockets
- `0004`: use `main` as the canonical review-release branch

## 10. Quality Requirements
- The repository must remain runnable and testable without live cloud credentials.
- Public route docs must match the running application.
- Review artifacts must be understandable without reading every legacy root file.

## 11. Risks And Technical Debt
- Legacy root files still exist and require clear routing through the docs index.
- HTTP auth is not uniformly enforced across all routes.
- Optional cloud integrations remain documented as optional rather than production-validated.

## 12. Glossary
- EventBus: in-process publish/subscribe transport used by the API and WebSocket layers
- QNF: Quantum Nexus Forge runtime used by the service layer
- Three-zone memory: entropy-based classification into active, pattern, and crystallized states
- Cognitive lens: response-shaping mode such as ADHD, autism, dyslexia, or neurotypical
