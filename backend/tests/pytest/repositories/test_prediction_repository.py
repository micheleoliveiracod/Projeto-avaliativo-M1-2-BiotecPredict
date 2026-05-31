"""
Tests for PredictionRepository.

This module tests the PredictionRepository class with optimized query methods
for filtering, aggregation, and analysis on ML predictions.

Test Coverage:
- CRUD operations (inherited from BaseRepository)
- Filtering by batch, risk level, confidence score range
- Aggregation queries (average confidence, risk distribution)
- Latest prediction retrieval
- Pagination with total count
- Statistics and analysis methods

Validates: Requirements 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8
"""

from datetime import datetime, timedelta
from uuid import uuid4

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from backend.db.repository import PredictionRepository
from backend.models.batch import Batch
from backend.models.prediction import Prediction


@pytest.fixture
async def batch(db_session: AsyncSession) -> Batch:
    """Create a test batch."""
    batch = Batch(status="PROCESSING")
    db_session.add(batch)
    await db_session.flush()
    return batch


@pytest.fixture
async def predictions(db_session: AsyncSession, batch: Batch) -> list[Prediction]:
    """Create test predictions with various risk levels and confidence scores."""
    predictions = [
        Prediction(
            batch_id=batch.id,
            model_version="v1.0.0",
            confidence_score=0.95,
            risk_level="LOW",
            prediction_timestamp=datetime.utcnow() - timedelta(hours=2),
        ),
        Prediction(
            batch_id=batch.id,
            model_version="v1.0.0",
            confidence_score=0.85,
            risk_level="MEDIUM",
            prediction_timestamp=datetime.utcnow() - timedelta(hours=1),
        ),
        Prediction(
            batch_id=batch.id,
            model_version="v1.0.0",
            confidence_score=0.92,
            risk_level="HIGH",
            prediction_timestamp=datetime.utcnow(),
        ),
    ]
    for prediction in predictions:
        db_session.add(prediction)
    await db_session.flush()
    return predictions


@pytest.mark.asyncio
async def test_get_by_batch(db_session: AsyncSession, batch: Batch, predictions: list[Prediction]):
    """Test retrieving all predictions for a batch."""
    repo = PredictionRepository(db_session)
    
    result_predictions, total = await repo.get_by_batch(batch.id)
    
    assert len(result_predictions) == 3
    assert total == 3
    # Should be ordered by timestamp (newest first)
    assert result_predictions[0].risk_level == "HIGH"
    assert result_predictions[1].risk_level == "MEDIUM"
    assert result_predictions[2].risk_level == "LOW"


@pytest.mark.asyncio
async def test_get_by_batch_pagination(db_session: AsyncSession, batch: Batch, predictions: list[Prediction]):
    """Test pagination when retrieving predictions for a batch."""
    repo = PredictionRepository(db_session)
    
    # Get first page
    page1, total = await repo.get_by_batch(batch.id, skip=0, limit=2)
    assert len(page1) == 2
    assert total == 3
    
    # Get second page
    page2, total = await repo.get_by_batch(batch.id, skip=2, limit=2)
    assert len(page2) == 1
    assert total == 3


@pytest.mark.asyncio
async def test_get_latest_by_batch(db_session: AsyncSession, batch: Batch, predictions: list[Prediction]):
    """Test retrieving the latest prediction for a batch."""
    repo = PredictionRepository(db_session)
    
    latest = await repo.get_latest_by_batch(batch.id)
    
    assert latest is not None
    assert latest.risk_level == "HIGH"
    assert latest.confidence_score == 0.92


@pytest.mark.asyncio
async def test_get_latest_by_batch_empty(db_session: AsyncSession):
    """Test retrieving latest prediction when batch has no predictions."""
    repo = PredictionRepository(db_session)
    batch_id = uuid4()
    
    latest = await repo.get_latest_by_batch(batch_id)
    
    assert latest is None


