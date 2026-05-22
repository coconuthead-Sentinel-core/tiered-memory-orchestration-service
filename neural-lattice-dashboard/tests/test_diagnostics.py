from app.services.diagnostic_engine import DiagnosticEngine


def test_run_all_returns_six_tests(db_session):
    results = DiagnosticEngine().run_all(db_session)
    assert len(results) == 6


def test_each_test_has_required_keys(db_session):
    for r in DiagnosticEngine().run_all(db_session):
        for key in ("id", "name", "status", "evidence", "timestamp"):
            assert key in r
        assert r["status"] in ("PASS", "FAIL")
        assert isinstance(r["evidence"], list)


def test_ids_are_sequential(db_session):
    results = DiagnosticEngine().run_all(db_session)
    assert [r["id"] for r in results] == [1, 2, 3, 4, 5, 6]
