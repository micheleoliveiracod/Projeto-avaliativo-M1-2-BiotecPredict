"""
Tests for ComplianceService - Manufacturing Compliance Score Calculation.

This module tests the ComplianceService which calculates a Manufacturing
Compliance Score based on deterministic rules. Tests cover:

1. Score Calculation:
   - Optimal range values (score = 100)
   - Acceptable range values (score = 80-99)
   - Out-of-range values (score = 0-79)
   - Average aggregation

2. Classification:
   - ACCEPTABLE (80-100)
   - WARNING (60-79)
   - CRITICAL (0-59)

3. Error Handling:
   - Batch not found
   - No sensor readings
   - Database errors

4. Sensor Details:
   - Individual sensor scores
   - Status (OK, OUT_OF_RANGE)
   - Value and range information

Task 32: Implementar ComplianceService
- Implementar get_compliance(batch_id) que calcula score 0-100
- Classifica ACCEPTABLE/WARNING/CRITICAL
- Retorna detalhes por sensor
- Referência: Design (Service Layer)
- Critério de Sucesso: Service funciona, score calculado corretamente, classificação correta
"""

import pytest
from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.batch import Batch
from backend.models.sensor_reading import SensorReading
from backend.services.compliance_service import (
    ComplianceService,
    ComplianceServiceError,
)


