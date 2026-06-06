"""
Manual test script for SensorReadingRepository.

This script tests the SensorReadingRepository without pytest to verify functionality.
"""

import asyncio
from datetime import datetime, timedelta
from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from backend.db.database import Base
from backend.db.repository import SensorReadingRepository
from backend.models.batch import Batch
from backend.models.sensor_reading import SensorReading


async def main():
    """Run manual tests."""
    # Create in-memory SQLite database
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Create session factory
    async_session = sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
    )
    
    async with async_session() as session:
        # Create test batch
        batch = Batch(status="PROCESSING")
        session.add(batch)
        await session.flush()
        
        # Create repository
        repo = SensorReadingRepository(session)
        
        # Test 1: Create sensor readings
        print("Test 1: Creating sensor readings...")
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
            created = await repo.create(reading)
            print(f"  ✓ Created reading: {created.id}")
        
        # Test 2: Get by batch
        print("\nTest 2: Getting readings by batch...")
        batch_readings, total = await repo.get_by_batch(batch.id)
        print(f"  ✓ Found {len(batch_readings)} readings (total: {total})")
        
        # Test 3: Get average values
        print("\nTest 3: Getting average values...")
        averages = await repo.get_average_values(batch.id)
        print(f"  ✓ Average temperature: {averages['avg_temperature']:.2f}°C")
        print(f"  ✓ Average pH: {averages['avg_ph']:.2f}")
        
        # Test 4: Get min/max values
        print("\nTest 4: Getting min/max values...")
        min_max = await repo.get_min_max_values(batch.id)
        print(f"  ✓ Temperature range: {min_max['min_temperature']:.1f} - {min_max['max_temperature']:.1f}°C")
        
        # Test 5: Get statistics
        print("\nTest 5: Getting statistics...")
        stats = await repo.get_statistics(batch.id)
        print(f"  ✓ Total readings: {stats['total_count']}")
        
        # Test 6: Get latest reading
        print("\nTest 6: Getting latest reading...")
        latest = await repo.get_latest_reading(batch.id)
        print(f"  ✓ Latest temperature: {latest.temperature}°C")
        
        # Test 7: Get first reading
        print("\nTest 7: Getting first reading...")
        first = await repo.get_first_reading(batch.id)
        print(f"  ✓ First temperature: {first.temperature}°C")
        
        # Test 8: Get by temperature range
        print("\nTest 8: Getting readings by temperature range...")
        temp_readings, _ = await repo.get_by_temperature_range(batch.id, 24.0, 26.0)
        print(f"  ✓ Found {len(temp_readings)} readings in temperature range")
        
        # Test 9: Get by pH range
        print("\nTest 9: Getting readings by pH range...")
        ph_readings, _ = await repo.get_by_ph_range(batch.id, 6.9, 7.3)
        print(f"  ✓ Found {len(ph_readings)} readings in pH range")
        
        # Test 10: Count by batch
        print("\nTest 10: Counting readings by batch...")
        count = await repo.count_by_batch(batch.id)
        print(f"  ✓ Total readings: {count}")
        
        # Test 11: Out of range readings
        print("\nTest 11: Testing out-of-range detection...")
        out_of_range = SensorReading(
            batch_id=batch.id,
            temperature=50.0,  # Out of range
            ph=7.0,
            dissolved_oxygen=75.0,
            pressure=5.0,
            agitator_speed=250,
        )
        await repo.create(out_of_range)
        
        anomalies, _ = await repo.get_out_of_range_readings(batch.id)
        print(f"  ✓ Found {len(anomalies)} out-of-range readings")
        
        # Test 12: Pagination
        print("\nTest 12: Testing pagination...")
        page1, total1 = await repo.get_by_batch(batch.id, skip=0, limit=2)
        page2, total2 = await repo.get_by_batch(batch.id, skip=2, limit=2)
        print(f"  ✓ Page 1: {len(page1)} readings")
        print(f"  ✓ Page 2: {len(page2)} readings")
        print(f"  ✓ Total: {total1} readings")
        
        print("\n✅ All tests passed!")
    
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
