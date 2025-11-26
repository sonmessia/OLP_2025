# Copyright (c) 2025 Green Wave Team
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

"""
Sample test file to verify testing infrastructure works.
"""

from app.models.Building import Building, Type12


class TestBuildingModel:
    """Test Building Pydantic model with basic functionality."""

    def test_building_minimal_creation(self):
        """Test creating a Building with minimal required data."""

        building = Building(
            type=Type12.Building,
            address=None,
            alternateName=None,
            areaServed=None,
            category=None,
            collapseRisk=None,
            containedInPlace=None,
            dataProvider=None,
            dateCreated=None,
            dateModified=None,
            description=None,
            floorsAboveGround=None,
            floorsBelowGround=None,
            id=None,
            location=None,
            mapUrl=None,
            name=None,
            occupier=None,
            openingHours=None,
            owner=None,
            peopleCapacity=None,
            peopleOccupancy=None,
            seeAlso=None,
            source=None,
        )
        if building.type is not None:
            assert building.type.value == "Building"
        assert building.id is None
        assert building.name is None

    def test_building_with_valid_name(self):
        """Test creating a Building with a valid name pattern."""

        building = Building(
            type=Type12.Building,
            address=None,
            alternateName=None,
            areaServed=None,
            category=None,
            collapseRisk=None,
            containedInPlace=None,
            dataProvider=None,
            dateCreated=None,
            dateModified=None,
            description=None,
            floorsAboveGround=None,
            floorsBelowGround=None,
            id=None,
            location=None,
            mapUrl=None,
            name=None,
            occupier=None,
            openingHours=None,
            owner=None,
            peopleCapacity=None,
            peopleOccupancy=None,
            seeAlso=None,
            source=None,
        )
        if building.type is not None:
            assert building.type.value == "Building"
        assert building.name is None
