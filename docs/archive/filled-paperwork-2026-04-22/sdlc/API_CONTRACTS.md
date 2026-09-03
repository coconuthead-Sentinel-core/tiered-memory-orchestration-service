# API / Interface Contracts
## Sentinel Forge Cognitive AI Orchestration Platform v4.0

**Architect:** Shannon Brian Kelley
**Implementation:** Claude AI (Anthropic)
**Date:** April 2026
**Base URL:** http://localhost:8000

---

## POST /api/chat

**Purpose:** Submit input for cognitive processing through lens + 14-Mirror Array + Azure OpenAI.

### Input
```json
{
    "message": "string (required) â€” user input text or glyph sequence",
    "lens": "adhd | autism | dyslexia | neurotypical (optional â€” defaults to profile)"
}
```

### Output (200 OK)
```json
{
    "response": "string â€” AI-processed cognitive output",
    "lens_applied": "adhd",
    "zone": "GREEN | YELLOW | RED",
    "entropy": 0.847,
    "mirror_array": ["M1", "M2", "M4"],
    "symbolic_matches": 3,
    "latency_ms": 11.90,
    "timestamp": "15:22:00"
}
```

### Error (400)
```json
{ "error": "message is required" }
```

---

## GET /api/status

**Purpose:** Health check and system state.

### Output (200 OK)
```json
{
    "status": "GREEN",
    "version": "4.0",
    "architect": "Shannon Brian Kelley",
    "platform": "Sentinel Forge Cognitive AI Orchestration Platform",
    "ai_mode": "live | mock",
    "uptime_seconds": 3600,
    "stillwater": true,
    "persona": "Crystalline Navigator"
}
```

---

## GET /api/metrics

**Purpose:** Full snapshot â€” zones, mirrors, CNO-AX performance, lens usage.

### Output (200 OK)
```json
{
    "system_status": "GREEN",
    "uptime_seconds": 3600,
    "cno_ax": {
        "flow_rate": 220.3,
        "efficiency": 0.941,
        "latency_ms": 11.90,
        "jitter_ms": 3.41,
        "stillwater": true,
        "strikes_completed": 1000
    },
    "zone_distribution": {
        "active": { "count": 45, "percentage": 30.0 },
        "pattern": { "count": 60, "percentage": 40.0 },
        "crystal": { "count": 45, "percentage": 30.0 }
    },
    "mirror_array": {
        "green_active": ["M1","M2","M4","M6"],
        "yellow_flux": ["M3","M5","M7","M8"],
        "red_crystal": ["M9","M10","M11","M12","M13","M14"]
    },
    "lens_usage": {
        "adhd": { "count": 40, "percentage": 26.7 },
        "autism": { "count": 35, "percentage": 23.3 },
        "dyslexia": { "count": 25, "percentage": 16.7 },
        "neurotypical": { "count": 50, "percentage": 33.3 }
    },
    "symbolic_matches": 23
}
```

---

## POST /api/glyph/process

**Purpose:** Process emoji or glyph sequences through the 14-Mirror Array.

### Input
```json
{
    "sequence": "ðŸ’ ðŸ”ºðŸŸ«"
}
```

### Output (200 OK)
```json
{
    "glyphs": ["ðŸ’ ", "ðŸ”º", "ðŸŸ«"],
    "interpretations": ["Metatron", "Apex", "Grounding"],
    "mirrors_activated": ["M1", "M4", "M9"],
    "zone": "GREEN",
    "confidence": 0.94,
    "spatial_vector": [0.8, 0.6, 0.9]
}
```

---

## WebSocket: /ws/cognitive

**Purpose:** Real-time combined event stream â€” cognitive events + periodic metrics.

### Zone Transition Event
```json
{
    "type": "cognitive.zone_transition",
    "data": {
        "note_id": "uuid",
        "input_zone": "active",
        "output_zone": "pattern",
        "entropy": 0.65,
        "timestamp": 1234567890
    }
}
```

### Metrics Event (every 2 seconds)
```json
{
    "type": "cognitive.metrics",
    "data": {
        "zone_metrics": {
            "total_processed": 150,
            "zone_distribution": {...},
            "lens_usage": {...},
            "symbolic_matches": 23
        },
        "cno_ax": {
            "latency_ms": 11.90,
            "efficiency": 0.941,
            "stillwater": true
        },
        "timestamp": 1234567890
    }
}
```

---

## WebSocket: /ws/metrics

**Purpose:** Legacy performance dashboard data (2-second intervals).

```json
{
    "event": "metrics_update",
    "latency_ms": 11.90,
    "jitter_ms": 3.41,
    "throughput": 220.3,
    "efficiency": 0.941,
    "memory_usage": 68,
    "timestamp": "15:22:00"
}
```

---

## WebSocket: /ws/events

**Purpose:** System event notifications.

```json
{
    "type": "system.event",
    "event": "stillwater_achieved | zone_overflow | profile_updated | lens_switched",
    "data": {...},
    "timestamp": 1234567890
}
```

---

## Cognitive Lens Interface Contract

All lenses implement:
```python
def transform_context(self, input_text: str, zone: str) -> dict:
    # Returns: { response, structured_output, lens_metadata }

def chunk_response(self, text: str) -> list:
    # Returns: list of chunked segments per lens rules

def get_mirror_affinity(self) -> list:
    # Returns: list of mirror IDs this lens activates preferentially
```

---

## Sentinel Profile API (Internal)

```python
service.profile_get() -> dict          # Returns current profile
service.profile_update(data) -> None   # Updates and persists profile
sigma_engine.get_feature_flags() -> dict  # Returns active feature flags
```

---

## Error Handling Standards

| HTTP Code | Meaning | When Used |
|-----------|---------|-----------|
| 200 | Success | All successful requests |
| 400 | Bad Request | Missing required fields |
| 422 | Unprocessable | Invalid glyph or lens value |
| 500 | Server Error | Unhandled exception |

Azure OpenAI failures handled internally â€” adapter falls back to mock silently.

