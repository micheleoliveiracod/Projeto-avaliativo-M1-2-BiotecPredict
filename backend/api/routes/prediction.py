"""API routes para ML Prediction."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.db.connection import get_db
from backend.services.ml_service import MLService
from backend.db.repository import BatchRepository, SensorReadingRepository
from typing import Dict, Any

router = APIRouter(prefix="/api/v1", tags=["prediction"])


@router.get("/prediction/{batch_id}")
def get_risk_prediction(batch_id: int, db: Session = Depends(get_db)) -> Dict[str, Any]:
    """
    Obtém predição de risco para um batch usando ML.

    Returns:
        - batch_id: ID do batch
        - risk_prediction: LOW_RISK, MEDIUM_RISK ou HIGH_RISK
        - confidence_score: Score 0-1
        - interpretation: Interpretação textual do risco
        - recommendations: Lista de recomendações baseadas no risco
    """
    batch = BatchRepository.get_by_id(db, batch_id)
    if not batch:
        raise HTTPException(status_code=404, detail=f"Batch {batch_id} não encontrado")

    sensor_readings = SensorReadingRepository.get_by_batch_id(db, batch_id)
    if not sensor_readings:
        raise HTTPException(status_code=404, detail=f"Nenhuma leitura de sensor para batch {batch_id}")

    # Converter para dicionários
    readings_data = [
        {
            "temperature": reading.temperature,
            "ph": reading.ph,
            "dissolved_oxygen": reading.dissolved_oxygen,
            "pressure": reading.pressure,
            "agitator_speed": reading.agitator_speed,
        }
        for reading in sensor_readings
    ]

    result = MLService.evaluate_batch_risk(readings_data)

    return {
        "batch_id": batch_id,
        **result,
    }


@router.get("/model/info")
def get_model_info() -> Dict[str, Any]:
    """
    Obtém informações sobre o modelo de predição.

    Returns:
        - model_type: Tipo do modelo (RandomForestClassifier)
        - n_estimators: Número de árvores
        - features: Features utilizadas no modelo
        - risk_classes: Classes de risco previstas
        - feature_importance: Importância de cada feature
    """
    return MLService.get_model_info()


@router.post("/predict")
def predict_risk(sensor_data: Dict[str, float]) -> Dict[str, Any]:
    """
    Faz predição de risco para dados de sensores fornecidos.

    Expected sensor_data:
    {
        "temperature": 25.0,
        "ph": 7.0,
        "dissolved_oxygen": 85.0,
        "pressure": 5.0,
        "agitator_speed": 250
    }

    Returns:
        - risk_prediction: LOW_RISK, MEDIUM_RISK ou HIGH_RISK
        - confidence_score: Score 0-1
        - interpretation: Interpretação textual do risco
        - recommendations: Lista de recomendações
    """
    risk_class, confidence = MLService.predict_risk([sensor_data])

    return {
        "risk_prediction": risk_class,
        "confidence_score": confidence,
        "interpretation": MLService._interpret_risk(risk_class),
        "recommendations": MLService._get_recommendations(risk_class),
    }
