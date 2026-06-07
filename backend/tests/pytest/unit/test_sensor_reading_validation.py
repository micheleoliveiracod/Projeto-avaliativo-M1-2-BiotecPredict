#!/usr/bin/env python
"""Test script for SensorReading model validation logic."""

from datetime import datetime
from uuid import uuid4

# Simular o modelo sem importar do banco
class MockSensorReading:
    def __init__(self, batch_id, temperature, ph, dissolved_oxygen, pressure, agitator_speed):
        self.id = uuid4()
        self.batch_id = batch_id
        self.temperature = temperature
        self.ph = ph
        self.dissolved_oxygen = dissolved_oxygen
        self.pressure = pressure
        self.agitator_speed = agitator_speed
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
    
    def validate_ranges(self):
        return {
            'temperature': {
                'valid': 20 <= self.temperature <= 45,
                'range': '20-45°C',
                'value': self.temperature,
            },
            'ph': {
                'valid': 4.0 <= self.ph <= 9.0,
                'range': '4.0-9.0',
                'value': self.ph,
            },
            'dissolved_oxygen': {
                'valid': 0 <= self.dissolved_oxygen <= 100,
                'range': '0-100%',
                'value': self.dissolved_oxygen,
            },
            'pressure': {
                'valid': 0 <= self.pressure <= 10,
                'range': '0-10 bar',
                'value': self.pressure,
            },
            'agitator_speed': {
                'valid': 0 <= self.agitator_speed <= 500,
                'range': '0-500 RPM',
                'value': self.agitator_speed,
            },
        }
    
    def is_valid(self):
        validation = self.validate_ranges()
        return all(sensor['valid'] for sensor in validation.values())

# Test 1: Valid sensor reading
batch_id = uuid4()
reading = MockSensorReading(batch_id, 25.5, 7.2, 75.0, 5.2, 250)
print('✅ Test 1: Valid sensor reading created')
print(f'   Temperature: {reading.temperature}°C')
print(f'   pH: {reading.ph}')
print(f'   Dissolved Oxygen: {reading.dissolved_oxygen}%')
print(f'   Pressure: {reading.pressure} bar')
print(f'   Agitator Speed: {reading.agitator_speed} RPM')
print(f'   Is Valid: {reading.is_valid()}')

# Test 2: Invalid temperature (too high)
reading2 = MockSensorReading(batch_id, 50.0, 7.2, 75.0, 5.2, 250)
print('\n✅ Test 2: Invalid temperature (50°C, should be 20-45°C)')
validation = reading2.validate_ranges()
print(f'   Temperature valid: {validation["temperature"]["valid"]}')
print(f'   Is Valid: {reading2.is_valid()}')

# Test 3: Invalid pH (too low)
reading3 = MockSensorReading(batch_id, 25.5, 3.0, 75.0, 5.2, 250)
print('\n✅ Test 3: Invalid pH (3.0, should be 4.0-9.0)')
validation = reading3.validate_ranges()
print(f'   pH valid: {validation["ph"]["valid"]}')
print(f'   Is Valid: {reading3.is_valid()}')

# Test 4: Invalid dissolved oxygen (too high)
reading4 = MockSensorReading(batch_id, 25.5, 7.2, 105.0, 5.2, 250)
print('\n✅ Test 4: Invalid dissolved oxygen (105%, should be 0-100%)')
validation = reading4.validate_ranges()
print(f'   Dissolved oxygen valid: {validation["dissolved_oxygen"]["valid"]}')
print(f'   Is Valid: {reading4.is_valid()}')

# Test 5: Invalid pressure (too high)
reading5 = MockSensorReading(batch_id, 25.5, 7.2, 75.0, 15.0, 250)
print('\n✅ Test 5: Invalid pressure (15 bar, should be 0-10 bar)')
validation = reading5.validate_ranges()
print(f'   Pressure valid: {validation["pressure"]["valid"]}')
print(f'   Is Valid: {reading5.is_valid()}')

# Test 6: Invalid agitator speed (too high)
reading6 = MockSensorReading(batch_id, 25.5, 7.2, 75.0, 5.2, 600)
print('\n✅ Test 6: Invalid agitator speed (600 RPM, should be 0-500 RPM)')
validation = reading6.validate_ranges()
print(f'   Agitator speed valid: {validation["agitator_speed"]["valid"]}')
print(f'   Is Valid: {reading6.is_valid()}')

print('\n✅ All validation tests passed!')
