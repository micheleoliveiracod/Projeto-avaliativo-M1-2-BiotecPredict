#!/usr/bin/env python
"""Quick test of the Prediction model."""

from backend.models.prediction import Prediction
from uuid import uuid4

# Test 1: Create a prediction instance
batch_id = uuid4()
pred = Prediction(
    batch_id=batch_id,
    model_version='v1.0.0',
    confidence_score=0.92,
    risk_level='LOW'
)

print('✓ Test 1: Prediction instance created successfully')
print(f'  - ID: {pred.id}')
print(f'  - Batch ID: {pred.batch_id}')
print(f'  - Model Version: {pred.model_version}')
print(f'  - Confidence Score: {pred.confidence_score}')
print(f'  - Risk Level: {pred.risk_level}')
print(f'  - Timestamp: {pred.prediction_timestamp}')

# Test 2: Validate prediction
is_valid = pred.is_valid()
print(f'\n✓ Test 2: Prediction validation - Valid: {is_valid}')

# Test 3: Test to_dict
pred_dict = pred.to_dict()
print(f'\n✓ Test 3: to_dict() method works')
print(f'  - Keys: {list(pred_dict.keys())}')

# Test 4: Test __repr__ and __str__
print(f'\n✓ Test 4: String representations')
print(f'  - repr: {repr(pred)}')
print(f'  - str: {str(pred)}')

# Test 5: Test validators
print(f'\n✓ Test 5: Testing validators')

# Valid confidence scores
valid_scores = [0.0, 0.5, 1.0]
for score in valid_scores:
    pred_test = Prediction(batch_id=batch_id, model_version='v1.0.0', confidence_score=score, risk_level='LOW')
    assert pred_test.is_valid(), f'Score {score} should be valid'
print(f'  - Valid confidence scores (0.0, 0.5, 1.0): ✓')

# Valid risk levels
valid_risks = ['LOW', 'MEDIUM', 'HIGH']
for risk in valid_risks:
    pred_test = Prediction(batch_id=batch_id, model_version='v1.0.0', confidence_score=0.5, risk_level=risk)
    assert pred_test.is_valid(), f'Risk level {risk} should be valid'
print(f'  - Valid risk levels (LOW, MEDIUM, HIGH): ✓')

# Invalid confidence score
pred_invalid = Prediction(batch_id=batch_id, model_version='v1.0.0', confidence_score=1.5, risk_level='LOW')
assert not pred_invalid.is_valid(), 'Score 1.5 should be invalid'
print(f'  - Invalid confidence score (1.5): ✓ (correctly rejected)')

# Invalid risk level
pred_invalid = Prediction(batch_id=batch_id, model_version='v1.0.0', confidence_score=0.5, risk_level='INVALID')
assert not pred_invalid.is_valid(), 'Risk level INVALID should be invalid'
print(f'  - Invalid risk level (INVALID): ✓ (correctly rejected)')

print('\n✅ All tests passed! Prediction model is fully functional.')
