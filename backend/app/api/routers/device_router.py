import logging
from typing import Any, Dict, List, Optional, Union

import httpx
from fastapi import APIRouter, Body, HTTPException, Query, Response, status
from pydantic import BaseModel, Field, model_validator

from app.services.device_service import device_service

router = APIRouter(prefix="/api/v1/devices", tags=["Device"])
logger = logging.getLogger(__name__)


class NgsiLdAttributePatch(BaseModel):
    """Model to validate attribute structure for updates."""

    type: str = Field(
        default="Property", pattern="^(Property|Relationship|GeoProperty)$"
    )
    value: Optional[Any] = None
    object: Optional[str] = None
    observedAt: Optional[str] = None
    unitCode: Optional[str] = None

    @model_validator(mode="after")
    def check_value_or_object_exists(self) -> "NgsiLdAttributePatch":
        if self.type == "Property" and self.value is None:
            raise ValueError('Property type attributes must have a "value" field.')
        if self.type == "Relationship" and self.object is None:
            raise ValueError(
                'Relationship type attributes must have an "object" field.'
            )
        return self


class BatchOperationRequest(BaseModel):
    """Model for batch operations."""

    entities: List[Dict[str, Any]] = Field(..., min_length=1)


class BatchDeleteRequest(BaseModel):
    """Model for batch delete operations."""

    entity_ids: List[str] = Field(..., min_length=1)


@router.get(
    "/",
    response_model=Union[List[Dict[str, Any]], int],
    summary="Query Device Entities",
    description="Retrieve IoT devices and sensors with advanced filtering and pagination.",
)
async def get_all_devices(
    # Filtering
    id: Optional[str] = Query(
        None, description="Filter by device ID(s), comma-separated"
    ),
    q: Optional[str] = Query(
        None, description="Query filter (e.g., 'batteryLevel<0.2', 'category==sensor')"
    ),
    # Attribute selection
    pick: Optional[str] = Query(
        None, description="Preferred - Comma-separated list of attributes"
    ),
    attrs: Optional[str] = Query(
        None, description="Legacy - Comma-separated list of attributes"
    ),
    # Geo-spatial
    georel: Optional[str] = Query(None, description="Geo-relationship"),
    geometry: Optional[str] = Query(None, description="Geometry type"),
    coordinates: Optional[str] = Query(None, description="Coordinates array as string"),
    geoproperty: Optional[str] = Query(None, description="Geo property name"),
    # Pagination
    limit: Optional[int] = Query(
        None, ge=1, le=1000, description="Maximum results (1-1000)"
    ),
    offset: Optional[int] = Query(None, ge=0, description="Skip results"),
    # Result options
    count: bool = Query(False, description="Return count only"),
    format: Optional[str] = Query(None, description="'simplified' for key-value pairs"),
    options: Optional[str] = Query(
        None, description="Query options (e.g., 'sysAttrs')"
    ),
    # Federation
    local: Optional[bool] = Query(None, description="Query only local entities"),
):
    """
    Query Device entities with comprehensive filtering options.

    Examples:
    - Get all: `/api/v1/devices/`
    - Low battery: `/api/v1/devices/?q=batteryLevel<0.2&format=simplified`
    - Sensors only: `/api/v1/devices/?q=category==sensor`
    """
    try:
        result = await device_service.get_all(
            id=id,
            q=q,
            pick=pick,
            attrs=attrs,
            georel=georel,
            geometry=geometry,
            coordinates=coordinates,
            geoproperty=geoproperty,
            limit=limit,
            offset=offset,
            count=count,
            format=format,
            options=options,
            local=local,
        )
        return result

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "Invalid query parameters", "message": str(e)},
        )
    except httpx.HTTPStatusError as e:
        logger.error(f"Orion-LD error: {e.response.status_code} - {e.response.text}")
        raise HTTPException(
            status_code=e.response.status_code, detail=e.response.json()
        )
    except httpx.RequestError as e:
        logger.error(f"Connection error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={"error": "Service Unavailable"},
        )


