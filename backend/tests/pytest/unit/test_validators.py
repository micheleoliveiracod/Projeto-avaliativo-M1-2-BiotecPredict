"""
Tests for Data Validator Module.

Task 19: Criar Validador de Dados
- Testes para validate_sensor_readings() com dados válidos e inválidos
- Testes para validação de ranges de sensores
- Testes para rejeição de dados fora de range
- Testes para aceitação de dados válidos
- Testes para tratamento de erros

Test Coverage:
- Valid sensor readings
- Out of range values (each sensor)
- Missing values
- Invalid data types
- Empty readings list
- Multiple errors
- Boundary values
- Pydantic validation
- Error reporting
"""

import pytest

from backend.processors.data_validator import (
    SensorDataValidator,
    ValidationError,
    ValidationResult,
    validate_sensor_readings,
)


class TestSensorDataValidator:
    """Test suite for SensorDataValidator class."""
    
    @pytest.fixture
    def validator(self):
        """Create a sensor data validator instance."""
        return SensorDataValidator()
    
    # ==================== Valid Readings Tests ====================
    
    def test_validate_single_valid_reading(self, validator):
        """Test validation of a single valid sensor reading."""
        readings = [
            {
                "temperature": 25.5,
                "ph": 7.2,
                "dissolved_oxygen": 75.0,
                "pressure": 5.2,
                "agitator_speed": 250,
            }
        ]
        
        result = validator.validate_sensor_readings(readings)
        
        assert result.success is True
        assert result.valid_count == 1
        assert result.invalid_count == 0
        assert len(result.errors) == 0
        assert len(result.valid_readings) == 1
        assert len(result.invalid_readings) == 0
    
    def test_validate_multiple_valid_readings(self, validator):
        """Test validation of multiple valid sensor readings."""
        readings = [
            {
                "temperature": 25.5,
                "ph": 7.2,
                "dissolved_oxygen": 75.0,
                "pressure": 5.2,
                "agitator_speed": 250,
            },
            {
                "temperature": 30.0,
                "ph": 6.5,
                "dissolved_oxygen": 80.0,
                "pressure": 3.5,
                "agitator_speed": 300,
            },
            {
                "temperature": 22.0,
                "ph": 8.0,
                "dissolved_oxygen": 60.0,
                "pressure": 7.0,
                "agitator_speed": 150,
            },
        ]
        
        result = validator.validate_sensor_readings(readings)
        
        assert result.success is True
        assert result.valid_count == 3
        assert result.invalid_count == 0
        assert len(result.errors) == 0
    
    def test_validate_boundary_values_min(self, validator):
        """Test validation with minimum boundary values."""
        readings = [
            {
                "temperature": 20.0,  # Min
                "ph": 4.0,  # Min
                "dissolved_oxygen": 0.0,  # Min
                "pressure": 0.0,  # Min
                "agitator_speed": 0.0,  # Min
            }
        ]
        
        result = validator.validate_sensor_readings(readings)
        
        assert result.success is True
        assert result.valid_count == 1
        assert result.invalid_count == 0
    
    def test_validate_boundary_values_max(self, validator):
        """Test validation with maximum boundary values."""
        readings = [
            {
                "temperature": 45.0,  # Max
                "ph": 9.0,  # Max
                "dissolved_oxygen": 100.0,  # Max
                "pressure": 10.0,  # Max
                "agitator_speed": 500.0,  # Max
            }
        ]
        
        result = validator.validate_sensor_readings(readings)
        
        assert result.success is True
        assert result.valid_count == 1
        assert result.invalid_count == 0
    
    # ==================== Out of Range Tests ====================
    
    def test_validate_temperature_below_min(self, validator):
        """Test validation rejects temperature below minimum."""
        readings = [
            {
                "temperature": 19.9,  # Below min (20)
                "ph": 7.2,
                "dissolved_oxygen": 75.0,
                "pressure": 5.2,
                "agitator_speed": 250,
            }
        ]
        
        result = validator.validate_sensor_readings(readings)
        
        assert result.success is False
        assert result.valid_count == 0
        assert result.invalid_count == 1
        assert len(result.errors) == 1
        assert result.errors[0].field_name == "temperature"
        assert result.errors[0].error_type == "OUT_OF_RANGE"
    
    def test_validate_temperature_above_max(self, validator):
        """Test validation rejects temperature above maximum."""
        readings = [
            {
                "temperature": 45.1,  # Above max (45)
                "ph": 7.2,
                "dissolved_oxygen": 75.0,
                "pressure": 5.2,
                "agitator_speed": 250,
            }
        ]
        
        result = validator.validate_sensor_readings(readings)
        
        assert result.success is False
        assert result.valid_count == 0
        assert result.invalid_count == 1
        assert len(result.errors) == 1
        assert result.errors[0].field_name == "temperature"
    
    def test_validate_ph_below_min(self, validator):
        """Test validation rejects pH below minimum."""
        readings = [
            {
                "temperature": 25.5,
                "ph": 3.9,  # Below min (4.0)
                "dissolved_oxygen": 75.0,
                "pressure": 5.2,
                "agitator_speed": 250,
            }
        ]
        
        result = validator.validate_sensor_readings(readings)
        
        assert result.success is False
        assert result.valid_count == 0
        assert result.invalid_count == 1
        assert len(result.errors) == 1
        assert result.errors[0].field_name == "ph"
    
    def test_validate_ph_above_max(self, validator):
        """Test validation rejects pH above maximum."""
        readings = [
            {
                "temperature": 25.5,
                "ph": 9.1,  # Above max (9.0)
                "dissolved_oxygen": 75.0,
                "pressure": 5.2,
                "agitator_speed": 250,
            }
        ]
        
        result = validator.validate_sensor_readings(readings)
        
        assert result.success is False
        assert result.valid_count == 0
        assert result.invalid_count == 1
        assert len(result.errors) == 1
        assert result.errors[0].field_name == "ph"
    
    def test_validate_dissolved_oxygen_below_min(self, validator):
        """Test validation rejects dissolved oxygen below minimum."""
        readings = [
            {
                "temperature": 25.5,
                "ph": 7.2,
                "dissolved_oxygen": -0.1,  # Below min (0)
                "pressure": 5.2,
                "agitator_speed": 250,
            }
        ]
        
        result = validator.validate_sensor_readings(readings)
        
        assert result.success is False
        assert result.valid_count == 0
        assert result.invalid_count == 1
        assert len(result.errors) == 1
        assert result.errors[0].field_name == "dissolved_oxygen"
    
    def test_validate_dissolved_oxygen_above_max(self, validator):
        """Test validation rejects dissolved oxygen above maximum."""
        readings = [
            {
                "temperature": 25.5,
                "ph": 7.2,
                "dissolved_oxygen": 100.1,  # Above max (100)
                "pressure": 5.2,
                "agitator_speed": 250,
            }
        ]
        
        result = validator.validate_sensor_readings(readings)
        
        assert result.success is False
        assert result.valid_count == 0
        assert result.invalid_count == 1
        assert len(result.errors) == 1
        assert result.errors[0].field_name == "dissolved_oxygen"
    
    def test_validate_pressure_below_min(self, validator):
        """Test validation rejects pressure below minimum."""
        readings = [
            {
                "temperature": 25.5,
                "ph": 7.2,
                "dissolved_oxygen": 75.0,
                "pressure": -0.1,  # Below min (0)
                "agitator_speed": 250,
            }
        ]
        
        result = validator.validate_sensor_readings(readings)
        
        assert result.success is False
        assert result.valid_count == 0
        assert result.invalid_count == 1
        assert len(result.errors) == 1
        assert result.errors[0].field_name == "pressure"
    
    def test_validate_pressure_above_max(self, validator):
        """Test validation rejects pressure above maximum."""
        readings = [
            {
                "temperature": 25.5,
                "ph": 7.2,
                "dissolved_oxygen": 75.0,
                "pressure": 10.1,  # Above max (10)
                "agitator_speed": 250,
            }
        ]
        
        result = validator.validate_sensor_readings(readings)
        
        assert result.success is False
        assert result.valid_count == 0
        assert result.invalid_count == 1
        assert len(result.errors) == 1
        assert result.errors[0].field_name == "pressure"
    
    def test_validate_agitator_speed_below_min(self, validator):
        """Test validation rejects agitator speed below minimum."""
        readings = [
            {
                "temperature": 25.5,
                "ph": 7.2,
                "dissolved_oxygen": 75.0,
                "pressure": 5.2,
                "agitator_speed": -0.1,  # Below min (0)
            }
        ]
        
        result = validator.validate_sensor_readings(readings)
        
        assert result.success is False
        assert result.valid_count == 0
        assert result.invalid_count == 1
        assert len(result.errors) == 1
        assert result.errors[0].field_name == "agitator_speed"
    
    def test_validate_agitator_speed_above_max(self, validator):
        """Test validation rejects agitator speed above maximum."""
        readings = [
            {
                "temperature": 25.5,
                "ph": 7.2,
                "dissolved_oxygen": 75.0,
                "pressure": 5.2,
                "agitator_speed": 500.1,  # Above max (500)
            }
        ]
        
        result = validator.validate_sensor_readings(readings)
        
        assert result.success is False
        assert result.valid_count == 0
        assert result.invalid_count == 1
        assert len(result.errors) == 1
        assert result.errors[0].field_name == "agitator_speed"
    
    # ==================== Missing Values Tests ====================
    
    def test_validate_missing_temperature(self, validator):
        """Test validation rejects missing temperature."""
        readings = [
            {
                # temperature missing
                "ph": 7.2,
                "dissolved_oxygen": 75.0,
                "pressure": 5.2,
                "agitator_speed": 250,
            }
        ]
        
        result = validator.validate_sensor_readings(readings)
        
        assert result.success is False
        assert result.valid_count == 0
        assert result.invalid_count == 1
        assert len(result.errors) == 1
        assert result.errors[0].field_name == "temperature"
        assert result.errors[0].error_type == "MISSING_VALUE"
    
    def test_validate_missing_ph(self, validator):
        """Test validation rejects missing pH."""
        readings = [
            {
                "temperature": 25.5,
                # ph missing
                "dissolved_oxygen": 75.0,
                "pressure": 5.2,
                "agitator_speed": 250,
            }
        ]
        
        result = validator.validate_sensor_readings(readings)
        
        assert result.success is False
        assert result.valid_count == 0
        assert result.invalid_count == 1
        assert len(result.errors) == 1
        assert result.errors[0].field_name == "ph"
        assert result.errors[0].error_type == "MISSING_VALUE"
    
    def test_validate_missing_dissolved_oxygen(self, validator):
        """Test validation rejects missing dissolved oxygen."""
        readings = [
            {
                "temperature": 25.5,
                "ph": 7.2,
                # dissolved_oxygen missing
                "pressure": 5.2,
                "agitator_speed": 250,
            }
        ]
        
        result = validator.validate_sensor_readings(readings)
        
        assert result.success is False
        assert result.valid_count == 0
        assert result.invalid_count == 1
        assert len(result.errors) == 1
        assert result.errors[0].field_name == "dissolved_oxygen"
    
    def test_validate_missing_pressure(self, validator):
        """Test validation rejects missing pressure."""
        readings = [
            {
                "temperature": 25.5,
                "ph": 7.2,
                "dissolved_oxygen": 75.0,
                # pressure missing
                "agitator_speed": 250,
            }
        ]
        
        result = validator.validate_sensor_readings(readings)
        
        assert result.success is False
        assert result.valid_count == 0
        assert result.invalid_count == 1
        assert len(result.errors) == 1
        assert result.errors[0].field_name == "pressure"
    
    def test_validate_missing_agitator_speed(self, validator):
        """Test validation rejects missing agitator speed."""
        readings = [
            {
                "temperature": 25.5,
                "ph": 7.2,
                "dissolved_oxygen": 75.0,
                "pressure": 5.2,
                # agitator_speed missing
            }
        ]
        
        result = validator.validate_sensor_readings(readings)
        
        assert result.success is False
        assert result.valid_count == 0
        assert result.invalid_count == 1
        assert len(result.errors) == 1
        assert result.errors[0].field_name == "agitator_speed"
    
    # ==================== Invalid Type Tests ====================
    
    def test_validate_temperature_invalid_type(self, validator):
        """Test validation rejects non-numeric temperature."""
        readings = [
            {
                "temperature": "invalid",  # String instead of float
                "ph": 7.2,
                "dissolved_oxygen": 75.0,
                "pressure": 5.2,
                "agitator_speed": 250,
            }
        ]
        
        result = validator.validate_sensor_readings(readings)
        
        assert result.success is False
        assert result.valid_count == 0
        assert result.invalid_count == 1
        assert len(result.errors) == 1
        assert result.errors[0].field_name == "temperature"
        assert result.errors[0].error_type == "INVALID_TYPE"
    
    def test_validate_ph_invalid_type(self, validator):
        """Test validation rejects non-numeric pH."""
        readings = [
            {
                "temperature": 25.5,
                "ph": "invalid",  # String instead of float
                "dissolved_oxygen": 75.0,
                "pressure": 5.2,
                "agitator_speed": 250,
            }
        ]
        
        result = validator.validate_sensor_readings(readings)
        
        assert result.success is False
        assert result.valid_count == 0
        assert result.invalid_count == 1
        assert len(result.errors) == 1
        assert result.errors[0].field_name == "ph"
        assert result.errors[0].error_type == "INVALID_TYPE"
    
    # ==================== Multiple Errors Tests ====================
    
    def test_validate_multiple_errors_in_single_reading(self, validator):
        """Test validation reports multiple errors in a single reading."""
        readings = [
            {
                "temperature": 50.0,  # Out of range
                "ph": 10.0,  # Out of range
                "dissolved_oxygen": 150.0,  # Out of range
                "pressure": 15.0,  # Out of range
                "agitator_speed": 600.0,  # Out of range
            }
        ]
        
        result = validator.validate_sensor_readings(readings)
        
        assert result.success is False
        assert result.valid_count == 0
        assert result.invalid_count == 1
        assert len(result.errors) == 5  # All 5 fields have errors
    
    def test_validate_multiple_errors_in_multiple_readings(self, validator):
        """Test validation reports errors across multiple readings."""
        readings = [
            {
                "temperature": 50.0,  # Out of range
                "ph": 7.2,
                "dissolved_oxygen": 75.0,
                "pressure": 5.2,
                "agitator_speed": 250,
            },
            {
                "temperature": 25.5,
                "ph": 10.0,  # Out of range
                "dissolved_oxygen": 75.0,
                "pressure": 5.2,
                "agitator_speed": 250,
            },
            {
                "temperature": 25.5,
                "ph": 7.2,
                "dissolved_oxygen": 75.0,
                "pressure": 5.2,
                "agitator_speed": 250,
            },  # Valid
        ]
        
        result = validator.validate_sensor_readings(readings)
        
        assert result.success is False
        assert result.valid_count == 1
        assert result.invalid_count == 2
        assert len(result.errors) == 2
    
    # ==================== Empty and Edge Cases ====================
    
    def test_validate_empty_readings_list(self, validator):
        """Test validation handles empty readings list."""
        readings = []
        
        result = validator.validate_sensor_readings(readings)
        
        assert result.success is False
        assert result.valid_count == 0
        assert result.invalid_count == 0
        assert result.total_readings == 0
    
    def test_validate_reading_with_extra_fields(self, validator):
        """Test validation ignores extra fields in reading."""
        readings = [
            {
                "temperature": 25.5,
                "ph": 7.2,
                "dissolved_oxygen": 75.0,
                "pressure": 5.2,
                "agitator_speed": 250,
                "extra_field": "should be ignored",
            }
        ]
        
        result = validator.validate_sensor_readings(readings)
        
        assert result.success is True
        assert result.valid_count == 1
        assert result.invalid_count == 0
    
    # ==================== Error Details Tests ====================
    
    def test_error_contains_reading_index(self, validator):
        """Test error contains correct reading index."""
        readings = [
            {
                "temperature": 25.5,
                "ph": 7.2,
                "dissolved_oxygen": 75.0,
                "pressure": 5.2,
                "agitator_speed": 250,
            },
            {
                "temperature": 50.0,  # Out of range
                "ph": 7.2,
                "dissolved_oxygen": 75.0,
                "pressure": 5.2,
                "agitator_speed": 250,
            },
        ]
        
        result = validator.validate_sensor_readings(readings)
        
        assert len(result.errors) == 1
        assert result.errors[0].reading_index == 1
    
    def test_error_to_dict_format(self, validator):
        """Test error can be converted to dictionary."""
        readings = [
            {
                "temperature": 50.0,  # Out of range
                "ph": 7.2,
                "dissolved_oxygen": 75.0,
                "pressure": 5.2,
                "agitator_speed": 250,
            }
        ]
        
        result = validator.validate_sensor_readings(readings)
        
        assert len(result.errors) == 1
        error_dict = result.errors[0].to_dict()
        
        assert "reading_index" in error_dict
        assert "field" in error_dict
        assert "value" in error_dict
        assert "message" in error_dict
        assert "error_type" in error_dict
    
    # ==================== Pydantic Validation Tests ====================
    
    def test_validate_with_pydantic_valid(self, validator):
        """Test Pydantic validation with valid readings."""
        readings = [
            {
                "temperature": 25.5,
                "ph": 7.2,
                "dissolved_oxygen": 75.0,
                "pressure": 5.2,
                "agitator_speed": 250,
            }
        ]
        
        result = validator.validate_with_pydantic(readings)
        
        assert result.success is True
        assert result.valid_count == 1
        assert result.invalid_count == 0
    
    def test_validate_with_pydantic_invalid(self, validator):
        """Test Pydantic validation with invalid readings."""
        readings = [
            {
                "temperature": 50.0,  # Out of range
                "ph": 7.2,
                "dissolved_oxygen": 75.0,
                "pressure": 5.2,
                "agitator_speed": 250,
            }
        ]
        
        result = validator.validate_with_pydantic(readings)
        
        assert result.success is False
        assert result.valid_count == 0
        assert result.invalid_count == 1
        assert len(result.errors) >= 1


