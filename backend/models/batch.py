"""
Modelo Batch - Representa um lote de manufatura processado.

Campos:
- id: Identificador único do batch
- upload_date: Data/hora do upload do arquivo CSV
- status: Status do processamento (PENDING, PROCESSING, COMPLETED, FAILED)
- compliance_score: Score de conformidade (0-100)
- risk_prediction: Predição de risco (LOW_RISK, MEDIUM_RISK, HIGH_RISK)
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.orm import relationship
from backend.db.database import Base


class Batch(Base):
    """Modelo SQLAlchemy para Batch de manufatura."""

    __tablename__ = "batches"

    id = Column(Integer, primary_key=True, index=True)
    upload_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    status = Column(String(50), default="PENDING", nullable=False)
    compliance_score = Column(Float, nullable=True)
    risk_prediction = Column(String(50), nullable=True)

    # Relacionamentos
    sensor_readings = relationship("SensorReading", back_populates="batch", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Batch(id={self.id}, status={self.status}, compliance_score={self.compliance_score})>"
