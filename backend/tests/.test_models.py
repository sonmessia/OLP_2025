"""
Unit tests for Pydantic models.
"""

import json
from datetime import datetime, timezone
from typing import List

import pytest
from pydantic import ValidationError

from app.models.AirQualityObserved import AirQualityObserved
from app.models.Building import Address, Building, CategoryEnum
from app.models.CarbonFootprint import CarbonFootprint
from app.models.Device import Device
from app.models.WaterQualityObserved import WaterQualityObserved


class TestBuildingModel:
    """Test cases for Building Pydantic model."""

    def test_building_model_minimal_data(self):
        """Test Building model with minimal required data."""
        building = Building(type="Building")

        assert building.type.value == "Building"
        assert building.id is None
        assert building.name is None
        assert building.category is None

    def test_building_model_complete_data(self):
        """Test Building model with complete data."""
        building = Building(
            id="urn-ngsi-ld-Building-test001",  # Fixed pattern to match regex
            type="Building",
            name="Test Building",  # Fixed pattern to match regex
            category=[CategoryEnum.office, CategoryEnum.commercial],
            description="A test building for unit testing",
            floorsAboveGround=5.0,
            floorsBelowGround=1.0,
            peopleCapacity=100.0,
            peopleOccupancy=25.5,
            collapseRisk=0.15,
            address=Address(
                streetAddress="123 Test Street",
                postalCode="12345",
                addressLocality="Test City",
                addressCountry="Test Country",
            ),
            location={"type": "Point", "coordinates": [-8.5, 41.2]},
            owner=["urn-ngsi-ld-Person-owner001"],  # Fixed pattern to match regex
            occupier=["urn-ngsi-ld-Person-occupier001"],  # Fixed pattern to match regex
            openingHours=["Mo-Fr 09:00-17:00"],
            dataProvider="Test Provider",
            source="http://example.com/source",
        )

        assert building.id == "urn:ngsi-ld:Building:test001"
        assert building.type.value == "Building"
        assert building.name == "Test Building"
        assert CategoryEnum.office in building.category
        assert CategoryEnum.commercial in building.category
        assert building.floorsAboveGround == 5.0
        assert building.floorsBelowGround == 1.0
        assert building.peopleCapacity == 100.0
        assert building.peopleOccupancy == 25.5
        assert building.collapseRisk == 0.15
        assert building.address.streetAddress == "123 Test Street"
        assert building.location["type"] == "Point"
        assert building.location["coordinates"] == [-8.5, 41.2]

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
            addressCountry="USA",
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
        """Test Building model serialization."""
        building = Building(
            id="urn-ngsi-ld-Building-test001",  # Fixed pattern
            type="Building",
            name="Test Building",  # Fixed pattern
            category=[CategoryEnum.office],
        )

        # Test model_dump
        data = building.model_dump()
        assert data["id"] == "urn-ngsi-ld-Building-test001"
        assert data["type"] == "Building"
        assert data["name"] == "Test Building"
        assert data["category"] == ["office"]

        # Test JSON serialization
        json_str = building.model_dump_json()
        parsed = json.loads(json_str)
        assert parsed["id"] == "urn-ngsi-ld-Building-test001"

    def test_building_model_deserialization(self):
        """Test Building model deserialization."""
        data = {
            "id": "urn-ngsi-ld-Building-test001",  # Fixed pattern
            "type": "Building",
            "name": "Test Building",  # Fixed pattern
            "category": ["office"],
            "floorsAboveGround": 5.0,
        }

        building = Building(**data)
        assert building.id == "urn-ngsi-ld-Building-test001"
        assert building.type.value == "Building"
        assert building.name == "Test Building"
        assert CategoryEnum.office in building.category
        assert building.floorsAboveGround == 5.0

    def test_building_model_optional_fields(self):
        """Test Building model with optional fields as None."""
        building = Building(type="Building")

        building_dict = building.model_dump(exclude_none=True)
        assert "type" in building_dict
        assert "id" not in building_dict
        assert "name" not in building_dict
        assert "category" not in building_dict


class TestAirQualityObservedModel:
    """Test cases for AirQualityObserved Pydantic model."""

    def test_air_quality_minimal_data(self):
        """Test AirQualityObserved model with minimal data."""
        air_quality = AirQualityObserved(type="AirQualityObserved")

        assert air_quality.type.value == "AirQualityObserved"
        assert air_quality.id is None

    def test_air_quality_complete_data(self):
        """Test AirQualityObserved model with complete data."""
        from app.models.AirQualityObserved import Location, Type

        air_quality = AirQualityObserved(
            id="urn-ngsi-ld-AirQualityObserved-test001",
            type="AirQualityObserved",
            temperature=25.5,
            humidity=65.0,
            airQualityIndex=85.0,
            location=Location(type=Type.Point, coordinates=[-8.5, 41.2]),
            dateObserved="2023-01-01T12:00:00Z",
        )

        assert air_quality.id == "urn:ngsi-ld:AirQualityObserved:test001"
        assert air_quality.type.value == "AirQualityObserved"
        assert air_quality.temperature == 25.5
        assert air_quality.humidity == 65.0
        assert air_quality.airQualityIndex == 85.0

    def test_air_quality_validation(self):
        """Test AirQualityObserved model validation."""
        # This would need to be implemented based on the actual model constraints
        # For now, just test basic instantiation
        air_quality = AirQualityObserved(type="AirQualityObserved")
        assert air_quality.type.value == "AirQualityObserved"


