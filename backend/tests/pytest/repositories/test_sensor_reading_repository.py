"""
Tests for SensorReadingRepository.

This module tests the SensorReadingRepository class with optimized query methods
for filtering, aggregation, and anomaly detection on sensor readings.

Test Coverage:
- CRUD operations (inherited from BaseRepository)
- Filtering by batch, date range, sensor value ranges
- Aggregation queries (average, min, max)
- Anomaly detection (out-of-range readings)
- Pagination with total count
- Statistics and analysis methods
"""

from datetime import datetime, timedelta
from uuid import uuid4

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from backend.db.repository import SensorReadingRepository
from backend.models.batch import Batch
from backend.models.sensor_reading import SensorReading


@pytest.fixture
async def batch(db_session: AsyncSession) -> Batch:
    """Create a test batch."""
    batch = Batch(status="PROCESSING")
    db_session.add(batch)
    await db_session.flush()
    return batch


@pytest.fixture
async def sensor_readings(db_session: AsyncSession, batch: Batch) -> list[SensorReading]:
    """Create test sensor readings."""
    readings = [
        SensorReading(
            batch_id=batch.id,
            temperature=25.0,
            ph=7.0,
            dissolved_oxygen=75.0,
            pressure=5.0,
            agitator_speed=250,
            timestamp=datetime.utcnow() - timedelta(hours=2),
        ),
        SensorReading(
            batch_id=batch.id,
            temperature=25.5,
            ph=7.1,
            dissolved_oxygen=76.0,
            pressure=5.1,
            agitator_speed=255,
            timestamp=datetime.utcnow() - timedelta(hours=1),
        ),
        SensorReading(
            batch_id=batch.id,
            temperature=26.0,
            ph=7.2,
            dissolved_oxygen=77.0,
            pressure=5.2,
            agitator_speed=260,
            timestamp=datetime.utcnow(),
        ),
    ]
    for reading in readings:
        db_session.add(reading)
    await db_session.flush()
    return readings


@pytest.fixture
async def out_of_range_readings(db_session: AsyncSession, batch: Batch) -> list[SensorReading]:
    """Create out-of-range sensor readings."""
    readings = [
        SensorReading(
            batch_id=batch.id,
            temperature=50.0,  # Out of range (> 45°C)
            ph=7.0,
            dissolved_oxygen=75.0,
            pressure=5.0,
            agitator_speed=250,
        ),
        SensorReading(
            batch_id=batch.id,
            temperature=25.0,
            ph=10.0,  # Out of range (> 9.0)
            dissolved_oxygen=75.0,
            pressure=5.0,
            agitator_speed=250,
        ),
        SensorReading(
            batch_id=batch.id,
            temperature=25.0,
            ph=7.0,
            dissolved_oxygen=150.0,  # Out of range (> 100%)
            pressure=5.0,
            agitator_speed=250,
        ),
    ]
    for reading in readings:
        db_session.add(reading)
    await db_session.flush()
    return readings


@pytest.fixture
async def repository(db_session: AsyncSession) -> SensorReadingRepository:
    """Create a SensorReadingRepository instance."""
    return SensorReadingRepository(db_session)


