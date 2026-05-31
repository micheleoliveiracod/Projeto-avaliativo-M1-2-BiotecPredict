"""
Schema Pydantic para Prediction.

Validações:
- confidence_score: 0-1 (confiança da predição)
- risk_level: LOW_RISK, MEDIUM_RISK, HIGH_RISK
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class PredictionSchema(BaseModel):
    """Schema para predição de risco."""

    id: Optional[int] = None
    batch_id: int
    model_version: str = Field(..., description="Versão do modelo utilizado")
    prediction_timestamp: Optional[datetime] = None
    confidence_score: float = Field(..., ge=0, le=1, description="Confiança da predição (0-1)")
    risk_level: str = Field(..., description="LOW_RISK, MEDIUM_RISK, HIGH_RISK")

    class Config:
        from_attributes = True
