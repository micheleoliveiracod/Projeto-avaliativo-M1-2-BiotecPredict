"""
API Routes - Endpoints da aplicação.

Rotas:
- batch: Gerenciamento de batches
- prediction: Consulta de predições
- compliance: Consulta de compliance score
"""

from .batch import router as batch_router
from .prediction import router as prediction_router
from .compliance import router as compliance_router

__all__ = ["batch_router", "prediction_router", "compliance_router"]
