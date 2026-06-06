"""
Schemas Pydantic para Batch.

- BatchCreate: Schema para criação de batch (upload de CSV)
- BatchResponse: Schema para resposta de batch
- BatchUpdate: Schema para atualização de batch
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class BatchCreate(BaseModel):
    """Schema para criação de batch."""

    pass  # Arquivo CSV é enviado como multipart/form-data


class BatchResponse(BaseModel):
    """Schema para resposta de batch."""

    id: int
    upload_date: datetime
    status: str = Field(..., description="PENDING, PROCESSING, COMPLETED, FAILED")
    compliance_score: Optional[float] = Field(None, ge=0, le=100)
    risk_prediction: Optional[str] = Field(None, description="LOW_RISK, MEDIUM_RISK, HIGH_RISK")

    class Config:
        from_attributes = True


class BatchUpdate(BaseModel):
    """Schema para atualização de batch."""

    status: Optional[str] = None
    compliance_score: Optional[float] = Field(None, ge=0, le=100)
    risk_prediction: Optional[str] = None

    class Config:
        from_attributes = True
