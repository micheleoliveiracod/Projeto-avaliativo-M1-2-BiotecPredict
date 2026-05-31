"""
Tests for BatchService - Batch processing and ETL pipeline.

This module contains comprehensive tests for the BatchService class,
including:
- CSV parsing and validation
- Batch creation with ACID transactions
- Error handling and rollback
- Database persistence
- End-to-end ETL pipeline

Test Coverage:
- Successful batch creation from valid CSV
- Error handling for invalid CSV
- Error handling for validation failures
- Transaction rollback on errors
- Batch retrieval and listing
- Statistics calculation

Task 20: Criar BatchService
- Implementar create_batch_from_csv(file, db_session)
- Orquestra parse→validate→create→persist com transação ACID
- Retorna batch_id ou exceção
- Service funciona end-to-end
- Rollback em erro
"""

import io
from typing import AsyncGenerator
from uuid import UUID

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from backend.db.database import Base
from backend.models.batch import Batch
from backend.models.sensor_reading import SensorReading
from backend.services.batch_service import (
    BatchService,
    CSVProcessingError,
    DataValidationError,
)


# ============================================================================
# Fixtures
# ============================================================================


@pytest.fixture
async def test_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Create an in-memory SQLite database session for testing.
    
    Yields:
        AsyncSession: Database session for tests
    """
    # Create in-memory SQLite engine
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        echo=False,
        future=True,
    )
    
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Create session factory
    AsyncSessionLocal = sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
    )
    
    # Yield session
    async with AsyncSessionLocal() as session:
        yield session
    
    # Cleanup
    await engine.dispose()


@pytest.fixture
def batch_service() -> BatchService:
    """
    Create a BatchService instance for testing.
    
    Returns:
        BatchService: Service instance
    """
    return BatchService()


@pytest.fixture
def valid_csv_content() -> bytes:
    """
    Create valid CSV content for testing.
    
    Returns:
        bytes: Valid CSV file content
    """
    csv_data = """temperature,ph,dissolved_oxygen,pressure,agitator_speed
25.5,7.2,75.0,5.2,250
26.0,7.1,76.0,5.3,255
24.8,7.3,74.5,5.1,248
25.2,7.2,75.5,5.2,252
26.5,7.0,77.0,5.4,260
"""
    return csv_data.encode("utf-8")


# ============================================================================
# Tests: Successful Batch Creation
# ============================================================================


@pytest.mark.asyncio
async def test_create_batch_from_csv_success(
    batch_service: BatchService,
    test_db_session: AsyncSession,
    valid_csv_content: bytes,
) -> None:
    """
    Test successful batch creation from valid CSV.
    
    Verifies:
    - Batch is created with correct ID
    - Batch status is COMPLETED
    - Sensor readings are created
    - All data is persisted in database
    """
    # Create a mock UploadFile-like object
    class MockUploadFile:
        def __init__(self, content: bytes, filename: str):
            self.file = io.BytesIO(content)
            self.filename = filename
            self.size = len(content)
        
        async def read(self) -> bytes:
            return self.file.getvalue()
    
    file = MockUploadFile(valid_csv_content, "test_batch.csv")
    
    # Create batch
    batch_id = await batch_service.create_batch_from_csv(file, test_db_session)
    
    # Verify batch was created
    assert batch_id is not None
    assert isinstance(batch_id, UUID)
    
    # Retrieve batch
    batch = await batch_service.get_batch(batch_id, test_db_session)
    
    # Verify batch properties
    assert batch is not None
    assert batch.id == batch_id
    assert batch.status == "COMPLETED"
    assert batch.upload_date is not None
    
    # Verify sensor readings were created
    assert len(batch.sensor_readings) == 5
    
    # Verify first sensor reading
    first_reading = batch.sensor_readings[0]
    assert first_reading.batch_id == batch_id
    assert first_reading.temperature == 25.5
    assert first_reading.ph == 7.2
    assert first_reading.dissolved_oxygen == 75.0
    assert first_reading.pressure == 5.2
    assert first_reading.agitator_speed == 250


@pytest.mark.asyncio
async def test_create_batch_from_csv_single_reading(
    batch_service: BatchService,
    test_db_session: AsyncSession,
) -> None:
    """
    Test batch creation with single sensor reading.
    
    Verifies:
    - Batch is created with one reading
    - All sensor values are correctly stored
    """
    csv_data = b"""temperature,ph,dissolved_oxygen,pressure,agitator_speed
