"""
Teste placeholder para validar que o pytest está funcionando.

Este arquivo será substituído pelos testes reais quando os módulos
backend.models, backend.schemas, etc. estiverem disponíveis.
"""

import pytest


def test_placeholder():
    """Teste placeholder que sempre passa."""
    assert True


def test_fixtures_available(sample_batch_data, sample_sensor_readings):
    """Validar que as fixtures estão disponíveis."""
    assert sample_batch_data is not None
    assert sample_sensor_readings is not None
    assert len(sample_sensor_readings) == 2
