"""
Testes de integração para endpoint de batch.

Testa:
- POST /api/v1/upload
- GET /api/v1/batches
- GET /api/v1/batch/{id}
"""

import pytest
from io import BytesIO


def test_upload_csv_valid(client):
    """Testar upload de CSV válido."""
    csv_content = b"""temperature,ph,dissolved_oxygen,pressure,agitator_speed
25.0,7.0,50.0,5.0,250.0
26.0,7.1,51.0,5.1,251.0"""

    response = client.post(
        "/api/v1/upload",
        files={"file": ("test.csv", BytesIO(csv_content), "text/csv")},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["id"] is not None
    assert data["status"] == "COMPLETED"


def test_upload_csv_invalid_format(client):
    """Testar upload de CSV com formato inválido."""
    csv_content = b"""temperature,ph
25.0,7.0"""

    response = client.post(
        "/api/v1/upload",
        files={"file": ("test.csv", BytesIO(csv_content), "text/csv")},
    )

    assert response.status_code == 400


def test_list_batches(client, db_session):
    """Testar listagem de batches."""
    response = client.get("/api/v1/batches")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_get_batch(client, test_batch):
    """Testar obtenção de batch específico."""
    response = client.get(f"/api/v1/batch/{test_batch.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_batch.id
    assert data["status"] == "COMPLETED"


def test_get_batch_not_found(client):
    """Testar obtenção de batch inexistente."""
    response = client.get("/api/v1/batch/9999")
    assert response.status_code == 404