class TestSensorReadingRepositoryBasics:
    """Test basic CRUD operations."""

    @pytest.mark.asyncio
    async def test_create_sensor_reading(
        self,
        repository: SensorReadingRepository,
        batch: Batch,
    ):
        """Test creating a sensor reading."""
        reading = SensorReading(
            batch_id=batch.id,
            temperature=25.0,
            ph=7.0,
            dissolved_oxygen=75.0,
            pressure=5.0,
            agitator_speed=250,
        )
        created = await repository.create(reading)
        
        assert created.id is not None
        assert created.batch_id == batch.id
        assert created.temperature == 25.0

    @pytest.mark.asyncio
    async def test_get_by_id(
        self,
        repository: SensorReadingRepository,
        sensor_readings: list[SensorReading],
    ):
        """Test retrieving a sensor reading by ID."""
        reading_id = sensor_readings[0].id
        retrieved = await repository.get_by_id(reading_id)
        
        assert retrieved is not None
        assert retrieved.id == reading_id
        assert retrieved.temperature == 25.0

    @pytest.mark.asyncio
    async def test_get_all(
        self,
        repository: SensorReadingRepository,
        sensor_readings: list[SensorReading],
    ):
        """Test retrieving all sensor readings."""
        all_readings = await repository.get_all(skip=0, limit=100)
        
        assert len(all_readings) >= 3
        assert all(isinstance(r, SensorReading) for r in all_readings)

    @pytest.mark.asyncio
    async def test_update_sensor_reading(
        self,
        repository: SensorReadingRepository,
        sensor_readings: list[SensorReading],
        db_session: AsyncSession,
    ):
        """Test updating a sensor reading."""
        reading = sensor_readings[0]
        reading.temperature = 30.0
        
        updated = await repository.update(reading)
        
        assert updated.temperature == 30.0

    @pytest.mark.asyncio
    async def test_delete_sensor_reading(
        self,
        repository: SensorReadingRepository,
        sensor_readings: list[SensorReading],
    ):
        """Test deleting a sensor reading."""
        reading_id = sensor_readings[0].id
        deleted = await repository.delete(reading_id)
        
        assert deleted is True
        
        # Verify it's deleted
        retrieved = await repository.get_by_id(reading_id)
        assert retrieved is None

    @pytest.mark.asyncio
    async def test_count(
        self,
        repository: SensorReadingRepository,
        sensor_readings: list[SensorReading],
    ):
        """Test counting sensor readings."""
        count = await repository.count()
        
        assert count >= 3


class TestSensorReadingRepositoryFiltering:
    """Test filtering operations."""

    @pytest.mark.asyncio
    async def test_get_by_batch(
        self,
        repository: SensorReadingRepository,
        batch: Batch,
        sensor_readings: list[SensorReading],
    ):
        """Test retrieving sensor readings by batch."""
        readings, total = await repository.get_by_batch(batch.id)
        
        assert len(readings) == 3
        assert total == 3
        assert all(r.batch_id == batch.id for r in readings)

    @pytest.mark.asyncio
    async def test_get_by_batch_pagination(
        self,
        repository: SensorReadingRepository,
        batch: Batch,
        sensor_readings: list[SensorReading],
    ):
        """Test pagination in get_by_batch."""
        readings1, total1 = await repository.get_by_batch(batch.id, skip=0, limit=2)
        readings2, total2 = await repository.get_by_batch(batch.id, skip=2, limit=2)
        
        assert len(readings1) == 2
        assert len(readings2) == 1
        assert total1 == 3
        assert total2 == 3

    @pytest.mark.asyncio
    async def test_get_by_batch_and_date_range(
        self,
        repository: SensorReadingRepository,
        batch: Batch,
        sensor_readings: list[SensorReading],
    ):
        """Test retrieving sensor readings by batch and date range."""
        from_date = datetime.utcnow() - timedelta(hours=3)
        to_date = datetime.utcnow() - timedelta(hours=1)
        
        readings, total = await repository.get_by_batch_and_date_range(
            batch.id, from_date, to_date
        )
        
        assert len(readings) >= 1
        assert all(from_date <= r.timestamp <= to_date for r in readings)

    @pytest.mark.asyncio
    async def test_get_by_temperature_range(
        self,
        repository: SensorReadingRepository,
        batch: Batch,
        sensor_readings: list[SensorReading],
    ):
        """Test retrieving sensor readings by temperature range."""
        readings, total = await repository.get_by_temperature_range(
            batch.id, 24.0, 26.0
        )
        
        assert len(readings) >= 2
        assert all(24.0 <= r.temperature <= 26.0 for r in readings)

    @pytest.mark.asyncio
    async def test_get_by_ph_range(
        self,
        repository: SensorReadingRepository,
        batch: Batch,
        sensor_readings: list[SensorReading],
    ):
        """Test retrieving sensor readings by pH range."""
        readings, total = await repository.get_by_ph_range(batch.id, 6.9, 7.3)
        
        assert len(readings) >= 2
        assert all(6.9 <= r.ph <= 7.3 for r in readings)

    @pytest.mark.asyncio
    async def test_get_out_of_range_readings(
        self,
        repository: SensorReadingRepository,
        batch: Batch,
        out_of_range_readings: list[SensorReading],
    ):
        """Test retrieving out-of-range sensor readings."""
        readings, total = await repository.get_out_of_range_readings(batch.id)
        
        assert len(readings) == 3
        assert total == 3


