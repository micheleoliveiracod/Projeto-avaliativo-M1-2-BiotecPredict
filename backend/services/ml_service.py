"""
ML Service - Orquestração de predições de risco.

Integra modelo ML com lógica de negócio para predição de risco de processo.
"""

from typing import List, Dict, Tuple
from backend.ml.model import MLModel


class MLService:
    """Serviço para predição de risco com Machine Learning."""

    _model_instance = None

    @classmethod
    def _get_model(cls) -> MLModel:
        """Obtém instância singleton do modelo."""
        if cls._model_instance is None:
            cls._model_instance = MLModel()
        return cls._model_instance

    @staticmethod
    def predict_risk(sensor_readings: List[Dict]) -> Tuple[str, float]:
        """
        Prediz risco baseado em sensor readings.

        Args:
            sensor_readings: Lista de dicionários com leituras de sensores

        Returns:
            Tupla (risco_classificacao, confidence_0_1)
            Classificações:
            - LOW_RISK: Processo dentro dos parâmetros esperados
            - MEDIUM_RISK: Desvios moderados detectados
            - HIGH_RISK: Risco significativo de falha de processo
        """
        model = MLService._get_model()
        return model.predict(sensor_readings)

    @staticmethod
    def get_model_info() -> Dict:
        """Retorna informações sobre o modelo."""
        model = MLService._get_model()
        return {
            "model_type": "RandomForestClassifier",
            "n_estimators": model.model.n_estimators,
            "features": model.FEATURES,
            "risk_classes": list(model.RISK_CLASSES.values()),
            "feature_importance": model.get_feature_importance(),
        }

    @staticmethod
    def evaluate_batch_risk(sensor_readings: List[Dict]) -> Dict:
        """
        Avaliação completa de risco para um batch.

        Retorna análise detalhada do risco.
        """
        risk_class, confidence = MLService.predict_risk(sensor_readings)

        return {
            "risk_prediction": risk_class,
            "confidence_score": confidence,
            "interpretation": MLService._interpret_risk(risk_class),
            "recommendations": MLService._get_recommendations(risk_class),
        }

    @staticmethod
    def _interpret_risk(risk_class: str) -> str:
        """Interpretação textual do risco."""
        interpretations = {
            "LOW_RISK": "Processo dentro dos parâmetros esperados. Nenhuma ação imediata necessária.",
            "MEDIUM_RISK": "Desvios moderados detectados. Recomenda-se acompanhamento próximo.",
            "HIGH_RISK": "Risco significativo de falha de processo. Intervenção recomendada.",
        }
        return interpretations.get(risk_class, "Risco desconhecido")

    @staticmethod
    def _get_recommendations(risk_class: str) -> List[str]:
        """Recomendações baseadas no risco."""
        recommendations = {
            "LOW_RISK": [
                "Manter monitoramento contínuo",
                "Prosseguir com processo conforme planejado",
            ],
            "MEDIUM_RISK": [
                "Aumentar frequência de leituras",
                "Investigar causa dos desvios",
                "Considerar ajuste de parâmetros",
            ],
            "HIGH_RISK": [
                "Intervenção imediata recomendada",
                "Revisar todos os parâmetros de processo",
                "Considerar interromper e re-calibrar",
                "Alertar supervisor de qualidade",
            ],
        }
        return recommendations.get(risk_class, [])
