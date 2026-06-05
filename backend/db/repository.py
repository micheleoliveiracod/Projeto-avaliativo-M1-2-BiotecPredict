"""Repository Pattern - Data access layer."""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc
from backend.models import Batch, SensorReading


class BatchRepository:
    """Repository for Batch model."""

    @staticmethod
    def create(db: Session, batch: Batch) -> Batch:
        """Create a new batch."""
        db.add(batch)
        db.commit()
        db.refresh(batch)
        return batch

    @staticmethod
    def get_by_id(db: Session, batch_id: int) -> Optional[Batch]:
        """Get batch by ID."""
        return db.query(Batch).filter(Batch.id == batch_id).first()

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[Batch]:
        """Get all batches with pagination."""
        return db.query(Batch).offset(skip).limit(limit).order_by(desc(Batch.upload_date)).all()

    @staticmethod
    def update(db: Session, batch_id: int, **kwargs) -> Optional[Batch]:
        """Update batch by ID."""
        batch = db.query(Batch).filter(Batch.id == batch_id).first()
        if batch:
            for key, value in kwargs.items():
                if hasattr(batch, key):
                    setattr(batch, key, value)
            db.commit()
            db.refresh(batch)
        return batch

    @staticmethod
    def delete(db: Session, batch_id: int) -> bool:
        """Delete batch by ID."""
        batch = db.query(Batch).filter(Batch.id == batch_id).first()
        if batch:
            db.delete(batch)
            db.commit()
            return True
        return False


class SensorReadingRepository:
    """Repository for SensorReading model."""

    @staticmethod
    def create(db: Session, sensor_reading: SensorReading) -> SensorReading:
        """Create a new sensor reading."""
        db.add(sensor_reading)
        db.commit()
        db.refresh(sensor_reading)
        return sensor_reading

    @staticmethod
    def get_by_id(db: Session, reading_id: int) -> Optional[SensorReading]:
        """Get sensor reading by ID."""
        return db.query(SensorReading).filter(SensorReading.id == reading_id).first()

    @staticmethod
    def get_by_batch_id(db: Session, batch_id: int) -> List[SensorReading]:
        """Get all sensor readings for a batch."""
        return (
            db.query(SensorReading)
            .filter(SensorReading.batch_id == batch_id)
            .order_by(SensorReading.recorded_at)
            .all()
        )

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[SensorReading]:
        """Get all sensor readings with pagination."""
        return db.query(SensorReading).offset(skip).limit(limit).all()

    @staticmethod
    def update(db: Session, reading_id: int, **kwargs) -> Optional[SensorReading]:
        """Update sensor reading by ID."""
        reading = db.query(SensorReading).filter(SensorReading.id == reading_id).first()
        if reading:
            for key, value in kwargs.items():
                if hasattr(reading, key):
                    setattr(reading, key, value)
            db.commit()
            db.refresh(reading)
        return reading

    @staticmethod
    def delete(db: Session, reading_id: int) -> bool:
        """Delete sensor reading by ID."""
        reading = db.query(SensorReading).filter(SensorReading.id == reading_id).first()
        if reading:
            db.delete(reading)
            db.commit()
            return True
        return False
