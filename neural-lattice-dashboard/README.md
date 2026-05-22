# Neural Lattice Live Diagnostic Dashboard

QNF-BLUEPRINT-DASH-001 · Single-page web app that monitors and validates the
Neural Lattice Cognitive Architecture in real time.

## Stack
- **Backend**: FastAPI + SQLAlchemy + SQLite
- **Frontend**: React 18 (Babel Standalone, no Node toolchain needed)
- **Served as**: one process — FastAPI mounts the built frontend at `/`

## Quick start
```bash
cd neural-lattice-dashboard
python3 -m venv .venv
.venv/bin/pip install -r backend/requirements.txt
.venv/bin/python -m uvicorn app.main:app --app-dir backend --host 0.0.0.0 --port 8000
# open http://localhost:8000
```

Swagger UI at `/docs`, health check at `/api/health`.

## Tests
```bash
.venv/bin/python -m pytest tests/ -q
# 40 passed
```

## Endpoints
| Method | Path | Purpose |
| --- | --- | --- |
| GET  | `/api/health` | Liveness probe |
| GET  | `/api/diagnostics` | Latest cached diagnostic run |
| GET  | `/api/diagnostics/run` | Execute all 6 diagnostic tests |
| GET  | `/api/zones` | Zone metadata + counts |
| POST | `/api/zones/classify` | Map cognitive_load → zone |
| POST | `/api/zones/migrate` | Apply FSM transition with guards |
| GET  | `/api/protocols` | 3 protocols with ACTIVE/STANDBY status |
| GET  | `/api/components` | Component registry (filter by `?zone=`) |
| POST | `/api/components` | Create registry entry |
| POST | `/api/metadata/validate` | Validate a 10-field metadata block |
| GET  | `/api/pipeline` | 8-stage cognitive pipeline definition |
| POST | `/api/sessions` | Start a session (Pomodoro) |
| GET  | `/api/sessions/current` | Active session + remaining time |

## Project layout
```
neural-lattice-dashboard/
  backend/
    app/
      main.py            FastAPI app + SPA hosting
      database.py        SQLite engine + session
      models.py          SQLAlchemy models
      schemas.py         Pydantic request/response models
      routers/           One file per resource
      services/
        zone_engine.py       FSM with transition guards
        metadata_engine.py   10-field validator + cross-checks
        diagnostic_engine.py 6 named tests (RSML, DPRU, AHCL, …)
        protocol_engine.py   3-protocol activation matrix
    run.py
    requirements.txt
  frontend/
    dist/                Production bundle (served by FastAPI)
      index.html
      assets/dashboard.css
      assets/app.jsx
    src/                 Source mirror of dist
    package.json
  tests/                 pytest suite (40 tests)
  README.md
```

## Frontend notes
The blueprint section 6 lists nine component files. To keep the project
zero-toolchain we bundle them as one `App.jsx` rendered via Babel Standalone;
all named components (`DiagnosticPanel`, `ZoneOverview`, `ProtocolStatus`,
`PipelineFlow`, `ComponentRegistry`, `MetadataValidator`, `CognitiveGauge`,
`SessionManager`) are defined inside that file.

## Acceptance checklist
- [x] `GET /api/diagnostics/run` returns 6 results with PASS/FAIL
- [x] `POST /api/zones/classify` maps load 1-10 to the correct zone
- [x] `POST /api/zones/migrate` enforces all 4 transition guards
- [x] `POST /api/metadata/validate` catches all 10 required fields
- [x] React dashboard loads in browser with 8 functional tabs
- [x] pytest passes — 40 tests
- [x] `http://localhost:8000` shows full dashboard