@pytest.mark.asyncio
async def test_get_by_risk_level(db_session: AsyncSession, batch: Batch, predictions: list[Prediction]):
    """Test filtering predictions by risk level."""
    repo = PredictionRepository(db_session)
    
    # Get HIGH risk predictions
    high_risk, total = await repo.get_by_risk_level("HIGH")
    assert len(high_risk) == 1
    assert total == 1
    assert high_risk[0].risk_level == "HIGH"
    
    # Get MEDIUM risk predictions
    medium_risk, total = await repo.get_by_risk_level("MEDIUM")
    assert len(medium_risk) == 1
    assert total == 1
    assert medium_risk[0].risk_level == "MEDIUM"
    
    # Get LOW risk predictions
    low_risk, total = await repo.get_by_risk_level("LOW")
    assert len(low_risk) == 1
    assert total == 1
    assert low_risk[0].risk_level == "LOW"


@pytest.mark.asyncio
async def test_get_by_risk_level_invalid(db_session: AsyncSession):
    """Test that invalid risk level raises ValueError."""
    repo = PredictionRepository(db_session)
    
    with pytest.raises(ValueError, match="Invalid risk level"):
        await repo.get_by_risk_level("INVALID")


@pytest.mark.asyncio
async def test_get_by_confidence_range(db_session: AsyncSession, batch: Batch, predictions: list[Prediction]):
    """Test filtering predictions by confidence score range."""
    repo = PredictionRepository(db_session)
    
    # Get high confidence predictions (0.9-1.0)
    high_conf, total = await repo.get_by_confidence_range(0.9, 1.0)
    assert len(high_conf) == 2
    assert total == 2
    
    # Get medium confidence predictions (0.8-0.9)
    medium_conf, total = await repo.get_by_confidence_range(0.8, 0.9)
    assert len(medium_conf) == 1
    assert total == 1
    assert medium_conf[0].confidence_score == 0.85


@pytest.mark.asyncio
async def test_get_by_confidence_range_invalid(db_session: AsyncSession):
    """Test that invalid confidence range raises ValueError."""
    repo = PredictionRepository(db_session)
    
    # Test min > 1
    with pytest.raises(ValueError, match="must be between 0 and 1"):
        await repo.get_by_confidence_range(1.5, 2.0)
    
    # Test max < 0
    with pytest.raises(ValueError, match="must be between 0 and 1"):
        await repo.get_by_confidence_range(-1.0, 0.5)
    
    # Test min > max
    with pytest.raises(ValueError, match="min_confidence must be <= max_confidence"):
        await repo.get_by_confidence_range(0.9, 0.5)


@pytest.mark.asyncio
async def test_get_by_model_version(db_session: AsyncSession, batch: Batch, predictions: list[Prediction]):
    """Test filtering predictions by model version."""
    repo = PredictionRepository(db_session)
    
    v1_predictions, total = await repo.get_by_model_version("v1.0.0")
    
    assert len(v1_predictions) == 3
    assert total == 3
    for pred in v1_predictions:
        assert pred.model_version == "v1.0.0"


@pytest.mark.asyncio
async def test_get_by_batch_and_risk_level(db_session: AsyncSession, batch: Batch, predictions: list[Prediction]):
    """Test filtering predictions by batch and risk level."""
    repo = PredictionRepository(db_session)
    
    high_risk, total = await repo.get_by_batch_and_risk_level(batch.id, "HIGH")
    
    assert len(high_risk) == 1
    assert total == 1
    assert high_risk[0].risk_level == "HIGH"
    assert high_risk[0].batch_id == batch.id


@pytest.mark.asyncio
async def test_count_by_risk_level(db_session: AsyncSession, batch: Batch, predictions: list[Prediction]):
    """Test counting predictions by risk level."""
    repo = PredictionRepository(db_session)
    
    high_count = await repo.count_by_risk_level("HIGH")
    medium_count = await repo.count_by_risk_level("MEDIUM")
    low_count = await repo.count_by_risk_level("LOW")
    
    assert high_count == 1
    assert medium_count == 1
    assert low_count == 1


