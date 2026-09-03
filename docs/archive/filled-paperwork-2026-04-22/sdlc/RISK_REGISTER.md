# Risk Register

| ID | Risk | Status | Owner | Mitigation | Review Date |
|---|---|---|---|---|---|
| R-001 | Documentation drifts from verified runtime behavior | Active | Shannon Brian Kelley | Update README and engineering-build docs in the same change set as route or behavior changes | 2026-04-22 |
| R-002 | Optional Azure dependencies create misleading claims in local-only runs | Active | Shannon Brian Kelley | Keep mock-mode workflow documented and treat live Azure as optional until revalidated | 2026-04-22 |
| R-003 | Legacy top-level files increase operator confusion | Active | Shannon Brian Kelley | Route operators through `docs/README.md` and `docs/engineering-build/README.md` | 2026-04-22 |
| R-004 | No iOS code exists but iOS compliance paperwork could be misread as implementation-ready | Controlled | Shannon Brian Kelley | Mark iOS packet as non-applicable for this repo version and record evidence | 2026-04-22 |
| R-005 | Security reports may be mishandled without a documented path | Controlled | Shannon Brian Kelley | Added `SECURITY.md` and interim disclosure instructions | 2026-04-22 |
