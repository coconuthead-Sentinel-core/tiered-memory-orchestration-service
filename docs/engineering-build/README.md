# Engineering Build Suite

## Status
- Project: Sentinel Forge Cognitive AI Orchestration Platform
- Document state: completed for the current review release
- Owner: Shannon Brian Kelley
- Review date: 2026-04-22

## Purpose
This directory is the canonical engineering-build packet for the repository. It holds the architecture, decision, interface, threat, and AI-governance paperwork that should match the running code on `main`.

## Included Artifacts
- arc42 summary: `arc42/README.md`
- ADR log:
  - `adr/0001-engineering-documentation-structure.md`
  - `adr/0002-adapter-first-orchestration.md`
  - `adr/0003-internal-eventbus-and-websocket-contract.md`
  - `adr/0004-main-branch-release-policy.md`
- C4 container view: `c4/container-model.md`
- OpenAPI workspace and generated schema: `openapi/README.md`
- AsyncAPI-style channel catalog: `asyncapi/README.md`
- Threat model: `threat-model/README.md`
- AI governance summary: `ai-governance/README.md`
- NIST AI RMF mapping: `nist-ai-rmf/README.md`

## Operating Rule
- Update this suite whenever code, routes, event contracts, or release policy change.
- Historical filled paperwork that no longer defines the active release lives under `../archive/`.