@router.get(
    "/{entity_id:path}",
    response_model=Dict[str, Any],
    summary="Get Device by ID",
)
async def get_device_by_id(
    entity_id: str,
    pick: Optional[str] = Query(None),
    attrs: Optional[str] = Query(None),
    format: Optional[str] = Query(None),
    options: Optional[str] = Query(None),
):
    """Retrieve a single Device entity by ID."""
    try:
        return await device_service.get_by_id(
            entity_id, pick=pick, attrs=attrs, format=format, options=options
        )
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"error": "Device not found", "entity_id": entity_id},
            )
        raise HTTPException(
            status_code=e.response.status_code, detail=e.response.json()
        )


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Create Device",
)
async def create_device(
    response: Response,
    entity_data: Dict[str, Any] = Body(
        ...,
        example={
            "id": "urn:ngsi-ld:Device:Sensor-Madrid-001",
            "category": {"type": "Property", "value": ["sensor"]},
            "controlledProperty": {
                "type": "Property",
                "value": ["temperature", "humidity"],
            },
            "serialNumber": {"type": "Property", "value": "SN-12345"},
            "batteryLevel": {"type": "Property", "value": 0.85},
        },
    ),
):
    """Create a new Device entity."""
    try:
        orion_response = await device_service.create(entity_data)
        response.headers["Location"] = orion_response.headers.get("Location", "")
        return {"message": "Device created successfully", "id": entity_data.get("id")}

    except httpx.HTTPStatusError as e:
        if e.response.status_code == 409:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"error": "Device already exists"},
            )
        raise HTTPException(
            status_code=e.response.status_code, detail=e.response.json()
        )


@router.patch(
    "/{entity_id:path}/attrs",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Update Device Attributes",
)
async def update_device_attributes(
    entity_id: str, update_data: Dict[str, NgsiLdAttributePatch]
):
    """Update specific attributes of a Device entity."""
    try:
        payload = {k: v.model_dump(exclude_unset=True) for k, v in update_data.items()}
        await device_service.update_attrs(entity_id, payload)
        return
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e)
        )
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"error": "Device not found"},
            )
        raise HTTPException(
            status_code=e.response.status_code, detail=e.response.json()
        )


@router.put(
    "/{entity_id:path}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Replace Device",
)
async def replace_device(entity_id: str, entity_data: Dict[str, Any] = Body(...)):
    """Replace an entire Device entity."""
    try:
        await device_service.replace(entity_id, entity_data)
        return
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"error": "Device not found"},
            )
        raise HTTPException(
            status_code=e.response.status_code, detail=e.response.json()
        )


@router.delete(
    "/{entity_id:path}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete Device",
)
async def delete_device(entity_id: str):
    """Delete a Device entity."""
    try:
        await device_service.delete(entity_id)
        return
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"error": "Device not found"},
            )
        raise HTTPException(
            status_code=e.response.status_code, detail=e.response.json()
        )


@router.delete(
    "/{entity_id:path}/attrs/{attribute_name}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete Device Attribute",
)
async def delete_device_attribute(entity_id: str, attribute_name: str):
    """Delete a specific attribute from a Device entity."""
    try:
        await device_service.delete_attribute(entity_id, attribute_name)
        return
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code, detail=e.response.json()
        )


# Batch Operations


@router.post("/batch/create", status_code=status.HTTP_201_CREATED)
async def batch_create_devices(request: BatchOperationRequest):
    """Create multiple devices at once."""
    try:
        response = await device_service.batch_create(request.entities)
        return response.json() if response.content else {"success": True}
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code, detail=e.response.json()
        )


