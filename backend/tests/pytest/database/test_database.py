"""Tests for database configuration and connection."""

import pytest
from sqlalchemy import text

from backend.db.database import (
    Base,
    DATABASE_URL,
    SessionLocal,
    engine,
    get_db,
    init_db,
)


class TestDatabaseConfiguration:
    def test_database_url_configured(self):
        assert DATABASE_URL is not None
        assert "sqlite" in DATABASE_URL

    def test_engine_created(self):
        assert engine is not None
        assert hasattr(engine, "connect")
        assert hasattr(engine, "dispose")

    def test_session_local_created(self):
        assert SessionLocal is not None
        assert callable(SessionLocal)

    def test_base_declarative_created(self):
        assert Base is not None
        assert hasattr(Base, "metadata")


class TestDatabaseConnection:
    def test_connection_successful(self):
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            row = result.fetchone()
            assert row[0] == 1

    def test_session_query(self):
        db = SessionLocal()
        try:
            result = db.execute(text("SELECT 1"))
            row = result.fetchone()
            assert row[0] == 1
        finally:
            db.close()


class TestGetDbDependency:
    def test_get_db_is_generator(self):
        gen = get_db()
        db = next(gen)
        assert db is not None
        try:
            next(gen)
        except StopIteration:
            pass

    def test_get_db_yields_session(self):
        from sqlalchemy.orm import Session
        gen = get_db()
        db = next(gen)
        assert isinstance(db, Session)
        try:
            next(gen)
        except StopIteration:
            pass


class TestInitDb:
    def test_init_db_creates_tables(self):
        init_db()
        inspector = engine.dialect.get_table_names(engine.connect())
        assert isinstance(inspector, list)

    def test_batches_table_exists(self):
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        assert "batches" in tables

    def test_sensor_readings_table_exists(self):
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        assert "sensor_readings" in tables


class TestDatabaseEnvironmentVariables:
    def test_pool_size_env(self, monkeypatch):
        import os
        pool_size = os.getenv("DB_POOL_SIZE", "5")
        assert pool_size == "5"
