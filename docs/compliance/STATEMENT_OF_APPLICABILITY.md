# Statement of Applicability (SoA)
## Sentinel Forge Cognitive AI Orchestration Platform v4.0

**Template source:** ICT Institute â€” ISO 27001:2022 Annex A (CC Attribution License)
**Prepared by:** Shannon Brian Kelley | **Date:** April 2026

---

## Key Controls â€” Sentinel Forge Cognitive AI Orchestration Platform Specific

| Control | Title | Status | Notes |
|---------|-------|--------|-------|
| 5.1 | Information security policies | âœ… | INFORMATION_SECURITY_POLICY.md |
| 5.8 | Security in project management | âœ… | SDLC suite; security in Definition of Done |
| 5.9 | Asset inventory | âœ… | ASSET_RISK_REGISTER.md |
| 5.12 | Classification of information | âœ… | IS Policy Â§3 |
| 5.14 | Information transfer | âœ… | Azure DPA; no third-party voice storage |
| 5.17 | Authentication information | âœ… | API keys in `.env`; excluded from GitHub |
| 5.19 | Supplier security | âœ… | Azure, GitHub ISO 27001 certified |
| 5.23 | Cloud service security | âœ… | Azure OpenAI â€” Microsoft certified |
| 5.24 | Incident management | âœ… | INCIDENT_LOG.md |
| 5.29 | Business continuity | âœ… | Mock mode fallback |
| 5.31 | Legal and regulatory compliance | âœ… | GDPR (DPIA); AI Act (FRIA) |
| 5.34 | Privacy and data protection | âœ… | No persistent user data by default |
| 8.1 | User endpoint devices | âœ… | Owner's laptop â€” standard security |
| 8.5 | Secure authentication | âœ… | GitHub MFA; Azure MFA |
| 8.7 | Malware protection | âœ… | Windows Defender |
| 8.10 | Information deletion | âœ… | Session-only; voice not recorded |
| 8.12 | Data leakage prevention | âœ… | `.gitignore` covers all credentials |
| 8.13 | Backup | âœ… | GitHub code backup |
| 8.14 | Redundancy | âœ… | Mock mode for Azure outages |
| 8.24 | Cryptography | âœ… | HTTPS to Azure; TLS in transit |
| 8.25 | Secure development lifecycle | âœ… | Full SDLC documentation |
| 8.28 | Secure coding | âœ… | No hardcoded secrets |
| 8.29 | Security testing | âœ… | Unit tests; 1000 Strikes protocol |
| 8.32 | Change management | âœ… | Git commits; version history |

### Voice Interface â€” Additional Controls

| Control | Requirement | Status |
|---------|-------------|--------|
| Audio data minimization | No audio files saved | âœ… STT in-browser only |
| User notification | Recording indicator in UI | âš ï¸ Planned |
| Consent for voice | Required before any recording storage | âœ… Not stored |

---

*Template adapted from ICT Institute Statement of Applicability ISO 27001-2022 under Creative Commons Attribution License.*
*Source: https://github.com/swzaken/freetemplates*

