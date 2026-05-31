"""
Testes de integração para endpoints de consulta.

Testa:
- GET /api/v1/prediction/{batch_id}
- GET /api/v1/compliance/{batch_id}
"""

import pytest
from backend.models import Prediction


def test_get_prediction(client, db_session, test_batch):
    """Testar obtenção de predição."""
    # Criar predição de teste
    prediction = Prediction(
        batch_id=test_batch.id,
        model_version="v1.0.0",
        confidence_score=0.95,
        risk_level="LOW_RISK",
    )
    db_session.add(prediction)
    db_session.commit()

    response = client.get(f"/api/v1/prediction/{test_batch.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["batch_id"] == test_batch.id
    assert data["confidence_score"] == 0.95


def test_get_prediction_not_found(client):
    """Testar obtenção de predição inexistente."""
    response = client.get("/api/v1/prediction/9999")
    assert response.status_code == 404


def test_get_compliance(client, test_batch):
    """Testar obtenção de compliance score."""
    response = client.get(f"/api/v1/compliance/{test_batch.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["batch_id"] == test_batch.id
    assert data["compliance_score"] == 85.0
    assert data["classification"] == "ACCEPTABLE"


def test_get_compliance_classification_warning(client, db_session):
    """Testar classificação WARNING."""
    from backend.models import Batch

    batch = Batch(status="COMPLETED", compliance_score=70.0)
    db_session.add(batch)
    db_session.commit()

    response = client.get(f"/api/v1/compliance/{batch.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["classification"] == "WARNING"


def test_get_compliance_classification_critical(client, db_session):
    """Testar classificação CRITICAL."""
    from backend.models import Batch

    batch = Batch(status="COMPLETED", compliance_score=50.0)
    db_session.add(batch)
    db_session.commit()

    response = client.get(f"/api/v1/compliance/{batch.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["classification"] == "CRITICAL"