@router.post("/batch/upsert", status_code=status.HTTP_200_OK)
async def batch_upsert_devices(
    request: BatchOperationRequest,
    options: str = Query("update", description="'update' or 'replace'"),
):
    """Create or update multiple devices."""
    try:
        response = await device_service.batch_upsert(request.entities, options=options)
        return response.json() if response.content else {"success": True}
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code, detail=e.response.json()
        )


@router.post("/batch/delete", status_code=status.HTTP_204_NO_CONTENT)
async def batch_delete_devices(request: BatchDeleteRequest):
    """Delete multiple devices."""
    try:
        await device_service.batch_delete(request.entity_ids)
        return
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code, detail=e.response.json()
        )


# Convenience Endpoints


@router.get("/category/{category}", response_model=List[Dict[str, Any]])
async def get_devices_by_category(
    category: str,
    limit: Optional[int] = Query(50, ge=1, le=100),
    format: Optional[str] = Query("simplified"),
):
    """
    Find devices by category.

    Categories: sensor, actuator, meter, HVAC, network, multimedia
    """
    try:
        return await device_service.find_by_category(
            category=category, limit=limit, format=format
        )
    except Exception as e:
        logger.error(f"Error in category search: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get("/low-battery", response_model=List[Dict[str, Any]])
async def get_low_battery_devices(
    threshold: float = Query(
        0.2, description="Battery level threshold (0.0-1.0)", ge=0, le=1
    ),
    limit: Optional[int] = Query(20, ge=1, le=100),
    format: Optional[str] = Query("simplified"),
):
    """Find devices with low battery levels."""
    try:
        return await device_service.find_low_battery(
            threshold=threshold, limit=limit, format=format
        )
    except Exception as e:
        logger.error(f"Error in low battery search: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get("/state/{device_state}", response_model=List[Dict[str, Any]])
async def get_devices_by_state(
    device_state: str,
    limit: Optional[int] = Query(50, ge=1, le=100),
    format: Optional[str] = Query("simplified"),
):
    """
    Find devices by operational state.

    States: active, inactive, error, maintenance, etc.
    """
    try:
        return await device_service.find_by_state(
            device_state=device_state, limit=limit, format=format
        )
    except Exception as e:
        logger.error(f"Error in state search: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get("/property/{controlled_property}", response_model=List[Dict[str, Any]])
async def get_devices_by_property(
    controlled_property: str,
    limit: Optional[int] = Query(30, ge=1, le=100),
    format: Optional[str] = Query("simplified"),
):
    """
    Find devices that control/sense a specific property.

    Properties: temperature, humidity, pressure, motion, etc.
    """
    try:
        return await device_service.find_by_controlled_property(
            controlled_property=controlled_property, limit=limit, format=format
        )
    except Exception as e:
        logger.error(f"Error in property search: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get("/inactive", response_model=List[Dict[str, Any]])
async def get_inactive_devices(
    days: int = Query(7, description="Days without data", ge=1),
    limit: Optional[int] = Query(20, ge=1, le=100),
    format: Optional[str] = Query("simplified"),
):
    """Find devices that haven't reported data recently."""
    try:
        return await device_service.find_inactive_devices(
            days_inactive=days, limit=limit, format=format
        )
    except Exception as e:
        logger.error(f"Error in inactive devices search: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get("/location/nearby", response_model=List[Dict[str, Any]])
async def find_nearby_devices(
    lon: float = Query(..., ge=-180, le=180),
    lat: float = Query(..., ge=-90, le=90),
    max_distance: int = Query(1000, ge=1),
    limit: Optional[int] = Query(10, ge=1, le=100),
    format: Optional[str] = Query("simplified"),
    pick: Optional[str] = Query(None),
):
    """Find devices near a location."""
    try:
        coordinates = f"[{lon},{lat}]"
        return await device_service.find_by_location(
            coordinates=coordinates,
            max_distance=max_distance,
            limit=limit,
            format=format,
            pick=pick,
        )
    except Exception as e:
        logger.error(f"Error in nearby search: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
