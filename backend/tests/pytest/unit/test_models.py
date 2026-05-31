"""
Testes unitários para modelos SQLAlchemy.

Testa:
- Criação de modelos
- Relacionamentos
- Validações
"""

import pytest
from backend.models import Batch, SensorReading, Prediction
from datetime import datetime


def test_batch_creation():
    """Testar criação de batch."""
    batch = Batch(
        upload_date=datetime.utcnow(),
        status="COMPLETED",
        compliance_score=85.0,
        risk_prediction="LOW_RISK",
    )
    assert batch.id is None  # Não persistido ainda
    assert batch.status == "COMPLETED"
    assert batch.compliance_score == 85.0


def test_sensor_reading_creation():
    """Testar criação de sensor reading."""
    reading = SensorReading(
        batch_id=1,
        temperature=25.0,
        ph=7.0,
        dissolved_oxygen=50.0,
        pressure=5.0,
        agitator_speed=250.0,
    )
    assert reading.batch_id == 1
    assert reading.temperature == 25.0
    assert reading.ph == 7.0


def test_prediction_creation():
    """Testar criação de prediction."""
    prediction = Prediction(
        batch_id=1,
        model_version="v1.0.0",
        confidence_score=0.95,
        risk_level="LOW_RISK",
    )
    assert prediction.batch_id == 1
    assert prediction.model_version == "v1.0.0"
    assert prediction.confidence_score == 0.95


def test_batch_relationships(db_session):
    """Testar relacionamentos de batch."""
    batch = Batch(status="COMPLETED")
    db_session.add(batch)
    db_session.commit()

    reading = SensorReading(
        batch_id=batch.id,
        temperature=25.0,
        ph=7.0,
        dissolved_oxygen=50.0,
        pressure=5.0,
        agitator_speed=250.0,
    )
    db_session.add(reading)
    db_session.commit()

    # Verificar relacionamento
    assert len(batch.sensor_readings) == 1
    assert batch.sensor_readings[0].temperature == 25.0
