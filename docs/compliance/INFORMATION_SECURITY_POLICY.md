# Information Security Policy
## Sentinel Forge Cognitive AI Orchestration Platform v4.0

**Template source:** ICT Institute â€” ISO 27001:2022 (CC Attribution License)
**Prepared by:** Shannon Brian Kelley | **Effective:** April 2026

---

## 1. Purpose and Scope

Protects all information assets of Sentinel Forge Cognitive AI Orchestration Platform â€” source code, credentials, voice data, Sentinel Profile, and Azure infrastructure.

---

## 2. Security Objectives

| Objective | Target |
|-----------|--------|
| No credentials in version control | Zero incidents |
| Voice data â€” session only, no recordings | 100% of sessions |
| CI pipeline passes before deployment | 100% of releases |
| Credentials rotated if compromised | Within 24 hours |

---

## 3. Asset Classification

| Asset | Classification |
|-------|---------------|
| Azure OpenAI API Key | ðŸ”´ Confidential |
| Azure Endpoint URL | ðŸ”´ Confidential |
| `.env` file | ðŸ”´ Confidential |
| Sentinel Profile (JSONStore) | ðŸŸ¡ Internal |
| Source code | ðŸŸ¡ Internal |
| GitHub repository (public) | ðŸŸ¢ Public |
| SDLC + compliance docs | ðŸŸ¢ Public |

---

## 4. Voice Interface Security

- No audio files written to disk by default
- STT processing occurs in browser (Web Speech API) â€” audio does not leave the device
- AI text response sent to Azure OpenAI â€” covered by Microsoft DPA
- TTS playback is local â€” no external audio service

---

## 5. Access Control

- Azure portal: owner only, MFA recommended
- GitHub: owner write access; public read
- `.env`: local machine only â€” excluded from GitHub via `.gitignore`
- Sentinel Profile: local machine only

---

## 6. Supplier Security

| Supplier | Certification |
|----------|--------------|
| Microsoft Azure | ISO 27001, SOC 2 Type II |
| GitHub | ISO 27001, SOC 2 Type II |
| Anthropic (development) | Enterprise privacy terms |

---

## 7. Incident Response

1. Detect â†’ Log in `INCIDENT_LOG.md`
2. Contain â†’ Set `MOCK_AI=true` if needed
3. Rotate credentials in Azure portal within 24 hours
4. Review root cause within 48 hours
5. Update controls within 1 week

---

## 8. Business Continuity

- Mock mode ensures platform available during Azure outages
- GitHub is complete code backup
- Sentinel Profile backed up on encrypted local storage

---

*Template adapted from ICT Institute Information Security Policy Template under Creative Commons Attribution License.*
*Source: https://github.com/swzaken/freetemplates*

