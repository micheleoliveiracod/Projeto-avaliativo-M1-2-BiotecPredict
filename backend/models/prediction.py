"""
Modelo Prediction - Representa predições de risco geradas pelo modelo ML.

Campos:
- id: Identificador único
- batch_id: Referência ao batch
- model_version: Versão do modelo utilizado
- prediction_timestamp: Quando a predição foi feita
- confidence_score: Confiança da predição (0-1)
- risk_level: Nível de risco (LOW_RISK, MEDIUM_RISK, HIGH_RISK)
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .batch import Base


class Prediction(Base):
    """Modelo SQLAlchemy para predições de risco."""

    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    batch_id = Column(Integer, ForeignKey("batches.id"), nullable=False)
    model_version = Column(String(50), nullable=False)
    prediction_timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    confidence_score = Column(Float, nullable=False)  # 0-1
    risk_level = Column(String(50), nullable=False)  # LOW_RISK, MEDIUM_RISK, HIGH_RISK

    # Relacionamento
    batch = relationship("Batch", back_populates="predictions")

    def __repr__(self):
        return f"<Prediction(batch_id={self.batch_id}, risk={self.risk_level}, confidence={self.confidence_score})>"
