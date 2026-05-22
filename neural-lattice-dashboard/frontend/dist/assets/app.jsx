const { useEffect, useMemo, useState, useCallback } = React;

const TABS = [
  { id: "overview",   label: "1 Overview" },
  { id: "memory",     label: "2 Memory Layers" },
  { id: "protocols",  label: "3 Protocols" },
  { id: "zones",      label: "4 Zones" },
  { id: "pipeline",   label: "5 Pipeline" },
  { id: "query",      label: "6 Query Interface" },
  { id: "components", label: "7 Components" },
  { id: "metadata",   label: "8 Metadata" },
];

const ZONE_CLASS = { GREEN: "zone-green", YELLOW: "zone-yellow", RED: "zone-red" };
const ZONE_COLOR = { GREEN: "#4CAF50", YELLOW: "#FFC107", RED: "#F44336" };

async function api(path, opts = {}) {
  const res = await fetch(path, {
    headers: { "Content-Type": "application/json" },
    ...opts,
  });
  if (!res.ok && res.status !== 400 && res.status !== 404 && res.status !== 409) {
    throw new Error(`${res.status} ${res.statusText}`);
  }
  return res.json();
}

function ZonePill({ zone }) {
  return <span className={`zone-pill ${ZONE_CLASS[zone] || ""}`}>{zone}</span>;
}

function StatusBadge({ status }) {
  const cls = status === "PASS" ? "pass" : "fail";
  return <span className={`status-badge ${cls}`}>{status}</span>;
}

function CognitiveGauge({ value }) {
  const v = Math.max(1, Math.min(10, Number(value) || 1));
  const pct = (v - 1) / 9;
  const r = 60, c = 2 * Math.PI * r;
  const stroke = v >= 7 ? ZONE_COLOR.GREEN : v >= 4 ? ZONE_COLOR.YELLOW : ZONE_COLOR.RED;
  return (
    <div className="gauge-wrap">
      <svg className="gauge" width="160" height="160" viewBox="0 0 160 160">
        <circle cx="80" cy="80" r={r} fill="none" stroke="var(--color-bg-tertiary)" strokeWidth="14" />
        <circle cx="80" cy="80" r={r} fill="none" stroke={stroke} strokeWidth="14"
          strokeDasharray={c} strokeDashoffset={c * (1 - pct)} strokeLinecap="round" />
      </svg>
      <div className="gauge-label" style={{ color: stroke }}>{v}/10</div>
      <div className="muted">Cognitive Load</div>
    </div>
  );
}

function DiagnosticCard({ test }) {
  const [open, setOpen] = useState(false);
  return (
    <div className="card diag-card">
      <div className="head">
        <div>
          <h3>{test.name}</h3>
          <div className="legacy">Legacy: {test.legacy_name}</div>
        </div>
        <StatusBadge status={test.status} />
      </div>
      <div className="row">
        <span className="muted">{test.evidence.length} evidence items</span>
        <button className="expand" onClick={() => setOpen(o => !o)}>{open ? "Hide" : "Show"} evidence</button>
      </div>
      {open && (
        <div className="evidence">
          <ul>{test.evidence.map((e, i) => <li key={i}>{e}</li>)}</ul>
        </div>
      )}
    </div>
  );
}

function DiagnosticPanel({ tests }) {
  return (
    <div className="grid grid-3">
      {tests.map(t => <DiagnosticCard key={t.id} test={t} />)}
    </div>
  );
}

function ZoneOverview({ zones, onSelect }) {
  return (
    <div className="grid grid-3">
      {zones.map(z => (
        <div key={z.name} className="card" onClick={() => onSelect && onSelect(z.name)} style={{ cursor: onSelect ? "pointer" : "default" }}>
          <div className="row">
            <ZonePill zone={z.name} />
            <span className="muted">{z.access}</span>
          </div>
          <div style={{ fontSize: 32, fontWeight: 700, marginTop: 10 }}>{z.count}</div>
          <div className="muted">documents · load {z.load_range}</div>
        </div>
      ))}
    </div>
  );
}

