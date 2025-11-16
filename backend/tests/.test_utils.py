"""
Test utilities and helper functions.
"""

import asyncio
from typing import Any, Dict, List, Optional
from unittest.mock import AsyncMock, MagicMock

import httpx
from pydantic import BaseModel


def create_mock_httpx_response(
    status_code: int = 200,
    json_data: Any = None,
    headers: Dict[str, str] = None,
    text: str = None
) -> MagicMock:
    """Create a mock HTTPX response for testing."""
    mock_response = MagicMock(spec=httpx.Response)
    mock_response.status_code = status_code
    mock_response.headers = headers or {}
    mock_response.json.return_value = json_data or {}
    mock_response.text = text or "{}"
    return mock_response


def create_mock_async_client() -> AsyncMock:
    """Create a mock async HTTPX client."""
    mock_client = AsyncMock(spec=httpx.AsyncClient)
    mock_client.is_closed = False
    return mock_client


def create_ngsi_entity(
    entity_id: str,
    entity_type: str,
    attributes: Dict[str, Any] = None
) -> Dict[str, Any]:
    """Create a basic NGSI-LD entity structure."""
    entity = {
        "id": entity_id,
        "type": entity_type,
        "@context": "http://context/datamodels.context-ngsi.jsonld"
    }
    
    if attributes:
        entity.update(attributes)
    
    return entity


def create_ngsi_property(
    value: Any,
    unit_code: Optional[str] = None,
    observed_at: Optional[str] = None
) -> Dict[str, Any]:
    """Create a NGSI-LD property structure."""
    prop = {
        "type": "Property",
        "value": value
    }
    
    if unit_code:
        prop["unitCode"] = unit_code
    if observed_at:
        prop["observedAt"] = observed_at
    
    return prop


def create_ngsi_relationship(
    object_ref: str,
    observed_at: Optional[str] = None
) -> Dict[str, Any]:
    """Create a NGSI-LD relationship structure."""
    rel = {
        "type": "Relationship",
        "object": object_ref
    }
    
    if observed_at:
        rel["observedAt"] = observed_at
    
    return rel


def create_ngsi_geoproperty(
    geometry: Dict[str, Any],
    observed_at: Optional[str] = None
) -> Dict[str, Any]:
    """Create a NGSI-LD geo-property structure."""
    geo = {
        "type": "GeoProperty",
        "value": geometry
    }
    
    if observed_at:
        geo["observedAt"] = observed_at
    
    return geo


def create_point_geometry(lon: float, lat: float) -> Dict[str, Any]:
    """Create a GeoJSON Point geometry."""
    return {
        "type": "Point",
        "coordinates": [lon, lat]
    }


def validate_ngsi_entity(entity: Dict[str, Any]) -> bool:
    """Validate that an entity follows NGSI-LD structure."""
    if not isinstance(entity, dict):
        return False
    
    # Check required fields
    if "id" not in entity or "type" not in entity:
        return False
    
    if not isinstance(entity["id"], str) or not isinstance(entity["type"], str):
        return False
    
    # Check that ID follows NGSI-LD pattern
    if not entity["id"].startswith("urn:ngsi-ld:"):
        return False
    
    return True


def validate_ngsi_attribute(attr: Dict[str, Any]) -> bool:
    """Validate that an attribute follows NGSI-LD structure."""
    if not isinstance(attr, dict) or "type" not in attr:
        return False
    
    attr_type = attr["type"]
    
    if attr_type == "Property":
        return "value" in attr
    elif attr_type == "Relationship":
        return "object" in attr and isinstance(attr["object"], str)
    elif attr_type == "GeoProperty":
        return "value" in attr and isinstance(attr["value"], dict)
    
    return False


def assert_valid_mock_response(mock_response: MagicMock, expected_status: int = 200):
    """Assert that a mock response has expected properties."""
    assert mock_response.status_code == expected_status
    assert isinstance(mock_response.headers, dict)
    assert hasattr(mock_response, 'json')
    assert hasattr(mock_response, 'text')


def assert_service_call_made(
    mock_service: AsyncMock,
    method_name: str,
    expected_args: tuple = None,
    expected_kwargs: dict = None
):
    """Assert that a service method was called with expected arguments."""
    mock_service.assert_called()
    
    if expected_args is not None:
        assert mock_service.call_args[0] == expected_args
    
    if expected_kwargs is not None:
        assert mock_service.call_args[1] == expected_kwargs


class MockAsyncContextManager:
    """Helper class for mocking async context managers."""
    
    def __init__(self, return_value=None, side_effect=None):
        self.return_value = return_value
        self.side_effect = side_effect
        self.enter_called = False
        self.exit_called = False
    
    async def __aenter__(self):
        self.enter_called = True
        if self.side_effect:
            raise self.side_effect
        return self.return_value
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.exit_called = True
        return False


