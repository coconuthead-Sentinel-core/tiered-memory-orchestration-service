# Governance

## Purpose
This document states how project decisions, paperwork ownership, and release approvals are handled for Sentinel Forge.

## Ownership
- Project owner: Shannon Brian Kelley
- Repository namespace owner: `coconuthead-Sentinel-core`
- Implementation support: AI-assisted coding and documentation workflows

## Decision Model
- Strategic product and release decisions are owner-approved.
- Documentation changes may be prepared by automation or AI, but acceptance remains with the owner.
- Code changes must land with validation evidence.

## Required Paperwork Families
- Product and SDLC: `docs/sdlc/`
- Engineering build suite: `docs/engineering-build/`
- Compliance and AI governance: `docs/compliance/`
- Legal launch packet: `docs/legal/`
- Production readiness: `docs/production/`

## Approval Path
- Engineering paperwork approval: project owner reviews the engineering-build and SDLC packets.
- Compliance approval: project owner reviews `docs/compliance/` and confirms the release exclusions.
- Release approval: project owner accepts `docs/sdlc/QA_RELEASE_READINESS.md` and `docs/sdlc/DELIVERY_HANDOFF.md`.

## Release Rules
- No release packet is considered complete without validation evidence.
- Known exclusions must be recorded explicitly, not implied.
- Repo documentation must not claim live capabilities that are not currently verified.
