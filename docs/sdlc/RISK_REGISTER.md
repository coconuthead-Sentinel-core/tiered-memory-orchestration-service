# Risk Register

| ID | Risk | Status | Owner | Mitigation | Review Date |
|---|---|---|---|---|---|
| R-001 | HTTP routes are not universally authenticated in the current release | Accepted | Shannon Brian Kelley | document the security posture clearly and keep the release scope local and review-oriented | 2026-04-22 |
| R-002 | Azure-backed live behavior is not validated in this cycle | Accepted | Shannon Brian Kelley | treat Azure deployment as a separate excluded workstream | 2026-04-22 |
| R-003 | Symbolic or lens behavior can drift from docs if routes change without a doc refresh | Controlled | Shannon Brian Kelley | keep tests, API docs, and engineering-build docs in the same change set | 2026-04-22 |
| R-004 | Reviewers may assume an iOS deliverable exists | Controlled | Shannon Brian Kelley | complete the iOS packet as a documented `not applicable` outcome | 2026-04-22 |
| R-005 | Historical paperwork can be mistaken for active release documents | Controlled | Shannon Brian Kelley | route active readers through `docs/README.md` and keep old material in `docs/archive/` | 2026-04-22 |
