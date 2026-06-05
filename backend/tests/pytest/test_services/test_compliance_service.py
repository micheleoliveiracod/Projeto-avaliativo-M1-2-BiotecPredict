"""Testes para Compliance Service."""

import pytest
from backend.services.compliance_service import ComplianceService


class TestComplianceService:
    """Testes de Manufacturing Compliance Score."""

    def test_acceptable_score(self):
        """Score dentro dos limites ideais deve retornar ACCEPTABLE."""
        sensor_readings = [
            {
                "temperature": 25.0,
                "ph": 7.0,
                "dissolved_oxygen": 85.0,
                "pressure": 5.0,
                "agitator_speed": 250,
            }
        ]

        score, classification = ComplianceService.calculate_compliance_score(sensor_readings)

        assert 80 <= score <= 100
        assert classification == "ACCEPTABLE"

    def test_warning_score(self):
        """Score com desvios moderados deve retornar WARNING."""
        sensor_readings = [
            {
                "temperature": 28.0,  # Acima do ideal mas dentro do aceitável
                "ph": 6.5,  # Abaixo do ideal mas dentro do aceitável
                "dissolved_oxygen": 75.0,  # Abaixo do ideal
                "pressure": 5.3,
                "agitator_speed": 260,
            }
        ]

        score, classification = ComplianceService.calculate_compliance_score(sensor_readings)

        assert 60 <= score < 80
        assert classification == "WARNING"

    def test_critical_score(self):
        """Score com violações críticas deve retornar CRITICAL."""
        sensor_readings = [
            {
                "temperature": 35.0,  # Fora da faixa aceitável
                "ph": 8.0,  # Fora da faixa aceitável
                "dissolved_oxygen": 110.0,  # Fora da faixa aceitável
                "pressure": 6.5,  # Fora da faixa aceitável
                "agitator_speed": 350,  # Fora da faixa aceitável
            }
        ]

        score, classification = ComplianceService.calculate_compliance_score(sensor_readings)

        assert score < 60
        assert classification == "CRITICAL"

    def test_empty_readings(self):
        """Sensor readings vazio deve retornar CRITICAL."""
        score, classification = ComplianceService.calculate_compliance_score([])

        assert score == 0.0
        assert classification == "CRITICAL"

    def test_multiple_readings_average(self):
        """Deve calcular média de múltiplas leituras."""
        sensor_readings = [
            {
                "temperature": 25.0,
                "ph": 7.0,
                "dissolved_oxygen": 85.0,
                "pressure": 5.0,
                "agitator_speed": 250,
            },
            {
                "temperature": 25.0,
                "ph": 7.0,
                "dissolved_oxygen": 85.0,
                "pressure": 5.0,
                "agitator_speed": 250,
            },
        ]

        score, classification = ComplianceService.calculate_compliance_score(sensor_readings)

        assert 80 <= score <= 100
        assert classification == "ACCEPTABLE"

    def test_get_sensor_metrics(self):
        """Deve retornar métricas detalhadas por sensor."""
        sensor_readings = [
            {
                "temperature": 24.0,
                "ph": 6.8,
                "dissolved_oxygen": 80.0,
                "pressure": 4.8,
                "agitator_speed": 240,
            },
            {
                "temperature": 26.0,
                "ph": 7.2,
                "dissolved_oxygen": 90.0,
                "pressure": 5.2,
                "agitator_speed": 260,
            },
        ]

        metrics = ComplianceService.get_sensor_metrics(sensor_readings)

        assert "temperature" in metrics
        assert metrics["temperature"]["average"] == 25.0
        assert metrics["temperature"]["min"] == 24.0
        assert metrics["temperature"]["max"] == 26.0
        assert metrics["temperature"]["count"] == 2

    def test_score_range(self):
        """Score deve estar sempre entre 0 e 100."""
        test_cases = [
            [],
            [{"temperature": 20.0, "ph": 5.0, "dissolved_oxygen": 50.0, "pressure": 3.0, "agitator_speed": 100}],
            [{"temperature": 25.0, "ph": 7.0, "dissolved_oxygen": 85.0, "pressure": 5.0, "agitator_speed": 250}],
            [{"temperature": 40.0, "ph": 9.0, "dissolved_oxygen": 150.0, "pressure": 10.0, "agitator_speed": 500}],
        ]

        for sensor_readings in test_cases:
            score, classification = ComplianceService.calculate_compliance_score(sensor_readings)
            assert 0.0 <= score <= 100.0
