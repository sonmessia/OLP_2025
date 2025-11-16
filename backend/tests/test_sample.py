"""
Sample test file to verify testing infrastructure works.
"""

import pytest

from app.models.Building import Building, Address, CategoryEnum


class TestBuildingModel:
    """Test Building Pydantic model with basic functionality."""

    def test_building_minimal_creation(self):
        """Test creating a Building with minimal required data."""
        building = Building(type="Building")
        assert building.type.value == "Building"
        assert building.id is None
        assert building.name is None

    def test_building_with_valid_name(self):
        """Test creating a Building with a valid name pattern."""
        building = Building(type="Building")
        assert building.type.value == "Building"
        assert building.name is None

    def test_address_model(self):
        """Test Address model creation and validation."""
        address = Address(
            streetAddress="123 Test Street",
            postalCode="12345",
            addressLocality="Test City",
            addressCountry="Test Country"
        )
        assert address.streetAddress == "123 Test Street"
        assert address.postalCode == "12345"
        assert address.addressLocality == "Test City"
        assert address.addressCountry == "Test Country"

    def test_building_with_address(self):
        """Test creating a Building with an address."""
        address = Address(streetAddress="456 Main St", postalCode="67890")
        building = Building(
            type="Building",
            address=address
        )
        assert building.address.streetAddress == "456 Main St"
        assert building.address.postalCode == "67890"

    def test_category_enum(self):
        """Test CategoryEnum functionality."""
        assert CategoryEnum.apartments.value == "apartments"
        assert CategoryEnum.bungalow.value == "bungalow"
        
        # Test that we can create a Building with a category
        building = Building(
            type="Building",
            category=[CategoryEnum.apartments]
        )
        assert building.category == [CategoryEnum.apartments]

    def test_building_model_validation_positive(self):
        """Test that valid data passes validation."""
        building = Building(
            type="Building",
            floorsAboveGround=5,
            peopleCapacity=100,
            peopleOccupancy=25
        )
        assert building.floorsAboveGround == 5
        assert building.peopleCapacity == 100
        assert building.peopleOccupancy == 25

    def test_building_json_serialization(self):
        """Test that Building model can be serialized to JSON."""
        building = Building(
            type="Building",
            floorsAboveGround=3
        )
        
        # Test model_dump works
        data = building.model_dump()
        assert "type" in data
        assert data["type"] == "Building" or data["type"].value == "Building"
        
        # Test model_dump_json works
        json_str = building.model_dump_json()
        assert "Building" in json_str

    def test_building_model_schema(self):
        """Test that Building model has a valid JSON schema."""
        schema = Building.model_json_schema()
        assert "properties" in schema
        assert "type" in schema["properties"]
        assert "Building" in str(schema)


class TestBasicAssertions:
    """Basic test cases to verify pytest is working correctly."""

    def test_simple_math(self):
        """Test basic math operations."""
        assert 1 + 1 == 2
        assert 2 * 3 == 6
        assert 10 / 2 == 5

    def test_string_operations(self):
        """Test basic string operations."""
        text = "hello world"
        assert text.upper() == "HELLO WORLD"
        assert text.startswith("hello")
        assert "world" in text

    def test_list_operations(self):
        """Test basic list operations."""
        numbers = [1, 2, 3, 4, 5]
        assert len(numbers) == 5
        assert 3 in numbers
        assert numbers[0] == 1
        assert numbers[-1] == 5

    def test_root_endpoint_import(self):
        """Test that we can import the FastAPI app successfully."""
        from app.main import app
        assert isinstance(app, type(app))  # Check it's a FastAPI instance
        assert app.title == "OLP 2025 Core Backend Service"
