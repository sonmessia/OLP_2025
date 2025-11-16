"""
Unit tests for AirQualityService.
"""

import json
from unittest.mock import AsyncMock, MagicMock

import pytest
import httpx

from app.services.air_quality_service import AirQualityService


class TestAirQualityService:
    """Test cases for AirQualityService."""

    @pytest.fixture
    def service(self):
        """Create AirQualityService instance for testing."""
        return AirQualityService()

    @pytest.fixture
    def mock_air_quality_response(self):
        """Mock response from Orion-LD for air quality observations."""
        return [
            {
                "id": "urn:ngsi-ld:AirQualityObserved:test001",
                "type": "AirQualityObserved",
                "temperature": {"type": "Property", "value": 25.5, "unitCode": "CEL"},
                "humidity": {"type": "Property", "value": 65.0, "unitCode": "P1"},
                "airQualityIndex": {"type": "Property", "value": 85.0},
                "location": {
                    "type": "GeoProperty",
                    "value": {
                        "type": "Point",
                        "coordinates": [-8.5, 41.2]
                    }
                }
            }
        ]

    @pytest.mark.asyncio
    async def test_get_all_with_type_filter(self, service, mock_air_quality_response):
        """Test getting all air quality observations with type filter."""
        service._client = AsyncMock()
        service._client.request.return_value.json.return_value = mock_air_quality_response

        result = await service.get_all(type="AirQualityObserved")

        assert result == mock_air_quality_response
        service._client.request.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_all_with_quality_filter(self, service, mock_air_quality_response):
        """Test getting all air quality observations with quality filter."""
        service._client = AsyncMock()
        service._client.request.return_value.json.return_value = mock_air_quality_response

        result = await service.get_all(airQualityIndex=">80")

        assert result == mock_air_quality_response
        call_args = service._client.request.call_args
        params = call_args[1]["params"]
        assert params["q"] == "airQualityIndex>80"

    @pytest.mark.asyncio
    async def test_get_all_with_temperature_range(self, service, mock_air_quality_response):
        """Test getting all air quality observations with temperature range."""
        service._client = AsyncMock()
        service._client.request.return_value.json.return_value = mock_air_quality_response

        result = await service.get_all(temp_min=20.0, temp_max=30.0)

        assert result == mock_air_quality_response
        call_args = service._client.request.call_args
        params = call_args[1]["params"]
        assert "temperature>=20.0" in params["q"]
        assert "temperature<=30.0" in params["q"]

    @pytest.mark.asyncio
    async def test_get_all_with_geo_query(self, service, mock_air_quality_response):
        """Test getting all air quality observations with geo query."""
        service._client = AsyncMock()
        service._client.request.return_value.json.return_value = mock_air_quality_response

        result = await service.get_all(
            georel="near;maxDistance==1000",
            geometry="Point",
            coordinates="[-8.5,41.2]"
        )

        assert result == mock_air_quality_response
        call_args = service._client.request.call_args
        params = call_args[1]["params"]
        assert params["georel"] == "near;maxDistance==1000"
        assert params["geometry"] == "Point"

    @pytest.mark.asyncio
    async def test_get_by_id_success(self, service):
        """Test getting air quality observation by ID successfully."""
        air_quality_data = {
            "id": "urn:ngsi-ld:AirQualityObserved:test001",
            "type": "AirQualityObserved",
            "temperature": {"type": "Property", "value": 25.5, "unitCode": "CEL"}
        }
        
        service._client = AsyncMock()
        service._client.request.return_value.json.return_value = air_quality_data

        result = await service.get_by_id("urn:ngsi-ld:AirQualityObserved:test001")

        assert result == air_quality_data
        service._client.request.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_success(self, service):
        """Test creating an air quality observation successfully."""
        air_quality_data = {
            "id": "urn:ngsi-ld:AirQualityObserved:test001",
            "type": "AirQualityObserved",
            "temperature": {"type": "Property", "value": 25.5, "unitCode": "CEL"},
            "humidity": {"type": "Property", "value": 65.0, "unitCode": "P1"}
        }
        
        service._client = AsyncMock()
        service._client.request.return_value.status_code = 201

        response = await service.create(air_quality_data)

        assert response.status_code == 201
        call_args = service._client.request.call_args
        json_payload = call_args[1]["json"]
        assert json_payload["temperature"]["value"] == 25.5
        assert "@context" in json_payload

    @pytest.mark.asyncio
    async def test_replace_success(self, service):
        """Test replacing an air quality observation successfully."""
        from app.models.AirQualityObserved import AirQualityObserved
        
        air_quality = AirQualityObserved(
            id="urn:ngsi-ld:AirQualityObserved:test001",
            temperature=25.5,
            humidity=65.0
        )
        
        service._client = AsyncMock()
        service._client.request.return_value.status_code = 204

        response = await service.replace("urn:ngsi-ld:AirQualityObserved:test001", air_quality)

        assert response.status_code == 204
        service._client.request.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_attrs_success(self, service):
        """Test updating air quality observation attributes successfully."""
        update_data = {
            "temperature": {"type": "Property", "value": 26.0, "unitCode": "CEL"},
            "airQualityIndex": {"type": "Property", "value": 90.0}
        }
        
        service._client = AsyncMock()
        service._client.request.return_value.status_code = 204

        response = await service.update_attrs("urn:ngsi-ld:AirQualityObserved:test001", update_data)

        assert response.status_code == 204
        call_args = service._client.request.call_args
        json_payload = call_args[1]["json"]
        assert "temperature" in json_payload
        assert "airQualityIndex" in json_payload

    @pytest.mark.asyncio
    async def test_delete_success(self, service):
        """Test deleting an air quality observation successfully."""
        service._client = AsyncMock()
        service._client.request.return_value.status_code = 204

        response = await service.delete("urn:ngsi-ld:AirQualityObserved:test001")

        assert response.status_code == 204
        service._client.request.assert_called_once()

    @pytest.mark.asyncio
    async def test_find_by_location_success(self, service):
        """Test finding air quality observations by location successfully."""
        observations = [
            {
                "id": "urn:ngsi-ld:AirQualityObserved:test001",
                "type": "AirQualityObserved",
                "temperature": {"type": "Property", "value": 25.5}
            }
        ]
        
        service._client = AsyncMock()
        service._client.request.return_value.json.return_value = observations

        result = await service.find_by_location(
            coordinates="[-8.5,41.2]",
            max_distance=1000,
            limit=10
        )

        assert result == observations
        call_args = service._client.request.call_args
        params = call_args[1]["params"]
        assert params["georel"] == "near;maxDistance==1000"

    @pytest.mark.asyncio
    async def test_find_by_quality_index_success(self, service):
        """Test finding air quality observations by quality index successfully."""
        observations = [
            {
                "id": "urn:ngsi-ld:AirQualityObserved:test001",
                "type": "AirQualityObserved",
                "airQualityIndex": {"type": "Property", "value": 85.0}
            }
        ]
        
        service._client = AsyncMock()
        service._client.request.return_value.json.return_value = observations

        result = await service.find_by_quality_index(min_index=80, max_index=100)

        assert result == observations
        call_args = service._client.request.call_args
        params = call_args[1]["params"]
        assert "airQualityIndex>=80" in params["q"]
        assert "airQualityIndex<=100" in params["q"]

    @pytest.mark.asyncio
    async def test_find_by_temperature_range_success(self, service):
        """Test finding air quality observations by temperature range successfully."""
        observations = [
            {
                "id": "urn:ngsi-ld:AirQualityObserved:test001",
                "type": "AirQualityObserved",
                "temperature": {"type": "Property", "value": 25.5}
            }
        ]
        
        service._client = AsyncMock()
        service._client.request.return_value.json.return_value = observations

        result = await service.find_by_temperature_range(
            min_temp=20.0, 
            max_temp=30.0, 
            limit=20
        )

        assert result == observations
        call_args = service._client.request.call_args
        params = call_args[1]["params"]
        assert "temperature>=20.0" in params["q"]
        assert "temperature<=30.0" in params["q"]
        assert params["limit"] == 20

    @pytest.mark.asyncio
    async def test_batch_create_success(self, service):
        """Test batch creating air quality observations successfully."""
        entities = [
            {"id": "urn:ngsi-ld:AirQualityObserved:test001", "type": "AirQualityObserved"},
            {"id": "urn:ngsi-ld:AirQualityObserved:test002", "type": "AirQualityObserved"}
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
        """Test batch upserting air quality observations successfully."""
        entities = [
            {"id": "urn:ngsi-ld:AirQualityObserved:test001", "type": "AirQualityObserved"}
        ]
        
        service._client = AsyncMock()
        service._client.request.return_value.status_code = 204

        response = await service.batch_upsert(entities, options="update")

        assert response.status_code == 204
        call_args = service._client.request.call_args
        assert call_args[1]["params"]["options"] == "update"

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
            await service.get_by_id("urn:ngsi-ld:AirQualityObserved:nonexistent")

    @pytest.mark.asyncio
    async def test_connection_error_handling(self, service):
        """Test handling of connection errors."""
        service._client = AsyncMock()
        service._client.request.side_effect = httpx.RequestError("Connection failed")

        with pytest.raises(httpx.RequestError):
            await service.get_all()

    @pytest.mark.asyncio
    async def test_get_all_with_multiple_filters(self, service, mock_air_quality_response):
        """Test getting all observations with multiple filters combined."""
        service._client = AsyncMock()
        service._client.request.return_value.json.return_value = mock_air_quality_response

        result = await service.get_all(
            temp_min=20.0,
            temp_max=30.0,
            airQualityIndex=">80",
            humidity="<70"
        )

        assert result == mock_air_quality_response
        call_args = service._client.request.call_args
        params = call_args[1]["params"]
        query = params["q"]
        assert "temperature>=20.0" in query
        assert "temperature<=30.0" in query
        assert "airQualityIndex>80" in query
        assert "humidity<70" in query

    @pytest.mark.asyncio
    async def test_find_by_quality_index_with_format_options(self, service):
        """Test find_by_quality_index with format options."""
        service._client = AsyncMock()
        service._client.request.return_value.json.return_value = []

        await service.find_by_quality_index(
            min_index=80,
            max_index=100,
            format="simplified",
            pick="id,type,airQualityIndex"
        )

        call_args = service._client.request.call_args
        params = call_args[1]["params"]
        assert params["format"] == "simplified"
        assert params["pick"] == "id,type,airQualityIndex"