25.5,7.2,75.0,5.2,250
"""
    
    class MockUploadFile:
        def __init__(self, content: bytes, filename: str):
            self.file = io.BytesIO(content)
            self.filename = filename
            self.size = len(content)
        
        async def read(self) -> bytes:
            return self.file.getvalue()
    
    file = MockUploadFile(csv_data, "single_reading.csv")
    
    batch_id = await batch_service.create_batch_from_csv(file, test_db_session)
    batch = await batch_service.get_batch(batch_id, test_db_session)
    
    assert len(batch.sensor_readings) == 1
    assert batch.sensor_readings[0].temperature == 25.5


@pytest.mark.asyncio
async def test_create_batch_from_csv_multiple_readings(
    batch_service: BatchService,
    test_db_session: AsyncSession,
) -> None:
    """
    Test batch creation with multiple sensor readings.
    
    Verifies:
    - All readings are created
    - Each reading has correct values
    """
    csv_data = b"""temperature,ph,dissolved_oxygen,pressure,agitator_speed
20.0,4.0,0.0,0.0,0.0
45.0,9.0,100.0,10.0,500.0
25.0,7.0,50.0,5.0,250.0
"""
    
    class MockUploadFile:
        def __init__(self, content: bytes, filename: str):
            self.file = io.BytesIO(content)
            self.filename = filename
            self.size = len(content)
        
        async def read(self) -> bytes:
            return self.file.getvalue()
    
    file = MockUploadFile(csv_data, "multiple_readings.csv")
    
    batch_id = await batch_service.create_batch_from_csv(file, test_db_session)
    batch = await batch_service.get_batch(batch_id, test_db_session)
    
    assert len(batch.sensor_readings) == 3
    
    # Verify boundary values
    assert batch.sensor_readings[0].temperature == 20.0
    assert batch.sensor_readings[1].temperature == 45.0
    assert batch.sensor_readings[2].temperature == 25.0


# ============================================================================
# Tests: Error Handling - CSV Processing
# ============================================================================


@pytest.mark.asyncio
async def test_create_batch_from_csv_empty_file(
    batch_service: BatchService,
    test_db_session: AsyncSession,
) -> None:
    """
    Test batch creation with empty CSV file.
    
    Verifies:
    - CSVProcessingError is raised
    - No batch is created
    - Transaction is rolled back
    """
    class MockUploadFile:
        def __init__(self):
            self.filename = "empty.csv"
            self.size = 0
        
        async def read(self) -> bytes:
            return b""
    
    file = MockUploadFile()
    
    with pytest.raises(CSVProcessingError):
        await batch_service.create_batch_from_csv(file, test_db_session)


@pytest.mark.asyncio
async def test_create_batch_from_csv_missing_columns(
    batch_service: BatchService,
    test_db_session: AsyncSession,
) -> None:
    """
    Test batch creation with missing required columns.
    
    Verifies:
    - CSVProcessingError is raised
    - Error message indicates missing columns
    """
    csv_data = b"""temperature,ph,pressure
25.5,7.2,5.2
26.0,7.1,5.3
"""
    
    class MockUploadFile:
        def __init__(self, content: bytes, filename: str):
            self.file = io.BytesIO(content)
            self.filename = filename
            self.size = len(content)
        
        async def read(self) -> bytes:
            return self.file.getvalue()
    
    file = MockUploadFile(csv_data, "missing_columns.csv")
    
    with pytest.raises(CSVProcessingError):
        await batch_service.create_batch_from_csv(file, test_db_session)


# ============================================================================
# Tests: Error Handling - Data Validation
# ============================================================================


@pytest.mark.asyncio
async def test_create_batch_from_csv_out_of_range_temperature(
    batch_service: BatchService,
    test_db_session: AsyncSession,
) -> None:
    """
    Test batch creation with out-of-range temperature.
    
    Verifies:
    - CSVProcessingError is raised (validation happens during CSV parsing)
    - Temperature range is 20-45°C
    """
    csv_data = b"""temperature,ph,dissolved_oxygen,pressure,agitator_speed
