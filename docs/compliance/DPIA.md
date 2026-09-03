# Data Protection Impact Assessment (DPIA)
## Sentinel Forge Cognitive AI Orchestration Platform v4.0

**Template source:** ICT Institute â€” DPIA Template (CC Attribution License)
**Prepared by:** Shannon Brian Kelley (Data Controller)
**Date:** April 2026

---

## 1. Is a DPIA Required?

| Criterion | Present? |
|-----------|---------|
| Innovative technology (AI + voice) | Yes |
| Audio/voice data processing | Yes |
| Persistent user profile | Yes (preferences only, not identity) |
| Large-scale processing | No |
| Special category data | No (by design) |

**DPIA Decision: Recommended** â€” Voice interface and Sentinel Profile warrant documented assessment.

---

## 2. Data Flow

```
User speaks / types input
        â†“
FastAPI (in-memory only)
        â†“
Azure OpenAI o4-mini (Microsoft cloud)
        â†“
Response â†’ TTS voice output
        â†“
[Optional] Cosmos DB â€” NOT active by default
Sentinel Profile â†’ JSONStore (local file, preferences only)
```

---

## 3. Personal Data Inventory

| Data Element | Type | Stored? | Legal Basis |
|-------------|------|---------|-------------|
| User text prompts | Personal (potentially) | No â€” session only | Legitimate interest |
| Voice/audio input | Personal | No â€” processed in-session, not recorded | Legitimate interest |
| Sentinel Profile | Preferences (not identity) | Yes â€” local JSONStore | Legitimate interest |
| IP address | Personal | No â€” not logged | N/A |
| WebSocket session | Technical | No â€” session only | Legitimate interest |

---

## 4. Risk Assessment

| Risk | Likelihood | Severity | Level | Mitigation | Residual |
|------|-----------|---------|-------|------------|---------|
| User enters PII in voice/text | Medium | Medium | ðŸŸ¡ MEDIUM | No storage; user guidance | ðŸŸ¢ LOW |
| Voice data inadvertently recorded | Low | High | ðŸŸ¡ MEDIUM | Session-only STT; no audio files saved | ðŸŸ¢ LOW |
| Sentinel Profile contains identifiable data | Low | Medium | ðŸŸ¢ LOW | Profile stores preferences only | ðŸŸ¢ LOW |
| Azure processes personal voice data | High (by design) | Low | ðŸŸ¢ LOW | Microsoft DPA applies; no training on data | ðŸŸ¢ LOW |
| Cosmos DB stores personal data when activated | Low (not active) | High | ðŸŸ¡ MEDIUM | Not active; full DPIA update required before activation | ðŸŸ¢ LOW |

**Overall: LOW RISK** at current deployment scope.

---

## 5. Data Subject Rights

All rights easily met â€” no personal data stored by default. Sentinel Profile contains only cognitive preferences and can be deleted by removing the local JSONStore file.

---

## 6. DPIA Conclusion

Processing may proceed. Must update before:
- Activating Cosmos DB persistence
- Multi-user deployment
- Any storage of voice recordings

---

## 7. Sign-Off

| Role | Name | Date |
|------|------|------|
| Data Controller / Architect | Shannon Brian Kelley | April 2026 |

---

*Template adapted from ICT Institute DPIA Template under Creative Commons Attribution License.*
*Source: https://github.com/swzaken/freetemplates*