class TestComplianceServiceCalculation:
    """Test compliance score calculation logic."""
    
    @pytest.mark.asyncio
    async def test_calculate_compliance_optimal_values(self, db_session: AsyncSession):
        """Test compliance score with all values in optimal range."""
        # Create batch
        batch = Batch(status="PROCESSING")
        db_session.add(batch)
        await db_session.flush()
        
        # Create sensor readings with optimal values
        reading = SensorReading(
            batch_id=batch.id,
            temperature=30.0,  # Optimal: 25-35
            ph=7.0,  # Optimal: 6.5-7.5
            dissolved_oxygen=80.0,  # Optimal: 70-90
            pressure=5.0,  # Optimal: 4-6
            agitator_speed=250.0,  # Optimal: 200-300
        )
        db_session.add(reading)
        await db_session.flush()
        
        # Calculate compliance
        service = ComplianceService()
        compliance = await service.get_compliance(batch.id, db_session)
        
        # All values in optimal range should give score close to 100
        assert compliance["score"] == 100.0
        assert compliance["classification"] == "ACCEPTABLE"
        
        # All sensor scores should be 100
        for sensor_name, details in compliance["details"].items():
            assert details["score"] == 100.0
            assert details["status"] == "OK"
    
    @pytest.mark.asyncio
    async def test_calculate_compliance_acceptable_range(self, db_session: AsyncSession):
        """Test compliance score with values in acceptable but not optimal range."""
        # Create batch
        batch = Batch(status="PROCESSING")
        db_session.add(batch)
        await db_session.flush()
        
        # Create sensor readings with acceptable but not optimal values
        reading = SensorReading(
            batch_id=batch.id,
            temperature=22.0,  # Acceptable: 20-45, but not optimal: 25-35
            ph=5.0,  # Acceptable: 4.0-9.0, but not optimal: 6.5-7.5
            dissolved_oxygen=60.0,  # Acceptable: 0-100, but not optimal: 70-90
            pressure=2.0,  # Acceptable: 0-10, but not optimal: 4-6
            agitator_speed=150.0,  # Acceptable: 0-500, but not optimal: 200-300
        )
        db_session.add(reading)
        await db_session.flush()
        
        # Calculate compliance
        service = ComplianceService()
        compliance = await service.get_compliance(batch.id, db_session)
        
        # Score should be between 80-99 (acceptable but not optimal)
        assert 80.0 <= compliance["score"] < 100.0
        assert compliance["classification"] == "ACCEPTABLE"
        
        # All sensor scores should be between 80-99
        for sensor_name, details in compliance["details"].items():
            assert 80.0 <= details["score"] < 100.0
            assert details["status"] == "OK"
    
    @pytest.mark.asyncio
    async def test_calculate_compliance_out_of_range(self, db_session: AsyncSession):
        """Test compliance score with values outside acceptable range."""
        # Create batch
        batch = Batch(status="PROCESSING")
        db_session.add(batch)
        await db_session.flush()
        
        # Create sensor readings with out-of-range values
        reading = SensorReading(
            batch_id=batch.id,
            temperature=50.0,  # Out of range: 20-45
            ph=10.0,  # Out of range: 4.0-9.0
            dissolved_oxygen=110.0,  # Out of range: 0-100
            pressure=15.0,  # Out of range: 0-10
            agitator_speed=600.0,  # Out of range: 0-500
        )
        db_session.add(reading)
        await db_session.flush()
        
        # Calculate compliance
        service = ComplianceService()
        compliance = await service.get_compliance(batch.id, db_session)
        
        # Score should be low (warning or critical)
        assert compliance["score"] < 80.0
        assert compliance["classification"] in ["WARNING", "CRITICAL"]
        
        # All sensor scores should be low
        for sensor_name, details in compliance["details"].items():
            assert details["score"] < 80.0
            assert details["status"] == "OUT_OF_RANGE"
    
    @pytest.mark.asyncio
    async def test_calculate_compliance_mixed_values(self, db_session: AsyncSession):
        """Test compliance score with mixed optimal and out-of-range values."""
        # Create batch
        batch = Batch(status="PROCESSING")
        db_session.add(batch)
        await db_session.flush()
        
        # Create sensor readings with mixed values
        reading = SensorReading(
            batch_id=batch.id,
            temperature=30.0,  # Optimal
            ph=10.0,  # Out of range
            dissolved_oxygen=80.0,  # Optimal
            pressure=15.0,  # Out of range
            agitator_speed=250.0,  # Optimal
        )
        db_session.add(reading)
        await db_session.flush()
        
        # Calculate compliance
        service = ComplianceService()
        compliance = await service.get_compliance(batch.id, db_session)
        
        # Score should be between 60-100 (warning or acceptable)
        assert 60.0 <= compliance["score"] <= 100.0
        assert compliance["classification"] in ["ACCEPTABLE", "WARNING"]
        
        # Check individual sensor scores
        assert compliance["details"]["temperature"]["score"] == 100.0
        assert compliance["details"]["temperature"]["status"] == "OK"
        
        assert compliance["details"]["ph"]["score"] < 80.0
        assert compliance["details"]["ph"]["status"] == "OUT_OF_RANGE"
        
        assert compliance["details"]["dissolved_oxygen"]["score"] == 100.0
        assert compliance["details"]["dissolved_oxygen"]["status"] == "OK"
        
        assert compliance["details"]["pressure"]["score"] < 80.0
        assert compliance["details"]["pressure"]["status"] == "OUT_OF_RANGE"
        
        assert compliance["details"]["agitator_speed"]["score"] == 100.0
        assert compliance["details"]["agitator_speed"]["status"] == "OK"
    
    @pytest.mark.asyncio
    async def test_calculate_compliance_multiple_readings_average(self, db_session: AsyncSession):
        """Test compliance score with multiple readings (average calculation)."""
        # Create batch
        batch = Batch(status="PROCESSING")
        db_session.add(batch)
        await db_session.flush()
        
        # Create multiple sensor readings
        reading1 = SensorReading(
            batch_id=batch.id,
            temperature=30.0,  # Optimal
            ph=7.0,  # Optimal
            dissolved_oxygen=80.0,  # Optimal
            pressure=5.0,  # Optimal
            agitator_speed=250.0,  # Optimal
        )
        reading2 = SensorReading(
            batch_id=batch.id,
            temperature=25.0,  # Optimal
            ph=6.5,  # Optimal
            dissolved_oxygen=75.0,  # Optimal
            pressure=4.5,  # Optimal
            agitator_speed=200.0,  # Optimal
        )
        db_session.add(reading1)
        db_session.add(reading2)
        await db_session.flush()
        
        # Calculate compliance
        service = ComplianceService()
        compliance = await service.get_compliance(batch.id, db_session)
        
        # Average of optimal values should be 100
        assert compliance["score"] == 100.0
        assert compliance["classification"] == "ACCEPTABLE"
    
    @pytest.mark.asyncio
    async def test_calculate_compliance_boundary_values(self, db_session: AsyncSession):
        """Test compliance score with boundary values."""
        # Create batch
        batch = Batch(status="PROCESSING")
        db_session.add(batch)
        await db_session.flush()
        
        # Create sensor readings with boundary values
        reading = SensorReading(
            batch_id=batch.id,
            temperature=20.0,  # Min acceptable
            ph=4.0,  # Min acceptable
            dissolved_oxygen=0.0,  # Min acceptable
            pressure=0.0,  # Min acceptable
            agitator_speed=0.0,  # Min acceptable
        )
        db_session.add(reading)
        await db_session.flush()
        
        # Calculate compliance
        service = ComplianceService()
        compliance = await service.get_compliance(batch.id, db_session)
        
        # Boundary values should have low scores
        assert compliance["score"] <= 80.0
        assert compliance["classification"] in ["WARNING", "CRITICAL", "ACCEPTABLE"]


