import logging
from typing import Any, Dict, List, Optional, Union

import httpx
from fastapi import APIRouter, Body, HTTPException, Query, Response, status
from pydantic import BaseModel, Field, model_validator

from app.services.air_quality_service import air_quality_service

router = APIRouter(prefix="/api/v1/air-quality", tags=["AirQualityObserved"])
logger = logging.getLogger(__name__)


class NgsiLdAttributePatch(BaseModel):
    """
    Model to validate the structure of an attribute when updating (PATCH).
    Ensures the payload sent to Orion-LD is always valid.
    """

    type: str = Field(
        default="Property",
        pattern="^(Property|Relationship|GeoProperty|VocabProperty)$",
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
    summary="Query AirQualityObserved Entities",
    description="Retrieve a list of AirQualityObserved entities with advanced filtering, pagination, and formatting options.",
)
async def get_all_air_quality(
    # Filtering
    id: Optional[str] = Query(
        None,
        description="Filter by entity ID(s), comma-separated (e.g., 'urn:ngsi-ld:AirQualityObserved:001,urn:ngsi-ld:AirQualityObserved:002')",
    ),
    q: Optional[str] = Query(
        None,
        description="NGSI-LD query filter string (e.g., 'pm25>50', 'temperature>25;pm25<100')",
    ),
    # Attribute selection
    pick: Optional[str] = Query(
        None,
        description="Preferred - Comma-separated list of attributes to select (e.g., 'id,type,pm25,temperature')",
    ),
    attrs: Optional[str] = Query(
        None, description="Legacy - Comma-separated list of attributes to include"
    ),
    # Geo-spatial queries
    georel: Optional[str] = Query(
        None, description="Geo-relationship (e.g., 'near;maxDistance==5000')"
    ),
    geometry: Optional[str] = Query(
        None,
        description="Geometry type (Point, LineString, Polygon, MultiPoint, MultiLineString, MultiPolygon)",
    ),
    coordinates: Optional[str] = Query(
        None, description="Coordinates array as string (e.g., '[-3.703790,40.416775]')"
    ),
    geoproperty: Optional[str] = Query(
        None, description="Property to use for geo-queries (default: 'location')"
    ),
    # Pagination
    limit: Optional[int] = Query(
        None, ge=1, le=1000, description="Maximum number of results to return (1-1000)"
    ),
    offset: Optional[int] = Query(
        None, ge=0, description="Number of results to skip for pagination"
    ),
    # Result options
    count: bool = Query(
        False,
        description="If true, return only the total count of matching entities in response",
    ),
    format: Optional[str] = Query(
        None,
        description="Response format: 'simplified' for key-value pairs, omit for normalized NGSI-LD",
    ),
    options: Optional[str] = Query(
        None,
        description="Query options (e.g., 'sysAttrs' to include createdAt/modifiedAt)",
    ),
    # Federation
    local: Optional[bool] = Query(
        None, description="If true, query only local entities (not federated)"
    ),
):
    """
    Query AirQualityObserved entities with comprehensive filtering options.

    Examples:
    - Get all entities: `/api/v1/air-quality/`
    - Get with high PM2.5: `/api/v1/air-quality/?q=pm25>50&limit=10`
    - Get specific attributes: `/api/v1/air-quality/?pick=id,type,pm25,temperature&format=simplified`
    - Get count only: `/api/v1/air-quality/?count=true`
    - Geo-spatial query: `/api/v1/air-quality/?georel=near;maxDistance==5000&geometry=Point&coordinates=[-3.70,40.41]`
    """
    try:
        result = await air_quality_service.get_all(
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
            status_code=e.response.status_code,
            detail=(
                e.response.json()
                if e.response.headers.get("content-type") == "application/json"
                else {"error": e.response.text}
            ),
        )
    except httpx.RequestError as e:
        logger.error(f"Connection error to Orion-LD: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "error": "Service Unavailable",
                "message": "Cannot connect to Orion-LD broker",
            },
        )


