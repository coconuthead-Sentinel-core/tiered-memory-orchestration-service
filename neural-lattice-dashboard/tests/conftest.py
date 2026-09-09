import os
import sys
import tempfile
import pytest

BACKEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend"))
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)


def _purge_app_modules():
    for name in list(sys.modules.keys()):
        if name == "app" or name.startswith("app."):
            sys.modules.pop(name, None)


@pytest.fixture()
def temp_db(monkeypatch):
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    monkeypatch.setenv("NLD_DB_PATH", path)
    _purge_app_modules()
    yield path
    _purge_app_modules()
    try:
        os.unlink(path)
    except OSError:
        pass


@pytest.fixture()
def client(temp_db):
    from fastapi.testclient import TestClient
    from app.main import create_app
    app = create_app()
    return TestClient(app)


@pytest.fixture()
def db_session(temp_db):
    from app.database import SessionLocal, Base, engine
    from app import models  # noqa: F401 — register tables with Base
    Base.metadata.create_all(bind=engine)
    s = SessionLocal()
    yield s
    s.close()
