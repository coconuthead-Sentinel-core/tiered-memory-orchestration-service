def test_health(client):
    r = client.get("/api/health")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "ok"
    assert "version" in body


def test_diagnostics_run(client):
    r = client.get("/api/diagnostics/run")
    assert r.status_code == 200
    body = r.json()
    assert len(body["tests"]) == 6


def test_zones_list(client):
    r = client.get("/api/zones")
    assert r.status_code == 200
    body = r.json()
    names = {z["name"] for z in body["zones"]}
    assert names == {"GREEN", "YELLOW", "RED"}


def test_zone_classify_each_range(client):
    for load, expected in [(10, "GREEN"), (5, "YELLOW"), (2, "RED")]:
        r = client.post("/api/zones/classify", json={"cognitive_load": load})
        assert r.status_code == 200
        assert r.json()["zone"] == expected


def test_metadata_validate_missing_fields(client):
    r = client.post("/api/metadata/validate", json={"metadata_block": {}})
    assert r.status_code == 200
    body = r.json()
    assert not body["valid"]
    assert len(body["errors"]) >= 10


def test_components_seed_present(client):
    r = client.get("/api/components")
    assert r.status_code == 200
    body = r.json()
    ids = {c["doc_id"] for c in body["components"]}
    assert "CSTM-V30-FINAL-001" in ids
    assert "NEURAL-LATTICE-001" in ids


def test_components_filter_by_zone(client):
    r = client.get("/api/components?zone=GREEN")
    assert r.status_code == 200
    body = r.json()
    assert all(c["zone"] == "GREEN" for c in body["components"])


def test_protocols_endpoint(client):
    r = client.get("/api/protocols")
    assert r.status_code == 200
    body = r.json()
    assert len(body["protocols"]) == 3


def test_pipeline_endpoint(client):
    r = client.get("/api/pipeline")
    assert r.status_code == 200
    body = r.json()
    assert len(body["stages"]) == 8


def test_sessions_lifecycle(client):
    r = client.post("/api/sessions", json={"objectives": "Build dashboard", "zone": "GREEN", "time_box": 25})
    assert r.status_code == 200
    cur = client.get("/api/sessions/current")
    assert cur.status_code == 200
    assert cur.json()["active"] is True


def test_zone_migrate_invalid_doc(client):
    r = client.post("/api/zones/migrate", json={"doc_id": "DOES-NOT-EXIST-001", "target_zone": "RED"})
    assert r.status_code == 404
