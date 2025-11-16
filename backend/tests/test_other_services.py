"""
Unit tests for DeviceService.
"""

from unittest.mock import AsyncMock, MagicMock

import pytest
import httpx

from app.services.device_service import DeviceService


class TestDeviceService:
    """Test cases for DeviceService."""

    @pytest.fixture
    def service(self):
        """Create DeviceService instance for testing."""
        return DeviceService()

    @pytest.fixture
    def mock_device_response(self):
        """Mock response from Orion-LD for devices."""
        return [
            {
                "id": "urn:ngsi-ld:Device:test001",
                "type": "Device",
                "name": {"type": "Property", "value": "Temperature Sensor 001"},
                "deviceState": {"type": "Property", "value": "ok"},
                "controlledAsset": {
                    "type": "Relationship", 
                    "object": "urn:ngsi-ld:Building:test001"
                },
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
    async def test_get_all_with_device_state_filter(self, service, mock_device_response):
        """Test getting all devices with device state filter."""
        service._client = AsyncMock()
        service._client.request.return_value.json.return_value = mock_device_response

        result = await service.get_all(deviceState="ok")

        assert result == mock_device_response
        call_args = service._client.request.call_args
        params = call_args[1]["params"]
        assert params["q"] == 'deviceState=="ok"'

    @pytest.mark.asyncio
    async def test_get_all_with_controlled_asset_filter(self, service, mock_device_response):
        """Test getting all devices with controlled asset filter."""
        service._client = AsyncMock()
        service._client.request.return_value.json.return_value = mock_device_response

        result = await service.get_all(
            controlledAsset="urn:ngsi-ld:Building:test001"
        )

        assert result == mock_device_response
        call_args = service._client.request.call_args
        params = call_args[1]["params"]
        assert 'controlledAsset=="urn:ngsi-ld:Building:test001"' in params["q"]

    @pytest.mark.asyncio
    async def test_get_by_id_success(self, service):
        """Test getting device by ID successfully."""
        device_data = {
            "id": "urn:ngsi-ld:Device:test001",
            "type": "Device",
            "name": {"type": "Property", "value": "Temperature Sensor 001"}
        }
        
        service._client = AsyncMock()
        service._client.request.return_value.json.return_value = device_data

        result = await service.get_by_id("urn:ngsi-ld:Device:test001")

        assert result == device_data
        service._client.request.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_success(self, service):
        """Test creating a device successfully."""
        device_data = {
            "id": "urn:ngsi-ld:Device:test001",
            "type": "Device",
            "name": "Temperature Sensor 001",
            "deviceState": "ok"
        }
        
        service._client = AsyncMock()
        service._client.request.return_value.status_code = 201

        response = await service.create(device_data)

        assert response.status_code == 201
        call_args = service._client.request.call_args
        json_payload = call_args[1]["json"]
        assert json_payload["id"] == "urn:ngsi-ld:Device:test001"
        assert "@context" in json_payload

    @pytest.mark.asyncio
    async def test_find_by_building_success(self, service):
        """Test finding devices by building successfully."""
        devices = [
            {
                "id": "urn:ngsi-ld:Device:test001",
                "type": "Device",
                "controlledAsset": {
                    "type": "Relationship",
                    "object": "urn:ngsi-ld:Building:test001"
                }
            }
        ]
        
        service._client = AsyncMock()
        service._client.request.return_value.json.return_value = devices

        result = await service.find_by_building(
            building_id="urn:ngsi-ld:Building:test001",
            limit=10
        )

        assert result == devices
        call_args = service._client.request.call_args
        params = call_args[1]["params"]
        assert 'controlledAsset=="urn:ngsi-ld:Building:test001"' in params["q"]
        assert params["limit"] == 10

    @pytest.mark.asyncio
    async def test_find_by_device_state_success(self, service):
        """Test finding devices by state successfully."""
        devices = [
            {
                "id": "urn:ngsi-ld:Device:test001",
                "type": "Device",
                "deviceState": {"type": "Property", "value": "ok"}
            }
        ]
        
        service._client = AsyncMock()
        service._client.request.return_value.json.return_value = devices

        result = await service.find_by_device_state(state="ok", limit=20)

        assert result == devices
        call_args = service._client.request.call_args
        params = call_args[1]["params"]
        assert params["q"] == 'deviceState=="ok"'
        assert params["limit"] == 20

    @pytest.mark.asyncio
    async def test_update_device_state_success(self, service):
        """Test updating device state successfully."""
        service._client = AsyncMock()
        service._client.request.return_value.status_code = 204

        response = await service.update_device_state(
            "urn:ngsi-ld:Device:test001",
            "offline"
        )

        assert response.status_code == 204
        call_args = service._client.request.call_args
        json_payload = call_args[1]["json"]
        assert "deviceState" in json_payload
        assert json_payload["deviceState"]["value"] == "offline"

    @pytest.mark.asyncio
    async def test_orion_error_handling(self, service):
        """Test handling of Orion-LD HTTP errors."""
        service._client = AsyncMock()
        service._client.request.side_effect = httpx.HTTPStatusError(
            "404 Not Found", 
            request=MagicMock(), 
            response=MagicMock(status_code=404, text="Device not found")
        )

        with pytest.raises(httpx.HTTPStatusError):
            await service.get_by_id("urn:ngsi-ld:Device:nonexistent")


class TestCarbonFootprintService:
    """Test cases for CarbonFootprintService."""

    @pytest.fixture
    def service(self):
        """Create CarbonFootprintService instance for testing."""
        return CarbonFootprintService()

    @pytest.fixture
    def mock_carbon_footprint_response(self):
        """Mock response from Orion-LD for carbon footprints."""
        return [
            {
                "id": "urn:ngsi-ld:CarbonFootprint:test001",
                "type": "CarbonFootprint",
                "co2Emissions": {"type": "Property", "value": 1500.5, "unitCode": "KGM"},
                "energyConsumption": {"type": "Property", "value": 2500.0, "unitCode": "KWH"},
                "period": {"type": "Property", "value": "P1Y"}
            }
        ]

    @pytest.mark.asyncio
    async def test_get_all_with_emissions_filter(self, service, mock_carbon_footprint_response):
        """Test getting all carbon footprints with emissions filter."""
        service._client = AsyncMock()
        service._client.request.return_value.json.return_value = mock_carbon_footprint_response

        result = await service.get_all(co2Emissions=">1000")

        assert result == mock_carbon_footprint_response
        call_args = service._client.request.call_args
        params = call_args[1]["params"]
        assert params["q"] == "co2Emissions>1000"

    @pytest.mark.asyncio
    async def test_find_by_emissions_range(self, service, mock_carbon_footprint_response):
        """Test finding carbon footprints by emissions range."""
        service._client = AsyncMock()
        service._client.request.return_value.json.return_value = mock_carbon_footprint_response

        result = await service.find_by_emissions_range(
            min_emissions=1000.0,
            max_emissions=2000.0,
            limit=10
        )

        assert result == mock_carbon_footprint_response
        call_args = service._client.request.call_args
        params = call_args[1]["params"]
        query = params["q"]
        assert "co2Emissions>=1000.0" in query
        assert "co2Emissions<=2000.0" in query
        assert params["limit"] == 10

    @pytest.mark.asyncio
    async def test_create_success(self, service):
        """Test creating a carbon footprint record successfully."""
        carbon_data = {
            "id": "urn:ngsi-ld:CarbonFootprint:test001",
            "type": "CarbonFootprint",
            "co2Emissions": {"type": "Property", "value": 1500.5, "unitCode": "KGM"},
            "energyConsumption": {"type": "Property", "value": 2500.0, "unitCode": "KWH"}
        }
        
        service._client = AsyncMock()
        service._client.request.return_value.status_code = 201

        response = await service.create(carbon_data)

        assert response.status_code == 201
        call_args = service._client.request.call_args
        json_payload = call_args[1]["json"]
        assert json_payload["id"] == "urn:ngsi-ld:CarbonFootprint:test001"
        assert "@context" in json_payload


class TestWaterQualityService:
    """Test cases for WaterQualityService."""

    @pytest.fixture
    def service(self):
        """Create WaterQualityService instance for testing."""
        return WaterQualityService()

    @pytest.fixture
    def mock_water_quality_response(self):
        """Mock response from Orion-LD for water quality observations."""
        return [
            {
                "id": "urn:ngsi-ld:WaterQualityObserved:test001",
                "type": "WaterQualityObserved",
                "ph": {"type": "Property", "value": 7.2},
                "dissolvedOxygen": {"type": "Property", "value": 8.5, "unitCode": "MG/L"},
                "turbidity": {"type": "Property", "value": 2.3, "unitCode": "NTU"}
            }
        ]

    @pytest.mark.asyncio
    async def test_get_all_with_ph_filter(self, service, mock_water_quality_response):
        """Test getting all water quality observations with pH filter."""
        service._client = AsyncMock()
        service._client.request.return_value.json.return_value = mock_water_quality_response

        result = await service.get_all(ph=">7.0")

        assert result == mock_water_quality_response
        call_args = service._client.request.call_args
        params = call_args[1]["params"]
        assert params["q"] == "ph>7.0"

    @pytest.mark.asyncio
    async def test_find_by_ph_range(self, service, mock_water_quality_response):
        """Test finding water quality observations by pH range."""
        service._client = AsyncMock()
        service._client.request.return_value.json.return_value = mock_water_quality_response

        result = await service.find_by_ph_range(
            min_ph=6.5,
            max_ph=8.5,
            limit=15
        )

        assert result == mock_water_quality_response
        call_args = service._client.request.call_args
        params = call_args[1]["params"]
        query = params["q"]
        assert "ph>=6.5" in query
        assert "ph<=8.5" in query
        assert params["limit"] == 15

    @pytest.mark.asyncio
    async def test_find_by_dissolved_oxygen(self, service, mock_water_quality_response):
        """Test finding water quality observations by dissolved oxygen."""
        service._client = AsyncMock()
        service._client.request.return_value.json.return_value = mock_water_quality_response

        result = await service.find_by_dissolved_oxygen(
            min_do=5.0,
            max_do=10.0,
            limit=20
        )

        assert result == mock_water_quality_response
        call_args = service._client.request.call_args
        params = call_args[1]["params"]
        query = params["q"]
        assert "dissolvedOxygen>=5.0" in query
        assert "dissolvedOxygen<=10.0" in query
        assert params["limit"] == 20

    @pytest.mark.asyncio
    async def test_create_success(self, service):
        """Test creating a water quality observation successfully."""
        water_data = {
            "id": "urn:ngsi-ld:WaterQualityObserved:test001",
            "type": "WaterQualityObserved",
            "ph": {"type": "Property", "value": 7.2},
            "dissolvedOxygen": {"type": "Property", "value": 8.5, "unitCode": "MG/L"}
        }
        
        service._client = AsyncMock()
        service._client.request.return_value.status_code = 201

        response = await service.create(water_data)

        assert response.status_code == 201
        call_args = service._client.request.call_args
        json_payload = call_args[1]["json"]
        assert json_payload["id"] == "urn:ngsi-ld:WaterQualityObserved:test001"
        assert "@context" in json_payload


class TestSubscriptionService:
    """Test cases for SubscriptionService."""

    @pytest.fixture
    def service(self):
        """Create SubscriptionService instance for testing."""
        return SubscriptionService()

    @pytest.fixture
    def mock_subscription_response(self):
        """Mock response from Orion-LD for subscriptions."""
        return [
            {
                "id": "urn:ngsi-ld:Subscription:test001",
                "type": "Subscription",
                "description": "Test subscription",
                "entities": [{"type": "Building", "idPattern": ".*"}],
                "notification": {
                    "endpoint": {
                        "uri": "http://localhost:8080/notification",
                        "accept": "application/json"
                    }
                }
            }
        ]

    @pytest.mark.asyncio
    async def test_get_all_subscriptions(self, service, mock_subscription_response):
        """Test getting all subscriptions."""
        service._client = AsyncMock()
        service._client.request.return_value.json.return_value = mock_subscription_response

        result = await service.get_all()

        assert result == mock_subscription_response
        service._client.request.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_subscription_success(self, service):
        """Test creating a subscription successfully."""
        subscription_data = {
            "id": "urn:ngsi-ld:Subscription:test001",
            "type": "Subscription",
            "description": "Test subscription",
            "entities": [{"type": "Building"}],
            "notification": {
                "endpoint": {
                    "uri": "http://localhost:8080/notification",
                    "accept": "application/json"
                }
            }
        }
        
        service._client = AsyncMock()
        service._client.request.return_value.status_code = 201

        response = await service.create(subscription_data)

        assert response.status_code == 201
        call_args = service._client.request.call_args
        json_payload = call_args[1]["json"]
        assert json_payload["id"] == "urn:ngsi-ld:Subscription:test001"

    @pytest.mark.asyncio
    async def test_delete_subscription_success(self, service):
        """Test deleting a subscription successfully."""
        service._client = AsyncMock()
        service._client.request.return_value.status_code = 204

        response = await service.delete("urn:ngsi-ld:Subscription:test001")

        assert response.status_code == 204
        service._client.request.assert_called_once()


class TestContextSourceService:
    """Test cases for ContextSourceService."""

    @pytest.fixture
    def service(self):
        """Create ContextSourceService instance for testing."""
        return ContextSourceService()

    @pytest.fixture
    def mock_context_source_response(self):
        """Mock response from Orion-LD for context sources."""
        return [
            {
                "id": "urn:ngsi-ld:ContextSource:test001",
                "type": "ContextSource",
                "name": {"type": "Property", "value": "Test Context Source"},
                "endpoint": {"type": "Property", "value": "http://example.com/ngsi-ld"},
                "information": [
                    {"entities": [{"type": "Building"}]}
                ]
            }
        ]

    @pytest.mark.asyncio
    async def test_get_all_context_sources(self, service, mock_context_source_response):
        """Test getting all context sources."""
        service._client = AsyncMock()
        service._client.request.return_value.json.return_value = mock_context_source_response

        result = await service.get_all()

        assert result == mock_context_source_response
        service._client.request.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_context_source_success(self, service):
        """Test creating a context source successfully."""
        context_source_data = {
            "id": "urn:ngsi-ld:ContextSource:test001",
            "type": "ContextSource",
            "name": {"type": "Property", "value": "Test Context Source"},
            "endpoint": {"type": "Property", "value": "http://example.com/ngsi-ld"}
        }
        
        service._client = AsyncMock()
        service._client.request.return_value.status_code = 201

        response = await service.create(context_source_data)

        assert response.status_code == 201
        call_args = service._client.request.call_args
        json_payload = call_args[1]["json"]
        assert json_payload["id"] == "urn:ngsi-ld:ContextSource:test001"

    @pytest.mark.asyncio
    async def test_delete_context_source_success(self, service):
        """Test deleting a context source successfully."""
        service._client = AsyncMock()
        service._client.request.return_value.status_code = 204

        response = await service.delete("urn:ngsi-ld:ContextSource:test001")

        assert response.status_code == 204
        service._client.request.assert_called_once()