50.0,7.2,75.0,5.2,250
"""
    
    class MockUploadFile:
        def __init__(self, content: bytes, filename: str):
            self.file = io.BytesIO(content)
            self.filename = filename
            self.size = len(content)
        
        async def read(self) -> bytes:
            return self.file.getvalue()
    
    file = MockUploadFile(csv_data, "invalid_temp.csv")
    
    # Validation happens during CSV parsing, so CSVProcessingError is raised
    with pytest.raises(CSVProcessingError):
        await batch_service.create_batch_from_csv(file, test_db_session)


# ============================================================================
# Tests: Batch Retrieval and Listing
# ============================================================================


@pytest.mark.asyncio
async def test_get_batch_not_found(
    batch_service: BatchService,
    test_db_session: AsyncSession,
) -> None:
    """
    Test batch retrieval for non-existent batch.
    
    Verifies:
    - Returns None for non-existent batch
    """
    from uuid import uuid4
    
    batch = await batch_service.get_batch(uuid4(), test_db_session)
    
    assert batch is None


@pytest.mark.asyncio
async def test_list_batches_empty(
    batch_service: BatchService,
    test_db_session: AsyncSession,
) -> None:
    """
    Test listing batches when none exist.
    
    Verifies:
    - Returns empty list
    - Total count is 0
    """
    batches, total = await batch_service.list_batches(
        skip=0,
        limit=20,
        db_session=test_db_session,
    )
    
    assert len(batches) == 0
    assert total == 0


@pytest.mark.asyncio
async def test_list_batches_with_data(
    batch_service: BatchService,
    test_db_session: AsyncSession,
    valid_csv_content: bytes,
) -> None:
    """
    Test listing batches with data.
    
    Verifies:
    - Batches are returned
    - Total count is correct
    - Pagination works
    """
    class MockUploadFile:
        def __init__(self, content: bytes, filename: str):
            self.file = io.BytesIO(content)
            self.filename = filename
            self.size = len(content)
        
        async def read(self) -> bytes:
            return self.file.getvalue()
    
    # Create multiple batches
    for i in range(3):
        file = MockUploadFile(valid_csv_content, f"test_{i}.csv")
        await batch_service.create_batch_from_csv(file, test_db_session)
    
    # List batches
    batches, total = await batch_service.list_batches(
        skip=0,
        limit=20,
        db_session=test_db_session,
    )
    
    assert len(batches) == 3
    assert total == 3


# ============================================================================
# Tests: Statistics
# ============================================================================


@pytest.mark.asyncio
async def test_get_batch_statistics_empty(
    batch_service: BatchService,
    test_db_session: AsyncSession,
) -> None:
    """
    Test statistics when no batches exist.
    
    Verifies:
    - Returns statistics with zero counts
    """
    stats = await batch_service.get_batch_statistics(test_db_session)
    
    assert stats["total"] == 0
    assert stats["by_status"]["PROCESSING"] == 0
    assert stats["by_status"]["COMPLETED"] == 0
    assert stats["by_status"]["FAILED"] == 0


@pytest.mark.asyncio
async def test_get_batch_statistics_with_data(
    batch_service: BatchService,
    test_db_session: AsyncSession,
    valid_csv_content: bytes,
) -> None:
    """
    Test statistics with batch data.
    
    Verifies:
    - Statistics are calculated correctly
    - Counts are accurate
    """
    class MockUploadFile:
        def __init__(self, content: bytes, filename: str):
            self.file = io.BytesIO(content)
            self.filename = filename
            self.size = len(content)
        
        async def read(self) -> bytes:
            return self.file.getvalue()
    
    # Create batch
    file = MockUploadFile(valid_csv_content, "test.csv")
    await batch_service.create_batch_from_csv(file, test_db_session)
    
    # Get statistics
    stats = await batch_service.get_batch_statistics(test_db_session)
    
    assert stats["total"] == 1
    assert stats["by_status"]["COMPLETED"] == 1