def create_test_building_data(
    building_id: str = "urn:ngsi-ld:Building:test001",
    name: str = "Test Building",
    category: List[str] = None,
    floors: float = 5.0
) -> Dict[str, Any]:
    """Create test building data."""
    return create_ngsi_entity(
        entity_id=building_id,
        entity_type="Building",
        attributes={
            "name": create_ngsi_property(name),
            "category": create_ngsi_property(category or ["office"]),
            "floorsAboveGround": create_ngsi_property(floors, "Level"),
            "location": create_ngsi_geoproperty(create_point_geometry(-8.5, 41.2))
        }
    )


def create_test_air_quality_data(
    observation_id: str = "urn:ngsi-ld:AirQualityObserved:test001",
    temperature: float = 25.5,
    humidity: float = 65.0,
    aqi: float = 85.0
) -> Dict[str, Any]:
    """Create test air quality observation data."""
    return create_ngsi_entity(
        entity_id=observation_id,
        entity_type="AirQualityObserved",
        attributes={
            "temperature": create_ngsi_property(temperature, "CEL"),
            "humidity": create_ngsi_property(humidity, "P1"),
            "airQualityIndex": create_ngsi_property(aqi),
            "location": create_ngsi_geoproperty(create_point_geometry(-8.5, 41.2))
        }
    )


def create_test_device_data(
    device_id: str = "urn:ngsi-ld:Device:test001",
    name: str = "Test Device",
    state: str = "ok",
    controlled_asset: str = "urn:ngsi-ld:Building:test001"
) -> Dict[str, Any]:
    """Create test device data."""
    return create_ngsi_entity(
        entity_id=device_id,
        entity_type="Device",
        attributes={
            "name": create_ngsi_property(name),
            "deviceState": create_ngsi_property(state),
            "controlledAsset": create_ngsi_relationship(controlled_asset),
            "location": create_ngsi_geoproperty(create_point_geometry(-8.5, 41.2))
        }
    )


def create_test_carbon_footprint_data(
    footprint_id: str = "urn:ngsi-ld:CarbonFootprint:test001",
    co2_emissions: float = 1500.5,
    energy_consumption: float = 2500.0
) -> Dict[str, Any]:
    """Create test carbon footprint data."""
    return create_ngsi_entity(
        entity_id=footprint_id,
        entity_type="CarbonFootprint",
        attributes={
            "co2Emissions": create_ngsi_property(co2_emissions, "KGM"),
            "energyConsumption": create_ngsi_property(energy_consumption, "KWH"),
            "period": create_ngsi_property("P1Y")
        }
    )


def create_test_water_quality_data(
    observation_id: str = "urn:ngsi-ld:WaterQualityObserved:test001",
    ph: float = 7.2,
    dissolved_oxygen: float = 8.5,
    turbidity: float = 2.3
) -> Dict[str, Any]:
    """Create test water quality observation data."""
    return create_ngsi_entity(
        entity_id=observation_id,
        entity_type="WaterQualityObserved",
        attributes={
            "ph": create_ngsi_property(ph),
            "dissolvedOxygen": create_ngsi_property(dissolved_oxygen, "MG/L"),
            "turbidity": create_ngsi_property(turbidity, "NTU"),
            "location": create_ngsi_geoproperty(create_point_geometry(-8.5, 41.2))
        }
    )


def create_test_subscription_data(
    subscription_id: str = "urn:ngsi-ld:Subscription:test001",
    description: str = "Test subscription",
    entity_types: List[str] = None
) -> Dict[str, Any]:
    """Create test subscription data."""
    return create_ngsi_entity(
        entity_id=subscription_id,
        entity_type="Subscription",
        attributes={
            "description": create_ngsi_property(description),
            "entities": create_ngsi_property([
                {"type": etype} for etype in (entity_types or ["Building"])
            ]),
            "notification": create_ngsi_property({
                "endpoint": {
                    "uri": "http://localhost:8080/notification",
                    "accept": "application/json"
                }
            })
        }
    )


def create_test_context_source_data(
    source_id: str = "urn:ngsi-ld:ContextSource:test001",
    name: str = "Test Context Source",
    endpoint: str = "http://example.com/ngsi-ld"
) -> Dict[str, Any]:
    """Create test context source data."""
    return create_ngsi_entity(
        entity_id=source_id,
        entity_type="ContextSource",
        attributes={
            "name": create_ngsi_property(name),
            "endpoint": create_ngsi_property(endpoint),
            "information": create_ngsi_property([
                {"entities": [{"type": "Building"}]}
            ])
        }
    )


async def run_async_test(test_func, *args, **kwargs):
    """Helper to run async test functions."""
    loop = asyncio.get_event_loop()
    return await test_func(*args, **kwargs)


def create_error_response(status_code: int, message: str) -> MagicMock:
    """Create a mock error response."""
    response = MagicMock(spec=httpx.Response)
    response.status_code = status_code
    response.text = message
    response.json.return_value = {"error": message}
    return response


def create_http_error(status_code: int, message: str) -> httpx.HTTPStatusError:
    """Create an HTTP error exception."""
    response = create_error_response(status_code, message)
    request = MagicMock()
    return httpx.HTTPStatusError(message, request=request, response=response)