function ProtocolStatus({ protocols }) {
  const classFor = id => id === "PROTO-001" ? "onset" : id === "PROTO-002" ? "joy" : "coconut";
  return (
    <div className="card">
      <h3>Active Protocols</h3>
      <div style={{ display: "flex", gap: 10, flexWrap: "wrap", marginTop: 8 }}>
        {protocols.map(p => (
          <span
            key={p.id}
            className={`proto-badge ${p.status === "ACTIVE" ? "active" : "standby"} ${classFor(p.id)}`}
            title={p.activation_rule}
          >
            {p.name} · {p.status}
          </span>
        ))}
      </div>
    </div>
  );
}

function PipelineFlow({ stages, activeIdx = -1 }) {
  return (
    <div className="pipeline">
      {stages.map((s, i) => (
        <React.Fragment key={s.id}>
          <div className={`node ${i === activeIdx ? "active" : ""}`}>
            <div className="muted">{s.id}</div>
            <div style={{ fontWeight: 700 }}>{s.name}</div>
            <div className="muted" style={{ marginTop: 6 }}>{s.description}</div>
            <div style={{ marginTop: 6, fontSize: 12 }}><strong>Output:</strong> {s.output}</div>
          </div>
          {i < stages.length - 1 && <div className="arrow">→</div>}
        </React.Fragment>
      ))}
    </div>
  );
}