class TestSensorReadingRepositoryAggregation:
    """Test aggregation operations."""

    @pytest.mark.asyncio
    async def test_get_average_values(
        self,
        repository: SensorReadingRepository,
        batch: Batch,
        sensor_readings: list[SensorReading],
    ):
        """Test calculating average sensor values."""
        averages = await repository.get_average_values(batch.id)
        
        assert averages["avg_temperature"] is not None
        assert averages["avg_ph"] is not None
        assert averages["avg_dissolved_oxygen"] is not None
        assert averages["avg_pressure"] is not None
        assert averages["avg_agitator_speed"] is not None
        
        # Verify averages are correct
        assert 25.0 <= averages["avg_temperature"] <= 26.0
        assert 7.0 <= averages["avg_ph"] <= 7.2

    @pytest.mark.asyncio
    async def test_get_min_max_values(
        self,
        repository: SensorReadingRepository,
        batch: Batch,
        sensor_readings: list[SensorReading],
    ):
        """Test calculating min/max sensor values."""
        min_max = await repository.get_min_max_values(batch.id)
        
        assert min_max["min_temperature"] == 25.0
        assert min_max["max_temperature"] == 26.0
        assert min_max["min_ph"] == 7.0
        assert min_max["max_ph"] == 7.2

    @pytest.mark.asyncio
    async def test_get_statistics(
        self,
        repository: SensorReadingRepository,
        batch: Batch,
        sensor_readings: list[SensorReading],
    ):
        """Test getting comprehensive statistics."""
        stats = await repository.get_statistics(batch.id)
        
        assert stats["total_count"] == 3
        assert "averages" in stats
        assert "min_max" in stats
        assert stats["averages"]["avg_temperature"] is not None
        assert stats["min_max"]["min_temperature"] == 25.0


class TestSensorReadingRepositoryCounting:
    """Test counting operations."""

    @pytest.mark.asyncio
    async def test_count_by_batch(
        self,
        repository: SensorReadingRepository,
        batch: Batch,
        sensor_readings: list[SensorReading],
    ):
        """Test counting sensor readings by batch."""
        count = await repository.count_by_batch(batch.id)
        
        assert count == 3

    @pytest.mark.asyncio
    async def test_count_out_of_range(
        self,
        repository: SensorReadingRepository,
        batch: Batch,
        out_of_range_readings: list[SensorReading],
    ):
        """Test counting out-of-range sensor readings."""
        count = await repository.count_out_of_range(batch.id)
        
        assert count == 3


class TestSensorReadingRepositorySpecialQueries:
    """Test special query methods."""

    @pytest.mark.asyncio
    async def test_get_latest_reading(
        self,
        repository: SensorReadingRepository,
        batch: Batch,
        sensor_readings: list[SensorReading],
    ):
        """Test getting the latest sensor reading."""
        latest = await repository.get_latest_reading(batch.id)
        
        assert latest is not None
        assert latest.temperature == 26.0

    @pytest.mark.asyncio
    async def test_get_first_reading(
        self,
        repository: SensorReadingRepository,
        batch: Batch,
        sensor_readings: list[SensorReading],
    ):
        """Test getting the first sensor reading."""
        first = await repository.get_first_reading(batch.id)
        
        assert first is not None
        assert first.temperature == 25.0

    @pytest.mark.asyncio
    async def test_delete_by_batch(
        self,
        repository: SensorReadingRepository,
        batch: Batch,
        sensor_readings: list[SensorReading],
    ):
        """Test deleting all sensor readings for a batch."""
        deleted = await repository.delete_by_batch(batch.id)
        
        assert deleted == 3
        
        # Verify they're deleted
        count = await repository.count_by_batch(batch.id)
        assert count == 0


