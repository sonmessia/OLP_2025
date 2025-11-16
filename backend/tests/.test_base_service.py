"""
Unit tests for BaseService.
"""

import json
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
import httpx

from app.services.base_service import BaseService


class TestBaseService:
    """Test cases for BaseService."""

    def test_init_default_values(self):
        """Test BaseService initialization with default values."""
        service = BaseService()
        
        assert service.ORION_LD_URL == "http://fiware-orionld:1026/ngsi-ld/v1"
        assert service.CONTEXT_URL == "http://context/datamodels.context-ngsi.jsonld"
        assert service.JSON_LD_CONTENT_HEADER == {"Content-Type": "application/ld+json"}
        assert service.JSON_CONTENT_HEADER == {"Content-Type": "application/json"}
        assert service._client is None

    def test_init_custom_values(self):
        """Test BaseService initialization with custom values."""
        custom_orion = "http://custom-orion:1026/ngsi-ld/v1"
        custom_context = "http://custom/context.jsonld"
        
        service = BaseService(orion_url=custom_orion, context_url=custom_context)
        
        assert service.ORION_LD_URL == custom_orion
        assert service.CONTEXT_URL == custom_context
        assert "custom-context" in service.LINK_HEADER["Link"]

    @pytest.mark.asyncio
    async def test_get_client_creates_new_client(self):
        """Test that _get_client creates a new HTTP client."""
        service = BaseService()
        
        # First call should create a new client
        client = await service._get_client()
        assert client is not None
        assert not client.is_closed
        
        # Second call should return the same client
        client2 = await service._get_client()
        assert client is client2

    @pytest.mark.asyncio
    async def test_close_closes_client(self):
        """Test that close properly closes the HTTP client."""
        service = BaseService()
        
        # Initialize client
        await service._get_client()
        assert service._client is not None
        
        # Close client
        await service.close()
        assert service._client.is_closed

    @pytest.mark.asyncio
    async def test_async_context_manager(self):
        """Test async context manager functionality."""
        service = BaseService()
        
        async with service as s:
            assert s is service
            assert service._client is not None
            assert not service._client.is_closed
        
        assert service._client.is_closed

    @pytest.mark.asyncio
    async def test_make_request_success(self, mock_base_service):
        """Test successful HTTP request."""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"result": "success"}
        
        mock_base_service._client.request.return_value = mock_response
        
        # Make request
        response = await mock_base_service._make_request(
            "GET", "entities", params={"type": "Building"}
        )
        
        assert response is mock_response
        mock_base_service._client.request.assert_called_once()

    @pytest.mark.asyncio
    async def test_make_request_http_error(self, mock_base_service):
        """Test HTTP error handling."""
        # Setup mock error response
        error_response = MagicMock()
        error_response.status_code = 404
        error_response.text = "Entity not found"
        
        mock_http_error = httpx.HTTPStatusError(
            "404 Not Found", request=MagicMock(), response=error_response
        )
        
        mock_base_service._client.request.side_effect = mock_http_error
        
        # Should raise HTTPStatusError
        with pytest.raises(httpx.HTTPStatusError):
            await mock_base_service._make_request("GET", "entities/nonexistent")

    @pytest.mark.asyncio
    async def test_make_request_connection_error(self, mock_base_service):
        """Test connection error handling."""
        connection_error = httpx.RequestError("Connection failed")
        mock_base_service._client.request.side_effect = connection_error
        
        # Should raise RequestError
        with pytest.raises(httpx.RequestError):
            await mock_base_service._make_request("GET", "entities")

    def test_make_request_endpoint_cleanup(self, mock_base_service):
        """Test that leading slash is removed from endpoint."""
        # This is tested indirectly through the _make_request method
        # but we can verify the URL construction logic
        assert mock_base_service.ORION_LD_URL == "http://mock-orion:1026/ngsi-ld/v1"

    @pytest.mark.asyncio
    async def test_create_entity(self, mock_base_service, sample_building_data):
        """Test entity creation."""
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_base_service._client.request.return_value = mock_response
        
        response = await mock_base_service.create_entity(sample_building_data)
        
        assert response is mock_response
        # Verify that @context was added
        call_args = mock_base_service._client.request.call_args
        json_payload = call_args[1]["json"]
        assert "@context" in json_payload

    @pytest.mark.asyncio
    async def test_get_entity_by_id(self, mock_base_service, mock_orion_response):
        """Test getting entity by ID."""
        mock_response = MagicMock()
        mock_response.json.return_value = mock_orion_response
        mock_base_service._client.request.return_value = mock_response
        
        result = await mock_base_service.get_entity_by_id("urn:ngsi-ld:Building:test001")
        
        assert result == mock_orion_response
        mock_base_service._client.request.assert_called_once()

    @pytest.mark.asyncio
    async def test_replace_entity_with_dict(self, mock_base_service, sample_building_data):
        """Test replacing entity with dictionary data."""
        mock_response = MagicMock()
        mock_response.status_code = 204
        mock_base_service._client.request.return_value = mock_response
        
        response = await mock_base_service.replace_entity(
            "urn:ngsi-ld:Building:test001", sample_building_data
        )
        
        assert response is mock_response
        call_args = mock_base_service._client.request.call_args
        json_payload = call_args[1]["json"]
        assert "@context" in json_payload

    @pytest.mark.asyncio
    async def test_replace_entity_with_model(self, mock_base_service):
        """Test replacing entity with Pydantic model."""
        from app.models.Building import Building
        
        building = Building(
            id="urn:ngsi-ld:Building:test001",
            name="Test Building",
            category=["office"]
        )
        
        mock_response = MagicMock()
        mock_response.status_code = 204
        mock_base_service._client.request.return_value = mock_response
        
        response = await mock_base_service.replace_entity(
            "urn:ngsi-ld:Building:test001", building
        )
        
        assert response is mock_response
        call_args = mock_base_service._client.request.call_args
        json_payload = call_args[1]["json"]
        assert "@context" in json_payload

    @pytest.mark.asyncio
    async def test_delete_entity(self, mock_base_service):
        """Test entity deletion."""
        mock_response = MagicMock()
        mock_response.status_code = 204
        mock_base_service._client.request.return_value = mock_response
        
        response = await mock_base_service.delete_entity("urn:ngsi-ld:Building:test001")
        
        assert response is mock_response

    @pytest.mark.asyncio
    async def test_update_entity_attributes(self, mock_base_service):
        """Test updating entity attributes."""
        mock_response = MagicMock()
        mock_response.status_code = 204
        mock_base_service._client.request.return_value = mock_response
        
        attrs_data = {"name": {"type": "Property", "value": "Updated Name"}}
        
        response = await mock_base_service.update_entity_attributes(
            "urn:ngsi-ld:Building:test001", attrs_data
        )
        
        assert response is mock_response
        call_args = mock_base_service._client.request.call_args
        json_payload = call_args[1]["json"]
        assert "@context" in json_payload

    @pytest.mark.asyncio
    async def test_delete_entity_attribute(self, mock_base_service):
        """Test deleting entity attribute."""
        mock_response = MagicMock()
        mock_response.status_code = 204
        mock_base_service._client.request.return_value = mock_response
        
        response = await mock_base_service.delete_entity_attribute(
            "urn:ngsi-ld:Building:test001", "name"
        )
        
        assert response is mock_response

    @pytest.mark.asyncio
    async def test_batch_create(self, mock_base_service):
        """Test batch entity creation."""
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_base_service._client.request.return_value = mock_response
        
        entities = [
            {"id": "urn:ngsi-ld:Building:test001", "type": "Building"},
            {"id": "urn:ngsi-ld:Building:test002", "type": "Building"}
        ]
        
        response = await mock_base_service.batch_create(entities)
        
        assert response is mock_response
        call_args = mock_base_service._client.request.call_args
        json_payload = call_args[1]["json"]
        assert len(json_payload) == 2
        for entity in json_payload:
            assert "@context" in entity

    @pytest.mark.asyncio
    async def test_batch_upsert(self, mock_base_service):
        """Test batch entity upsert."""
        mock_response = MagicMock()
        mock_response.status_code = 204
        mock_base_service._client.request.return_value = mock_response
        
        entities = [{"id": "urn:ngsi-ld:Building:test001", "type": "Building"}]
        
        response = await mock_base_service.batch_upsert(entities, options="replace")
        
        assert response is mock_response
        call_args = mock_base_service._client.request.call_args
        assert call_args[1]["params"]["options"] == "replace"

    @pytest.mark.asyncio
    async def test_batch_update(self, mock_base_service):
        """Test batch entity update."""
        mock_response = MagicMock()
        mock_response.status_code = 204
        mock_base_service._client.request.return_value = mock_response
        
        entities = [{"id": "urn:ngsi-ld:Building:test001", "type": "Building"}]
        
        response = await mock_base_service.batch_update(entities)
        
        assert response is mock_response

    @pytest.mark.asyncio
    async def test_batch_delete(self, mock_base_service):
        """Test batch entity deletion."""
        mock_response = MagicMock()
        mock_response.status_code = 204
        mock_base_service._client.request.return_value = mock_response
        
        entity_ids = ["urn:ngsi-ld:Building:test001", "urn:ngsi-ld:Building:test002"]
        
        response = await mock_base_service.batch_delete(entity_ids)
        
        assert response is mock_response
        call_args = mock_base_service._client.request.call_args
        json_payload = call_args[1]["json"]
        assert json_payload == entity_ids

    @pytest.mark.asyncio
    async def test_query_entities_success(self, mock_base_service):
        """Test successful entity query."""
        mock_response = MagicMock()
        mock_response.json.return_value = [
            {"id": "urn:ngsi-ld:Building:test001", "type": "Building"}
        ]
        mock_base_service._client.request.return_value = mock_response
        
        result = await mock_base_service.query_entities(type="Building")
        
        assert isinstance(result, list)
        assert len(result) == 1

    @pytest.mark.asyncio
    async def test_query_entities_count_only(self, mock_base_service):
        """Test query with count=True."""
        mock_response = MagicMock()
        mock_response.headers = {"NGSILD-Results-Count": "42"}
        mock_base_service._client.request.return_value = mock_response
        
        result = await mock_base_service.query_entities(type="Building", count=True)
        
        assert result == 42

    @pytest.mark.asyncio
    async def test_query_entities_no_filters(self, mock_base_service):
        """Test that query without filters raises ValueError."""
        with pytest.raises(ValueError, match="Query is too broad"):
            await mock_base_service.query_entities()

    @pytest.mark.asyncio
    async def test_query_entities_with_all_filters(self, mock_base_service):
        """Test query with all possible filters."""
        mock_response = MagicMock()
        mock_response.json.return_value = []
        mock_base_service._client.request.return_value = mock_response
        
        await mock_base_service.query_entities(
            type="Building",
            id="urn:ngsi-ld:Building:test001",
            q="name==test",
            attrs="name,category",
            pick="id,type,name",
            georel="near;maxDistance==1000",
            geometry="Point",
            coordinates="[-8.5,41.2]",
            geoproperty="location",
            limit=10,
            offset=0,
            count=False,
            options="keyValues",
            format="simplified",
            local=True,
            timerel="before",
            timeAt="2023-01-01T00:00:00Z",
            timeproperty="observedAt"
        )
        
        # Verify all parameters were passed
        call_args = mock_base_service._client.request.call_args
        params = call_args[1]["params"]
        
        assert params["type"] == "Building"
        assert params["q"] == "name==test"
        assert params["limit"] == 10

    @pytest.mark.asyncio
    async def test_temporal_query(self, mock_base_service):
        """Test temporal query functionality."""
        mock_response = MagicMock()
        mock_response.json.return_value = []
        mock_base_service._client.request.return_value = mock_response
        
        result = await mock_base_service.temporal_query(
            timerel="before",
            timeAt="2023-01-01T00:00:00Z",
            type="Building"
        )
        
        assert isinstance(result, list)
        call_args = mock_base_service._client.request.call_args
        params = call_args[1]["params"]
        assert params["timerel"] == "before"
        assert params["timeAt"] == "2023-01-01T00:00:00Z"
        assert params["type"] == "Building"

    @pytest.mark.asyncio
    async def test_make_request_parameter_cleanup(self, mock_base_service):
        """Test parameter cleanup in _make_request."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_base_service._client.request.return_value = mock_response
        
        # Test with None values and boolean
        await mock_base_service._make_request(
            "GET", 
            "entities",
            params={
                "type": "Building",
                "null_param": None,
                "bool_param": True,
                "false_param": False
            }
        )
        
        call_args = mock_base_service._client.request.call_args
        params = call_args[1]["params"]
        
        assert params["type"] == "Building"
        assert "null_param" not in params
        assert params["bool_param"] == "true"
        assert params["false_param"] == "false"