function ComponentRegistry({ rows, zoneFilter, onZoneFilter }) {
  const [search, setSearch] = useState("");
  const [sortKey, setSortKey] = useState("doc_id");
  const [sortDir, setSortDir] = useState(1);
  const [expanded, setExpanded] = useState(null);

  const filtered = useMemo(() => {
    let r = rows;
    if (zoneFilter) r = r.filter(x => x.zone === zoneFilter);
    if (search) {
      const q = search.toLowerCase();
      r = r.filter(x => x.doc_id.toLowerCase().includes(q) || x.name.toLowerCase().includes(q));
    }
    return [...r].sort((a, b) => {
      const av = a[sortKey], bv = b[sortKey];
      if (av === bv) return 0;
      return av > bv ? sortDir : -sortDir;
    });
  }, [rows, zoneFilter, search, sortKey, sortDir]);

  const toggleSort = k => {
    if (sortKey === k) setSortDir(d => -d);
    else { setSortKey(k); setSortDir(1); }
  };

  return (
    <div className="card">
      <div className="controls">
        <input placeholder="Search doc_id or name…" value={search} onChange={e => setSearch(e.target.value)} />
        <select value={zoneFilter || ""} onChange={e => onZoneFilter(e.target.value || null)}>
          <option value="">All zones</option>
          <option value="GREEN">GREEN</option>
          <option value="YELLOW">YELLOW</option>
          <option value="RED">RED</option>
        </select>
        <span className="muted">{filtered.length} of {rows.length}</span>
      </div>
      <table>
        <thead>
          <tr>
            {["doc_id","name","zone","cognitive_load","status","artifact_type"].map(k => (
              <th key={k} onClick={() => toggleSort(k)}>{k} {sortKey===k ? (sortDir>0?"▲":"▼") : ""}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {filtered.map(r => (
            <React.Fragment key={r.doc_id}>
              <tr onClick={() => setExpanded(expanded === r.doc_id ? null : r.doc_id)} style={{ cursor: "pointer" }}>
                <td>{r.doc_id}</td>
                <td>{r.name}</td>
                <td><ZonePill zone={r.zone} /></td>
                <td>{r.cognitive_load}</td>
                <td>{r.status}</td>
                <td>{r.artifact_type}</td>
              </tr>
              {expanded === r.doc_id && (
                <tr><td colSpan="6" style={{ background: "var(--color-bg-tertiary)" }}>
                  <pre style={{ margin: 0, whiteSpace: "pre-wrap" }}>{JSON.stringify(r, null, 2)}</pre>
                </td></tr>
              )}
            </React.Fragment>
          ))}
        </tbody>
      </table>
    </div>
  );
}

const SAMPLE_METADATA = JSON.stringify({
  doc_id: "QNF-DIAG-001",
  title: "Live Diagnostic",
  zone: "GREEN",
  protocol: "Onset_Omega_1",
  artifact_type: "DIAGNOSTIC",
  cognitive_load: 8,
  timestamp: "2026-05-21T00:00:00+00:00",
  dependencies: ["CSTM-V30-FINAL-001"],
  tags: ["diagnostic"],
  status: "ACTIVE"
}, null, 2);

function MetadataValidator() {
  const [text, setText] = useState(SAMPLE_METADATA);
  const [result, setResult] = useState(null);
  const [err, setErr] = useState("");

  const validate = async () => {
    setErr("");
    let block;
    try { block = JSON.parse(text); }
    catch (e) { setErr("Invalid JSON: " + e.message); return; }
    const res = await api("/api/metadata/validate", { method: "POST", body: JSON.stringify({ metadata_block: block }) });
    setResult(res);
  };

  return (
    <div className="card metadata-form">
      <h3>Metadata Validator</h3>
      <div className="muted">Paste a 10-field metadata block. Zone and cognitive_load are cross-validated.</div>
      <textarea value={text} onChange={e => setText(e.target.value)} />
      <div className="controls">
        <button onClick={validate}>Validate</button>
        <button onClick={() => setText(SAMPLE_METADATA)}>Reset sample</button>
      </div>
      {err && <div className="error-list">{err}</div>}
      {result && (
        result.valid
          ? <div className="success-text">✓ Valid (all 10 fields pass)</div>
          : <ul className="error-list">{result.errors.map((e,i) => <li key={i}>{e}</li>)}</ul>
      )}
    </div>
  );
}

function SessionManager({ session, onStart, onRefresh }) {
  useEffect(() => {
    const id = setInterval(onRefresh, 1000);
    return () => clearInterval(id);
  }, [onRefresh]);

  const [obj, setObj] = useState("Build diagnostic dashboard");
  const [zone, setZone] = useState("GREEN");
  const [box, setBox] = useState(25);

  const fmt = secs => {
    const m = String(Math.floor(secs / 60)).padStart(2, "0");
    const s = String(secs % 60).padStart(2, "0");
    return `${m}:${s}`;
  };

  return (
    <div className="card">
      <h3>Session Manager</h3>
      {session && session.active ? (
        <>
          <div className="row"><span className="muted">Objectives</span><ZonePill zone={session.session.zone} /></div>
          <div>{session.session.objectives}</div>
          <div className="session-timer" style={{ marginTop: 10 }}>{fmt(session.remaining_seconds)}</div>
          <div className="muted">elapsed {fmt(session.elapsed_seconds)} · box {session.session.time_box_minutes}m</div>
        </>
      ) : (
        <>
          <div className="muted">No active session</div>
          <div className="controls" style={{ marginTop: 8 }}>
            <input value={obj} onChange={e => setObj(e.target.value)} style={{ flex: 1 }} />
            <select value={zone} onChange={e => setZone(e.target.value)}>
              <option>GREEN</option><option>YELLOW</option><option>RED</option>
            </select>
            <input type="number" value={box} min="5" max="120" onChange={e => setBox(Number(e.target.value))} style={{ width: 70 }} />
            <button onClick={() => onStart(obj, zone, box)}>Start</button>
          </div>
        </>
      )}
    </div>
  );
}

function MemoryLayers({ tests }) {
  const tiers = [
    { id: "L0", name: "Identity & Charter", desc: "Persistent self-model + governing principles" },
    { id: "L1", name: "Working Context",    desc: "Active conversation and scratchpad" },
    { id: "L2", name: "Project Knowledge",  desc: "Codebase, blueprints, structured artifacts" },
    { id: "L3", name: "Archive & Retrieval",desc: "Long-term store, retrievable on demand" },
  ];
  const ctxTest = tests.find(t => t.id === 1);
  return (
    <>
      <div className="grid grid-4">
        {tiers.map(t => (
          <div key={t.id} className="card">
            <div className="row"><h3>{t.id} · {t.name}</h3><ZonePill zone="GREEN" /></div>
            <div className="muted" style={{ marginTop: 6 }}>{t.desc}</div>
          </div>
        ))}
      </div>
      {ctxTest && (
        <div style={{ marginTop: 14 }}>
          <div className="card">
            <div className="row"><h3>Context Assembly (RSML)</h3><StatusBadge status={ctxTest.status} /></div>
            <ul>{ctxTest.evidence.map((e,i) => <li key={i}>{e}</li>)}</ul>
          </div>
        </div>
      )}
    </>
  );
}

function MetadataSchema() {
  const fields = [
    ["doc_id", "String", "PREFIX-TYPE-###", "Regex match", "QNF-DIAG-001"],
    ["title", "String", "1-200 chars", "Unique, descriptive", "Live Diagnostic"],
    ["zone", "Enum", "GREEN|YELLOW|RED", "Must match load", "GREEN"],
    ["protocol", "String", "Protocol name(s)", "Valid protocol", "Onset_Omega_1"],
    ["artifact_type", "Enum", "Predefined list", "Type validity", "DIAGNOSTIC"],
    ["cognitive_load", "Integer", "1-10", "Aligns with zone", "8"],
    ["timestamp", "ISO8601", "RFC3339", "Valid datetime", "2026-05-21T00:00Z"],
    ["dependencies", "Array", "doc_id list", "IDs must exist", "[CSTM-V30-FINAL-001]"],
    ["tags", "Array", "lowercase_underscore", "Format check", "[diagnostic]"],
    ["status", "Enum", "Lifecycle state", "Valid state", "ACTIVE"],
  ];
  return (
    <div className="card">
      <h3>Metadata Schema · 10 Required Fields</h3>
      <table>
        <thead><tr><th>Field</th><th>Type</th><th>Format</th><th>Validation</th><th>Example</th></tr></thead>
        <tbody>{fields.map(f => <tr key={f[0]}>{f.map((c,i)=><td key={i}>{c}</td>)}</tr>)}</tbody>
      </table>
    </div>
  );
}

function App() {
  const [tab, setTab] = useState("overview");
  const [theme, setTheme] = useState(() => localStorage.getItem("theme") || "light");
  const [tests, setTests] = useState([]);
  const [zones, setZones] = useState([]);
  const [protocols, setProtocols] = useState([]);
  const [components, setComponents] = useState([]);
  const [pipeline, setPipeline] = useState([]);
  const [session, setSession] = useState(null);
  const [zoneFilter, setZoneFilter] = useState(null);
  const [load, setLoad] = useState(8);

  useEffect(() => {
    document.documentElement.setAttribute("data-theme", theme);
    localStorage.setItem("theme", theme);
  }, [theme]);

  const refreshAll = useCallback(async () => {
    const [diag, z, p, c, pl] = await Promise.all([
      api("/api/diagnostics/run"),
      api("/api/zones"),
      api(`/api/protocols?cognitive_load=${load}`),
      api("/api/components"),
      api("/api/pipeline"),
    ]);
    setTests(diag.tests);
    setZones(z.zones);
    setProtocols(p.protocols);
    setComponents(c.components);
    setPipeline(pl.stages);
  }, [load]);

  const refreshSession = useCallback(async () => {
    const s = await api("/api/sessions/current");
    setSession(s);
  }, []);

  useEffect(() => { refreshAll(); refreshSession(); }, [refreshAll, refreshSession]);

  const startSession = async (objectives, zone, time_box) => {
    await api("/api/sessions", { method: "POST", body: JSON.stringify({ objectives, zone, time_box }) });
    refreshSession();
    refreshAll();
  };

  const passCount = tests.filter(t => t.status === "PASS").length;

  return (
    <div className="app">
      <div className="topbar">
        <h1>NEURAL LATTICE · Live Diagnostic Dashboard</h1>
        <div className="badge-row">
          <span className="muted">{passCount}/{tests.length} tests pass</span>
          <button className="theme-toggle" onClick={() => setTheme(theme === "light" ? "dark" : "light")}>
            {theme === "light" ? "Dark" : "Light"} mode
          </button>
        </div>
      </div>

      <div className="tabs">
        {TABS.map(t => (
          <button key={t.id} className={`tab ${tab === t.id ? "active" : ""}`} onClick={() => setTab(t.id)}>{t.label}</button>
        ))}
      </div>

      <div className="content">
        {tab === "overview" && (
          <div className="grid grid-2">
            <div className="card">
              <h3>System Stats</h3>
              <div className="row" style={{ marginTop: 8 }}>
                <span className="muted">Diagnostics</span>
                <span className="success-text">{passCount}/{tests.length} PASS</span>
              </div>
              <div className="row"><span className="muted">Active protocols</span><span>{protocols.filter(p=>p.status==="ACTIVE").length}/3</span></div>
              <div className="row"><span className="muted">Registry size</span><span>{components.length}</span></div>
              <div className="controls" style={{ marginTop: 10 }}>
                <label>Cognitive load</label>
                <input type="range" min="1" max="10" value={load} onChange={e=>setLoad(Number(e.target.value))} />
                <span>{load}</span>
              </div>
            </div>
            <div className="card">
              <CognitiveGauge value={load} />
            </div>
            <ZoneOverview zones={zones} onSelect={(z) => { setZoneFilter(z); setTab("components"); }} />
            <SessionManager session={session} onStart={startSession} onRefresh={refreshSession} />
          </div>
        )}

        {tab === "memory" && <MemoryLayers tests={tests} />}

        {tab === "protocols" && (
          <div className="grid grid-2">
            <ProtocolStatus protocols={protocols} />
            <div className="card">
              <h3>Activation Rules</h3>
              <ul>
                <li><strong>Onset Omega 1</strong> — always active</li>
                <li><strong>Joy Protocol</strong> — when cognitive_load &gt; 7</li>
                <li><strong>Coconut Head</strong> — when a session is active</li>
              </ul>
              <div className="muted">Adjust load on the Overview tab to see Joy toggle.</div>
            </div>
          </div>
        )}

        {tab === "zones" && (
          <>
            <ZoneOverview zones={zones} onSelect={(z) => { setZoneFilter(z); setTab("components"); }} />
            <div style={{ marginTop: 14 }} className="card">
              <h3>Zone Transitions (FSM)</h3>
              <table>
                <thead><tr><th>From</th><th>To</th><th>Guard</th><th>Action</th></tr></thead>
                <tbody>
                  <tr><td><ZonePill zone="GREEN"/></td><td><ZonePill zone="YELLOW"/></td><td>load &lt; 7 AND status ≠ DRAFT</td><td>Update zone, timestamp</td></tr>
                  <tr><td><ZonePill zone="YELLOW"/></td><td><ZonePill zone="RED"/></td><td>load &lt; 4 AND version ≥ 1.0</td><td>Set ARCHIVED, timestamp</td></tr>
                  <tr><td><ZonePill zone="RED"/></td><td><ZonePill zone="YELLOW"/></td><td>Manual approval</td><td>Set ACTIVE, timestamp</td></tr>
                  <tr><td><ZonePill zone="RED"/></td><td><ZonePill zone="GREEN"/></td><td>Scope change approved</td><td>Set DRAFT, timestamp</td></tr>
                </tbody>
              </table>
            </div>
          </>
        )}

        {tab === "pipeline" && (
          <div className="card">
            <h3>8-Stage Cognitive Pipeline</h3>
            <PipelineFlow stages={pipeline} activeIdx={3} />
          </div>
        )}

        {tab === "query" && <MetadataValidator />}

        {tab === "components" && (
          <ComponentRegistry rows={components} zoneFilter={zoneFilter} onZoneFilter={setZoneFilter} />
        )}

        {tab === "metadata" && <MetadataSchema />}

        <div style={{ marginTop: 16 }}>
          <DiagnosticPanel tests={tests} />
        </div>
      </div>
    </div>
  );
}

ReactDOM.createRoot(document.getElementById("root")).render(<App />);
