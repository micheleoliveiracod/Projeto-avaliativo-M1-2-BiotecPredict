"""API routes para Compliance Score."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.db.connection import get_db
from backend.services.compliance_service import ComplianceService
from backend.db.repository import BatchRepository, SensorReadingRepository
from typing import Dict, Any

router = APIRouter(prefix="/api/v1", tags=["compliance"])


@router.get("/compliance/{batch_id}")
def get_compliance_score(batch_id: int, db: Session = Depends(get_db)) -> Dict[str, Any]:
    """
    Obtém Manufacturing Compliance Score para um batch.

    Returns:
        - score: Score 0-100
        - classification: ACCEPTABLE, WARNING ou CRITICAL
        - metrics: Métricas detalhadas por sensor
    """
    batch = BatchRepository.get_by_id(db, batch_id)
    if not batch:
        raise HTTPException(status_code=404, detail=f"Batch {batch_id} não encontrado")

    sensor_readings = SensorReadingRepository.get_by_batch_id(db, batch_id)
    if not sensor_readings:
        raise HTTPException(status_code=404, detail=f"Nenhuma leitura de sensor para batch {batch_id}")

    # Converter para dicionários
    readings_data = [
        {
            "temperature": reading.temperature,
            "ph": reading.ph,
            "dissolved_oxygen": reading.dissolved_oxygen,
            "pressure": reading.pressure,
            "agitator_speed": reading.agitator_speed,
        }
        for reading in sensor_readings
    ]

    score, classification = ComplianceService.calculate_compliance_score(readings_data)
    metrics = ComplianceService.get_sensor_metrics(readings_data)

    return {
        "batch_id": batch_id,
        "compliance_score": score,
        "classification": classification,
        "sensor_metrics": metrics,
        "interpretation": ComplianceService._interpret_risk(classification),
    }


@router.get("/batch/{batch_id}/sensors")
def get_batch_sensors(batch_id: int, db: Session = Depends(get_db)) -> Dict[str, Any]:
    """
    Obtém todas as leituras de sensores para um batch.

    Returns:
        - batch_id: ID do batch
        - count: Número de leituras
        - readings: Lista de leituras com dados de sensores
    """
    batch = BatchRepository.get_by_id(db, batch_id)
    if not batch:
        raise HTTPException(status_code=404, detail=f"Batch {batch_id} não encontrado")

    sensor_readings = SensorReadingRepository.get_by_batch_id(db, batch_id)

    readings = [
        {
            "id": reading.id,
            "temperature": reading.temperature,
            "ph": reading.ph,
            "dissolved_oxygen": reading.dissolved_oxygen,
            "pressure": reading.pressure,
            "agitator_speed": reading.agitator_speed,
            "recorded_at": reading.recorded_at.isoformat() if reading.recorded_at else None,
        }
        for reading in sensor_readings
    ]

    return {
        "batch_id": batch_id,
        "count": len(readings),
        "readings": readings,
    }
