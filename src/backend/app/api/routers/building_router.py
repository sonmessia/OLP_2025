# Copyright (c) 2025 Green Wave Team
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import logging
from typing import Any, Dict, List, Optional, Union

import httpx
from fastapi import APIRouter, HTTPException, Query, Response, status
from pydantic import BaseModel, Field, model_validator

from app.models.Building import Building
from app.services.building_service import building_service

router = APIRouter(prefix="/api/v1/buildings", tags=["Building"])
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
    summary="Query Building Entities",
    description="Retrieve a list of Building entities with advanced filtering and pagination.",
)
async def get_all_buildings(
    # Filtering
    id: Optional[str] = Query(
        None, description="Filter by building ID(s), comma-separated"
    ),
    q: Optional[str] = Query(
        None,
        description="Query filter (e.g., 'floorsAboveGround>5', 'category==hotel')",
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
    Query Building entities with comprehensive filtering options.
    """
    try:
        result = await building_service.get_all(
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
        ) from e
    except httpx.HTTPStatusError as e:
        logger.error(f"Orion-LD error: {e.response.status_code} - {e.response.text}")
        raise HTTPException(
            status_code=e.response.status_code, detail=e.response.json()
        ) from e
    except httpx.RequestError as e:
        logger.error(f"Connection error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={"error": "Service Unavailable"},
        ) from e


@router.get(
    "/{entity_id:path}",
    response_model=Dict[str, Any],
    summary="Get Building by ID",
)
async def get_building_by_id(
    entity_id: str,
    pick: Optional[str] = Query(None),
    attrs: Optional[str] = Query(None),
    format: Optional[str] = Query(None),
    options: Optional[str] = Query(None),
):
    """Retrieve a single Building entity by ID."""
    try:
        return await building_service.get_by_id(
            entity_id, pick=pick, attrs=attrs, format=format, options=options
        )
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"error": "Building not found", "entity_id": entity_id},
            ) from e
        raise HTTPException(
            status_code=e.response.status_code, detail=e.response.json()
        ) from e


@router.post("/", status_code=status.HTTP_201_CREATED, summary="Create Building")
async def create_building(
    response: Response,
    entity_data: Building,
):
    """Create a new Building entity."""
    try:
        # Convert Pydantic model to dict for service layer
        entity_dict = entity_data.model_dump(exclude_unset=True)
        orion_response = await building_service.create(entity_dict)
        response.headers["Location"] = orion_response.headers.get("Location", "")
        return {"message": "Building created successfully", "id": entity_data.id}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e)
        ) from e
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 409:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"error": "Building already exists", "id": entity_data.id},
            ) from e
        raise HTTPException(
            status_code=e.response.status_code, detail=e.response.json()
        ) from e


@router.patch(
    "/{entity_id:path}/attrs",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Update Building Attributes",
)
async def update_building_attributes(
    entity_id: str, update_data: Dict[str, NgsiLdAttributePatch]
):
    """Update specific attributes of a Building entity."""
    try:
        payload = {k: v.model_dump(exclude_unset=True) for k, v in update_data.items()}
        await building_service.update_attrs(entity_id, payload)
        return
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e)
        ) from e
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"error": "Building not found"},
            ) from e
        raise HTTPException(
            status_code=e.response.status_code, detail=e.response.json()
        ) from e


@router.put(
    "/{entity_id:path}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Replace Building",
)
async def replace_building(entity_id: str, entity_data: Building):
    """Replace an entire Building entity."""
    try:
        await building_service.replace(entity_id, entity_data)
        return
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"error": "Building not found"},
            ) from e
        raise HTTPException(
            status_code=e.response.status_code, detail=e.response.json()
        ) from e


@router.delete(
    "/{entity_id:path}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete Building",
)
async def delete_building(entity_id: str):
    """Delete a Building entity."""
    try:
        await building_service.delete(entity_id)
        return
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"error": "Building not found"},
            ) from e
        raise HTTPException(
            status_code=e.response.status_code, detail=e.response.json()
        ) from e


@router.delete(
    "/{entity_id:path}/attrs/{attribute_name}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete Building Attribute",
)
async def delete_building_attribute(entity_id: str, attribute_name: str):
    """Delete a specific attribute from a Building."""
    try:
        await building_service.delete_attribute(entity_id, attribute_name)
        return
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code, detail=e.response.json()
        ) from e


# Batch Operations


@router.post("/batch/create", status_code=status.HTTP_201_CREATED)
async def batch_create_buildings(request: BatchOperationRequest):
    """Create multiple buildings at once."""
    try:
        response = await building_service.batch_create(request.entities)
        return response.json() if response.content else {"success": True}
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code, detail=e.response.json()
        ) from e


@router.post("/batch/upsert", status_code=status.HTTP_200_OK)
async def batch_upsert_buildings(
    request: BatchOperationRequest,
    options: str = Query("update", description="'update' or 'replace'"),
):
    """Create or update multiple buildings."""
    try:
        response = await building_service.batch_upsert(
            request.entities, options=options
        )
        return response.json() if response.content else {"success": True}
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code, detail=e.response.json()
        ) from e


@router.post("/batch/delete", status_code=status.HTTP_204_NO_CONTENT)
async def batch_delete_buildings(request: BatchDeleteRequest):
    """Delete multiple buildings."""
    try:
        await building_service.batch_delete(request.entity_ids)
        return
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code, detail=e.response.json()
        ) from e


# Convenience Endpoints


@router.get("/location/nearby", response_model=List[Dict[str, Any]])
async def find_nearby_buildings(
    lon: float = Query(..., ge=-180, le=180),
    lat: float = Query(..., ge=-90, le=90),
    max_distance: int = Query(1000, ge=1),
    limit: Optional[int] = Query(10, ge=1, le=100),
    format: Optional[str] = Query("simplified"),
    pick: Optional[str] = Query(None),
):
    """Find buildings near a location."""
    try:
        coordinates = f"[{lon},{lat}]"
        return await building_service.find_by_location(
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
        ) from e


@router.get("/category/{category}", response_model=List[Dict[str, Any]])
async def get_buildings_by_category(
    category: str,
    limit: Optional[int] = Query(20, ge=1, le=100),
    format: Optional[str] = Query("simplified"),
):
    """Find buildings by category."""
    try:
        return await building_service.find_by_category(
            category=category, limit=limit, format=format
        )
    except Exception as e:
        logger.error(f"Error in category search: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        ) from e


@router.get("/tall", response_model=List[Dict[str, Any]])
async def get_tall_buildings(
    min_floors: int = Query(10, ge=1),
    limit: Optional[int] = Query(20, ge=1, le=100),
    format: Optional[str] = Query("simplified"),
):
    """Find tall buildings."""
    try:
        return await building_service.find_tall_buildings(
            min_floors=min_floors, limit=limit, format=format
        )
    except Exception as e:
        logger.error(f"Error in tall buildings search: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        ) from e
