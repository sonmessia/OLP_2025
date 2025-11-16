"""
Test configuration and fixtures for the OLP 2025 backend.
"""

import asyncio
import json
from typing import Any, Dict, Generator
from unittest.mock import AsyncMock, MagicMock

import pytest
import pytest_asyncio
from httpx import AsyncClient, Response

from app.main import app
from app.services.base_service import BaseService


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def client() -> AsyncClient:
    """Create a test client for FastAPI app."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture
def mock_orion_response() -> Dict[str, Any]:
    """Mock response data from Orion-LD."""
    return {
        "id": "urn:ngsi-ld:Building:test001",
        "type": "Building",
        "name": {"type": "Property", "value": "Test Building"},
        "category": {"type": "Property", "value": ["office"]},
        "floorsAboveGround": {"type": "Property", "value": 5.0},
        "location": {
            "type": "GeoProperty",
            "value": {
                "type": "Point",
                "coordinates": [-8.5, 41.2]
            }
        }
    }


@pytest.fixture
def sample_building_data() -> Dict[str, Any]:
    """Sample building data for testing."""
    return {
        "id": "urn:ngsi-ld:Building:test001",
        "type": "Building",
        "name": "Test Building",
        "category": ["office"],
        "floorsAboveGround": 5.0,
        "location": {
            "type": "Point",
            "coordinates": [-8.5, 41.2]
        }
    }


@pytest.fixture
def mock_base_service() -> BaseService:
    """Create a mock BaseService with patched HTTP client."""
    service = BaseService(orion_url="http://mock-orion:1026/ngsi-ld/v1")
    service._client = AsyncMock()
    return service


@pytest.fixture
def mock_http_response() -> Response:
    """Create a mock HTTP response."""
    mock_response = MagicMock(spec=Response)
    mock_response.status_code = 200
    mock_response.headers = {"Content-Type": "application/json"}
    mock_response.json.return_value = {"id": "test", "type": "Building"}
    mock_response.text = '{"id": "test", "type": "Building"}'
    return mock_response


@pytest.fixture
def mock_air_quality_data() -> Dict[str, Any]:
    """Sample air quality data for testing."""
    return {
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


@pytest.fixture
def mock_device_data() -> Dict[str, Any]:
    """Sample device data for testing."""
    return {
        "id": "urn:ngsi-ld:Device:test001",
        "type": "Device",
        "name": {"type": "Property", "value": "Temperature Sensor 001"},
        "deviceState": {"type": "Property", "value": "ok"},
        "controlledAsset": {"type": "Relationship", "object": "urn:ngsi-ld:Building:test001"}
    }


@pytest.fixture
def mock_carbon_footprint_data() -> Dict[str, Any]:
    """Sample carbon footprint data for testing."""
    return {
        "id": "urn:ngsi-ld:CarbonFootprint:test001",
        "type": "CarbonFootprint",
        "co2Emissions": {"type": "Property", "value": 1500.5, "unitCode": "KGM"},
        "energyConsumption": {"type": "Property", "value": 2500.0, "unitCode": "KWH"},
        "period": {"type": "Property", "value": "P1Y"}
    }


@pytest.fixture
def mock_water_quality_data() -> Dict[str, Any]:
    """Sample water quality data for testing."""
    return {
        "id": "urn:ngsi-ld:WaterQualityObserved:test001",
        "type": "WaterQualityObserved",
        "ph": {"type": "Property", "value": 7.2},
        "dissolvedOxygen": {"type": "Property", "value": 8.5, "unitCode": "MG/L"},
        "turbidity": {"type": "Property", "value": 2.3, "unitCode": "NTU"}
    }


@pytest.fixture
def mock_subscription_data() -> Dict[str, Any]:
    """Sample subscription data for testing."""
    return {
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


@pytest.fixture
def mock_context_source_data() -> Dict[str, Any]:
    """Sample context source data for testing."""
    return {
        "id": "urn:ngsi-ld:ContextSource:test001",
        "type": "ContextSource",
        "name": {"type": "Property", "value": "Test Context Source"},
        "endpoint": {"type": "Property", "value": "http://example.com/ngsi-ld"},
        "information": [
            {"entities": [{"type": "Building"}]}
        ]
    }


class MockAsyncContextManager:
    """Helper class for mocking async context managers."""
    
    def __init__(self, return_value=None, side_effect=None):
        self.return_value = return_value
        self.side_effect = side_effect
        self.enter_calls = []
        self.exit_calls = []
    
    async def __aenter__(self):
        self.enter_calls.append(True)
        if self.side_effect:
            raise self.side_effect
        return self.return_value
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.exit_calls.append((exc_type, exc_val, exc_tb))
        return False


def create_mock_response(
    status_code: int = 200,
    json_data: Any = None,
    headers: Dict[str, str] = None,
    text: str = None
) -> MagicMock:
    """Create a mock HTTP response with given parameters."""
    mock_response = MagicMock(spec=Response)
    mock_response.status_code = status_code
    mock_response.headers = headers or {}
    mock_response.json.return_value = json_data or {}
    mock_response.text = text or json.dumps(json_data or {})
    return mock_response


def assert_valid_ngsi_entity(entity: Dict[str, Any]) -> None:
    """Assert that an entity follows NGSI-LD format."""
    assert "id" in entity
    assert "type" in entity
    assert isinstance(entity["id"], str)
    assert isinstance(entity["type"], str)
    assert entity["id"].startswith("urn:ngsi-ld:")


def assert_valid_ngsi_attribute(attr: Dict[str, Any]) -> None:
    """Assert that an attribute follows NGSI-LD format."""
    assert "type" in attr
    assert attr["type"] in ["Property", "Relationship", "GeoProperty"]
    
    if attr["type"] == "Property":
        assert "value" in attr
    elif attr["type"] == "Relationship":
        assert "object" in attr
    elif attr["type"] == "GeoProperty":
        assert "value" in attr
        assert isinstance(attr["value"], dict)
