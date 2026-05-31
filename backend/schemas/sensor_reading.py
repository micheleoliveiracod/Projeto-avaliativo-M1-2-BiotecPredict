"""
Schema Pydantic para SensorReading.

Validações de ranges:
- Temperature: 20-45 °C
- pH: 4.0-9.0
- Dissolved Oxygen: 0-100 %
- Pressure: 0-10 bar
- Agitator Speed: 0-500 RPM
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class SensorReadingSchema(BaseModel):
    """Schema para leitura de sensor com validações."""

    id: Optional[int] = None
    batch_id: int
    temperature: float = Field(..., ge=20, le=45, description="Temperatura em °C (20-45)")
    ph: float = Field(..., ge=4.0, le=9.0, description="pH (4.0-9.0)")
    dissolved_oxygen: float = Field(..., ge=0, le=100, description="Oxigênio dissolvido em % (0-100)")
    pressure: float = Field(..., ge=0, le=10, description="Pressão em bar (0-10)")
    agitator_speed: float = Field(..., ge=0, le=500, description="Velocidade do agitador em RPM (0-500)")
    timestamp: Optional[datetime] = None

    class Config:
        from_attributes = True
