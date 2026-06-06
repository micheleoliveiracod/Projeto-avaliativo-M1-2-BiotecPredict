"""Tests for database configuration values."""

from backend.db.database import DATABASE_URL, engine, SessionLocal, Base, get_db


def test_database_url_is_sqlite():
    assert "sqlite" in DATABASE_URL


def test_engine_has_correct_url():
    assert str(engine.url) == DATABASE_URL or "sqlite" in str(engine.url)


def test_session_local_is_callable():
    assert callable(SessionLocal)


def test_get_db_is_callable():
    assert callable(get_db)


def test_base_has_metadata():
    assert hasattr(Base, "metadata")
    assert Base.metadata is not None
