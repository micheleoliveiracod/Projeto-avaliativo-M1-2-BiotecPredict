"""
Tests for CSV Processor Module.

Task 18: Criar Processador CSV
- Testes para parse_csv() com dados válidos e inválidos
- Testes para validação de colunas obrigatórias
- Testes para validação de tipos de dados
- Testes para validação de ranges de sensores
- Testes para identificação de erros com linha/coluna

Test Coverage:
- Valid CSV parsing
- Missing columns
- Invalid data types
- Out of range values
- Empty files
- Missing values
- Column name variations
- Multiple errors
- Performance with large files
"""

import io
from uuid import UUID

import pytest

from backend.processors.csv_processor import (
    CSVError,
    CSVParseResult,
    CSVProcessor,
    parse_csv,
)


class TestCSVProcessor:
    """Test suite for CSVProcessor class."""
    
    @pytest.fixture
    def processor(self):
        """Create a CSV processor instance."""
        return CSVProcessor()
    
    # ==================== Valid CSV Tests ====================
    
    def test_parse_valid_csv_with_all_fields(self, processor):
        """Test parsing valid CSV with all required fields."""
        csv_content = (
            "temperature,ph,dissolved_oxygen,pressure,agitator_speed\n"
            "25.5,7.2,75.0,5.2,250\n"
            "26.0,7.1,76.0,5.1,255\n"
        )
        
        result = processor.parse_csv(csv_content)
        
        assert result.success is True
        assert result.valid_rows == 2
        assert result.invalid_rows == 0
        assert len(result.errors) == 0
        assert len(result.sensor_readings) == 2
        
        # Check first reading
        reading = result.sensor_readings[0]
        assert reading["temperature"] == 25.5
        assert reading["ph"] == 7.2
        assert reading["dissolved_oxygen"] == 75.0
        assert reading["pressure"] == 5.2
        assert reading["agitator_speed"] == 250
    
    def test_parse_valid_csv_single_row(self, processor):
        """Test parsing valid CSV with single data row."""
        csv_content = (
            "temperature,ph,dissolved_oxygen,pressure,agitator_speed\n"
            "25.5,7.2,75.0,5.2,250\n"
        )
        
        result = processor.parse_csv(csv_content)
        
        assert result.success is True
        assert result.valid_rows == 1
        assert len(result.sensor_readings) == 1
    
    def test_parse_valid_csv_with_bytes(self, processor):
        """Test parsing CSV from bytes."""
        csv_content = (
            "temperature,ph,dissolved_oxygen,pressure,agitator_speed\n"
            "25.5,7.2,75.0,5.2,250\n"
        ).encode("utf-8")
        
        result = processor.parse_csv(csv_content)
        
        assert result.success is True
        assert result.valid_rows == 1
    
    def test_parse_valid_csv_with_file_object(self, processor):
        """Test parsing CSV from file-like object."""
        csv_content = (
            "temperature,ph,dissolved_oxygen,pressure,agitator_speed\n"
            "25.5,7.2,75.0,5.2,250\n"
        )
        file_obj = io.StringIO(csv_content)
        
        result = processor.parse_csv(file_obj)
        
        assert result.success is True
        assert result.valid_rows == 1
    
    def test_parse_csv_with_column_aliases(self, processor):
        """Test parsing CSV with column name aliases."""
        csv_content = (
            "temp,ph,do,press,speed\n"
            "25.5,7.2,75.0,5.2,250\n"
        )
        
        result = processor.parse_csv(csv_content)
        
        assert result.success is True
        assert result.valid_rows == 1
    
    def test_parse_csv_with_mixed_case_columns(self, processor):
        """Test parsing CSV with mixed case column names."""
        csv_content = (
            "Temperature,PH,Dissolved_Oxygen,Pressure,Agitator_Speed\n"
            "25.5,7.2,75.0,5.2,250\n"
        )
        
        result = processor.parse_csv(csv_content)
        
        assert result.success is True
        assert result.valid_rows == 1
    
    def test_parse_csv_with_whitespace_in_values(self, processor):
        """Test parsing CSV with whitespace in values."""
        csv_content = (
            "temperature,ph,dissolved_oxygen,pressure,agitator_speed\n"
            " 25.5 , 7.2 , 75.0 , 5.2 , 250 \n"
        )
        
        result = processor.parse_csv(csv_content)
        
        assert result.success is True
        assert result.valid_rows == 1
    
    def test_parse_csv_boundary_values(self, processor):
        """Test parsing CSV with boundary values."""
        csv_content = (
            "temperature,ph,dissolved_oxygen,pressure,agitator_speed\n"
            "20.0,4.0,0.0,0.0,0.0\n"  # Minimum values
            "45.0,9.0,100.0,10.0,500.0\n"  # Maximum values
        )
        
        result = processor.parse_csv(csv_content)
        
        assert result.success is True
        assert result.valid_rows == 2
        assert result.errors == []
    
    def test_parse_csv_with_many_rows(self, processor):
        """Test parsing CSV with many rows."""
        rows = ["temperature,ph,dissolved_oxygen,pressure,agitator_speed"]
        for i in range(100):
            rows.append(f"25.{i%10},7.{i%5},75.{i%10},5.{i%5},250")
        
        csv_content = "\n".join(rows) + "\n"
        
        result = processor.parse_csv(csv_content)
        
        assert result.success is True
        assert result.valid_rows == 100
        assert len(result.sensor_readings) == 100
    
    # ==================== Missing Columns Tests ====================
    
    def test_parse_csv_missing_required_column(self, processor):
        """Test parsing CSV with missing required column."""
        csv_content = (
            "temperature,ph,dissolved_oxygen,pressure\n"  # Missing agitator_speed
            "25.5,7.2,75.0,5.2\n"
        )
        
        result = processor.parse_csv(csv_content)
        
        assert result.success is False
        assert result.valid_rows == 0
        assert len(result.errors) == 1
        assert result.errors[0].error_type == "MISSING_COLUMNS"
        assert "agitator_speed" in result.errors[0].message
    
    def test_parse_csv_missing_multiple_columns(self, processor):
        """Test parsing CSV with multiple missing columns."""
        csv_content = (
            "temperature,ph\n"  # Missing 3 columns
            "25.5,7.2\n"
        )
        
        result = processor.parse_csv(csv_content)
        
        assert result.success is False
        assert len(result.errors) == 1
        assert result.errors[0].error_type == "MISSING_COLUMNS"
    
    def test_parse_csv_no_header(self, processor):
        """Test parsing CSV with no header."""
        csv_content = "25.5,7.2,75.0,5.2,250\n"
        
        result = processor.parse_csv(csv_content)
        
        assert result.success is False
        assert len(result.errors) == 1
        # When no header is present, the first row is treated as header
        # and required columns are missing, so error_type is MISSING_COLUMNS
        assert result.errors[0].error_type == "MISSING_COLUMNS"
    
    # ==================== Invalid Data Type Tests ====================
    
    def test_parse_csv_invalid_temperature_type(self, processor):
        """Test parsing CSV with invalid temperature type."""
        csv_content = (
            "temperature,ph,dissolved_oxygen,pressure,agitator_speed\n"
            "invalid,7.2,75.0,5.2,250\n"
        )
        
        result = processor.parse_csv(csv_content)
        
        assert result.success is False
        assert result.valid_rows == 0
        assert result.invalid_rows == 1
        assert len(result.errors) == 1
        assert result.errors[0].column_name == "temperature"
        assert result.errors[0].error_type == "INVALID_TYPE"
        assert result.errors[0].line_number == 2
    
    def test_parse_csv_invalid_ph_type(self, processor):
        """Test parsing CSV with invalid pH type."""
        csv_content = (
            "temperature,ph,dissolved_oxygen,pressure,agitator_speed\n"
            "25.5,not_a_number,75.0,5.2,250\n"
        )
        
        result = processor.parse_csv(csv_content)
        
        assert result.success is False
        assert result.errors[0].column_name == "ph"
        assert result.errors[0].error_type == "INVALID_TYPE"
    
    def test_parse_csv_multiple_invalid_types(self, processor):
        """Test parsing CSV with multiple invalid types."""
        csv_content = (
            "temperature,ph,dissolved_oxygen,pressure,agitator_speed\n"
            "invalid,not_a_number,bad,wrong,nope\n"
        )
        
        result = processor.parse_csv(csv_content)
        
        assert result.success is False
        assert result.invalid_rows == 1
        assert len(result.errors) == 5  # One error per column
    
    # ==================== Out of Range Tests ====================
    
    def test_parse_csv_temperature_too_low(self, processor):
        """Test parsing CSV with temperature below minimum."""
        csv_content = (
            "temperature,ph,dissolved_oxygen,pressure,agitator_speed\n"
            "19.9,7.2,75.0,5.2,250\n"  # Below 20°C
        )
        
        result = processor.parse_csv(csv_content)
        
        assert result.success is False
        assert result.invalid_rows == 1
        assert len(result.errors) == 1
        assert result.errors[0].column_name == "temperature"
        assert result.errors[0].error_type == "VALIDATION_ERROR"
    
    def test_parse_csv_temperature_too_high(self, processor):
        """Test parsing CSV with temperature above maximum."""
        csv_content = (
            "temperature,ph,dissolved_oxygen,pressure,agitator_speed\n"
            "45.1,7.2,75.0,5.2,250\n"  # Above 45°C
        )
        
        result = processor.parse_csv(csv_content)
        
        assert result.success is False
        assert result.errors[0].column_name == "temperature"
    
    def test_parse_csv_ph_too_low(self, processor):
        """Test parsing CSV with pH below minimum."""
        csv_content = (
            "temperature,ph,dissolved_oxygen,pressure,agitator_speed\n"
            "25.5,3.9,75.0,5.2,250\n"  # Below 4.0
        )
        
        result = processor.parse_csv(csv_content)
        
        assert result.success is False
        assert result.errors[0].column_name == "ph"
    
    def test_parse_csv_ph_too_high(self, processor):
        """Test parsing CSV with pH above maximum."""
        csv_content = (
            "temperature,ph,dissolved_oxygen,pressure,agitator_speed\n"
            "25.5,9.1,75.0,5.2,250\n"  # Above 9.0
        )
        
        result = processor.parse_csv(csv_content)
        
        assert result.success is False
        assert result.errors[0].column_name == "ph"
    
    def test_parse_csv_dissolved_oxygen_too_low(self, processor):
        """Test parsing CSV with dissolved oxygen below minimum."""
        csv_content = (
            "temperature,ph,dissolved_oxygen,pressure,agitator_speed\n"
            "25.5,7.2,-0.1,5.2,250\n"  # Below 0%
        )
        
        result = processor.parse_csv(csv_content)
        
        assert result.success is False
        assert result.errors[0].column_name == "dissolved_oxygen"
    
    def test_parse_csv_dissolved_oxygen_too_high(self, processor):
        """Test parsing CSV with dissolved oxygen above maximum."""
        csv_content = (
            "temperature,ph,dissolved_oxygen,pressure,agitator_speed\n"
            "25.5,7.2,100.1,5.2,250\n"  # Above 100%
        )
        
        result = processor.parse_csv(csv_content)
        
        assert result.success is False
        assert result.errors[0].column_name == "dissolved_oxygen"
    
    def test_parse_csv_pressure_too_low(self, processor):
        """Test parsing CSV with pressure below minimum."""
        csv_content = (
            "temperature,ph,dissolved_oxygen,pressure,agitator_speed\n"
            "25.5,7.2,75.0,-0.1,250\n"  # Below 0 bar
        )
        
        result = processor.parse_csv(csv_content)
        
        assert result.success is False
        assert result.errors[0].column_name == "pressure"
    
    def test_parse_csv_pressure_too_high(self, processor):
        """Test parsing CSV with pressure above maximum."""
        csv_content = (
            "temperature,ph,dissolved_oxygen,pressure,agitator_speed\n"
            "25.5,7.2,75.0,10.1,250\n"  # Above 10 bar
        )
        
        result = processor.parse_csv(csv_content)
        
        assert result.success is False
        assert result.errors[0].column_name == "pressure"
    
    def test_parse_csv_agitator_speed_too_low(self, processor):
        """Test parsing CSV with agitator speed below minimum."""
        csv_content = (
            "temperature,ph,dissolved_oxygen,pressure,agitator_speed\n"
            "25.5,7.2,75.0,5.2,-1\n"  # Below 0 RPM
        )
        
        result = processor.parse_csv(csv_content)
        
        assert result.success is False
        assert result.errors[0].column_name == "agitator_speed"
    
    def test_parse_csv_agitator_speed_too_high(self, processor):
        """Test parsing CSV with agitator speed above maximum."""
        csv_content = (
            "temperature,ph,dissolved_oxygen,pressure,agitator_speed\n"
            "25.5,7.2,75.0,5.2,500.1\n"  # Above 500 RPM
        )
        
        result = processor.parse_csv(csv_content)
        
        assert result.success is False
        assert result.errors[0].column_name == "agitator_speed"
    
    def test_parse_csv_multiple_out_of_range(self, processor):
        """Test parsing CSV with multiple out of range values."""
        csv_content = (
            "temperature,ph,dissolved_oxygen,pressure,agitator_speed\n"
            "19.0,3.0,101.0,11.0,501.0\n"  # All out of range
        )
        
        result = processor.parse_csv(csv_content)
        
        assert result.success is False
        assert result.invalid_rows == 1
        assert len(result.errors) == 5  # One error per column
    
    # ==================== Missing Values Tests ====================
    
    def test_parse_csv_missing_temperature_value(self, processor):
        """Test parsing CSV with missing temperature value."""
        csv_content = (
            "temperature,ph,dissolved_oxygen,pressure,agitator_speed\n"
            ",7.2,75.0,5.2,250\n"
        )
        
        result = processor.parse_csv(csv_content)
        
        assert result.success is False
        assert result.errors[0].column_name == "temperature"
        assert result.errors[0].error_type == "MISSING_VALUE"
    
    def test_parse_csv_missing_multiple_values(self, processor):
        """Test parsing CSV with multiple missing values."""
        csv_content = (
            "temperature,ph,dissolved_oxygen,pressure,agitator_speed\n"
            ",,75.0,,250\n"
        )
        
        result = processor.parse_csv(csv_content)
        
        assert result.success is False
        assert result.invalid_rows == 1
        # All missing values are reported: temperature, ph, and pressure
        assert len(result.errors) == 3
    
    # ==================== Empty File Tests ====================
    
    def test_parse_empty_csv(self, processor):
        """Test parsing empty CSV file."""
        csv_content = ""
        
        result = processor.parse_csv(csv_content)
        
        assert result.success is False
        assert result.valid_rows == 0
        assert len(result.errors) == 1
        assert result.errors[0].error_type == "EMPTY_FILE"
    
    def test_parse_csv_only_whitespace(self, processor):
        """Test parsing CSV with only whitespace."""
        csv_content = "   \n  \n  "
        
        result = processor.parse_csv(csv_content)
        
        assert result.success is False
        assert result.errors[0].error_type == "EMPTY_FILE"
    
    # ==================== Mixed Valid and Invalid Rows ====================
    
    def test_parse_csv_mixed_valid_and_invalid_rows(self, processor):
        """Test parsing CSV with mix of valid and invalid rows."""
        csv_content = (
            "temperature,ph,dissolved_oxygen,pressure,agitator_speed\n"
            "25.5,7.2,75.0,5.2,250\n"  # Valid
            "invalid,7.2,75.0,5.2,250\n"  # Invalid type
            "26.0,7.1,76.0,5.1,255\n"  # Valid
            "45.1,7.2,75.0,5.2,250\n"  # Out of range
        )
        
        result = processor.parse_csv(csv_content)
        
        assert result.success is False
        assert result.valid_rows == 2
        assert result.invalid_rows == 2
        assert result.total_rows == 4
        assert len(result.errors) == 2
    
    # ==================== Error Details Tests ====================
    
    def test_csv_error_line_number(self, processor):
        """Test that CSV errors include correct line numbers."""
        csv_content = (
            "temperature,ph,dissolved_oxygen,pressure,agitator_speed\n"
            "25.5,7.2,75.0,5.2,250\n"  # Line 2
            "invalid,7.2,75.0,5.2,250\n"  # Line 3
        )
        
        result = processor.parse_csv(csv_content)
        
        assert result.errors[0].line_number == 3
    
    def test_csv_error_to_dict(self):
        """Test CSVError.to_dict() method."""
        error = CSVError(
            line_number=5,
            column_name="temperature",
            value="invalid",
            message="Invalid value",
            error_type="INVALID_TYPE",
        )
        
        error_dict = error.to_dict()
        
        assert error_dict["line"] == 5
        assert error_dict["column"] == "temperature"
        assert error_dict["value"] == "invalid"
        assert error_dict["message"] == "Invalid value"
        assert error_dict["error_type"] == "INVALID_TYPE"
    
    def test_csv_error_string_representation(self):
        """Test CSVError string representation."""
        error = CSVError(
            line_number=5,
            column_name="temperature",
            value="invalid",
            message="Invalid value",
        )
        
        error_str = str(error)
        
        assert "Line 5" in error_str
        assert "temperature" in error_str
        assert "invalid" in error_str
    
    # ==================== Parse Result Tests ====================
    
    def test_parse_result_success_string(self):
        """Test CSVParseResult string representation for success."""
        result = CSVParseResult(
            success=True,
            sensor_readings=[],
            errors=[],
            total_rows=10,
            valid_rows=10,
            invalid_rows=0,
        )
        
        result_str = str(result)
        
        assert "successful" in result_str
        assert "10 valid rows" in result_str
    
    def test_parse_result_failure_string(self):
        """Test CSVParseResult string representation for failure."""
        result = CSVParseResult(
            success=False,
            sensor_readings=[],
            errors=[CSVError(1, "col", "val", "msg")],
            total_rows=10,
            valid_rows=5,
            invalid_rows=5,
        )
        
        result_str = str(result)
        
        assert "failed" in result_str
        assert "1 errors" in result_str