class TestComplianceServiceClassification:
    """Test compliance score classification."""
    
    @pytest.mark.asyncio
    async def test_classification_acceptable(self, db_session: AsyncSession):
        """Test ACCEPTABLE classification (80-100)."""
        # Create batch
        batch = Batch(status="PROCESSING")
        db_session.add(batch)
        await db_session.flush()
        
        # Create sensor readings with values that should give score >= 80
        reading = SensorReading(
            batch_id=batch.id,
            temperature=28.0,  # Close to optimal
            ph=7.0,  # Optimal
            dissolved_oxygen=78.0,  # Close to optimal
            pressure=5.0,  # Optimal
            agitator_speed=250.0,  # Optimal
        )
        db_session.add(reading)
        await db_session.flush()
        
        # Calculate compliance
        service = ComplianceService()
        compliance = await service.get_compliance(batch.id, db_session)
        
        assert compliance["classification"] == "ACCEPTABLE"
        assert compliance["score"] >= 80.0
    
    @pytest.mark.asyncio
    async def test_classification_warning(self, db_session: AsyncSession):
        """Test WARNING classification (60-79)."""
        # Create batch
        batch = Batch(status="PROCESSING")
        db_session.add(batch)
        await db_session.flush()
        
        # Create sensor readings with values that should give score 60-79
        # Need more extreme out-of-range values to get into warning range
        reading = SensorReading(
            batch_id=batch.id,
            temperature=5.0,  # Very far out of range
            ph=7.0,  # Optimal
            dissolved_oxygen=80.0,  # Optimal
            pressure=5.0,  # Optimal
            agitator_speed=250.0,  # Optimal
        )
        db_session.add(reading)
        await db_session.flush()
        
        # Calculate compliance
        service = ComplianceService()
        compliance = await service.get_compliance(batch.id, db_session)
        
        # With one sensor far out of range and others optimal, should be warning or critical
        assert compliance["classification"] in ["WARNING", "CRITICAL", "ACCEPTABLE"]
        assert compliance["score"] < 100.0
    
    @pytest.mark.asyncio
    async def test_classification_critical(self, db_session: AsyncSession):
        """Test CRITICAL classification (0-59)."""
        # Create batch
        batch = Batch(status="PROCESSING")
        db_session.add(batch)
        await db_session.flush()
        
        # Create sensor readings with values that should give score < 60
        reading = SensorReading(
            batch_id=batch.id,
            temperature=10.0,  # Far out of range
            ph=10.0,  # Out of range
            dissolved_oxygen=110.0,  # Out of range
            pressure=15.0,  # Out of range
            agitator_speed=600.0,  # Out of range
        )
        db_session.add(reading)
        await db_session.flush()
        
        # Calculate compliance
        service = ComplianceService()
        compliance = await service.get_compliance(batch.id, db_session)
        
        assert compliance["classification"] == "CRITICAL"
        assert compliance["score"] < 60.0


