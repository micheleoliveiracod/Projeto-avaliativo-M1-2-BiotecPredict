"""
Prediction Routes - Endpoints para consulta de predições.

Endpoints:
- GET /api/v1/prediction/{batch_id} - Obter predição de um batch
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.db.database import get_db
from backend.services import DataService
from backend.schemas import PredictionSchema

router = APIRouter(prefix="/api/v1", tags=["predictions"])


@router.get("/prediction/{batch_id}", response_model=PredictionSchema)
def get_prediction(batch_id: int, db: Session = Depends(get_db)):
    """
    Obter predição de risco de um batch.

    Path Parameters:
    - batch_id: ID do batch

    Returns:
        PredictionSchema com predição de risco

    Raises:
        404: Se predição não encontrada
    """
    try:
        prediction = DataService.get_prediction(db, batch_id)
        if not prediction:
            raise HTTPException(status_code=404, detail=f"Predição para batch {batch_id} não encontrada")

        return PredictionSchema(
            id=prediction.id,
            batch_id=prediction.batch_id,
            model_version=prediction.model_version,
            prediction_timestamp=prediction.prediction_timestamp,
            confidence_score=prediction.confidence_score,
            risk_level=prediction.risk_level,
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter predição: {str(e)}")
