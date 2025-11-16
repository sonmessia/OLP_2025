"""
Integration tests for Building Router.
"""

import json
from unittest.mock import AsyncMock, patch

import pytest
from httpx import AsyncClient

from app.main import app


class TestBuildingRouterIntegration:
    """Integration tests for Building API endpoints."""

    @pytest.mark.asyncio
    async def test_get_all_buildings_success(self, client, mock_orion_response):
        """Test GET /api/v1/buildings endpoint successfully."""
        with patch('app.services.building_service.building_service') as mock_service:
            mock_service.get_all.return_value = mock_orion_response

            response = await client.get("/api/v1/buildings/")

            assert response.status_code == 200
            data = response.json()
            assert data == mock_orion_response
            mock_service.get_all.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_all_buildings_with_query_params(self, client, mock_orion_response):
        """Test GET /api/v1/buildings with query parameters."""
        with patch('app.services.building_service.building_service') as mock_service:
            mock_service.get_all.return_value = mock_orion_response

            response = await client.get(
                "/api/v1/buildings/?type=Building&q=floorsAboveGround>5&limit=10"
            )

            assert response.status_code == 200
            mock_service.get_all.assert_called_once_with(
                type="Building",
                q="floorsAboveGround>5",
                limit=10,
                attrs=None,
                pick=None,
                georel=None,
                geometry=None,
                coordinates=None,
                geoproperty=None,
                offset=None,
                count=False,
                format=None,
                options=None,
                local=None
            )

    @pytest.mark.asyncio
    async def test_get_all_buildings_with_geo_params(self, client, mock_orion_response):
        """Test GET /api/v1/buildings with geo-spatial parameters."""
        with patch('app.services.building_service.building_service') as mock_service:
            mock_service.get_all.return_value = mock_orion_response

            response = await client.get(
                "/api/v1/buildings/?georel=near;maxDistance==1000&geometry=Point&coordinates=[-8.5,41.2]"
            )

            assert response.status_code == 200
            mock_service.get_all.assert_called_once()
            call_args = mock_service.get_all.call_args[1]
            assert call_args["georel"] == "near;maxDistance==1000"
            assert call_args["geometry"] == "Point"
            assert call_args["coordinates"] == "[-8.5,41.2]"

    @pytest.mark.asyncio
    async def test_get_all_buildings_count_only(self, client):
        """Test GET /api/v1/buildings with count=true."""
        with patch('app.services.building_service.building_service') as mock_service:
            mock_service.get_all.return_value = 42

            response = await client.get("/api/v1/buildings/?count=true")

            assert response.status_code == 200
            assert response.json() == 42
            mock_service.get_all.assert_called_once_with(count=True)

    @pytest.mark.asyncio
    async def test_get_all_buildings_invalid_query(self, client):
        """Test GET /api/v1/buildings with invalid query parameters."""
        with patch('app.services.building_service.building_service') as mock_service:
            from fastapi import HTTPException
            mock_service.get_all.side_effect = ValueError("Query is too broad")

            response = await client.get("/api/v1/buildings/")

            assert response.status_code == 400
            error_data = response.json()
            assert error_data["error"] == "Invalid query parameters"
            assert "Query is too broad" in error_data["message"]

    @pytest.mark.asyncio
    async def test_get_building_by_id_success(self, client, mock_orion_response):
        """Test GET /api/v1/buildings/{id} endpoint successfully."""
        with patch('app.services.building_service.building_service') as mock_service:
            mock_service.get_by_id.return_value = mock_orion_response

            response = await client.get("/api/v1/buildings/urn:ngsi-ld:Building:test001")

            assert response.status_code == 200
            data = response.json()
            assert data == mock_orion_response
            mock_service.get_by_id.assert_called_once_with(
                "urn:ngsi-ld:Building:test001",
                pick=None,
                attrs=None,
                format=None,
                options=None
            )

    @pytest.mark.asyncio
    async def test_get_building_by_id_not_found(self, client):
        """Test GET /api/v1/buildings/{id} when building not found."""
        with patch('app.services.building_service.building_service') as mock_service:
            import httpx
            mock_service.get_by_id.side_effect = httpx.HTTPStatusError(
                "404 Not Found",
                request=AsyncMock(),
                response=AsyncMock(status_code=404)
            )

            response = await client.get("/api/v1/buildings/urn:ngsi-ld:Building:nonexistent")

            assert response.status_code == 404
            error_data = response.json()
            assert error_data["error"] == "Building not found"

    @pytest.mark.asyncio
    async def test_create_building_success(self, client, sample_building_data):
        """Test POST /api/v1/buildings endpoint successfully."""
        with patch('app.services.building_service.building_service') as mock_service:
            mock_response = AsyncMock()
            mock_response.headers = {"Location": "/entities/urn:ngsi-ld:Building:test001"}
            mock_service.create.return_value = mock_response

            response = await client.post(
                "/api/v1/buildings/",
                json=sample_building_data
            )

            assert response.status_code == 201
            data = response.json()
            assert data["message"] == "Building created successfully"
            assert data["id"] == "urn:ngsi-ld:Building:test001"
            mock_service.create.assert_called_once_with(sample_building_data)

    @pytest.mark.asyncio
    async def test_create_building_conflict(self, client, sample_building_data):
        """Test POST /api/v1/buildings when building already exists."""
        with patch('app.services.building_service.building_service') as mock_service:
            import httpx
            mock_service.create.side_effect = httpx.HTTPStatusError(
                "409 Conflict",
                request=AsyncMock(),
                response=AsyncMock(status_code=409)
            )

            response = await client.post(
                "/api/v1/buildings/",
                json=sample_building_data
            )

            assert response.status_code == 409
            error_data = response.json()
            assert error_data["error"] == "Building already exists"

    @pytest.mark.asyncio
    async def test_create_building_invalid_data(self, client):
        """Test POST /api/v1/buildings with invalid data."""
        invalid_data = {
            "id": "urn:ngsi-ld:Building:test001",
            "type": "Building",
            "floorsAboveGround": "invalid_number"  # Should be a number
        }

        response = await client.post(
            "/api/v1/buildings/",
            json=invalid_data
        )

        # FastAPI should validate this before reaching the service
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_update_building_attributes_success(self, client):
        """Test PATCH /api/v1/buildings/{id}/attrs endpoint successfully."""
        with patch('app.services.building_service.building_service') as mock_service:
            mock_service.update_attrs.return_value = None

            update_data = {
                "name": {
                    "type": "Property",
                    "value": "Updated Building Name"
                },
                "category": {
                    "type": "Property",
                    "value": ["residential"]
                }
            }

            response = await client.patch(
                "/api/v1/buildings/urn:ngsi-ld:Building:test001/attrs",
                json=update_data
            )

            assert response.status_code == 204
            mock_service.update_attrs.assert_called_once()
            call_args = mock_service.update_attrs.call_args
            assert call_args[0][0] == "urn:ngsi-ld:Building:test001"
            assert "name" in call_args[0][1]
            assert "category" in call_args[0][1]

    @pytest.mark.asyncio
    async def test_update_building_attributes_invalid_structure(self, client):
        """Test PATCH /api/v1/buildings/{id}/attrs with invalid attribute structure."""
        invalid_data = {
            "name": {
                "type": "Property",
                # Missing 'value' field for Property type
            }
        }

        response = await client.patch(
            "/api/v1/buildings/urn:ngsi-ld:Building:test001/attrs",
            json=invalid_data
        )

        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_replace_building_success(self, client, sample_building_data):
        """Test PUT /api/v1/buildings/{id} endpoint successfully."""
        with patch('app.services.building_service.building_service') as mock_service:
            mock_service.replace.return_value = None

            response = await client.put(
                "/api/v1/buildings/urn:ngsi-ld:Building:test001",
                json=sample_building_data
            )

            assert response.status_code == 204
            mock_service.replace.assert_called_once_with(
                "urn:ngsi-ld:Building:test001",
                sample_building_data
            )

    @pytest.mark.asyncio
    async def test_delete_building_success(self, client):
        """Test DELETE /api/v1/buildings/{id} endpoint successfully."""
        with patch('app.services.building_service.building_service') as mock_service:
            mock_service.delete.return_value = None

            response = await client.delete("/api/v1/buildings/urn:ngsi-ld:Building:test001")

            assert response.status_code == 204
            mock_service.delete.assert_called_once_with("urn:ngsi-ld:Building:test001")

    @pytest.mark.asyncio
    async def test_delete_building_attribute_success(self, client):
        """Test DELETE /api/v1/buildings/{id}/attrs/{attribute_name} endpoint successfully."""
        with patch('app.services.building_service.building_service') as mock_service:
            mock_service.delete_attribute.return_value = None

            response = await client.delete(
                "/api/v1/buildings/urn:ngsi-ld:Building:test001/attrs/name"
            )

            assert response.status_code == 204
            mock_service.delete_attribute.assert_called_once_with(
                "urn:ngsi-ld:Building:test001",
                "name"
            )

    @pytest.mark.asyncio
    async def test_batch_create_buildings_success(self, client):
        """Test POST /api/v1/buildings/batch/create endpoint successfully."""
        with patch('app.services.building_service.building_service') as mock_service:
            mock_response = AsyncMock()
            mock_response.json.return_value = {"success": True, "created": 2}
            mock_service.batch_create.return_value = mock_response

            batch_data = {
                "entities": [
                    {"id": "urn:ngsi-ld:Building:test001", "type": "Building"},
                    {"id": "urn:ngsi-ld:Building:test002", "type": "Building"}
                ]
            }

            response = await client.post(
                "/api/v1/buildings/batch/create",
                json=batch_data
            )

            assert response.status_code == 201
            data = response.json()
            assert data["success"] is True
            mock_service.batch_create.assert_called_once_with(batch_data["entities"])

    @pytest.mark.asyncio
    async def test_batch_upsert_buildings_success(self, client):
        """Test POST /api/v1/buildings/batch/upsert endpoint successfully."""
        with patch('app.services.building_service.building_service') as mock_service:
            mock_response = AsyncMock()
            mock_response.json.return_value = {"success": True, "updated": 1}
            mock_service.batch_upsert.return_value = mock_response

            batch_data = {
                "entities": [
                    {"id": "urn:ngsi-ld:Building:test001", "type": "Building"}
                ]
            }

            response = await client.post(
                "/api/v1/buildings/batch/upsert?options=replace",
                json=batch_data
            )

            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
            mock_service.batch_upsert.assert_called_once_with(
                batch_data["entities"], 
                options="replace"
            )

    @pytest.mark.asyncio
    async def test_batch_delete_buildings_success(self, client):
        """Test POST /api/v1/buildings/batch/delete endpoint successfully."""
        with patch('app.services.building_service.building_service') as mock_service:
            mock_service.batch_delete.return_value = None

            delete_data = {
                "entity_ids": [
                    "urn:ngsi-ld:Building:test001",
                    "urn:ngsi-ld:Building:test002"
                ]
            }

            response = await client.post(
                "/api/v1/buildings/batch/delete",
                json=delete_data
            )

            assert response.status_code == 204
            mock_service.batch_delete.assert_called_once_with(delete_data["entity_ids"])

    @pytest.mark.asyncio
    async def test_find_nearby_buildings_success(self, client, mock_orion_response):
        """Test GET /api/v1/buildings/location/nearby endpoint successfully."""
        with patch('app.services.building_service.building_service') as mock_service:
            mock_service.find_by_location.return_value = mock_orion_response

            response = await client.get(
                "/api/v1/buildings/location/nearby?lon=-8.5&lat=41.2&max_distance=1000&limit=5"
            )

            assert response.status_code == 200
            data = response.json()
            assert data == mock_orion_response
            mock_service.find_by_location.assert_called_once_with(
                coordinates="[-8.5,41.2]",
                max_distance=1000,
                limit=5,
                format="simplified",
                pick=None
            )

    @pytest.mark.asyncio
    async def test_find_nearby_buildings_invalid_coordinates(self, client):
        """Test GET /api/v1/buildings/location/nearby with invalid coordinates."""
        response = await client.get(
            "/api/v1/buildings/location/nearby?lon=181&lat=91"  # Invalid coordinates
        )

        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_get_buildings_by_category_success(self, client, mock_orion_response):
        """Test GET /api/v1/buildings/category/{category} endpoint successfully."""
        with patch('app.services.building_service.building_service') as mock_service:
            mock_service.find_by_category.return_value = mock_orion_response

            response = await client.get("/api/v1/buildings/category/office?limit=10")

            assert response.status_code == 200
            data = response.json()
            assert data == mock_orion_response
            mock_service.find_by_category.assert_called_once_with(
                category="office",
                limit=10,
                format="simplified"
            )

    @pytest.mark.asyncio
    async def test_get_tall_buildings_success(self, client, mock_orion_response):
        """Test GET /api/v1/buildings/tall endpoint successfully."""
        with patch('app.services.building_service.building_service') as mock_service:
            mock_service.find_tall_buildings.return_value = mock_orion_response

            response = await client.get("/api/v1/buildings/tall?min_floors=10&limit=20")

            assert response.status_code == 200
            data = response.json()
            assert data == mock_orion_response
            mock_service.find_tall_buildings.assert_called_once_with(
                min_floors=10,
                limit=20,
                format="simplified"
            )

    @pytest.mark.asyncio
    async def test_service_unavailable_error(self, client):
        """Test handling of service unavailable errors."""
        with patch('app.services.building_service.building_service') as mock_service:
            import httpx
            mock_service.get_all.side_effect = httpx.RequestError("Connection failed")

            response = await client.get("/api/v1/buildings/")

            assert response.status_code == 503
            error_data = response.json()
            assert error_data["error"] == "Service Unavailable"