@router.get(
    "/{entity_id:path}",
    response_model=Dict[str, Any],
    summary="Get AirQualityObserved Entity by ID",
    description="Retrieve a single AirQualityObserved entity by its full URN with optional attribute selection.",
)
async def get_air_quality_by_id(
    entity_id: str,
    pick: Optional[str] = Query(
        None, description="Preferred - Comma-separated list of attributes to select"
    ),
    attrs: Optional[str] = Query(
        None, description="Legacy - Comma-separated list of attributes to include"
    ),
    format: Optional[str] = Query(
        None, description="Response format: 'simplified' for key-value pairs"
    ),
    options: Optional[str] = Query(
        None, description="Query options (e.g., 'sysAttrs')"
    ),
):
    """
    Retrieve a single AirQualityObserved entity by its ID.

    Examples:
    - Get full entity: `/api/v1/air-quality/urn:ngsi-ld:AirQualityObserved:Madrid-001`
    - Get simplified: `/api/v1/air-quality/urn:ngsi-ld:AirQualityObserved:Madrid-001?format=simplified`
    - Get specific attrs: `/api/v1/air-quality/urn:ngsi-ld:AirQualityObserved:Madrid-001?pick=id,type,pm25&format=simplified`
    """
    try:
        return await air_quality_service.get_by_id(
            entity_id, pick=pick, attrs=attrs, format=format, options=options
        )
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"error": "Entity not found", "entity_id": entity_id},
            )
        raise HTTPException(
            status_code=e.response.status_code,
            detail=(
                e.response.json()
                if e.response.headers.get("content-type") == "application/json"
                else {"error": e.response.text}
            ),
        )
    except httpx.RequestError as e:
        logger.error(f"Connection error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={"error": "Service Unavailable"},
        )


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Create AirQualityObserved Entity",
    description="Create a new AirQualityObserved entity. The 'dateObserved' field is required.",
)
async def create_air_quality(
    response: Response,
    entity_data: Dict[str, Any] = Body(
        ...,
        example={
            "id": "urn:ngsi-ld:AirQualityObserved:Madrid-001",
            "dateObserved": "2025-11-15T10:31:41Z",
            "temperature": {"type": "Property", "value": 25.5, "unitCode": "CEL"},
            "pm25": {"type": "Property", "value": 35.2, "unitCode": "GQ"},
            "location": {
                "type": "GeoProperty",
                "value": {"type": "Point", "coordinates": [-3.703790, 40.416775]},
            },
        },
    ),
):
    """
    Create a new AirQualityObserved entity.

    The entity must include:
    - `id`: Unique identifier (URN format)
    - `dateObserved`: Observation timestamp (ISO8601 format)

    Returns a 201 status with Location header pointing to the created entity.
    """
    try:
        orion_response = await air_quality_service.create(entity_data)
        response.headers["Location"] = orion_response.headers.get("Location", "")
        return {"message": "Entity created successfully", "id": entity_data.get("id")}

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"error": "Validation error", "message": str(e)},
        )
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 409:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"error": "Entity already exists", "id": entity_data.get("id")},
            )
        raise HTTPException(
            status_code=e.response.status_code,
            detail=(
                e.response.json()
                if e.response.headers.get("content-type") == "application/json"
                else {"error": e.response.text}
            ),
        )


@router.patch(
    "/{entity_id:path}/attrs",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Update Entity Attributes (Partial Update)",
    description="Update one or more attributes of an AirQualityObserved entity.",
)
async def update_air_quality_attributes(
    entity_id: str,
    update_data: Dict[str, NgsiLdAttributePatch] = Body(
        ...,
        example={
            "temperature": {"type": "Property", "value": 26.8, "unitCode": "CEL"},
            "pm25": {"type": "Property", "value": 42.1, "unitCode": "GQ"},
        },
    ),
):
    """
    Update specific attributes of an AirQualityObserved entity.

    This performs a partial update - only the specified attributes are updated,
    existing attributes not mentioned in the request are preserved.
    """
    try:
        payload_to_send = {
            key: value.model_dump(exclude_unset=True)
            for key, value in update_data.items()
        }
        await air_quality_service.update_attrs(entity_id, payload_to_send)
        return

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"error": "Validation error", "message": str(e)},
        )
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"error": "Entity not found", "entity_id": entity_id},
            )
        raise HTTPException(
            status_code=e.response.status_code,
            detail=(
                e.response.json()
                if e.response.headers.get("content-type") == "application/json"
                else {"error": e.response.text}
            ),
        )


