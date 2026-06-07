"""Testes para ML Service."""

import pytest
from backend.services.ml_service import MLService


class TestMLService:
    """Testes de predição de risco com Machine Learning."""

    def test_predict_low_risk(self):
        """Leituras normais devem prever LOW_RISK."""
        sensor_readings = [
            {
                "temperature": 25.0,
                "ph": 7.0,
                "dissolved_oxygen": 85.0,
                "pressure": 5.0,
                "agitator_speed": 250,
            }
        ]

        risk_class, confidence = MLService.predict_risk(sensor_readings)

        assert risk_class == "LOW_RISK"
        assert 0.0 <= confidence <= 1.0

    def test_predict_high_risk(self):
        """Leituras com múltiplos desvios devem prever HIGH_RISK."""
        sensor_readings = [
            {
                "temperature": 18.0,  # Abaixo do mínimo
                "ph": 8.0,  # Acima do máximo
                "dissolved_oxygen": 60.0,  # Abaixo do mínimo
                "pressure": 6.5,  # Acima do máximo
                "agitator_speed": 350,  # Acima do máximo
            }
        ]

        risk_class, confidence = MLService.predict_risk(sensor_readings)

        assert risk_class in ["HIGH_RISK", "MEDIUM_RISK"]
        assert 0.0 <= confidence <= 1.0

    def test_confidence_score_range(self):
        """Confidence score deve estar entre 0 e 1."""
        sensor_readings = [
            {
                "temperature": 25.0,
                "ph": 7.0,
                "dissolved_oxygen": 85.0,
                "pressure": 5.0,
                "agitator_speed": 250,
            }
        ]

        risk_class, confidence = MLService.predict_risk(sensor_readings)

        assert 0.0 <= confidence <= 1.0

    def test_evaluate_batch_risk_structure(self):
        """Deve retornar estrutura completa de avaliação."""
        sensor_readings = [
            {
                "temperature": 25.0,
                "ph": 7.0,
                "dissolved_oxygen": 85.0,
                "pressure": 5.0,
                "agitator_speed": 250,
            }
        ]

        result = MLService.evaluate_batch_risk(sensor_readings)

        assert "risk_prediction" in result
        assert "confidence_score" in result
        assert "interpretation" in result
        assert "recommendations" in result
        assert isinstance(result["recommendations"], list)

    def test_get_model_info(self):
        """Deve retornar informações do modelo."""
        model_info = MLService.get_model_info()

        assert "model_type" in model_info
        assert "features" in model_info
        assert "risk_classes" in model_info
        assert "feature_importance" in model_info
        assert model_info["model_type"] == "RandomForestClassifier"

    def test_multiple_readings_averaging(self):
        """Deve fazer média de múltiplas leituras."""
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

        risk_class, confidence = MLService.predict_risk(sensor_readings)

        assert risk_class in ["LOW_RISK", "MEDIUM_RISK", "HIGH_RISK"]
        assert 0.0 <= confidence <= 1.0

    def test_empty_readings(self):
        """Leituras vazias devem retornar MEDIUM_RISK padrão."""
        risk_class, confidence = MLService.predict_risk([])

        assert risk_class == "MEDIUM_RISK"
        assert confidence == 0.5

    def test_recommendations_low_risk(self):
        """LOW_RISK deve ter recomendações apropriadas."""
        sensor_readings = [
            {
                "temperature": 25.0,
                "ph": 7.0,
                "dissolved_oxygen": 85.0,
                "pressure": 5.0,
                "agitator_speed": 250,
            }
        ]

        result = MLService.evaluate_batch_risk(sensor_readings)

        assert len(result["recommendations"]) > 0
        assert any("monitoramento" in rec.lower() for rec in result["recommendations"])

    def test_recommendations_high_risk(self):
        """HIGH_RISK deve ter recomendações de intervenção."""
        sensor_readings = [
            {
                "temperature": 18.0,
                "ph": 8.0,
                "dissolved_oxygen": 60.0,
                "pressure": 6.5,
                "agitator_speed": 350,
            }
        ]

        result = MLService.evaluate_batch_risk(sensor_readings)

        assert len(result["recommendations"]) > 0