class TestDeviceModel:
    """Test cases for Device Pydantic model."""

    def test_device_minimal_data(self):
        """Test Device model with minimal data."""
        device = Device(type="Device")

        assert device.type.value == "Device"
        assert device.id is None

    def test_device_complete_data(self):
        """Test Device model with complete data."""
        from app.models.Device import Location, Type

        device = Device(
            id="urn-ngsi-ld-Device-test001",
            type="Device",
            name="Test Device",
            deviceState="ok",
            controlledAsset=["urn-ngsi-ld-Building-test001"],  # Should be list
            location=Location(type=Type.Point, coordinates=[-8.5, 41.2]),
        )

        assert device.id == "urn-ngsi-ld-Device-test001"
        assert device.type.value == "Device"
        assert device.name == "Test Device"
        assert device.deviceState == "ok"
        assert "urn-ngsi-ld-Building-test001" in device.controlledAsset


class TestCarbonFootprintModel:
    """Test cases for CarbonFootprint Pydantic model."""

    def test_carbon_footprint_minimal_data(self):
        """Test CarbonFootprint model with minimal data."""
        carbon_footprint = CarbonFootprint(type="CarbonFootprint")

        assert carbon_footprint.type.value == "CarbonFootprint"
        assert carbon_footprint.id is None

    def test_carbon_footprint_complete_data(self):
        """Test CarbonFootprint model with complete data."""
        carbon_footprint = CarbonFootprint(
            id="urn-ngsi-ld-CarbonFootprint-test001",
            type="CarbonFootprint",
            co2Emissions=1500.5,
            energyConsumption=2500.0,
            period="P1Y",
        )

        assert carbon_footprint.id == "urn-ngsi-ld-CarbonFootprint-test001"
        assert carbon_footprint.type.value == "CarbonFootprint"
        assert carbon_footprint.co2Emissions == 1500.5
        assert carbon_footprint.energyConsumption == 2500.0
        assert carbon_footprint.period == "P1Y"


class TestWaterQualityObservedModel:
    """Test cases for WaterQualityObserved Pydantic model."""

    def test_water_quality_minimal_data(self):
        """Test WaterQualityObserved model with minimal data."""
        water_quality = WaterQualityObserved(type="WaterQualityObserved")

        assert water_quality.type.value == "WaterQualityObserved"
        assert water_quality.id is None

    def test_water_quality_complete_data(self):
        """Test WaterQualityObserved model with complete data."""
        water_quality = WaterQualityObserved(
            id="urn-ngsi-ld-WaterQualityObserved-test001",
            type="WaterQualityObserved",
            ph=7.2,
            dissolvedOxygen=8.5,
            turbidity=2.3,
            dateObserved="2023-01-01T12:00:00Z",
        )

        assert water_quality.id == "urn-ngsi-ld-WaterQualityObserved-test001"
        assert water_quality.type.value == "WaterQualityObserved"
        assert water_quality.ph == 7.2
        assert water_quality.dissolvedOxygen == 8.5
        assert water_quality.turbidity == 2.3


class TestModelUtilities:
    """Test utility functions for model handling."""

    def test_model_json_serialization(self):
        """Test JSON serialization of models."""
        building = Building(
            id="urn:ngsi-ld:Building:test001",
            type="Building",
            name="Test Building",
            category=[CategoryEnum.office],
        )

        # Test that the model can be properly serialized to JSON
        json_str = building.model_dump_json()
        assert isinstance(json_str, str)

        # Test that it can be deserialized back
        parsed = json.loads(json_str)
        assert "type" in parsed
        assert parsed["type"] == "Building"

    def test_model_exclude_unset(self):
        """Test model serialization excluding unset fields."""
        building = Building(
            type="Building",
            name="Test Building",
            # category is not set
        )

        data = building.model_dump(exclude_unset=True)
        assert "name" in data
        assert "type" in data
        assert "category" not in data

    def test_model_exclude_none(self):
        """Test model serialization excluding None fields."""
        building = Building(
            type="Building", name="Test Building", category=None  # Explicitly None
        )

        data = building.model_dump(exclude_none=True)
        assert "name" in data
        assert "type" in data
        assert "category" not in data

    def test_model_copy_and_update(self):
        """Test model copying and updating."""
        original = Building(
            id="urn:ngsi-ld:Building:test001",
            type="Building",
            name="Original Name",
            floorsAboveGround=3.0,
        )

        # Copy with updates
        updated = original.model_copy(
            update={"name": "Updated Name", "floorsAboveGround": 5.0}
        )

        assert updated.id == original.id
        assert updated.name == "Updated Name"
        assert updated.floorsAboveGround == 5.0

        # Original should be unchanged
        assert original.name == "Original Name"
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
            Building(type="Building", collapseRisk=2.0)  # Invalid: > 1.0

        errors = exc_info.value.errors()
        assert len(errors) > 0
        assert any("collapseRisk" in str(error) for error in errors)
        assert any("greater than or equal to 1" in str(error) for error in errors)
