"""
Batch Routes - Endpoints para gerenciamento de batches.

Endpoints:
- POST /api/v1/upload - Upload de arquivo CSV
- GET /api/v1/batches - Listar todos os batches
- GET /api/v1/batch/{id} - Detalhes do batch
"""

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.db.database import get_db
from backend.services import BatchService
from backend.schemas import BatchResponse
from typing import List

router = APIRouter(prefix="/api/v1", tags=["batches"])


@router.post("/upload", response_model=BatchResponse)
async def upload_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Upload de arquivo CSV com dados de sensores.

    Processa o arquivo através do pipeline:
    1. Parse CSV
    2. Validação de ranges
    3. Limpeza de dados
    4. Persistência no banco

    Returns:
        BatchResponse com ID do batch criado
    """
    try:
        # Ler conteúdo do arquivo
        content = await file.read()
        file_content = content.decode("utf-8")

        # Processar através do service
        batch, warnings = BatchService.process_csv_upload(db, file_content)

        return BatchResponse(
            id=batch.id,
            upload_date=batch.upload_date,
            status=batch.status,
            compliance_score=batch.compliance_score,
            risk_prediction=batch.risk_prediction,
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar arquivo: {str(e)}")


@router.get("/batches", response_model=List[BatchResponse])
def list_batches(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Listar todos os batches com paginação.

    Query Parameters:
    - skip: Número de registros a pular (padrão: 0)
    - limit: Número máximo de registros (padrão: 100)

    Returns:
        Lista de BatchResponse
    """
    batches = BatchService.list_batches(db, skip, limit)
    return [
        BatchResponse(
            id=b.id,
            upload_date=b.upload_date,
            status=b.status,
            compliance_score=b.compliance_score,
            risk_prediction=b.risk_prediction,
        )
        for b in batches
    ]


@router.get("/batch/{batch_id}", response_model=BatchResponse)
def get_batch(batch_id: int, db: Session = Depends(get_db)):
    """
    Obter detalhes de um batch específico.

    Path Parameters:
    - batch_id: ID do batch

    Returns:
        BatchResponse com detalhes do batch

    Raises:
        404: Se batch não encontrado
    """
    try:
        batch = BatchService.get_batch(db, batch_id)
        return BatchResponse(
            id=batch.id,
            upload_date=batch.upload_date,
            status=batch.status,
            compliance_score=batch.compliance_score,
            risk_prediction=batch.risk_prediction,
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
