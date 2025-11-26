# Copyright (c) 2025 Green Wave Team
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import logging
from typing import Any, Dict, List, Optional, Union

import httpx
from fastapi import APIRouter, HTTPException, Query, Response, status
from pydantic import BaseModel, Field, model_validator

from app.models.WaterQualityObserved import WaterQualityObserved
from app.services.water_quality_service import water_quality_service

router = APIRouter(prefix="/api/v1/water-quality", tags=["WaterQualityObserved"])
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
    summary="Query WaterQualityObserved Entities",
    description="Retrieve water quality observations with advanced filtering and pagination.",
)
async def get_all_water_quality(
    # Filtering
    id: Optional[str] = Query(
        None, description="Filter by observation ID(s), comma-separated"
    ),
    q: Optional[str] = Query(
        None, description="Query filter (e.g., 'pH>7', 'temperature<20')"
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
    Query WaterQualityObserved entities with comprehensive filtering options.

    Examples:
    - Get all: `/api/v1/water-quality/`
    - Alkaline water: `/api/v1/water-quality/?q=pH>8&format=simplified`
    - High turbidity: `/api/v1/water-quality/?q=turbidity>10`
    """
    try:
        result = await water_quality_service.get_all(
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
    summary="Get WaterQualityObserved by ID",
)
async def get_water_quality_by_id(
    entity_id: str,
    pick: Optional[str] = Query(None),
    attrs: Optional[str] = Query(None),
    format: Optional[str] = Query(None),
    options: Optional[str] = Query(None),
):
    """Retrieve a single WaterQualityObserved entity by ID."""
    try:
        return await water_quality_service.get_by_id(
            entity_id, pick=pick, attrs=attrs, format=format, options=options
        )
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "error": "Water quality observation not found",
                    "entity_id": entity_id,
                },
            ) from e
        raise HTTPException(
            status_code=e.response.status_code, detail=e.response.json()
        ) from e


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Create WaterQualityObserved",
    description="Create a new water quality observation. The 'dateObserved' field is required.",
)
async def create_water_quality(response: Response, entity_data: WaterQualityObserved):
    """Create a new WaterQualityObserved entity."""
    try:
        # Convert Pydantic model to dict for service layer
        entity_dict = entity_data.model_dump(exclude_unset=True)
        orion_response = await water_quality_service.create(entity_dict)
        response.headers["Location"] = orion_response.headers.get("Location", "")
        return {
            "message": "Water quality observation created successfully",
            "id": entity_data.id,
        }

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"error": "Validation error", "message": str(e)},
        ) from e
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 409:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"error": "Observation already exists", "id": entity_data.id},
            ) from e
        raise HTTPException(
            status_code=e.response.status_code, detail=e.response.json()
        ) from e


@router.patch(
    "/{entity_id:path}/attrs",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Update WaterQualityObserved Attributes",
)
async def update_water_quality_attributes(
    entity_id: str, update_data: Dict[str, NgsiLdAttributePatch]
):
    """Update specific attributes of a WaterQualityObserved entity."""
    try:
        payload = {k: v.model_dump(exclude_unset=True) for k, v in update_data.items()}
        await water_quality_service.update_attrs(entity_id, payload)
        return
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e)
        ) from e
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"error": "Observation not found"},
            ) from e
        raise HTTPException(
            status_code=e.response.status_code, detail=e.response.json()
        ) from e


@router.put(
    "/{entity_id:path}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Replace WaterQualityObserved",
)
async def replace_water_quality(entity_id: str, entity_data: WaterQualityObserved):
    """Replace an entire WaterQualityObserved entity."""
    try:
        await water_quality_service.replace(entity_id, entity_data)
        return
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"error": "Observation not found"},
            ) from e
        raise HTTPException(
            status_code=e.response.status_code, detail=e.response.json()
        ) from e


@router.delete(
    "/{entity_id:path}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete WaterQualityObserved",
)
async def delete_water_quality(entity_id: str):
    """Delete a WaterQualityObserved entity."""
    try:
        await water_quality_service.delete(entity_id)
        return
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"error": "Observation not found"},
            ) from e
        raise HTTPException(
            status_code=e.response.status_code, detail=e.response.json()
        ) from e


@router.delete(
    "/{entity_id:path}/attrs/{attribute_name}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete Attribute",
)
async def delete_water_quality_attribute(entity_id: str, attribute_name: str):
    """Delete a specific attribute from a WaterQualityObserved entity."""
    try:
        await water_quality_service.delete_attribute(entity_id, attribute_name)
        return
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code, detail=e.response.json()
        ) from e


# Batch Operations


@router.post("/batch/create", status_code=status.HTTP_201_CREATED)
async def batch_create_water_quality(request: BatchOperationRequest):
    """Create multiple water quality observations at once."""
    try:
        response = await water_quality_service.batch_create(request.entities)
        return response.json() if response.content else {"success": True}
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code, detail=e.response.json()
        ) from e


@router.post("/batch/upsert", status_code=status.HTTP_200_OK)
async def batch_upsert_water_quality(
    request: BatchOperationRequest,
    options: str = Query("update", description="'update' or 'replace'"),
):
    """Create or update multiple water quality observations."""
    try:
        response = await water_quality_service.batch_upsert(
            request.entities, options=options
        )
        return response.json() if response.content else {"success": True}
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code, detail=e.response.json()
        ) from e


@router.post("/batch/delete", status_code=status.HTTP_204_NO_CONTENT)
async def batch_delete_water_quality(request: BatchDeleteRequest):
    """Delete multiple water quality observations."""
    try:
        await water_quality_service.batch_delete(request.entity_ids)
        return
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code, detail=e.response.json()
        ) from e


# Convenience Endpoints


@router.get("/poor-quality/{parameter}", response_model=List[Dict[str, Any]])
async def get_poor_quality(
    parameter: str,
    min_value: Optional[float] = Query(None, description="Minimum acceptable value"),
    max_value: Optional[float] = Query(None, description="Maximum acceptable value"),
    limit: Optional[int] = Query(20, ge=1, le=100),
    format: Optional[str] = Query("simplified"),
):
    """
    Find water quality observations outside acceptable ranges.

    Parameters: pH, turbidity, temperature, conductivity, etc.
    """
    try:
        return await water_quality_service.find_poor_quality(
            parameter=parameter,
            min_value=min_value,
            max_value=max_value,
            limit=limit,
            format=format,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        ) from e
    except Exception as e:
        logger.error(f"Error in poor quality search: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        ) from e


@router.get("/contaminated/{contaminant}", response_model=List[Dict[str, Any]])
async def get_contaminated(
    contaminant: str,
    threshold: float = Query(..., description="Threshold value", ge=0),
    limit: Optional[int] = Query(20, ge=1, le=100),
    format: Optional[str] = Query("simplified"),
):
    """
    Find water samples with high contaminant levels.

    Contaminants: Pb (lead), Hg (mercury), Cd (cadmium), escherichiaColi, etc.
    """
    try:
        return await water_quality_service.find_contaminated(
            contaminant=contaminant, threshold=threshold, limit=limit, format=format
        )
    except Exception as e:
        logger.error(f"Error in contamination search: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        ) from e


@router.get("/recent", response_model=List[Dict[str, Any]])
async def get_recent_observations(
    since: str = Query(..., description="ISO8601 timestamp"),
    limit: Optional[int] = Query(50, ge=1, le=100),
    format: Optional[str] = Query("simplified"),
    pick: Optional[str] = Query(None),
):
    """Get recent water quality observations since a specific time."""
    try:
        return await water_quality_service.get_recent(
            since=since, limit=limit, format=format, pick=pick
        )
    except Exception as e:
        logger.error(f"Error in recent observations query: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        ) from e


@router.get("/location/nearby", response_model=List[Dict[str, Any]])
async def find_nearby_observations(
    lon: float = Query(..., ge=-180, le=180),
    lat: float = Query(..., ge=-90, le=90),
    max_distance: int = Query(5000, ge=1),
    limit: Optional[int] = Query(10, ge=1, le=100),
    format: Optional[str] = Query("simplified"),
    pick: Optional[str] = Query(None),
):
    """Find water quality observations near a location."""
    try:
        coordinates = f"[{lon},{lat}]"
        return await water_quality_service.find_by_location(
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
