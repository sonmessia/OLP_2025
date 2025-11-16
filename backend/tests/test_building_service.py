"""
Unit tests for BuildingService.
"""

import json
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
import httpx

from app.services.building_service import BuildingService


class TestBuildingService:
    """Test cases for BuildingService."""

    @pytest.fixture
    def service(self):
        """Create BuildingService instance for testing."""
        return BuildingService()

    @pytest.fixture
    def mock_orion_response(self):
        """Mock response from Orion-LD for buildings."""
        return [
            {
                "id": "urn:ngsi-ld:Building:test001",
                "type": "Building",
                "name": {"type": "Property", "value": "Test Building"},
                "category": {"type": "Property", "value": ["office"]},
                "floorsAboveGround": {"type": "Property", "value": 5.0}
            }
        ]

    @pytest.mark.asyncio
    async def test_get_all_with_type_filter(self, service, mock_orion_response):
        """Test getting all buildings with type filter."""
        service._client = AsyncMock()
        service._client.request.return_value.json.return_value = mock_orion_response

        result = await service.get_all(type="Building")

        assert result == mock_orion_response
        service._client.request.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_all_with_query_filter(self, service, mock_orion_response):
        """Test getting all buildings with query filter."""
        service._client = AsyncMock()
        service._client.request.return_value.json.return_value = mock_orion_response

        result = await service.get_all(q="floorsAboveGround>5")

        assert result == mock_orion_response
        call_args = service._client.request.call_args
        params = call_args[1]["params"]
        assert params["q"] == "floorsAboveGround>5"

    @pytest.mark.asyncio
    async def test_get_all_with_geo_query(self, service, mock_orion_response):
        """Test getting all buildings with geo query."""
        service._client = AsyncMock()
        service._client.request.return_value.json.return_value = mock_orion_response

        result = await service.get_all(
            georel="near;maxDistance==1000",
            geometry="Point",
            coordinates="[-8.5,41.2]"
        )

        assert result == mock_orion_response
        call_args = service._client.request.call_args
        params = call_args[1]["params"]
        assert params["georel"] == "near;maxDistance==1000"
        assert params["geometry"] == "Point"
        assert params["coordinates"] == "[-8.5,41.2]"

    @pytest.mark.asyncio
    async def test_get_all_with_pagination(self, service, mock_orion_response):
        """Test getting all buildings with pagination."""
        service._client = AsyncMock()
        service._client.request.return_value.json.return_value = mock_orion_response

        result = await service.get_all(limit=10, offset=20)

        assert result == mock_orion_response
        call_args = service._client.request.call_args
        params = call_args[1]["params"]
        assert params["limit"] == 10
        assert params["offset"] == 20

    @pytest.mark.asyncio
    async def test_get_all_with_count(self, service):
        """Test getting count of buildings."""
        service._client = AsyncMock()
        service._client.request.return_value.headers = {"NGSILD-Results-Count": "42"}

        result = await service.get_all(type="Building", count=True)

        assert result == 42
        call_args = service._client.request.call_args
        params = call_args[1]["params"]
        assert params["count"] is True

    @pytest.mark.asyncio
    async def test_get_all_with_attribute_selection(self, service, mock_orion_response):
        """Test getting all buildings with attribute selection."""
        service._client = AsyncMock()
        service._client.request.return_value.json.return_value = mock_orion_response

        result = await service.get_all(pick="id,type,name,category")

        assert result == mock_orion_response
        call_args = service._client.request.call_args
        params = call_args[1]["params"]
        assert params["pick"] == "id,type,name,category"

    @pytest.mark.asyncio
    async def test_get_by_id_success(self, service):
        """Test getting building by ID successfully."""
        building_data = {
            "id": "urn:ngsi-ld:Building:test001",
            "type": "Building",
            "name": {"type": "Property", "value": "Test Building"}
        }
        
        service._client = AsyncMock()
        service._client.request.return_value.json.return_value = building_data

        result = await service.get_by_id("urn:ngsi-ld:Building:test001")

        assert result == building_data
        service._client.request.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_by_id_with_options(self, service):
        """Test getting building by ID with options."""
        building_data = {
            "id": "urn:ngsi-ld:Building:test001",
            "type": "Building",
            "name": {"type": "Property", "value": "Test Building"}
        }
        
        service._client = AsyncMock()
        service._client.request.return_value.json.return_value = building_data

        result = await service.get_by_id(
            "urn:ngsi-ld:Building:test001",
            options="keyValues",
            format="simplified"
        )

        assert result == building_data
        call_args = service._client.request.call_args
        params = call_args[1]["params"]
        assert params["options"] == "keyValues"
        assert params["format"] == "simplified"

    @pytest.mark.asyncio
    async def test_create_success(self, service):
        """Test creating a building successfully."""
        building_data = {
            "id": "urn:ngsi-ld:Building:test001",
            "type": "Building",
            "name": "Test Building",
            "category": ["office"]
        }
        
        service._client = AsyncMock()
        service._client.request.return_value.status_code = 201

        response = await service.create(building_data)

        assert response.status_code == 201
        call_args = service._client.request.call_args
        json_payload = call_args[1]["json"]
        assert json_payload["id"] == "urn:ngsi-ld:Building:test001"
        assert "@context" in json_payload

    @pytest.mark.asyncio
    async def test_replace_success(self, service):
        """Test replacing a building successfully."""
        from app.models.Building import Building
        
        building = Building(
            id="urn:ngsi-ld:Building:test001",
            name="Updated Building",
            category=["office"]
        )
        
        service._client = AsyncMock()
        service._client.request.return_value.status_code = 204

        response = await service.replace("urn:ngsi-ld:Building:test001", building)

        assert response.status_code == 204
        service._client.request.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_attrs_success(self, service):
        """Test updating building attributes successfully."""
        update_data = {
            "name": {"type": "Property", "value": "Updated Name"},
            "category": {"type": "Property", "value": ["residential"]}
        }
        
        service._client = AsyncMock()
        service._client.request.return_value.status_code = 204

        response = await service.update_attrs("urn:ngsi-ld:Building:test001", update_data)

        assert response.status_code == 204
        call_args = service._client.request.call_args
        json_payload = call_args[1]["json"]
        assert "name" in json_payload
        assert "category" in json_payload

    @pytest.mark.asyncio
    async def test_delete_success(self, service):
        """Test deleting a building successfully."""
        service._client = AsyncMock()
        service._client.request.return_value.status_code = 204

        response = await service.delete("urn:ngsi-ld:Building:test001")

        assert response.status_code == 204
        service._client.request.assert_called_once()

    @pytest.mark.asyncio
    async def test_delete_attribute_success(self, service):
        """Test deleting building attribute successfully."""
        service._client = AsyncMock()
        service._client.request.return_value.status_code = 204

        response = await service.delete_attribute("urn:ngsi-ld:Building:test001", "name")

        assert response.status_code == 204
        service._client.request.assert_called_once()

    @pytest.mark.asyncio
    async def test_batch_create_success(self, service):
        """Test batch creating buildings successfully."""
        entities = [
            {"id": "urn:ngsi-ld:Building:test001", "type": "Building"},
            {"id": "urn:ngsi-ld:Building:test002", "type": "Building"}
        ]
        
        service._client = AsyncMock()
        service._client.request.return_value.status_code = 201

        response = await service.batch_create(entities)

        assert response.status_code == 201
        call_args = service._client.request.call_args
        json_payload = call_args[1]["json"]
        assert len(json_payload) == 2

    @pytest.mark.asyncio
    async def test_batch_upsert_success(self, service):
        """Test batch upserting buildings successfully."""
        entities = [
            {"id": "urn:ngsi-ld:Building:test001", "type": "Building"}
        ]
        
        service._client = AsyncMock()
        service._client.request.return_value.status_code = 204

        response = await service.batch_upsert(entities, options="replace")

        assert response.status_code == 204
        call_args = service._client.request.call_args
        assert call_args[1]["params"]["options"] == "replace"

    @pytest.mark.asyncio
    async def test_batch_delete_success(self, service):
        """Test batch deleting buildings successfully."""
        entity_ids = ["urn:ngsi-ld:Building:test001", "urn:ngsi-ld:Building:test002"]
        
        service._client = AsyncMock()
        service._client.request.return_value.status_code = 204

        response = await service.batch_delete(entity_ids)

        assert response.status_code == 204
        call_args = service._client.request.call_args
        json_payload = call_args[1]["json"]
        assert json_payload == entity_ids

    @pytest.mark.asyncio
    async def test_find_by_location_success(self, service):
        """Test finding buildings by location successfully."""
        buildings = [
            {
                "id": "urn:ngsi-ld:Building:test001",
                "type": "Building",
                "name": {"type": "Property", "value": "Nearby Building"}
            }
        ]
        
        service._client = AsyncMock()
        service._client.request.return_value.json.return_value = buildings

        result = await service.find_by_location(
            coordinates="[-8.5,41.2]",
            max_distance=1000,
            limit=10
        )

        assert result == buildings
        call_args = service._client.request.call_args
        params = call_args[1]["params"]
        assert params["georel"] == "near;maxDistance==1000"
        assert params["geometry"] == "Point"
        assert params["coordinates"] == "[-8.5,41.2]"
        assert params["limit"] == 10

    @pytest.mark.asyncio
    async def test_find_by_category_success(self, service):
        """Test finding buildings by category successfully."""
        buildings = [
            {
                "id": "urn:ngsi-ld:Building:test001",
                "type": "Building",
                "category": {"type": "Property", "value": ["office"]}
            }
        ]
        
        service._client = AsyncMock()
        service._client.request.return_value.json.return_value = buildings

        result = await service.find_by_category(category="office", limit=20)

        assert result == buildings
        call_args = service._client.request.call_args
        params = call_args[1]["params"]
        assert params["q"] == 'category=="office"'
        assert params["limit"] == 20

    @pytest.mark.asyncio
    async def test_find_tall_buildings_success(self, service):
        """Test finding tall buildings successfully."""
        buildings = [
            {
                "id": "urn:ngsi-ld:Building:test001",
                "type": "Building",
                "floorsAboveGround": {"type": "Property", "value": 15.0}
            }
        ]
        
        service._client = AsyncMock()
        service._client.request.return_value.json.return_value = buildings

        result = await service.find_tall_buildings(min_floors=10, limit=20)

        assert result == buildings
        call_args = service._client.request.call_args
        params = call_args[1]["params"]
        assert params["q"] == "floorsAboveGround>=10"
        assert params["limit"] == 20

    @pytest.mark.asyncio
    async def test_orion_error_handling(self, service):
        """Test handling of Orion-LD HTTP errors."""
        service._client = AsyncMock()
        service._client.request.side_effect = httpx.HTTPStatusError(
            "404 Not Found", 
            request=MagicMock(), 
            response=MagicMock(status_code=404, text="Entity not found")
        )

        with pytest.raises(httpx.HTTPStatusError):
            await service.get_by_id("urn:ngsi-ld:Building:nonexistent")

    @pytest.mark.asyncio
    async def test_connection_error_handling(self, service):
        """Test handling of connection errors."""
        service._client = AsyncMock()
        service._client.request.side_effect = httpx.RequestError("Connection failed")

        with pytest.raises(httpx.RequestError):
            await service.get_all()

    @pytest.mark.asyncio
    async def test_find_by_location_with_format_options(self, service):
        """Test find_by_location with format options."""
        service._client = AsyncMock()
        service._client.request.return_value.json.return_value = []

        await service.find_by_location(
            coordinates="[-8.5,41.2]",
            max_distance=1000,
            format="simplified",
            pick="id,type,name"
        )

        call_args = service._client.request.call_args
        params = call_args[1]["params"]
        assert params["format"] == "simplified"
        assert params["pick"] == "id,type,name"

    @pytest.mark.asyncio
    async def test_find_by_category_with_format_options(self, service):
        """Test find_by_category with format options."""
        service._client = AsyncMock()
        service._client.request.return_value.json.return_value = []

        await service.find_by_category(
            category="office",
            format="simplified"
        )

        call_args = service._client.request.call_args
        params = call_args[1]["params"]
        assert params["format"] == "simplified"

    @pytest.mark.asyncio
    async def test_find_tall_buildings_with_format_options(self, service):
        """Test find_tall_buildings with format options."""
        service._client = AsyncMock()
        service._client.request.return_value.json.return_value = []

        await service.find_tall_buildings(
            min_floors=10,
            format="simplified"
        )

        call_args = service._client.request.call_args
        params = call_args[1]["params"]
        assert params["format"] == "simplified"
