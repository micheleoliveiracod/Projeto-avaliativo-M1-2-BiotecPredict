"""
Fixtures compartilhadas para testes.

Fornece:
- db_session: Sessão de banco de dados em memória
- client: Cliente FastAPI para testes
- test_batch: Batch de teste pré-configurado
- test_sensor_readings: Leituras de sensores de teste
"""

import sys
import os

# Adicionar backend ao path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from fastapi.testclient import TestClient
from backend.models import Batch, SensorReading
from backend.db.database import Base, get_db
from backend.main import app
from datetime import datetime


@pytest.fixture(scope="function")
def db_session() -> Session:
    """Criar sessão de banco de dados em memória para testes."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()

    yield db

    db.close()


@pytest.fixture(scope="function")
def client(db_session: Session) -> TestClient:
    """Criar cliente FastAPI com banco de dados de teste."""

    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)


@pytest.fixture(scope="function")
def test_batch(db_session: Session) -> Batch:
    """Criar batch de teste."""
    batch = Batch(
        upload_date=datetime.utcnow(),
        status="COMPLETED",
        compliance_score=85.0,
        risk_prediction="LOW_RISK",
    )
    db_session.add(batch)
    db_session.commit()
    db_session.refresh(batch)
    return batch


@pytest.fixture(scope="function")
def test_sensor_readings(db_session: Session, test_batch: Batch) -> list:
    """Criar leituras de sensores de teste."""
    readings = [
        SensorReading(
            batch_id=test_batch.id,
            temperature=25.0,
            ph=7.0,
            dissolved_oxygen=50.0,
            pressure=5.0,
            agitator_speed=250.0,
        ),
        SensorReading(
            batch_id=test_batch.id,
            temperature=26.0,
            ph=7.1,
            dissolved_oxygen=51.0,
            pressure=5.1,
            agitator_speed=251.0,
        ),
    ]
    for reading in readings:
        db_session.add(reading)
    db_session.commit()
    return readings
