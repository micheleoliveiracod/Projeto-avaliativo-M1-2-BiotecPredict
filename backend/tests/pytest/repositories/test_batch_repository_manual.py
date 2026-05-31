"""
Manual test runner for BatchRepository - bypasses pytest configuration issues.

This script tests the BatchRepository implementation directly without pytest.
"""

import asyncio
import sys
from datetime import datetime, timedelta
from pathlib import Path
from uuid import uuid4

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from backend.db.database import Base
from backend.db.repository import BatchRepository
from backend.models.batch import Batch
from backend.models.sensor_reading import SensorReading


async def setup_test_db():
    """Create in-memory test database."""
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async_session = sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
    )
    
    return engine, async_session


async def test_crud_operations():
    """Test CRUD operations."""
    print("\n=== Testing CRUD Operations ===")
    engine, async_session = await setup_test_db()
    
    async with async_session() as session:
        repo = BatchRepository(session)
        
        # Create
        print("✓ Testing create...")
        batch = Batch(status="PROCESSING")
        created = await repo.create(batch)
        assert created.id is not None
        assert created.status == "PROCESSING"
        print(f"  Created batch: {created.id}")
        
        # Read
        print("✓ Testing get_by_id...")
        retrieved = await repo.get_by_id(created.id)
        assert retrieved is not None
        assert retrieved.id == created.id
        print(f"  Retrieved batch: {retrieved.id}")
        
        # Update
        print("✓ Testing update...")
        retrieved.status = "COMPLETED"
        retrieved.compliance_score = 85.5
        updated = await repo.update(retrieved)
        assert updated.status == "COMPLETED"
        print(f"  Updated batch status to: {updated.status}")
        
        # Delete
        print("✓ Testing delete...")
        deleted = await repo.delete(created.id)
        assert deleted is True
        final = await repo.get_by_id(created.id)
        assert final is None
        print(f"  Deleted batch successfully")
    
    await engine.dispose()
    print("✓ CRUD operations test passed!")


async def test_filtering():
    """Test filtering operations."""
    print("\n=== Testing Filtering Operations ===")
    engine, async_session = await setup_test_db()
    
    async with async_session() as session:
        repo = BatchRepository(session)
        
        # Create test batches
        print("✓ Creating test batches...")
        batches = []
        statuses = ["PROCESSING", "COMPLETED", "FAILED"]
        scores = [None, 45.0, 65.0, 75.0, 85.0, 95.0, 50.0, 70.0, 80.0, 90.0]
        
        for i, score in enumerate(scores):
            batch = Batch(
                status=statuses[i % 3],
                compliance_score=score,
                risk_prediction="LOW" if score and score >= 80 else "HIGH"
            )
            session.add(batch)
            batches.append(batch)
        
        await session.flush()
        for batch in batches:
            await session.refresh(batch)
        
        print(f"  Created {len(batches)} test batches")
        
        # Test filtering by status
        print("✓ Testing filter by status...")
        completed, total = await repo.get_by_status("COMPLETED")
        assert all(b.status == "COMPLETED" for b in completed)
        print(f"  Found {len(completed)} completed batches (total: {total})")
        
        # Test filtering by compliance score
        print("✓ Testing filter by compliance score...")
        acceptable, total = await repo.get_acceptable_batches()
        assert all(b.compliance_score is None or b.compliance_score >= 80 for b in acceptable)
        print(f"  Found {len(acceptable)} acceptable batches (total: {total})")
        
        # Test filtering by date range
        print("✓ Testing filter by date range...")
        now = datetime.utcnow()
        from_date = now - timedelta(days=1)
        to_date = now + timedelta(days=1)
        recent, total = await repo.get_by_date_range(from_date, to_date)
        assert len(recent) > 0
        print(f"  Found {len(recent)} recent batches (total: {total})")
    
    await engine.dispose()
    print("✓ Filtering operations test passed!")


async def test_pagination():
    """Test pagination operations."""
    print("\n=== Testing Pagination Operations ===")
    engine, async_session = await setup_test_db()
    
    async with async_session() as session:
        repo = BatchRepository(session)
        
        # Create test batches
        print("✓ Creating test batches...")
        for i in range(10):
            batch = Batch(status="COMPLETED", compliance_score=85.0 + i)
            session.add(batch)
        
        await session.flush()
        
        # Test pagination
        print("✓ Testing pagination...")
        page1, total1 = await repo.list_all_with_readings(skip=0, limit=3)
        page2, total2 = await repo.list_all_with_readings(skip=3, limit=3)
        
        assert len(page1) == 3
        assert len(page2) == 3
        assert total1 == total2 == 10
        assert page1[0].id != page2[0].id
        print(f"  Page 1: {len(page1)} batches")
        print(f"  Page 2: {len(page2)} batches")
        print(f"  Total: {total1} batches")
    
    await engine.dispose()
    print("✓ Pagination operations test passed!")


async def test_statistics():
    """Test statistics operations."""
    print("\n=== Testing Statistics Operations ===")
    engine, async_session = await setup_test_db()
    
    async with async_session() as session:
        repo = BatchRepository(session)
        
        # Create test batches
        print("✓ Creating test batches...")
        statuses = ["PROCESSING", "COMPLETED", "FAILED"]
        for i in range(9):
            batch = Batch(
                status=statuses[i % 3],
                compliance_score=50.0 + i * 10
            )
            session.add(batch)
        
        await session.flush()
        
        # Test statistics
        print("✓ Testing statistics...")
        stats = await repo.get_statistics()
        
        assert stats["total"] == 9
        assert "by_status" in stats
        assert "compliance_score" in stats
        print(f"  Total batches: {stats['total']}")
        print(f"  By status: {stats['by_status']}")
        print(f"  Compliance score - Avg: {stats['compliance_score']['average']:.2f}")
    
    await engine.dispose()
    print("✓ Statistics operations test passed!")


async def test_eager_loading():
    """Test eager loading of relationships."""
    print("\n=== Testing Eager Loading ===")
    engine, async_session = await setup_test_db()
    
    # Create batch with sensor readings in one session
    async with async_session() as session:
        batch = Batch(status="COMPLETED", compliance_score=85.0)
        session.add(batch)
        await session.flush()
        await session.refresh(batch)
        
        for i in range(5):
            reading = SensorReading(
                batch_id=batch.id,
                temperature=25.0 + i,
                ph=7.0 + i * 0.1,
                dissolved_oxygen=75.0 + i * 2,
                pressure=5.0 + i * 0.5,
                agitator_speed=250 + i * 10
            )
            session.add(reading)
        
        await session.flush()
        await session.commit()
        batch_id = batch.id
    
    # Test eager loading in a new session
    print("✓ Creating batch with sensor readings...")
    print("✓ Testing eager loading...")
    async with async_session() as session:
        repo = BatchRepository(session)
        retrieved = await repo.get_by_id_with_readings(batch_id)
        
        assert retrieved is not None
        print(f"  Retrieved batch with {len(retrieved.sensor_readings)} sensor readings")
        assert len(retrieved.sensor_readings) == 5, f"Expected 5 readings, got {len(retrieved.sensor_readings)}"
    
    await engine.dispose()
    print("✓ Eager loading test passed!")


async def main():
    """Run all tests."""
    print("=" * 60)
    print("BatchRepository Manual Test Suite")
    print("=" * 60)
    
    try:
        await test_crud_operations()
        await test_filtering()
        await test_pagination()
        await test_statistics()
        await test_eager_loading()
        
        print("\n" + "=" * 60)
        print("✓ All tests passed successfully!")
        print("=" * 60)
        return 0
    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
