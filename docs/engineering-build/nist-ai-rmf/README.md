# NIST AI RMF Mapping

## System Metadata
- AI system name: Sentinel Forge Cognitive AI Orchestration Platform
- AI capability: generative and rules-assisted orchestration
- Model(s): mock adapter by default, optional Azure-backed adapter path, fallback Quantum Nexus processing path
- Intended users: project owner, technical reviewers, and future contributors
- Deployment context: local review release on `main`, not public cloud production

## GOVERN
- Roles and responsibilities:
  - Owner: Shannon Brian Kelley
  - Engineering documentation support: Codex
  - Security disclosure owner: Shannon Brian Kelley
  - Privacy and legal review: owner-managed for the current release
- Policies:
  - data handling: review and compliance documents under `docs/compliance/`
  - model update control: code and docs change together on `main`
- Audit requirements:
  - tests, smoke checks, route inventory, and generated OpenAPI schema

## MAP
- Intended purpose:
  - present a reviewable AI orchestration repository with cognitive-lens and symbolic-routing behavior
- Misuse and abuse cases:
  - over-trusting advisory outputs
  - supplying malicious symbolic payloads
  - exposing optional cloud credentials through misconfiguration
- Affected stakeholders:
  - project owner
  - technical reviewers
  - future maintainers
- Harm types:
  - reliability
  - security
  - documentation drift
  - privacy if cloud credentials or note contents are mishandled

## MEASURE
- Quality metrics:
  - full pytest suite passes
  - smoke test passes
  - API docs and route inventory match
- Safety metrics:
  - L6 firewall output constraints stay active
  - no secrets are committed
- Adversarial testing:
  - route validation, glyph validation, and negative-path tests
- Monitoring and drift:
  - metrics endpoints
  - status endpoints
  - documentation review against current routes

## MANAGE
- Controls and mitigations:
  - mock-mode default for review
  - archived paperwork separation
  - branch reduction to `main`
  - documented security disclosure path
- Incident response:
  - record incidents in `docs/compliance/INCIDENT_LOG.md`
  - route sensitive issues through `SECURITY.md`
- Rollback or disable path:
  - revert on `main`
  - stop raw-event orchestration listener through `/api/task/orchestrate/stop`
  - run in mock mode with optional cloud integrations disabled

## Data And Privacy
- Data sources:
  - request payloads
  - symbolic seeds and rules
  - local JSON state
  - optional cloud-backed persistence
- PII handling:
  - no special PII workflow is claimed for the review release
  - callers should avoid sending sensitive data into demo flows
- Retention:
  - local JSON and note data persist until cleared or repo state is changed by the owner
