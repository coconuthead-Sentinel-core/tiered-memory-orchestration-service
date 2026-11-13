# Asset Inventory and Risk Register
## Sentinel Forge Cognitive AI Orchestration Platform v4.0

**Template source:** ICT Institute â€” ISO 27001:2022 (CC Attribution License)
**Prepared by:** Shannon Brian Kelley | **Date:** April 2026

---

## Asset Inventory

| ID | Asset | Type | Classification |
|----|-------|------|---------------|
| A-001 | Azure OpenAI API Key | Credential | ðŸ”´ Confidential |
| A-002 | Azure Endpoint URL | Credential | ðŸ”´ Confidential |
| A-003 | `.env` file | Credential | ðŸ”´ Confidential |
| A-004 | `backend/` FastAPI application | Source code | ðŸŸ¡ Internal |
| A-005 | `sigma_network_engine.py` | Source code | ðŸŸ¡ Internal |
| A-006 | `sentinel_profile.py` + JSONStore | Source code + Data | ðŸŸ¡ Internal |
| A-007 | `l7_singularity_kernel.py` | Source code | ðŸŸ¡ Internal |
| A-008 | `recursive_nexus_sigil_dashboard_unified.html` | Frontend | ðŸŸ¢ Public |
| A-009 | GitHub repository | Platform | ðŸŸ¢ Public |
| A-010 | Azure OpenAI resource | Platform | ðŸ”´ Confidential |
| A-011 | SDLC + compliance documentation | Documentation | ðŸŸ¢ Public |
| A-012 | Developer laptop | Hardware | ðŸŸ¡ Internal |
| A-013 | `results_1000_strikes.txt` | Performance data | ðŸŸ¡ Internal |

---

## Risk Register

| ID | Risk | Likelihood | Severity | Level | Controls | Residual |
|----|------|-----------|---------|-------|---------|---------|
| R-001 | API key committed to GitHub | 2 | 5 | ðŸŸ¡ HIGH | `.gitignore`; secret scanning | ðŸŸ¢ LOW |
| R-002 | Azure account compromised | 2 | 5 | ðŸŸ¡ HIGH | MFA; limited access | ðŸŸ¢ LOW |
| R-003 | Voice data inadvertently recorded | 2 | 4 | ðŸŸ¡ MEDIUM | No audio files; STT in-browser | ðŸŸ¢ LOW |
| R-004 | User speaks PII into voice interface | 3 | 3 | ðŸŸ¡ MEDIUM | No storage; user guidance | ðŸŸ¢ LOW |
| R-005 | Sentinel Profile contains identifiable data | 1 | 3 | ðŸŸ¢ LOW | Preferences only; not identity | ðŸŸ¢ LOW |
| R-006 | Azure outage | 3 | 2 | ðŸŸ¡ MEDIUM | Mock mode fallback | ðŸŸ¢ LOW |
| R-007 | Laptop lost or stolen with Sentinel Profile | 2 | 3 | ðŸŸ¡ MEDIUM | Disk encryption; preferences only | ðŸŸ¡ MEDIUM |
| R-008 | WebSocket connection exposes unencrypted data | 2 | 3 | ðŸŸ¡ MEDIUM | Localhost only; no external exposure | ðŸŸ¢ LOW |
| R-009 | Malicious dependency | 2 | 3 | ðŸŸ¡ MEDIUM | Dependabot; pinned versions | ðŸŸ¡ MEDIUM |

---

## Treatment Plan

| Risk | Action | Owner | Date |
|------|--------|-------|------|
| R-001 | Maintain `.gitignore`; pre-commit review | Shannon Brian Kelley | Ongoing |
| R-002 | Enable Azure MFA | Shannon Brian Kelley | April 2026 |
| R-003 | Add voice recording indicator to UI | Shannon Brian Kelley | Next sprint |
| R-007 | Enable full disk encryption | Shannon Brian Kelley | April 2026 |

---

*Template adapted from ICT Institute Assets-and-risks-ISO-27001 under Creative Commons Attribution License.*
*Source: https://github.com/swzaken/freetemplates*

