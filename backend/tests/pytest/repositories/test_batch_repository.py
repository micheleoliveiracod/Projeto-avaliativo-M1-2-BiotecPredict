"""
Testes para BatchRepository (CRUD).

Testa:
- Create
- Read
- Update
- Delete
"""

import pytest
from backend.models import Batch
from backend.db.repository import BatchRepository


def test_create_batch(db_session):
    """Testar criação de batch."""
    batch = Batch(status="PENDING")
    created = BatchRepository.create(db_session, batch)

    assert created.id is not None
    assert created.status == "PENDING"


def test_get_batch_by_id(db_session):
    """Testar obtenção de batch por ID."""
    batch = Batch(status="COMPLETED")
    created = BatchRepository.create(db_session, batch)

    retrieved = BatchRepository.get_by_id(db_session, created.id)
    assert retrieved is not None
    assert retrieved.id == created.id


def test_get_all_batches(db_session):
    """Testar listagem de batches."""
    for i in range(3):
        batch = Batch(status="COMPLETED")
        BatchRepository.create(db_session, batch)

    batches = BatchRepository.get_all(db_session)
    assert len(batches) == 3


def test_update_batch(db_session):
    """Testar atualização de batch."""
    batch = Batch(status="PENDING", compliance_score=0.0)
    created = BatchRepository.create(db_session, batch)

    updated = BatchRepository.update(
        db_session, created.id, status="COMPLETED", compliance_score=85.0
    )
    assert updated.status == "COMPLETED"
    assert updated.compliance_score == 85.0


def test_delete_batch(db_session):
    """Testar deleção de batch."""
    batch = Batch(status="COMPLETED")
    created = BatchRepository.create(db_session, batch)

    deleted = BatchRepository.delete(db_session, created.id)
    assert deleted is True

    retrieved = BatchRepository.get_by_id(db_session, created.id)
    assert retrieved is None
