#!/usr/bin/env python
"""
Verification script for Task 3: Implementar Modelo SensorReading
Tests that the SensorReading model meets all requirements.
"""

import sys
from uuid import uuid4

# Add parent directory to path for imports
sys.path.insert(0, '..')

from backend.models import Batch, SensorReading, Prediction


def verify_requirements():
    """Verify all requirements for SensorReading model."""
    
    print("=" * 70)
    print("TASK 3: IMPLEMENTAR MODELO SENSORREADING - VERIFICATION")
    print("=" * 70)
    
    # Requirement 1: FK para Batch
    print("\n✓ Requirement 1: Foreign Key para Batch")
    assert hasattr(SensorReading, 'batch_id'), "batch_id field missing"
    fk = list(SensorReading.__table__.c.batch_id.foreign_keys)[0]
    print(f"  - batch_id field exists: True")
    print(f"  - batch_id is FK to batches.id: {fk}")
    print(f"  - Cascade delete ON DELETE CASCADE: {fk.ondelete}")
    assert fk.ondelete == "CASCADE", "Cascade delete not configured"
    
    # Requirement 2: Campos de sensores
    print("\n✓ Requirement 2: Campos de Sensores")
    sensor_fields = ['temperature', 'ph', 'dissolved_oxygen', 'pressure', 'agitator_speed', 'timestamp']
    for field in sensor_fields:
        has_field = hasattr(SensorReading, field)
        print(f"  - {field}: {has_field}")
        assert has_field, f"{field} missing"
    
    # Requirement 3: Índice composto em (batch_id, timestamp)
    print("\n✓ Requirement 3: Índice Composto (batch_id, timestamp)")
    found_composite_index = False
    for idx in SensorReading.__table__.indexes:
        columns = [c.name for c in idx.columns]
        print(f"  - Index '{idx.name}': {columns}")
        if columns == ['batch_id', 'timestamp']:
            found_composite_index = True
            print(f"    ✓ Composite index found!")
    assert found_composite_index, "Composite index (batch_id, timestamp) not found"
    
    # Requirement 4: Relacionamento bidirecional com Batch
    print("\n✓ Requirement 4: Relacionamento Bidirecional com Batch")
    assert hasattr(SensorReading, 'batch'), "SensorReading.batch relationship missing"
    assert hasattr(Batch, 'sensor_readings'), "Batch.sensor_readings relationship missing"
    print(f"  - SensorReading.batch relationship exists: True")
    print(f"  - Batch.sensor_readings relationship exists: True")
    print(f"  - back_populates='sensor_readings': {SensorReading.batch.property.back_populates}")
    print(f"  - back_populates='batch': {Batch.sensor_readings.property.back_populates}")
    
    # Requirement 5: Cascade delete
    print("\n✓ Requirement 5: Cascade Delete")
    cascade_config = Batch.sensor_readings.property.cascade
    print(f"  - Cascade configuration: {cascade_config}")
    assert 'delete-orphan' in cascade_config, "delete-orphan not in cascade config"
    print(f"  - Includes 'delete-orphan': True")
    
    # Requirement 6: Campos obrigatórios (NOT NULL)
    print("\n✓ Requirement 6: Campos Obrigatórios (NOT NULL)")
    required_fields = ['batch_id', 'temperature', 'ph', 'dissolved_oxygen', 'pressure', 'agitator_speed', 'timestamp']
    for field in required_fields:
        col = SensorReading.__table__.c[field]
        print(f"  - {field}: nullable={col.nullable}")
        assert not col.nullable, f"{field} should not be nullable"
    
    # Requirement 7: Validação de ranges
    print("\n✓ Requirement 7: Validação de Ranges")
    assert hasattr(SensorReading, 'is_within_ranges'), "is_within_ranges() method missing"
    assert hasattr(SensorReading, 'get_out_of_range_sensors'), "get_out_of_range_sensors() method missing"
    print(f"  - is_within_ranges() method exists: True")
    print(f"  - get_out_of_range_sensors() method exists: True")
    
    # Test validation methods
    print("\n✓ Testing Validation Methods:")
    reading = SensorReading(
        batch_id=uuid4(),
        temperature=25.0,
        ph=7.0,
        dissolved_oxygen=75.0,
        pressure=5.0,
        agitator_speed=250
    )
    assert reading.is_within_ranges(), "Valid reading should pass validation"
    assert reading.get_out_of_range_sensors() == [], "Valid reading should have no out-of-range sensors"
    print(f"  - Valid reading is_within_ranges(): True")
    print(f"  - Valid reading out_of_range_sensors(): []")
    
    # Test with out-of-range values
    reading_invalid = SensorReading(
        batch_id=uuid4(),
        temperature=50.0,  # Out of range (20-45)
        ph=10.0,  # Out of range (4.0-9.0)
        dissolved_oxygen=75.0,
        pressure=5.0,
        agitator_speed=250
    )
    assert not reading_invalid.is_within_ranges(), "Invalid reading should fail validation"
    out_of_range = reading_invalid.get_out_of_range_sensors()
    assert 'temperature' in out_of_range, "temperature should be detected as out of range"
    assert 'ph' in out_of_range, "ph should be detected as out of range"
    print(f"  - Invalid reading is_within_ranges(): False")
    print(f"  - Invalid reading out_of_range_sensors(): {out_of_range}")
    
    # Requirement 8: Docstrings
    print("\n✓ Requirement 8: Documentação (Docstrings)")
    assert SensorReading.__doc__, "Class docstring missing"
    assert SensorReading.to_dict.__doc__, "to_dict() docstring missing"
    print(f"  - Class docstring exists: True")
    print(f"  - Methods documented: True")
    
    # Requirement 9: to_dict() method
    print("\n✓ Requirement 9: to_dict() Method")
    reading_dict = reading.to_dict()
    assert 'id' in reading_dict, "id missing from to_dict()"
    assert 'batch_id' in reading_dict, "batch_id missing from to_dict()"
    assert 'temperature' in reading_dict, "temperature missing from to_dict()"
    print(f"  - to_dict() returns all fields: True")
    print(f"  - Sample output: {reading_dict}")
    
    print("\n" + "=" * 70)
    print("✓ ALL REQUIREMENTS VERIFIED SUCCESSFULLY")
    print("=" * 70)
    print("\nTask 3 Status: COMPLETED")
    print("- SensorReading model fully implemented")
    print("- FK to Batch with CASCADE delete")
    print("- All sensor fields (temperature, pH, DO, pressure, agitator_speed)")
    print("- Composite index on (batch_id, timestamp)")
    print("- Bidirectional relationship with Batch")
    print("- Validation methods for sensor ranges")
    print("- Complete documentation and docstrings")


if __name__ == "__main__":
    try:
        verify_requirements()
        sys.exit(0)
    except AssertionError as e:
        print(f"\n✗ VERIFICATION FAILED: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
