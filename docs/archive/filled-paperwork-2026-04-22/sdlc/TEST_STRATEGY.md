# Test Strategy
## Sentinel Forge Cognitive AI Orchestration Platform v4.0

**Architect:** Shannon Brian Kelley
**Implementation:** Claude AI (Anthropic)
**Date:** April 2026

---

## 1. Testing Philosophy

Sentinel Forge Cognitive AI Orchestration Platform has a unique testing requirement no other platform in the trilogy has: the CNO-AX Metacognition Engine must be validated through a live performance protocol â€” not just unit tests. Code correctness and system performance are both first-class test targets.

---

## 2. Test Levels

### Unit Tests â€” `tests/`

| Test ID | What It Covers | Pass Criteria |
|---------|---------------|---------------|
| UT-001 | `CognitiveOrchestrator` initialization | Object created, Sentinel Profile loaded |
| UT-002 | ADHD lens â€” 50-word chunking | Response chunked; action words emphasized |
| UT-003 | Autism lens â€” structure enhancement | Explicit categorization present in output |
| UT-004 | Dyslexia lens â€” spatial anchors | Navigation paths and visual chunks returned |
| UT-005 | Neurotypical lens â€” baseline | Standard response, no chunking |
| UT-006 | Zone classification â€” GREEN | entropy > 0.7 â†’ GREEN |
| UT-007 | Zone classification â€” YELLOW | entropy 0.3â€“0.7 â†’ YELLOW |
| UT-008 | Zone classification â€” RED | entropy < 0.3 â†’ RED |
| UT-009 | GlyphProcessor â€” 14-Mirror routing | Glyph maps to correct mirror(s) |
| UT-010 | SigmaNetworkEngine â€” feature flags | Profile flags correctly set runtime behavior |
| UT-011 | Sentinel Profile â€” persist and reload | Profile survives server restart |
| UT-012 | Azure adapter â€” mock mode | Returns non-empty response without API call |
| UT-013 | A1 Filing System â€” node stored in correct zone | GREEN node â†’ GREEN directory |
| UT-014 | WebSocket event publishing | Zone transition triggers ws event |

**Run command:**
```bash
pytest tests/ -v
```

---

### CNO-AX Performance Protocol â€” "1000 Strikes"

This is Sentinel Forge Cognitive AI Orchestration Platform's unique performance test â€” no other platform has an equivalent.

| Metric | Target | Achieved |
|--------|--------|---------|
| Average Latency | < 20ms | **11.90ms** âœ… |
| Jitter (StDev) | < 5ms | **3.41ms** âœ… |
| Stillwater State | Confirmed | **Confirmed** âœ… |
| Persona | Crystalline Navigator | **Confirmed** âœ… |

**Run command:**
```bash
python launch_1000_strikes.py
```

Results saved to `results_1000_strikes.txt`.

---

### Integration Tests â€” Manual

| Test ID | Scenario | Steps | Pass Criteria |
|---------|----------|-------|---------------|
| IT-001 | FastAPI server starts | `uvicorn backend.main:app` | Server live at localhost:8000 |
| IT-002 | GET /api/status | curl or browser | Returns JSON with platform, ai_mode, stillwater |
| IT-003 | POST /api/chat mock | POST with MOCK_AI=true | Returns response, zone, mirror_array, latency |
| IT-004 | POST /api/chat live | POST with MOCK_AI=false | Returns o4-mini response |
| IT-005 | GET /api/metrics | GET request | Full JSON with cno_ax, zone_distribution, lens_usage |
| IT-006 | WebSocket /ws/cognitive | Browser DevTools | Events stream in real time |
| IT-007 | Dashboard loads | Open HTML file | UI elements present; WebSocket connecting |
| IT-008 | Voice input | Speak into microphone | STT captured; AI response spoken back |
| IT-009 | Profile persistence | Restart server | Sentinel Profile state preserved |

---

### Evaluation Pipeline â€” `evaluation/`

| Metric | Target | Current Score |
|--------|--------|---------------|
| Relevance | â‰¥ 3.8 / 5.0 | **3.97** âœ… |
| Coherence | â‰¥ 3.8 / 5.0 | **3.94** âœ… |
| Groundedness | â‰¥ 3.8 / 5.0 | **3.96** âœ… |
| **Overall** | **â‰¥ 3.9 / 5.0** | **3.96** âœ… |

80 prompts across all four lenses (20 per lens).

**Run command:**
```bash
python evaluation/run_evaluation.py
```

---

## 3. Agent + Mirror Coverage Matrix

| Component | Unit Test | Performance | Integration | Eval |
|-----------|-----------|-------------|-------------|------|
| CNO-AX Engine | â€” | âœ… 1000 Strikes | IT-003 | â€” |
| 14-Mirror Array | UT-009 | â€” | IT-003 | âœ… |
| ADHD Lens | UT-002 | â€” | IT-003 | âœ… |
| Autism Lens | UT-003 | â€” | IT-003 | âœ… |
| Dyslexia Lens | UT-004 | â€” | IT-003 | âœ… |
| Neurotypical | UT-005 | â€” | IT-003 | âœ… |
| WebSocket | UT-014 | â€” | IT-006 | â€” |
| Sigma Engine | UT-010 | â€” | IT-009 | â€” |
| A1 Filing | UT-013 | â€” | â€” | â€” |
| Voice Interface | â€” | â€” | IT-008 | â€” |

---

## 4. Environments

| Environment | AI Mode | Purpose |
|-------------|---------|---------|
| Local Dev | Mock (`MOCK_AI=true`) | Fast iteration |
| Local Live | Live (`MOCK_AI=false`) | Full pipeline validation |
| Performance | Live or Mock | 1000 Strikes protocol |
| CI (GitHub Actions) | Mock | Automated regression |

---

## 5. Known Gaps

| Gap | Risk | Mitigation |
|-----|------|------------|
| Dashboard WebSocket not yet wired | UI shows mock data | SF-027 in backlog |
| Voice pipeline not yet connected to /api/chat | Voice doesn't reach AI | SF-028 in backlog |
| No CI pipeline yet | No automated testing on push | SF-026 in backlog |
| Cosmos DB not active | No persistence | SF-029 in backlog |

---

## Definition of Test Done

- [ ] Test written and passes locally
- [ ] CNO-AX metrics not degraded by change
- [ ] 1000 Strikes protocol re-run if performance-critical code changed
- [ ] No existing tests broken
- [ ] Accessibility: lens outputs reviewed for neurodivergent dignity