@router.put(
    "/{entity_id:path}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Replace Entity (Full Update)",
    description="Replace an entire AirQualityObserved entity with new data.",
)
async def replace_air_quality(entity_id: str, entity_data: Dict[str, Any] = Body(...)):
    """
    Replace an entire entity. All existing attributes will be removed
    and replaced with the new data provided.
    """
    try:
        await air_quality_service.replace(entity_id, entity_data)
        return

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"error": "Validation error", "message": str(e)},
        )
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"error": "Entity not found", "entity_id": entity_id},
            )
        raise HTTPException(
            status_code=e.response.status_code,
            detail=(
                e.response.json()
                if e.response.headers.get("content-type") == "application/json"
                else {"error": e.response.text}
            ),
        )


@router.delete(
    "/{entity_id:path}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete AirQualityObserved Entity",
    description="Delete an AirQualityObserved entity by its ID.",
)
async def delete_air_quality(entity_id: str):
    """
    Delete an AirQualityObserved entity.

    Returns 204 No Content on success, 404 if entity not found.
    """
    try:
        await air_quality_service.delete(entity_id)
        return

    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"error": "Entity not found", "entity_id": entity_id},
            )
        raise HTTPException(
            status_code=e.response.status_code,
            detail=(
                e.response.json()
                if e.response.headers.get("content-type") == "application/json"
                else {"error": e.response.text}
            ),
        )


@router.delete(
    "/{entity_id:path}/attrs/{attribute_name}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete Entity Attribute",
    description="Delete a specific attribute from an AirQualityObserved entity.",
)
async def delete_air_quality_attribute(entity_id: str, attribute_name: str):
    """
    Delete a specific attribute from an entity.

    Example: DELETE /api/v1/air-quality/urn:ngsi-ld:AirQualityObserved:Madrid-001/attrs/relativeHumidity
    """
    try:
        await air_quality_service.delete_attribute(entity_id, attribute_name)
        return

    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"error": "Entity or attribute not found"},
            )
        raise HTTPException(
            status_code=e.response.status_code,
            detail=(
                e.response.json()
                if e.response.headers.get("content-type") == "application/json"
                else {"error": e.response.text}
            ),
        )


# ==================== BATCH OPERATIONS ====================


@router.post(
    "/batch/create",
    status_code=status.HTTP_201_CREATED,
    summary="Batch Create Entities",
    description="Create multiple AirQualityObserved entities in a single request.",
)
async def batch_create_air_quality(request: BatchOperationRequest):
    """
    Create multiple entities at once. Fails if any entity already exists.

    Returns a list of created entity IDs or error details.
    """
    try:
        response = await air_quality_service.batch_create(request.entities)
        return response.json() if response.content else {"success": True}

    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code,
            detail=(
                e.response.json()
                if e.response.headers.get("content-type") == "application/json"
                else {"error": e.response.text}
            ),
        )


@router.post(
    "/batch/upsert",
    status_code=status.HTTP_200_OK,
    summary="Batch Upsert Entities",
    description="Create or update multiple AirQualityObserved entities.",
)
async def batch_upsert_air_quality(
    request: BatchOperationRequest,
    options: str = Query(
        "update",
        description="'update' to keep existing attrs, 'replace' to remove unlisted attrs",
    ),
):
    """
    Create or update multiple entities.

    - If entity exists: updates it (behavior depends on 'options' parameter)
    - If entity doesn't exist: creates it
    """
    try:
        response = await air_quality_service.batch_upsert(
            request.entities, options=options
        )
        return response.json() if response.content else {"success": True}

    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code,
            detail=(
                e.response.json()
                if e.response.headers.get("content-type") == "application/json"
                else {"error": e.response.text}
            ),
        )


@router.post(
    "/batch/delete",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Batch Delete Entities",
    description="Delete multiple AirQualityObserved entities by their IDs.",
)
async def batch_delete_air_quality(request: BatchDeleteRequest):
    """
    Delete multiple entities at once.

    Example request body:
    {
        "entity_ids": [
            "urn:ngsi-ld:AirQualityObserved:Madrid-001",
            "urn:ngsi-ld:AirQualityObserved:Madrid-002"
        ]
    }
    """
    try:
        await air_quality_service.batch_delete(request.entity_ids)
        return

    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code,
            detail=(
                e.response.json()
                if e.response.headers.get("content-type") == "application/json"
                else {"error": e.response.text}
            ),
        )


# ==================== CONVENIENCE ENDPOINTS ====================