class TestSensorReadingRepositoryEdgeCases:
    """Test edge cases and error handling."""

    @pytest.mark.asyncio
    async def test_get_by_batch_empty(
        self,
        repository: SensorReadingRepository,
    ):
        """Test retrieving readings for non-existent batch."""
        empty_batch_id = uuid4()
        readings, total = await repository.get_by_batch(empty_batch_id)
        
        assert len(readings) == 0
        assert total == 0

    @pytest.mark.asyncio
    async def test_get_average_values_empty(
        self,
        repository: SensorReadingRepository,
    ):
        """Test calculating averages for empty batch."""
        empty_batch_id = uuid4()
        averages = await repository.get_average_values(empty_batch_id)
        
        assert averages["avg_temperature"] is None
        assert averages["avg_ph"] is None

    @pytest.mark.asyncio
    async def test_get_min_max_values_empty(
        self,
        repository: SensorReadingRepository,
    ):
        """Test calculating min/max for empty batch."""
        empty_batch_id = uuid4()
        min_max = await repository.get_min_max_values(empty_batch_id)
        
        assert min_max["min_temperature"] is None
        assert min_max["max_temperature"] is None

    @pytest.mark.asyncio
    async def test_get_latest_reading_empty(
        self,
        repository: SensorReadingRepository,
    ):
        """Test getting latest reading for empty batch."""
        empty_batch_id = uuid4()
        latest = await repository.get_latest_reading(empty_batch_id)
        
        assert latest is None

    @pytest.mark.asyncio
    async def test_get_first_reading_empty(
        self,
        repository: SensorReadingRepository,
    ):
        """Test getting first reading for empty batch."""
        empty_batch_id = uuid4()
        first = await repository.get_first_reading(empty_batch_id)
        
        assert first is None


class TestSensorReadingRepositoryPerformance:
    """Test performance-related aspects."""

    @pytest.mark.asyncio
    async def test_get_by_batch_large_dataset(
        self,
        repository: SensorReadingRepository,
        batch: Batch,
        db_session: AsyncSession,
    ):
        """Test retrieving readings from large dataset."""
        # Create many readings
        for i in range(100):
            reading = SensorReading(
                batch_id=batch.id,
                temperature=20.0 + (i % 25),
                ph=4.0 + (i % 5),
                dissolved_oxygen=i % 100,
                pressure=i % 10,
                agitator_speed=i % 500,
            )
            db_session.add(reading)
        await db_session.flush()
        
        # Test pagination
        readings1, total1 = await repository.get_by_batch(batch.id, skip=0, limit=50)
        readings2, total2 = await repository.get_by_batch(batch.id, skip=50, limit=50)
        
        assert len(readings1) == 50
        assert len(readings2) == 50
        assert total1 == 100  # 100 created in this test

    @pytest.mark.asyncio
    async def test_get_statistics_performance(
        self,
        repository: SensorReadingRepository,
        batch: Batch,
        db_session: AsyncSession,
    ):
        """Test statistics calculation performance."""
        # Create many readings
        for i in range(100):
            reading = SensorReading(
                batch_id=batch.id,
                temperature=20.0 + (i % 25),
                ph=4.0 + (i % 5),
                dissolved_oxygen=i % 100,
                pressure=i % 10,
                agitator_speed=i % 500,
            )
            db_session.add(reading)
        await db_session.flush()
        
        # Get statistics
        stats = await repository.get_statistics(batch.id)
        
        assert stats["total_count"] == 100
        assert stats["averages"]["avg_temperature"] is not None


class TestSensorReadingRepositoryValidation:
    """Test validation and data integrity."""

    @pytest.mark.asyncio
    async def test_sensor_reading_valid_ranges(
        self,
        repository: SensorReadingRepository,
        batch: Batch,
    ):
        """Test that valid sensor readings are accepted."""
        reading = SensorReading(
            batch_id=batch.id,
            temperature=25.0,  # Valid: 20-45°C
            ph=7.0,  # Valid: 4.0-9.0
            dissolved_oxygen=75.0,  # Valid: 0-100%
            pressure=5.0,  # Valid: 0-10 bar
            agitator_speed=250,  # Valid: 0-500 RPM
        )
        created = await repository.create(reading)
        
        assert created.is_valid() is True

    @pytest.mark.asyncio
    async def test_sensor_reading_out_of_range(
        self,
        repository: SensorReadingRepository,
        batch: Batch,
    ):
        """Test that out-of-range sensor readings are detected."""
        reading = SensorReading(
            batch_id=batch.id,
            temperature=50.0,  # Invalid: > 45°C
            ph=7.0,
            dissolved_oxygen=75.0,
            pressure=5.0,
            agitator_speed=250,
        )
        created = await repository.create(reading)
        
        assert created.is_valid() is False
        out_of_range = created.get_out_of_range_sensors()
        assert "temperature" in out_of_range


