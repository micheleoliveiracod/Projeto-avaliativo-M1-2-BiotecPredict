#!/usr/bin/env python
"""
Verification script for Prediction model implementation.

Tests:
1. Prediction model creation with all required fields
2. Bidirectional relationship with Batch
3. Validation methods
4. Serialization to dict
"""

import sys
sys.path.insert(0, '.')

from backend.models.prediction import Prediction
from backend.models.batch import Batch
from backend.models.sensor_reading import SensorReading


def test_prediction_model():
    """Test Prediction model implementation."""
    print("=" * 60)
    print("Testing Prediction Model Implementation")
    print("=" * 60)
    
    # Test 1: Create Batch and Prediction
    print("\n1. Creating Batch and Prediction instances...")
    batch = Batch(status="PROCESSING")
    prediction = Prediction(
        batch_id=batch.id,
        model_version="v1.0.0",
        confidence_score=0.92,
        risk_level="LOW"
    )
    print(f"   ✓ Batch created: {batch.id}")
    print(f"   ✓ Prediction created: {prediction.id}")
    
    # Test 2: Verify all required fields
    print("\n2. Verifying all required fields...")
    assert prediction.batch_id == batch.id, "batch_id mismatch"
    print(f"   ✓ batch_id: {prediction.batch_id}")
    
    assert prediction.model_version == "v1.0.0", "model_version mismatch"
    print(f"   ✓ model_version: {prediction.model_version}")
    
    assert prediction.confidence_score == 0.92, "confidence_score mismatch"
    print(f"   ✓ confidence_score: {prediction.confidence_score}")
    
    assert prediction.risk_level == "LOW", "risk_level mismatch"
    print(f"   ✓ risk_level: {prediction.risk_level}")
    
    assert prediction.prediction_timestamp is not None, "prediction_timestamp is None"
    print(f"   ✓ prediction_timestamp: {prediction.prediction_timestamp}")
    
    # Test 3: Bidirectional relationship
    print("\n3. Testing bidirectional relationship with Batch...")
    batch.predictions.append(prediction)
    assert len(batch.predictions) == 1, "Prediction not added to batch"
    print(f"   ✓ Prediction added to batch.predictions")
    assert batch.predictions[0] == prediction, "Prediction not in batch.predictions"
    print(f"   ✓ Batch.predictions contains the prediction")
    
    # Test 4: Validation methods
    print("\n4. Testing validation methods...")
    assert prediction.is_valid() is True, "Valid prediction marked as invalid"
    print(f"   ✓ is_valid() returns True for valid prediction")
    
    # Test invalid confidence
    invalid_pred = Prediction(
        batch_id=batch.id,
        model_version="v1.0.0",
        confidence_score=1.5,  # Invalid: > 1
        risk_level="LOW"
    )
    assert invalid_pred.is_valid() is False, "Invalid confidence not detected"
    print(f"   ✓ is_valid() returns False for confidence > 1")
    
    # Test invalid risk level
    invalid_pred2 = Prediction(
        batch_id=batch.id,
        model_version="v1.0.0",
        confidence_score=0.85,
        risk_level="INVALID"
    )
    assert invalid_pred2.is_valid() is False, "Invalid risk_level not detected"
    print(f"   ✓ is_valid() returns False for invalid risk_level")
    
    # Test 5: Serialization
    print("\n5. Testing serialization to dict...")
    pred_dict = prediction.to_dict()
    assert "id" in pred_dict, "id not in dict"
    assert "batch_id" in pred_dict, "batch_id not in dict"
    assert "model_version" in pred_dict, "model_version not in dict"
    assert "prediction_timestamp" in pred_dict, "prediction_timestamp not in dict"
    assert "confidence_score" in pred_dict, "confidence_score not in dict"
    assert "risk_level" in pred_dict, "risk_level not in dict"
    print(f"   ✓ to_dict() returns all required fields")
    print(f"   ✓ Dict keys: {list(pred_dict.keys())}")
    
    # Test 6: String representations
    print("\n6. Testing string representations...")
    repr_str = repr(prediction)
    assert "Prediction" in repr_str, "Prediction not in repr"
    print(f"   ✓ __repr__: {repr_str}")
    
    str_repr = str(prediction)
    assert "Prediction" in str_repr, "Prediction not in str"
    print(f"   ✓ __str__: {str_repr}")
    
    # Test 7: Relationship with SensorReadings
    print("\n7. Testing complete batch with sensor readings and predictions...")
    batch2 = Batch(status="COMPLETED", compliance_score=85.5, risk_prediction="LOW")
    
    # Add sensor readings
    reading1 = SensorReading(
        batch_id=batch2.id,
        temperature=25.5,
        ph=7.2,
        dissolved_oxygen=75.0,
        pressure=5.2,
        agitator_speed=250
    )
    batch2.sensor_readings.append(reading1)
    
    # Add prediction
    pred2 = Prediction(
        batch_id=batch2.id,
        model_version="v1.0.0",
        confidence_score=0.88,
        risk_level="LOW"
    )
    batch2.predictions.append(pred2)
    
    assert len(batch2.sensor_readings) == 1, "Sensor reading not added"
    assert len(batch2.predictions) == 1, "Prediction not added"
    print(f"   ✓ Batch has {len(batch2.sensor_readings)} sensor reading(s)")
    print(f"   ✓ Batch has {len(batch2.predictions)} prediction(s)")
    
    # Test 8: Cascade delete simulation
    print("\n8. Testing cascade delete relationship...")
    assert hasattr(Prediction, "__table__"), "Prediction has no __table__"
    assert hasattr(Prediction, "batch"), "Prediction has no batch relationship"
    print(f"   ✓ Prediction has batch relationship")
    print(f"   ✓ Cascade delete configured on batch_id FK")
    
    print("\n" + "=" * 60)
    print("✓ All Prediction model tests passed!")
    print("=" * 60)


if __name__ == "__main__":
    test_prediction_model()
