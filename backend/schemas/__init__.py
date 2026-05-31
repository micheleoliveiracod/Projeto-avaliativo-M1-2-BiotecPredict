"""
Schemas Pydantic para validação de entrada/saída da API.

Este módulo contém os schemas para:
- Batch: Criação e resposta de batches
- SensorReading: Leituras de sensores
- Prediction: Predições de risco
"""

from .batch import BatchCreate, BatchResponse, BatchUpdate
from .sensor_reading import SensorReadingSchema
from .prediction import PredictionSchema

__all__ = [
    "BatchCreate",
    "BatchResponse",
    "BatchUpdate",
    "SensorReadingSchema",
    "PredictionSchema",
]