class TestSensorReadingRepositoryAcceptanceCriteria:
    """Test acceptance criteria for SensorReadingRepository."""

    @pytest.mark.asyncio
    async def test_ac1_crud_operations(
        self,
        repository: SensorReadingRepository,
        batch: Batch,
    ):
        """AC1: CRUD operations work correctly."""
        # Create
        reading = SensorReading(
            batch_id=batch.id,
            temperature=25.0,
            ph=7.0,
            dissolved_oxygen=75.0,
            pressure=5.0,
            agitator_speed=250,
        )
        created = await repository.create(reading)
        assert created.id is not None
        
        # Read
        retrieved = await repository.get_by_id(created.id)
        assert retrieved is not None
        assert retrieved.temperature == 25.0
        
        # Update
        retrieved.temperature = 26.0
        updated = await repository.update(retrieved)
        assert updated.temperature == 26.0
        
        # Delete
        deleted = await repository.delete(created.id)
        assert deleted is True

    @pytest.mark.asyncio
    async def test_ac2_filtering_by_batch(
        self,
        repository: SensorReadingRepository,
        batch: Batch,
        sensor_readings: list[SensorReading],
    ):
        """AC2: Filtering by batch works correctly."""
        readings, total = await repository.get_by_batch(batch.id)
        
        assert len(readings) == 3
        assert total == 3
        assert all(r.batch_id == batch.id for r in readings)

    @pytest.mark.asyncio
    async def test_ac3_filtering_by_date_range(
        self,
        repository: SensorReadingRepository,
        batch: Batch,
        sensor_readings: list[SensorReading],
    ):
        """AC3: Filtering by date range works correctly."""
        from_date = datetime.utcnow() - timedelta(hours=3)
        to_date = datetime.utcnow()
        
        readings, total = await repository.get_by_batch_and_date_range(
            batch.id, from_date, to_date
        )
        
        assert len(readings) >= 1
        assert all(from_date <= r.timestamp <= to_date for r in readings)

    @pytest.mark.asyncio
    async def test_ac4_filtering_by_sensor_ranges(
        self,
        repository: SensorReadingRepository,
        batch: Batch,
        sensor_readings: list[SensorReading],
    ):
        """AC4: Filtering by sensor value ranges works correctly."""
        # Temperature range
        temp_readings, _ = await repository.get_by_temperature_range(
            batch.id, 24.0, 26.0
        )
        assert len(temp_readings) >= 2
        
        # pH range
        ph_readings, _ = await repository.get_by_ph_range(batch.id, 6.9, 7.3)
        assert len(ph_readings) >= 2

    @pytest.mark.asyncio
    async def test_ac5_aggregation_queries(
        self,
        repository: SensorReadingRepository,
        batch: Batch,
        sensor_readings: list[SensorReading],
    ):
        """AC5: Aggregation queries work correctly."""
        # Average values
        averages = await repository.get_average_values(batch.id)
        assert averages["avg_temperature"] is not None
        
        # Min/max values
        min_max = await repository.get_min_max_values(batch.id)
        assert min_max["min_temperature"] == 25.0
        assert min_max["max_temperature"] == 26.0

    @pytest.mark.asyncio
    async def test_ac6_anomaly_detection(
        self,
        repository: SensorReadingRepository,
        batch: Batch,
        out_of_range_readings: list[SensorReading],
    ):
        """AC6: Anomaly detection works correctly."""
        readings, total = await repository.get_out_of_range_readings(batch.id)
        
        assert len(readings) == 3
        assert total == 3

    @pytest.mark.asyncio
    async def test_ac7_pagination(
        self,
        repository: SensorReadingRepository,
        batch: Batch,
        sensor_readings: list[SensorReading],
    ):
        """AC7: Pagination works correctly."""
        readings1, total1 = await repository.get_by_batch(batch.id, skip=0, limit=2)
        readings2, total2 = await repository.get_by_batch(batch.id, skip=2, limit=2)
        
        assert len(readings1) == 2
        assert len(readings2) == 1
        assert total1 == 3
        assert total2 == 3

    @pytest.mark.asyncio
    async def test_ac8_statistics(
        self,
        repository: SensorReadingRepository,
        batch: Batch,
        sensor_readings: list[SensorReading],
    ):
        """AC8: Statistics calculation works correctly."""
        stats = await repository.get_statistics(batch.id)
        
        assert stats["total_count"] == 3
        assert "averages" in stats
        assert "min_max" in stats
        assert stats["averages"]["avg_temperature"] is not None
        assert stats["min_max"]["min_temperature"] == 25.0