@pytest.mark.asyncio
async def test_count_by_batch(db_session: AsyncSession, batch: Batch, predictions: list[Prediction]):
    """Test counting predictions for a batch."""
    repo = PredictionRepository(db_session)
    
    count = await repo.count_by_batch(batch.id)
    
    assert count == 3


@pytest.mark.asyncio
async def test_get_average_confidence(db_session: AsyncSession, batch: Batch, predictions: list[Prediction]):
    """Test calculating average confidence across all predictions."""
    repo = PredictionRepository(db_session)
    
    avg_conf = await repo.get_average_confidence()
    
    assert avg_conf is not None
    # (0.95 + 0.85 + 0.92) / 3 = 0.9066...
    assert abs(avg_conf - 0.9066666666666666) < 0.0001


@pytest.mark.asyncio
async def test_get_average_confidence_empty(db_session: AsyncSession):
    """Test average confidence when no predictions exist."""
    repo = PredictionRepository(db_session)
    
    avg_conf = await repo.get_average_confidence()
    
    assert avg_conf is None


@pytest.mark.asyncio
async def test_get_average_confidence_by_batch(db_session: AsyncSession, batch: Batch, predictions: list[Prediction]):
    """Test calculating average confidence for a batch."""
    repo = PredictionRepository(db_session)
    
    avg_conf = await repo.get_average_confidence_by_batch(batch.id)
    
    assert avg_conf is not None
    # (0.95 + 0.85 + 0.92) / 3 = 0.9066...
    assert abs(avg_conf - 0.9066666666666666) < 0.0001


@pytest.mark.asyncio
async def test_get_risk_distribution(db_session: AsyncSession, batch: Batch, predictions: list[Prediction]):
    """Test getting risk distribution across all predictions."""
    repo = PredictionRepository(db_session)
    
    dist = await repo.get_risk_distribution()
    
    assert dist["LOW"] == 1
    assert dist["MEDIUM"] == 1
    assert dist["HIGH"] == 1
    assert dist["total"] == 3


@pytest.mark.asyncio
async def test_get_risk_distribution_by_batch(db_session: AsyncSession, batch: Batch, predictions: list[Prediction]):
    """Test getting risk distribution for a batch."""
    repo = PredictionRepository(db_session)
    
    dist = await repo.get_risk_distribution_by_batch(batch.id)
    
    assert dist["LOW"] == 1
    assert dist["MEDIUM"] == 1
    assert dist["HIGH"] == 1
    assert dist["total"] == 3


@pytest.mark.asyncio
async def test_get_statistics(db_session: AsyncSession, batch: Batch, predictions: list[Prediction]):
    """Test getting comprehensive statistics for all predictions."""
    repo = PredictionRepository(db_session)
    
    stats = await repo.get_statistics()
    
    assert stats["total_count"] == 3
    assert stats["risk_distribution"]["LOW"] == 1
    assert stats["risk_distribution"]["MEDIUM"] == 1
    assert stats["risk_distribution"]["HIGH"] == 1
    assert stats["average_confidence"] is not None


@pytest.mark.asyncio
async def test_get_statistics_by_batch(db_session: AsyncSession, batch: Batch, predictions: list[Prediction]):
    """Test getting comprehensive statistics for a batch."""
    repo = PredictionRepository(db_session)
    
    stats = await repo.get_statistics_by_batch(batch.id)
    
    assert stats["total_count"] == 3
    assert stats["risk_distribution"]["LOW"] == 1
    assert stats["risk_distribution"]["MEDIUM"] == 1
    assert stats["risk_distribution"]["HIGH"] == 1
    assert stats["average_confidence"] is not None


