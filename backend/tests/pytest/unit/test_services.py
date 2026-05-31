"""
Testes unitários para services.

Testa:
- BatchService
- DataService
- Processamento de CSV
"""

import pytest
from backend.services import BatchService, DataService
from backend.processors import CSVProcessor, DataValidator, DataCleaner


def test_csv_processor_valid():
    """Testar processamento de CSV válido."""
    csv_content = """temperature,ph,dissolved_oxygen,pressure,agitator_speed
25.0,7.0,50.0,5.0,250.0
26.0,7.1,51.0,5.1,251.0"""

    rows = CSVProcessor.process(csv_content)
    assert len(rows) == 2
    assert rows[0]["temperature"] == 25.0


def test_csv_processor_missing_columns():
    """Testar CSV com colunas faltando."""
    csv_content = """temperature,ph
25.0,7.0"""

    with pytest.raises(ValueError):
        CSVProcessor.process(csv_content)


def test_data_validator_valid():
    """Testar validação de dados válidos."""
    rows = [
        {
            "temperature": 25.0,
            "ph": 7.0,
            "dissolved_oxygen": 50.0,
            "pressure": 5.0,
            "agitator_speed": 250.0,
        }
    ]

    valid_rows, errors = DataValidator.validate_batch(rows)
    assert len(valid_rows) == 1
    assert len(errors) == 0


def test_data_validator_out_of_range():
    """Testar validação com valores fora do range."""
    rows = [
        {
            "temperature": 50.0,  # Fora do range
            "ph": 7.0,
            "dissolved_oxygen": 50.0,
            "pressure": 5.0,
            "agitator_speed": 250.0,
        }
    ]

    valid_rows, errors = DataValidator.validate_batch(rows)
    assert len(valid_rows) == 0
    assert len(errors) > 0


def test_data_cleaner_remove_nulls():
    """Testar remoção de nulos."""
    rows = [
        {
            "temperature": 25.0,
            "ph": 7.0,
            "dissolved_oxygen": 50.0,
            "pressure": 5.0,
            "agitator_speed": 250.0,
        },
        {
            "temperature": None,
            "ph": 7.0,
            "dissolved_oxygen": 50.0,
            "pressure": 5.0,
            "agitator_speed": 250.0,
        },
    ]

    cleaned = DataCleaner.remove_nulls(rows)
    assert len(cleaned) == 1


def test_batch_service_process_csv(db_session):
    """Testar processamento de CSV através do service."""
    csv_content = """temperature,ph,dissolved_oxygen,pressure,agitator_speed
25.0,7.0,50.0,5.0,250.0
26.0,7.1,51.0,5.1,251.0"""

    batch, warnings = BatchService.process_csv_upload(db_session, csv_content)
    assert batch.id is not None
    assert batch.status == "COMPLETED"
    assert len(batch.sensor_readings) == 2


def test_data_service_get_sensor_readings(db_session, test_batch, test_sensor_readings):
    """Testar obtenção de sensor readings."""
    readings = DataService.get_sensor_readings(db_session, test_batch.id)
    assert len(readings) == 2
    assert readings[0].temperature == 25.0
