"""
Data Service - Acesso a dados do banco.

Responsabilidades:
- Consultar dados de sensores
- Consultar predições
- Consultar compliance scores
"""

from sqlalchemy.orm import Session
from backend.models import Batch, SensorReading, Prediction
from backend.db.repository import SensorReadingRepository, PredictionRepository
from typing import List, Optional


class DataService:
    """Serviço para acesso a dados."""

    @staticmethod
    def get_sensor_readings(db: Session, batch_id: int) -> List[SensorReading]:
        """Obter todas as leituras de sensores de um batch."""
        return SensorReadingRepository.get_by_batch(db, batch_id)

    @staticmethod
    def get_prediction(db: Session, batch_id: int) -> Optional[Prediction]:
        """Obter predição de um batch."""
        return PredictionRepository.get_by_batch(db, batch_id)

    @staticmethod
    def get_compliance_score(db: Session, batch_id: int) -> Optional[float]:
        """Obter compliance score de um batch."""
        batch = db.query(Batch).filter(Batch.id == batch_id).first()
        if batch:
            return batch.compliance_score
        return None