class TestParseCSVFunction:
    """Test suite for parse_csv convenience function."""
    
    def test_parse_csv_function_with_string(self):
        """Test parse_csv function with string input."""
        csv_content = (
            "temperature,ph,dissolved_oxygen,pressure,agitator_speed\n"
            "25.5,7.2,75.0,5.2,250\n"
        )
        
        result = parse_csv(csv_content)
        
        assert result.success is True
        assert result.valid_rows == 1
    
    def test_parse_csv_function_with_bytes(self):
        """Test parse_csv function with bytes input."""
        csv_content = (
            "temperature,ph,dissolved_oxygen,pressure,agitator_speed\n"
            "25.5,7.2,75.0,5.2,250\n"
        ).encode("utf-8")
        
        result = parse_csv(csv_content)
        
        assert result.success is True
        assert result.valid_rows == 1
    
    def test_parse_csv_function_with_custom_delimiter(self):
        """Test parse_csv function with custom delimiter."""
        csv_content = (
            "temperature;ph;dissolved_oxygen;pressure;agitator_speed\n"
            "25.5;7.2;75.0;5.2;250\n"
        )
        
        result = parse_csv(csv_content, delimiter=";")
        
        assert result.success is True
        assert result.valid_rows == 1


class TestCSVProcessorEdgeCases:
    """Test edge cases and special scenarios."""
    
    @pytest.fixture
    def processor(self):
        """Create a CSV processor instance."""
        return CSVProcessor()
    
    def test_parse_csv_with_extra_columns(self, processor):
        """Test parsing CSV with extra columns."""
        csv_content = (
            "temperature,ph,dissolved_oxygen,pressure,agitator_speed,extra_column\n"
            "25.5,7.2,75.0,5.2,250,extra_value\n"
        )
        
        result = processor.parse_csv(csv_content)
        
        assert result.success is True
        assert result.valid_rows == 1
    
    def test_parse_csv_with_different_column_order(self, processor):
        """Test parsing CSV with different column order."""
        csv_content = (
            "agitator_speed,pressure,dissolved_oxygen,ph,temperature\n"
            "250,5.2,75.0,7.2,25.5\n"
        )
        
        result = processor.parse_csv(csv_content)
        
        assert result.success is True
        assert result.valid_rows == 1
        reading = result.sensor_readings[0]
        assert reading["temperature"] == 25.5
        assert reading["agitator_speed"] == 250
    
    def test_parse_csv_with_scientific_notation(self, processor):
        """Test parsing CSV with scientific notation."""
        csv_content = (
            "temperature,ph,dissolved_oxygen,pressure,agitator_speed\n"
            "2.55e1,7.2,7.5e1,5.2,2.5e2\n"  # 25.5, 75.0, 250
        )
        
        result = processor.parse_csv(csv_content)
        
        assert result.success is True
        assert result.valid_rows == 1
    
    def test_parse_csv_with_negative_zero(self, processor):
        """Test parsing CSV with negative zero."""
        csv_content = (
            "temperature,ph,dissolved_oxygen,pressure,agitator_speed\n"
            "25.5,7.2,-0.0,5.2,250\n"
        )
        
        result = processor.parse_csv(csv_content)
        
        assert result.success is True
        assert result.valid_rows == 1
    
    def test_parse_csv_with_very_large_numbers(self, processor):
        """Test parsing CSV with very large numbers."""
        csv_content = (
            "temperature,ph,dissolved_oxygen,pressure,agitator_speed\n"
            "25.5,7.2,75.0,5.2,999999\n"  # agitator_speed out of range
        )
        
        result = processor.parse_csv(csv_content)
        
        assert result.success is False
        assert result.errors[0].column_name == "agitator_speed"
    
    def test_parse_csv_with_very_small_numbers(self, processor):
        """Test parsing CSV with very small numbers."""
        csv_content = (
            "temperature,ph,dissolved_oxygen,pressure,agitator_speed\n"
            "25.5,7.2,0.0000001,5.2,250\n"
        )
        
        result = processor.parse_csv(csv_content)
        
        assert result.success is True
        assert result.valid_rows == 1