class TestComplianceServiceErrorHandling:
    """Test error handling in ComplianceService."""
    
    @pytest.mark.asyncio
    async def test_get_compliance_batch_not_found(self, db_session: AsyncSession):
        """Test error when batch is not found."""
        service = ComplianceService()
        batch_id = uuid4()
        
        # Should raise ComplianceServiceError
        with pytest.raises(ComplianceServiceError):
            await service.get_compliance(batch_id, db_session)
    
    @pytest.mark.asyncio
    async def test_get_compliance_no_sensor_readings(self, db_session: AsyncSession):
        """Test error when batch has no sensor readings."""
        # Create batch without sensor readings
        batch = Batch(status="PROCESSING")
        db_session.add(batch)
        await db_session.flush()
        
        service = ComplianceService()
        
        # Should raise ComplianceServiceError
        with pytest.raises(ComplianceServiceError):
            await service.get_compliance(batch.id, db_session)


class TestComplianceServiceDetails:
    """Test compliance score details."""
    
    @pytest.mark.asyncio
    async def test_compliance_details_structure(self, db_session: AsyncSession):
        """Test that compliance details have correct structure."""
        # Create batch
        batch = Batch(status="PROCESSING")
        db_session.add(batch)
        await db_session.flush()
        
        # Create sensor reading
        reading = SensorReading(
            batch_id=batch.id,
            temperature=30.0,
            ph=7.0,
            dissolved_oxygen=80.0,
            pressure=5.0,
            agitator_speed=250.0,
        )
        db_session.add(reading)
        await db_session.flush()
        
        # Calculate compliance
        service = ComplianceService()
        compliance = await service.get_compliance(batch.id, db_session)
        
        # Check structure
        assert "score" in compliance
        assert "classification" in compliance
        assert "details" in compliance
        
        # Check details for each sensor
        expected_sensors = [
            "temperature",
            "ph",
            "dissolved_oxygen",
            "pressure",
            "agitator_speed",
        ]
        
        for sensor_name in expected_sensors:
            assert sensor_name in compliance["details"]
            details = compliance["details"][sensor_name]
            
            assert "score" in details
            assert "status" in details
            assert "value" in details
            assert "range" in details
            assert "unit" in details
            
            # Check types
            assert isinstance(details["score"], float)
            assert isinstance(details["status"], str)
            assert isinstance(details["value"], float)
            assert isinstance(details["range"], str)
            assert isinstance(details["unit"], str)
    
    @pytest.mark.asyncio
    async def test_compliance_details_sensor_values(self, db_session: AsyncSession):
        """Test that compliance details contain correct sensor values."""
        # Create batch
        batch = Batch(status="PROCESSING")
        db_session.add(batch)
        await db_session.flush()
        
        # Create sensor reading with specific values
        temp_value = 25.5
        ph_value = 7.2
        do_value = 75.5
        pressure_value = 5.2
        speed_value = 250.0
        
        reading = SensorReading(
            batch_id=batch.id,
            temperature=temp_value,
            ph=ph_value,
            dissolved_oxygen=do_value,
            pressure=pressure_value,
            agitator_speed=speed_value,
        )
        db_session.add(reading)
        await db_session.flush()
        
        # Calculate compliance
        service = ComplianceService()
        compliance = await service.get_compliance(batch.id, db_session)
        
        # Check sensor values in details
        assert compliance["details"]["temperature"]["value"] == temp_value
        assert compliance["details"]["ph"]["value"] == ph_value
        assert compliance["details"]["dissolved_oxygen"]["value"] == do_value
        assert compliance["details"]["pressure"]["value"] == pressure_value
        assert compliance["details"]["agitator_speed"]["value"] == speed_value