# ==================== Convenience Function Tests ====================

class TestValidateSensorReadingsFunction:
    """Test suite for convenience function."""
    
    def test_validate_sensor_readings_valid(self):
        """Test convenience function with valid readings."""
        readings = [
            {
                "temperature": 25.5,
                "ph": 7.2,
                "dissolved_oxygen": 75.0,
                "pressure": 5.2,
                "agitator_speed": 250,
            }
        ]
        
        result = validate_sensor_readings(readings)
        
        assert result.success is True
        assert result.valid_count == 1
    
    def test_validate_sensor_readings_invalid(self):
        """Test convenience function with invalid readings."""
        readings = [
            {
                "temperature": 50.0,  # Out of range
                "ph": 7.2,
                "dissolved_oxygen": 75.0,
                "pressure": 5.2,
                "agitator_speed": 250,
            }
        ]
        
        result = validate_sensor_readings(readings)
        
        assert result.success is False
        assert result.invalid_count == 1


# ==================== Integration Tests ====================

class TestDataValidatorIntegration:
    """Integration tests for data validator."""
    
    def test_validate_realistic_batch_data(self):
        """Test validation with realistic batch data."""
        readings = [
            {
                "temperature": 25.5,
                "ph": 7.2,
                "dissolved_oxygen": 75.0,
                "pressure": 5.2,
                "agitator_speed": 250,
            },
            {
                "temperature": 26.0,
                "ph": 7.1,
                "dissolved_oxygen": 76.0,
                "pressure": 5.3,
                "agitator_speed": 255,
            },
            {
                "temperature": 25.8,
                "ph": 7.3,
                "dissolved_oxygen": 74.5,
                "pressure": 5.1,
                "agitator_speed": 248,
            },
        ]
        
        validator = SensorDataValidator()
        result = validator.validate_sensor_readings(readings)
        
        assert result.success is True
        assert result.valid_count == 3
        assert result.invalid_count == 0
    
    def test_validate_mixed_valid_invalid_batch(self):
        """Test validation with mix of valid and invalid readings."""
        readings = [
            {
                "temperature": 25.5,
                "ph": 7.2,
                "dissolved_oxygen": 75.0,
                "pressure": 5.2,
                "agitator_speed": 250,
            },
            {
                "temperature": 50.0,  # Invalid
                "ph": 7.1,
                "dissolved_oxygen": 76.0,
                "pressure": 5.3,
                "agitator_speed": 255,
            },
            {
                "temperature": 25.8,
                "ph": 7.3,
                "dissolved_oxygen": 74.5,
                "pressure": 5.1,
                "agitator_speed": 248,
            },
        ]
        
        validator = SensorDataValidator()
        result = validator.validate_sensor_readings(readings)
        
        assert result.success is False
        assert result.valid_count == 2
        assert result.invalid_count == 1
        assert len(result.errors) == 1
