# Product Requirements Document

## Metadata
- Product: Sentinel Forge Cognitive AI Orchestration Platform
- Version: 2026-04-22 review release
- Owner: Shannon Brian Kelley
- Date: 2026-04-22

## Problem Statement
Most AI interfaces assume a single presentation style. Sentinel Forge addresses that gap by adding a cognitive orchestration layer that can route, transform, and present responses through multiple output lenses while staying testable in a local engineering workflow.

## Product Vision
Provide a review-ready orchestration platform that demonstrates:
- adaptive response formatting for different cognitive styles
- symbolic and glyph-aware routing
- three-zone memory classification
- observable HTTP and WebSocket runtime surfaces
- reproducible local validation without cloud-only dependencies

## Target Users
| User | Need |
|---|---|
| Technical reviewer | Understand the architecture, runtime behavior, and validation evidence quickly |
| Hiring manager or HR reviewer | See a coherent, complete project packet with clear paperwork and proof of finish |
| Developer contributor | Run the stack locally, inspect APIs, and extend the cognitive or symbolic systems safely |
| Neurodivergent-aware product stakeholder | Evaluate whether the lens model supports multiple communication styles |

## Core Features
- FastAPI runtime with health, metrics, chat, glyph, cognition, dashboard, and operational endpoints
- Cognitive orchestrator with neurotypical, ADHD, autism, and dyslexia-oriented presentation lenses
- Three-zone memory classification with entropy-driven routing
- Symbolic glyph interpretation and EventBus publication
- WebSocket streams for sync, cognitive, and metrics traffic
- Mock-mode local development and validation path without required Azure credentials
- Completed engineering-build, SDLC, review, and iOS applicability paperwork

## Non-Functional Requirements
| Requirement | Target |
|---|---|
| Local reliability | Full smoke test and automated test suite pass in local mock mode |
| Documentation coherence | README, architecture, API docs, engineering-build suite, and SDLC packet agree on runtime behavior |
| Traceability | Major product requirements map to code, tests, and paperwork artifacts |
| Review readiness | Repository is cleanly packaged on `main` with completed release paperwork |
| Extensibility | Lens, glyph, and event-driven behaviors can be extended without rewriting the whole service |

## Out Of Scope
- Azure credential provisioning and live cloud deployment
- Public SaaS billing launch and merchant onboarding
- iOS or App Store delivery
- Multi-tenant production hardening beyond the current review release

## Success Criteria
- The repository runs locally in mock mode.
- The automated validation and smoke-test commands pass.
- The active documentation set reflects the implementation instead of blank templates.
- The project is packaged on `main` for technical and hiring review.