@pytest.mark.asyncio
async def test_delete_by_batch(db_session: AsyncSession, batch: Batch, predictions: list[Prediction]):
    """Test deleting all predictions for a batch."""
    repo = PredictionRepository(db_session)
    
    # Verify predictions exist
    count_before = await repo.count_by_batch(batch.id)
    assert count_before == 3
    
    # Delete predictions
    deleted = await repo.delete_by_batch(batch.id)
    assert deleted == 3
    
    # Verify predictions are deleted
    count_after = await repo.count_by_batch(batch.id)
    assert count_after == 0


@pytest.mark.asyncio
async def test_delete_old_predictions(db_session: AsyncSession, batch: Batch):
    """Test deleting predictions older than N days."""
    repo = PredictionRepository(db_session)
    
    # Create old prediction
    old_pred = Prediction(
        batch_id=batch.id,
        model_version="v1.0.0",
        confidence_score=0.9,
        risk_level="LOW",
        prediction_timestamp=datetime.utcnow() - timedelta(days=400),
    )
    db_session.add(old_pred)
    
    # Create recent prediction
    recent_pred = Prediction(
        batch_id=batch.id,
        model_version="v1.0.0",
        confidence_score=0.9,
        risk_level="LOW",
        prediction_timestamp=datetime.utcnow() - timedelta(days=10),
    )
    db_session.add(recent_pred)
    await db_session.flush()
    
    # Delete predictions older than 365 days
    deleted = await repo.delete_old_predictions(days=365)
    assert deleted == 1
    
    # Verify recent prediction still exists
    count = await repo.count_by_batch(batch.id)
    assert count == 1


@pytest.mark.asyncio
async def test_create_prediction(db_session: AsyncSession, batch: Batch):
    """Test creating a new prediction."""
    repo = PredictionRepository(db_session)
    
    prediction = Prediction(
        batch_id=batch.id,
        model_version="v1.0.0",
        confidence_score=0.88,
        risk_level="MEDIUM",
    )
    
    created = await repo.create(prediction)
    
    assert created.id is not None
    assert created.batch_id == batch.id
    assert created.confidence_score == 0.88
    assert created.risk_level == "MEDIUM"


@pytest.mark.asyncio
async def test_get_by_id(db_session: AsyncSession, batch: Batch, predictions: list[Prediction]):
    """Test retrieving a prediction by ID."""
    repo = PredictionRepository(db_session)
    
    prediction = await repo.get_by_id(predictions[0].id)
    
    assert prediction is not None
    assert prediction.id == predictions[0].id
    assert prediction.risk_level == "LOW"


@pytest.mark.asyncio
async def test_update_prediction(db_session: AsyncSession, batch: Batch, predictions: list[Prediction]):
    """Test updating a prediction."""
    repo = PredictionRepository(db_session)
    
    prediction = predictions[0]
    prediction.risk_level = "HIGH"
    
    updated = await repo.update(prediction)
    
    assert updated.risk_level == "HIGH"


@pytest.mark.asyncio
async def test_delete_prediction(db_session: AsyncSession, batch: Batch, predictions: list[Prediction]):
    """Test deleting a prediction."""
    repo = PredictionRepository(db_session)
    
    deleted = await repo.delete(predictions[0].id)
    
    assert deleted is True
    
    # Verify prediction is deleted
    prediction = await repo.get_by_id(predictions[0].id)
    assert prediction is None


@pytest.mark.asyncio
async def test_get_all_predictions(db_session: AsyncSession, batch: Batch, predictions: list[Prediction]):
    """Test retrieving all predictions with pagination."""
    repo = PredictionRepository(db_session)
    
    all_predictions = await repo.get_all(skip=0, limit=100)
    
    assert len(all_predictions) >= 3


@pytest.mark.asyncio
async def test_count_predictions(db_session: AsyncSession, batch: Batch, predictions: list[Prediction]):
    """Test counting total predictions."""
    repo = PredictionRepository(db_session)
    
    count = await repo.count()
    
    assert count >= 3