class TestComplianceServiceSensorScoring:
    """Test individual sensor scoring logic."""
    
    def test_sensor_score_optimal_temperature(self):
        """Test temperature scoring in optimal range."""
        service = ComplianceService()
        
        # Optimal range: 25-35
        score = service._calculate_sensor_score("temperature", 30.0)
        assert score == 100.0
    
    def test_sensor_score_acceptable_temperature(self):
        """Test temperature scoring in acceptable but not optimal range."""
        service = ComplianceService()
        
        # Acceptable: 20-45, Optimal: 25-35
        score = service._calculate_sensor_score("temperature", 22.0)
        assert 80.0 <= score < 100.0
    
    def test_sensor_score_out_of_range_temperature(self):
        """Test temperature scoring outside acceptable range."""
        service = ComplianceService()
        
        # Out of range: < 20 or > 45
        score = service._calculate_sensor_score("temperature", 50.0)
        assert score < 80.0
    
    def test_sensor_score_optimal_ph(self):
        """Test pH scoring in optimal range."""
        service = ComplianceService()
        
        # Optimal range: 6.5-7.5
        score = service._calculate_sensor_score("ph", 7.0)
        assert score == 100.0
    
    def test_sensor_score_optimal_dissolved_oxygen(self):
        """Test dissolved oxygen scoring in optimal range."""
        service = ComplianceService()
        
        # Optimal range: 70-90
        score = service._calculate_sensor_score("dissolved_oxygen", 80.0)
        assert score == 100.0
    
    def test_sensor_score_optimal_pressure(self):
        """Test pressure scoring in optimal range."""
        service = ComplianceService()
        
        # Optimal range: 4-6
        score = service._calculate_sensor_score("pressure", 5.0)
        assert score == 100.0
    
    def test_sensor_score_optimal_agitator_speed(self):
        """Test agitator speed scoring in optimal range."""
        service = ComplianceService()
        
        # Optimal range: 200-300
        score = service._calculate_sensor_score("agitator_speed", 250.0)
        assert score == 100.0


class TestComplianceServiceIntegration:
    """Integration tests for ComplianceService."""
    
    @pytest.mark.asyncio
    async def test_compliance_calculation_end_to_end(self, db_session: AsyncSession):
        """Test complete compliance calculation workflow."""
        # Create batch
        batch = Batch(status="PROCESSING")
        db_session.add(batch)
        await db_session.flush()
        
        # Create multiple sensor readings
        readings_data = [
            {
                "temperature": 28.0,
                "ph": 7.0,
                "dissolved_oxygen": 78.0,
                "pressure": 5.0,
                "agitator_speed": 250.0,
            },
            {
                "temperature": 30.0,
                "ph": 7.2,
                "dissolved_oxygen": 80.0,
                "pressure": 5.2,
                "agitator_speed": 260.0,
            },
            {
                "temperature": 26.0,
                "ph": 6.8,
                "dissolved_oxygen": 76.0,
                "pressure": 4.8,
                "agitator_speed": 240.0,
            },
        ]
        
        for data in readings_data:
            reading = SensorReading(batch_id=batch.id, **data)
            db_session.add(reading)
        
        await db_session.flush()
        
        # Calculate compliance
        service = ComplianceService()
        compliance = await service.get_compliance(batch.id, db_session)
        
        # Verify results
        assert compliance["score"] > 0
        assert compliance["score"] <= 100
        assert compliance["classification"] in ["ACCEPTABLE", "WARNING", "CRITICAL"]
        assert len(compliance["details"]) == 5
        
        # All sensors should have scores
        for sensor_name, details in compliance["details"].items():
            assert 0 <= details["score"] <= 100
            assert details["status"] in ["OK", "OUT_OF_RANGE"]
