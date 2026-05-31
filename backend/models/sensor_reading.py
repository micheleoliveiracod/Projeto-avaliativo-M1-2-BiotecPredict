"""
Modelo SensorReading - Representa leituras de sensores do biorreator.

Campos:
- id: Identificador único
- batch_id: Referência ao batch
- temperature: Temperatura em °C (20-45)
- ph: Potencial hidrogeniônico (4.0-9.0)
- dissolved_oxygen: Oxigênio dissolvido em % (0-100)
- pressure: Pressão em bar (0-10)
- agitator_speed: Velocidade do agitador em RPM (0-500)
"""

from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.db.database import Base


class SensorReading(Base):
    """Modelo SQLAlchemy para leituras de sensores."""

    __tablename__ = "sensor_readings"

    id = Column(Integer, primary_key=True, index=True)
    batch_id = Column(Integer, ForeignKey("batches.id"), nullable=False)
    temperature = Column(Float, nullable=False)  # °C
    ph = Column(Float, nullable=False)  # pH
    dissolved_oxygen = Column(Float, nullable=False)  # %
    pressure = Column(Float, nullable=False)  # bar
    agitator_speed = Column(Float, nullable=False)  # RPM
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relacionamento
    batch = relationship("Batch", back_populates="sensor_readings")

    def __repr__(self):
        return f"<SensorReading(batch_id={self.batch_id}, temp={self.temperature}°C, pH={self.ph})>"
