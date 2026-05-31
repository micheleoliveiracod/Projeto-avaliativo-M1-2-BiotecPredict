"""
Compliance Routes - Endpoints para consulta de compliance score.

Endpoints:
- GET /api/v1/compliance/{batch_id} - Obter compliance score de um batch
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.db.database import get_db
from backend.services import DataService
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/api/v1", tags=["compliance"])


class ComplianceResponse(BaseModel):
    """Response model para compliance score."""

    batch_id: int
    compliance_score: Optional[float]
    classification: Optional[str]  # ACCEPTABLE, WARNING, CRITICAL

    class Config:
        from_attributes = True


@router.get("/compliance/{batch_id}", response_model=ComplianceResponse)
def get_compliance(batch_id: int, db: Session = Depends(get_db)):
    """
    Obter compliance score de um batch.

    Path Parameters:
    - batch_id: ID do batch

    Returns:
        ComplianceResponse com score e classificação

    Raises:
        404: Se batch não encontrado
    """
    try:
        compliance_score = DataService.get_compliance_score(db, batch_id)
        if compliance_score is None:
            raise HTTPException(status_code=404, detail=f"Batch {batch_id} não encontrado")

        # Classificar score
        if compliance_score >= 80:
            classification = "ACCEPTABLE"
        elif compliance_score >= 60:
            classification = "WARNING"
        else:
            classification = "CRITICAL"

        return ComplianceResponse(
            batch_id=batch_id,
            compliance_score=compliance_score,
            classification=classification,
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter compliance: {str(e)}")
