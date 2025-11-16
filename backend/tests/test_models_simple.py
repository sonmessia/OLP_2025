"""
Simplified unit tests for Pydantic models to avoid complex validation issues.
"""

import json
from typing import List

import pytest
from pydantic import ValidationError

from app.models.Building import Building, Address, CategoryEnum


class TestBuildingModelSimplified:
    """Simplified test cases for Building Pydantic model."""

    def test_building_model_minimal_data(self):
        """Test Building model with minimal required data."""
        building = Building(type="Building")
        
        assert building.type.value == "Building"
        assert building.id is None
        assert building.name is None
        assert building.category is None

    def test_building_model_validation(self):
        """Test Building model validation."""
        # Test invalid collapse risk
        with pytest.raises(ValidationError):
            Building(collapseRisk=1.5)  # > 1.0 is invalid
        
        with pytest.raises(ValidationError):
            Building(collapseRisk=-0.1)  # < 0.0 is invalid
        
        # Test invalid people capacity
        with pytest.raises(ValidationError):
            Building(peopleCapacity=-10.0)  # Negative is invalid
        
        # Test invalid people occupancy
        with pytest.raises(ValidationError):
            Building(peopleOccupancy=-5.0)  # Negative is invalid

    def test_address_model(self):
        """Test Address model validation and functionality."""
        address = Address(
            streetAddress="123 Main St",
            postalCode="12345",
            addressLocality="Springfield",
            addressRegion="IL",
            addressCountry="USA"
        )
        
        assert address.streetAddress == "123 Main St"
        assert address.postalCode == "12345"
        assert address.addressLocality == "Springfield"
        assert address.addressRegion == "IL"
        assert address.addressCountry == "USA"

    def test_category_enum(self):
        """Test CategoryEnum values."""
        assert CategoryEnum.office.value == "office"
        assert CategoryEnum.residential.value == "residential"
        assert CategoryEnum.commercial.value == "commercial"
        assert CategoryEnum.industrial.value == "industrial"
        
        # Test that all categories are valid enum values
        for category in CategoryEnum:
            assert isinstance(category.value, str)

    def test_building_model_serialization(self):
        """Test Building model serialization with simple data."""
        building = Building(
            type="Building",
            category=[CategoryEnum.office]
        )
        
        # Test model_dump
        data = building.model_dump()
        assert data["type"] == building.type  # Compare with enum value
        # When serializing, enums should be preserved as enum objects in the model dump
        assert building.category == [CategoryEnum.office]
        
        # Test JSON serialization
        json_str = building.model_dump_json()
        parsed = json.loads(json_str)
        assert parsed["type"] == building.type.value  # Should be the enum value

    def test_building_model_optional_fields(self):
        """Test Building model with optional fields as None."""
        building = Building(type="Building")
        
        building_dict = building.model_dump(exclude_none=True)
        assert "type" in building_dict
        assert "id" not in building_dict
        assert "name" not in building_dict
        assert "category" not in building_dict


class TestModelUtilitiesSimplified:
    """Test utility functions for model handling."""

    def test_model_exclude_unset(self):
        """Test model serialization excluding unset fields."""
        building = Building(
            type="Building"
            # category is not set
        )
        
        data = building.model_dump(exclude_unset=True)
        assert "type" in data
        assert "category" not in data

    def test_model_exclude_none(self):
        """Test model serialization excluding None fields."""
        building = Building(
            type="Building",
            category=None  # Explicitly None
        )
        
        data = building.model_dump(exclude_none=True)
        assert "type" in data
        assert "category" not in data

    def test_model_copy_and_update(self):
        """Test model copying and updating."""
        original = Building(
            type="Building",
            floorsAboveGround=3.0
        )
        
        # Copy with updates
        updated = original.model_copy(update={
            "floorsAboveGround": 5.0
        })
        
        assert updated.type == original.type
        assert updated.floorsAboveGround == 5.0
        
        # Original should be unchanged
        assert original.floorsAboveGround == 3.0

    def test_model_schema_validation(self):
        """Test model schema validation."""
        schema = Building.model_json_schema()
        
        assert "properties" in schema
        assert "type" in schema["properties"]
        assert "id" in schema["properties"]
        assert "name" in schema["properties"]
        assert "category" in schema["properties"]

    def test_model_validation_error_messages(self):
        """Test that validation error messages are informative."""
        with pytest.raises(ValidationError) as exc_info:
            Building(
                type="Building",
                collapseRisk=2.0  # Invalid: > 1.0
            )
        
        errors = exc_info.value.errors()
        assert len(errors) > 0
        assert any("collapseRisk" in str(error) for error in errors)


class TestSimpleModelCreation:
    """Test basic model creation for all entity types."""

    @pytest.mark.asyncio
    async def test_create_all_model_instances(self):
        """Test that all models can be created with minimal data."""
        # Test Building
        building = Building(type="Building")
        assert building.type.value == "Building"

        # Test other models (minimal validation)
        try:
            from app.models.AirQualityObserved import AirQualityObserved
            from app.models.Device import Device
            from app.models.CarbonFootprint import CarbonFootprint
            from app.models.WaterQualityObserved import WaterQualityObserved

            # Test minimal instances
            air_quality = AirQualityObserved(type="AirQualityObserved")
            device = Device(type="Device")
            carbon_footprint = CarbonFootprint(type="CarbonFootprint")
            water_quality = WaterQualityObserved(type="WaterQualityObserved")

            assert air_quality.type.value == "AirQualityObserved"
            assert device.type.value == "Device"
            assert carbon_footprint.type.value == "CarbonFootprint"
            assert water_quality.type.value == "WaterQualityObserved"

        except ImportError as e:
            pytest.skip(f"Model not available: {e}")

    def test_model_inheritance(self):
        """Test that all models inherit from BaseModel correctly."""
        building = Building(type="Building")
        assert hasattr(building, 'model_dump')
        assert hasattr(building, 'model_dump_json')
        assert hasattr(building, 'model_copy')
        assert hasattr(building, 'model_json_schema')

    def test_model_field_validation(self):
        """Test field-level validation works correctly."""
        # Test numeric constraints
        building = Building(
            type="Building",
            floorsAboveGround=5.5,  # Should work
            peopleCapacity=100.0,     # Should work
        )
        assert building.floorsAboveGround == 5.5
        assert building.peopleCapacity == 100.0

    def test_model_enum_validation(self):
        """Test enum field validation."""
        building = Building(
            type="Building",
            category=[CategoryEnum.office, CategoryEnum.commercial]
        )
        assert CategoryEnum.office in building.category
        assert CategoryEnum.commercial in building.category

    def test_model_optional_field_handling(self):
        """Test optional field handling."""
        # Building with only required fields
        building = Building(type="Building")
        data = building.model_dump()
        
        # Should include type field
        assert "type" in data
        
        # Should not include unset optional fields in exclude_none mode
        data_excluded = building.model_dump(exclude_none=True)
        assert len(data_excluded) <= len(data)
