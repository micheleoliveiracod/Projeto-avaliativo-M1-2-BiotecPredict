"""
Testes unitários para schemas Pydantic.

Testa:
- Validação de ranges
- Validação de tipos
- Serialização/desserialização
"""

import pytest
from pydantic import ValidationError
from backend.schemas import SensorReadingSchema, PredictionSchema, BatchResponse


def test_sensor_reading_valid():
    """Testar sensor reading válido."""
    data = {
        "batch_id": 1,
        "temperature": 25.0,
        "ph": 7.0,
        "dissolved_oxygen": 50.0,
        "pressure": 5.0,
        "agitator_speed": 250.0,
    }
    reading = SensorReadingSchema(**data)
    assert reading.temperature == 25.0


def test_sensor_reading_temperature_out_of_range():
    """Testar temperatura fora do range."""
    data = {
        "batch_id": 1,
        "temperature": 50.0,  # Fora do range 20-45
        "ph": 7.0,
        "dissolved_oxygen": 50.0,
        "pressure": 5.0,
        "agitator_speed": 250.0,
    }
    with pytest.raises(ValidationError):
        SensorReadingSchema(**data)


def test_sensor_reading_ph_out_of_range():
    """Testar pH fora do range."""
    data = {
        "batch_id": 1,
        "temperature": 25.0,
        "ph": 10.0,  # Fora do range 4.0-9.0
        "dissolved_oxygen": 50.0,
        "pressure": 5.0,
        "agitator_speed": 250.0,
    }
    with pytest.raises(ValidationError):
        SensorReadingSchema(**data)


def test_prediction_valid():
    """Testar prediction válida."""
    data = {
        "batch_id": 1,
        "model_version": "v1.0.0",
        "confidence_score": 0.95,
        "risk_level": "LOW_RISK",
    }
    prediction = PredictionSchema(**data)
    assert prediction.confidence_score == 0.95


def test_prediction_confidence_out_of_range():
    """Testar confidence score fora do range."""
    data = {
        "batch_id": 1,
        "model_version": "v1.0.0",
        "confidence_score": 1.5,  # Fora do range 0-1
        "risk_level": "LOW_RISK",
    }
    with pytest.raises(ValidationError):
        PredictionSchema(**data)


def test_batch_response():
    """Testar batch response."""
    from datetime import datetime

    data = {
        "id": 1,
        "upload_date": datetime.utcnow(),
        "status": "COMPLETED",
        "compliance_score": 85.0,
        "risk_prediction": "LOW_RISK",
    }
    batch = BatchResponse(**data)
    assert batch.id == 1
    assert batch.compliance_score == 85.0
