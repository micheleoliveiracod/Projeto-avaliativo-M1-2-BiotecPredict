"""
Repository Pattern - Abstração para acesso a dados.

Implementa operações CRUD básicas para os modelos.
"""

from sqlalchemy.orm import Session
from backend.models import Batch, SensorReading, Prediction
from typing import List, Optional


class BatchRepository:
    """Repository para operações com Batch."""

    @staticmethod
    def create(db: Session, batch: Batch) -> Batch:
        """Criar novo batch."""
        db.add(batch)
        db.commit()
        db.refresh(batch)
        return batch

    @staticmethod
    def get_by_id(db: Session, batch_id: int) -> Optional[Batch]:
        """Obter batch por ID."""
        return db.query(Batch).filter(Batch.id == batch_id).first()

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[Batch]:
        """Listar todos os batches com paginação."""
        return db.query(Batch).offset(skip).limit(limit).all()

    @staticmethod
    def update(db: Session, batch_id: int, **kwargs) -> Optional[Batch]:
        """Atualizar batch."""
        batch = db.query(Batch).filter(Batch.id == batch_id).first()
        if batch:
            for key, value in kwargs.items():
                setattr(batch, key, value)
            db.commit()
            db.refresh(batch)
        return batch

    @staticmethod
    def delete(db: Session, batch_id: int) -> bool:
        """Deletar batch."""
        batch = db.query(Batch).filter(Batch.id == batch_id).first()
        if batch:
            db.delete(batch)
            db.commit()
            return True
        return False


class SensorReadingRepository:
    """Repository para operações com SensorReading."""

    @staticmethod
    def create(db: Session, sensor_reading: SensorReading) -> SensorReading:
        """Criar nova leitura de sensor."""
        db.add(sensor_reading)
        db.commit()
        db.refresh(sensor_reading)
        return sensor_reading

    @staticmethod
    def get_by_batch(db: Session, batch_id: int) -> List[SensorReading]:
        """Obter todas as leituras de um batch."""
        return db.query(SensorReading).filter(SensorReading.batch_id == batch_id).all()


class PredictionRepository:
    """Repository para operações com Prediction."""

    @staticmethod
    def create(db: Session, prediction: Prediction) -> Prediction:
        """Criar nova predição."""
        db.add(prediction)
        db.commit()
        db.refresh(prediction)
        return prediction

    @staticmethod
    def get_by_batch(db: Session, batch_id: int) -> Optional[Prediction]:
        """Obter predição de um batch."""
        return db.query(Prediction).filter(Prediction.batch_id == batch_id).first()
