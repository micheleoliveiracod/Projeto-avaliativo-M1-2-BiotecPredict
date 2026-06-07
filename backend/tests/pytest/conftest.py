"""
Fixtures compartilhadas para todos os testes pytest do BiotecPredict.

Fornece:
- test_engine: Engine SQLite in-memory por teste
- db_session: Sessão de banco de dados isolada por teste
- client: TestClient FastAPI com banco de dados de teste injetado
- sample_batch_data / sample_sensor_readings: dados de exemplo
"""

import sys
from pathlib import Path

# Garante que o root do projeto esteja no sys.path
ROOT = Path(__file__).parent.parent.parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient
from datetime import datetime

from backend.db.database import Base, get_db
from backend.main import app


# ── Fixtures de banco de dados ────────────────────────────────────────────────

@pytest.fixture(scope="function")
def test_engine():
    """
    Cria engine SQLite in-memory isolado por função de teste.
    StaticPool garante que todas as sessões compartilhem a mesma conexão
    (necessário para SQLite in-memory, onde cada conexão é um DB diferente).
    """
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


@pytest.fixture(scope="function")
def db_session(test_engine):
    """Sessão de banco de dados vinculada ao engine de teste."""
    TestingSession = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    session = TestingSession()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture(scope="function")
def client(db_session):
    """
    TestClient FastAPI com get_db sobrescrito para usar o banco de teste.
    Garante isolamento completo entre testes.
    """
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


# ── Fixtures de dados de exemplo ─────────────────────────────────────────────

@pytest.fixture(scope="function")
def sample_batch_data() -> dict:
    """Dados de exemplo para batch de teste."""
    return {
        "upload_date": datetime.utcnow(),
        "status": "COMPLETED",
        "compliance_score": 85.0,
        "risk_prediction": "LOW_RISK",
    }


@pytest.fixture(scope="function")
def sample_sensor_readings() -> list:
    """Leituras de sensores dentro dos ranges ideais do ComplianceService."""
    return [
        {
            "temperature": 25.0,
            "ph": 7.0,
            "dissolved_oxygen": 85.0,
            "pressure": 5.0,
            "agitator_speed": 260.0,
        },
        {
            "temperature": 25.5,
            "ph": 7.1,
            "dissolved_oxygen": 87.0,
            "pressure": 5.1,
            "agitator_speed": 255.0,
        },
    ]


@pytest.fixture(scope="function")
def valid_csv_content() -> bytes:
    """CSV válido com dados dentro dos ranges ideais."""
    return b"""temperature,ph,dissolved_oxygen,pressure,agitator_speed
25.0,7.0,85.0,5.0,260
25.5,7.1,87.0,5.1,255
24.8,7.0,86.0,4.9,258
25.2,7.2,88.0,5.2,262
"""


@pytest.fixture(scope="function")
def valid_csv_boundary() -> bytes:
    """CSV válido com valores nos limites aceitáveis do DataValidator."""
    return b"""temperature,ph,dissolved_oxygen,pressure,agitator_speed
20.0,4.0,0.0,0.0,0.0
45.0,9.0,100.0,10.0,500.0
"""
