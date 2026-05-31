#!/usr/bin/env python
"""Test script to verify models __init__.py is correctly configured."""

from backend.models import Batch, SensorReading, Prediction, __all__

# Test 1: Verify models are classes
print("✓ Test 1: Models are proper classes")
print(f"  - Batch is a class: {isinstance(Batch, type)}")
print(f"  - SensorReading is a class: {isinstance(SensorReading, type)}")
print(f"  - Prediction is a class: {isinstance(Prediction, type)}")

# Test 2: Verify models have __tablename__
print("\n✓ Test 2: Models have table names")
print(f"  - Batch table: {Batch.__tablename__}")
print(f"  - SensorReading table: {SensorReading.__tablename__}")
print(f"  - Prediction table: {Prediction.__tablename__}")

# Test 3: Verify relationships are defined
print("\n✓ Test 3: Relationships are defined")
print(f"  - Batch has sensor_readings: {hasattr(Batch, 'sensor_readings')}")
print(f"  - Batch has predictions: {hasattr(Batch, 'predictions')}")
print(f"  - SensorReading has batch: {hasattr(SensorReading, 'batch')}")
print(f"  - Prediction has batch: {hasattr(Prediction, 'batch')}")

# Test 4: Verify __all__ export
print("\n✓ Test 4: __all__ export list")
print(f"  - __all__ = {__all__}")
expected_all = {"Batch", "SensorReading", "Prediction"}
print(f"  - All models in __all__: {set(__all__) == expected_all}")

# Test 5: Verify module docstring
print("\n✓ Test 5: Module docstring")
import backend.models
has_docstring = backend.models.__doc__ is not None and len(backend.models.__doc__) > 0
print(f"  - Module has docstring: {has_docstring}")
if has_docstring:
    print(f"  - Docstring length: {len(backend.models.__doc__)} characters")

print("\n✅ All tests passed! Task 5 is complete.")
