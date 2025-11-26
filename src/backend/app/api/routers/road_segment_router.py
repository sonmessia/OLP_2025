# Copyright (c) 2025 Green Wave Team
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import logging
from typing import Any, Dict, List, Optional, Union

import httpx
from fastapi import APIRouter, HTTPException, Query, Response, status
from pydantic import BaseModel, Field, model_validator

from app.models.RoadSegment import RoadSegment
from app.services.road_segment_service import road_segment_service

router = APIRouter(prefix="/api/v1/road-segments", tags=["RoadSegment"])
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
    summary="Query RoadSegment Entities",
    description="Retrieve a list of RoadSegment entities with advanced filtering, pagination, and formatting options.",
)
async def get_all_road_segments(
    # Filtering
    id: Optional[str] = Query(
        None,
        description="Filter by entity ID(s), comma-separated (e.g., 'urn:ngsi-ld:RoadSegment:001,urn:ngsi-ld:RoadSegment:002')",
    ),
    q: Optional[str] = Query(
        None,
        description="NGSI-LD query filter string (e.g., 'roadClass==MAJOR_CITY_ROAD', 'length>5.0')",
    ),
    # Attribute selection
    pick: Optional[str] = Query(
        None,
        description="Preferred - Comma-separated list of attributes to select (e.g., 'id,type,roadName,roadClass,length')",
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
        description="Geometry type for geo-spatial queries (Point, LineString, Polygon, MultiPoint, MultiLineString, MultiPolygon)",
    ),
    coordinates: Optional[str] = Query(
        None,
        description="Coordinates for geo-spatial queries as JSON array string (e.g., '[-3.7038,40.4168]' or '[[-3.7038,40.4168],[-3.7038,40.4268]]')",
    ),
    geoproperty: Optional[str] = Query(
        None,
        description="Property to use for geo-spatial queries (default: 'location')",
    ),
    # Pagination
    limit: Optional[int] = Query(
        None, ge=1, le=1000, description="Maximum number of results to return (1-1000)"
    ),
    offset: Optional[int] = Query(
        None, ge=0, description="Number of results to skip for pagination"
    ),
    # Result options
    count: Optional[bool] = Query(
        False,
        description="If true, returns only the count of matching entities in the response headers",
    ),
    format: Optional[str] = Query(
        None,
        description="Response format. Use 'simplified' for key-value pairs format",
    ),
    options: Optional[str] = Query(
        None,
        description="Query options (e.g., 'sysAttrs' for system attributes, 'keyValues' for key-value format)",
    ),
    # Federation
    local: Optional[bool] = Query(
        None,
        description="If true, query only local entities (not federated from remote sources)",
    ),
):
    """
    Get RoadSegment entities with comprehensive filtering and pagination.

    Examples:
        - Get all entities: GET /
        - Get entities by ID: GET /?id=urn:ngsi-ld:RoadSegment:001
        - Get major city roads: GET /?q=roadClass==MAJOR_CITY_ROAD
        - Get roads with specific speed limit: GET /?q=maximumAllowedSpeed==50
        - Get entities with pagination: GET /?limit=20&offset=40
        - Get count only: GET /?count=true
        - Get simplified format: GET /?format=simplified&pick=id,type,roadName
        - Geo-spatial query: GET /?georel=near;maxDistance==2000&geometry=Point&coordinates=[-3.7038,40.4168]
    """
    try:
        return await road_segment_service.get_all(
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
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error retrieving road segments: {e.response.text}")
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"Failed to retrieve road segments: {e.response.text}",
        ) from e
    except Exception as e:
        logger.error(f"Unexpected error retrieving road segments: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}",
        ) from e


@router.get(
    "/{entity_id}",
    response_model=Dict[str, Any],
    summary="Get RoadSegment by ID",
    description="Retrieve a specific RoadSegment entity by its unique identifier.",
)
async def get_road_segment_by_id(
    entity_id: str,
    attrs: Optional[str] = Query(
        None,
        description="Comma-separated list of attribute names to retrieve (e.g., 'id,type,roadName,roadClass,length')",
    ),
    options: Optional[str] = Query(
        None,
        description="Query options (e.g., 'keyValues' for key-value format, 'sysAttrs' for system attributes)",
    ),
):
    """
    Get a specific RoadSegment entity by its ID.

    Examples:
        - Get full entity: GET /urn:ngsi-ld:RoadSegment:001
        - Get specific attributes: GET /urn:ngsi-ld:RoadSegment:001?attrs=id,type,roadName,roadClass
        - Get in key-value format: GET /urn:ngsi-ld:RoadSegment:001?option=keyValues
    """
    try:
        return await road_segment_service.get_by_id(
            entity_id=entity_id, attrs=attrs, options=options
        )
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"RoadSegment entity with ID '{entity_id}' not found",
            ) from e
        logger.error(f"HTTP error retrieving entity {entity_id}: {e.response.text}")
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"Failed to retrieve entity: {e.response.text}",
        ) from e
    except Exception as e:
        logger.error(f"Unexpected error retrieving entity {entity_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}",
        ) from e


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Create RoadSegment Entity",
    description="Create a new RoadSegment entity with the provided data.",
)
async def create_road_segment(
    entity_data: Dict[str, Any],
):
    """
    Create a new RoadSegment entity.

    Required fields:
        - id: Unique identifier (URN format recommended)

    Optional fields:
        - roadName: Name of the road
        - roadClass: Type of road (MAJOR_CITY_ROAD, MINOR_CITY_ROAD, etc.)
        - length: Length in kilometers
        - width: Width in meters
        - totalLaneNumber: Number of lanes
        - maximumAllowedSpeed: Speed limit in km/h
        - location: GeoJSON location data
        - address: Address information
        - Any other standard NGSI-LD attributes

    Example:
    {
        "id": "urn:ngsi-ld:RoadSegment:Madrid-001",
        "roadName": "Gran Via",
        "roadClass": "MAJOR_CITY_ROAD",
        "length": 2.5,
        "width": 12.0,
        "totalLaneNumber": 4,
        "maximumAllowedSpeed": 50.0,
        "location": {
            "type": "LineString",
            "coordinates": [[-3.7038, 40.4168], [-3.7038, 40.4268]]
        }
    }
    """
    try:
        response = await road_segment_service.create(entity_data)
        return Response(
            content=response.content,
            status_code=response.status_code,
            headers=dict(response.headers),
        )
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error creating entity: {e.response.text}")
        if e.response.status_code == 409:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"RoadSegment entity already exists: {e.response.text}",
            ) from e
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"Failed to create entity: {e.response.text}",
        ) from e
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Validation error: {str(e)}",
        ) from e
    except Exception as e:
        logger.error(f"Unexpected error creating entity: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}",
        ) from e


@router.patch(
    "/{entity_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Update RoadSegment Entity",
    description="Update specific attributes of an existing RoadSegment entity.",
)
async def update_road_segment(
    entity_id: str,
    attributes: Dict[str, NgsiLdAttributePatch],
):
    """
    Update specific attributes of a RoadSegment entity.

    Provide only the attributes you want to update in the request body.

    Example:
    {
        "maximumAllowedSpeed": {
            "type": "Property",
            "value": 60.0,
            "unitCode": "KMH"
        },
        "dateModified": {
            "type": "Property",
            "value": "2025-11-22T15:30:00Z"
        }
    }
    """
    try:
        # Convert Pydantic models to dictionaries
        attrs_data = {
            key: attr.model_dump(exclude_unset=True) for key, attr in attributes.items()
        }

        response = await road_segment_service.update(
            entity_id=entity_id, attrs_data=attrs_data
        )
        return Response(
            content=response.content,
            status_code=response.status_code,
            headers=dict(response.headers),
        )
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"RoadSegment entity with ID '{entity_id}' not found",
            ) from e
        logger.error(f"HTTP error updating entity {entity_id}: {e.response.text}")
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"Failed to update entity: {e.response.text}",
        ) from e
    except Exception as e:
        logger.error(f"Unexpected error updating entity {entity_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}",
        ) from e


@router.put(
    "/{entity_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Replace RoadSegment Entity",
    description="Replace an entire RoadSegment entity with new data.",
)
async def replace_road_segment(
    entity_id: str,
    entity_data: Union[RoadSegment, Dict[str, Any]],
):
    """
    Replace an entire RoadSegment entity.

    Provide the complete entity data including type and all required attributes.

    Example:
    {
        "id": "urn:ngsi-ld:RoadSegment:Madrid-001",
        "type": "RoadSegment",
        "roadName": "Gran Via",
        "roadClass": "MAJOR_CITY_ROAD",
        "length": 2.8,
        "width": 14.0,
        "totalLaneNumber": 6,
        "maximumAllowedSpeed": 50.0
    }
    """
    try:
        response = await road_segment_service.replace(
            entity_id=entity_id, entity_data=entity_data
        )
        return Response(
            content=response.content,
            status_code=response.status_code,
            headers=dict(response.headers),
        )
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"RoadSegment entity with ID '{entity_id}' not found",
            ) from e
        logger.error(f"HTTP error replacing entity {entity_id}: {e.response.text}")
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"Failed to replace entity: {e.response.text}",
        ) from e
    except Exception as e:
        logger.error(f"Unexpected error replacing entity {entity_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}",
        ) from e


@router.delete(
    "/{entity_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete RoadSegment Entity",
    description="Delete a RoadSegment entity by its ID.",
)
async def delete_road_segment(entity_id: str):
    """
    Delete a RoadSegment entity.

    Example: DELETE /urn:ngsi-ld:RoadSegment:001
    """
    try:
        response = await road_segment_service.delete(entity_id=entity_id)
        return Response(
            content=response.content,
            status_code=response.status_code,
            headers=dict(response.headers),
        )
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"RoadSegment entity with ID '{entity_id}' not found",
            ) from e
        logger.error(f"HTTP error deleting entity {entity_id}: {e.response.text}")
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"Failed to delete entity: {e.response.text}",
        ) from e
    except Exception as e:
        logger.error(f"Unexpected error deleting entity {entity_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}",
        ) from e


@router.post(
    "/batch/create",
    status_code=status.HTTP_201_CREATED,
    summary="Batch Create RoadSegment Entities",
    description="Create multiple RoadSegment entities in a single request.",
)
async def batch_create_road_segments(
    request: BatchOperationRequest,
):
    """
    Create multiple RoadSegment entities in batch.

    Each entity must include at least:
        - id: Unique identifier

    Example:
    {
        "entities": [
            {
                "id": "urn:ngsi-ld:RoadSegment:001",
                "roadName": "Main Street",
                "roadClass": "MAJOR_CITY_ROAD",
                "length": 1.5
            },
            {
                "id": "urn:ngsi-ld:RoadSegment:002",
                "roadName": "Second Avenue",
                "roadClass": "MINOR_CITY_ROAD",
                "length": 0.8
            }
        ]
    }
    """
    try:
        response = await road_segment_service.batch_create(request.entities)
        return Response(
            content=response.content,
            status_code=response.status_code,
            headers=dict(response.headers),
        )
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error in batch create: {e.response.text}")
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"Batch create failed: {e.response.text}",
        ) from e
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Validation error: {str(e)}",
        ) from e
    except Exception as e:
        logger.error(f"Unexpected error in batch create: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}",
        ) from e


@router.post(
    "/batch/upsert",
    status_code=status.HTTP_201_CREATED,
    summary="Batch Upsert RoadSegment Entities",
    description="Create or update multiple RoadSegment entities in a single request.",
)
async def batch_upsert_road_segments(
    request: BatchOperationRequest,
    options: str = Query(
        "update",
        description="Upsert option: 'update' (default) to modify existing entities, or 'replace' to completely replace them",
    ),
):
    """
    Create or update multiple RoadSegment entities in batch.

    The request body format is the same as batch create.
    Use the 'options' parameter to control how existing entities are handled.
    """
    try:
        response = await road_segment_service.batch_upsert(
            request.entities, options=options
        )
        return Response(
            content=response.content,
            status_code=response.status_code,
            headers=dict(response.headers),
        )
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error in batch upsert: {e.response.text}")
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"Batch upsert failed: {e.response.text}",
        ) from e
    except Exception as e:
        logger.error(f"Unexpected error in batch upsert: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}",
        ) from e


@router.post(
    "/batch/update",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Batch Update RoadSegment Entities",
    description="Update multiple RoadSegment entities in a single request.",
)
async def batch_update_road_segments(
    request: BatchOperationRequest,
    options: str = Query(
        "update",
        description="Update option: 'update' (default) to modify existing attributes, or 'replace' to replace entire entities",
    ),
):
    """
    Update multiple RoadSegment entities in batch.

    Each entity in the request should include the 'id' and the attributes to update.
    """
    try:
        response = await road_segment_service.batch_update(
            request.entities, options=options
        )
        return Response(
            content=response.content,
            status_code=response.status_code,
            headers=dict(response.headers),
        )
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error in batch update: {e.response.text}")
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"Batch update failed: {e.response.text}",
        ) from e
    except Exception as e:
        logger.error(f"Unexpected error in batch update: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}",
        ) from e


@router.post(
    "/batch/delete",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Batch Delete RoadSegment Entities",
    description="Delete multiple RoadSegment entities in a single request.",
)
async def batch_delete_road_segments(
    request: BatchDeleteRequest,
):
    """
    Delete multiple RoadSegment entities by their IDs.

    Example:
    {
        "entity_ids": [
            "urn:ngsi-ld:RoadSegment:001",
            "urn:ngsi-ld:RoadSegment:002"
        ]
    }
    """
    try:
        response = await road_segment_service.batch_delete(request.entity_ids)
        return Response(
            content=response.content,
            status_code=response.status_code,
            headers=dict(response.headers),
        )
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error in batch delete: {e.response.text}")
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"Batch delete failed: {e.response.text}",
        ) from e
    except Exception as e:
        logger.error(f"Unexpected error in batch delete: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}",
        ) from e


@router.get(
    "/by-road-class/{road_class}",
    response_model=List[Dict[str, Any]],
    summary="Query by Road Class",
    description="Retrieve RoadSegment entities filtered by road class.",
)
async def get_road_segments_by_class(
    road_class: str,
    limit: Optional[int] = Query(
        None, ge=1, le=1000, description="Maximum number of results to return"
    ),
):
    """
    Query road segments by road class.

    Examples:
        - Get major city roads: GET /by-road-class/MAJOR_CITY_ROAD
        - Get highways: GET /by-road-class/NATIONAL_HIGHWAY
        - Get minor roads: GET /by-road-class/MINOR_CITY_ROAD?limit=20
    """
    try:
        return await road_segment_service.get_by_road_class(
            road_class=road_class, limit=limit
        )
    except Exception as e:
        logger.error(f"Error querying by road class {road_class}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to query by road class: {str(e)}",
        ) from e


@router.get(
    "/by-speed-limit",
    response_model=List[Dict[str, Any]],
    summary="Query by Speed Limit Range",
    description="Retrieve RoadSegment entities filtered by speed limit range.",
)
async def get_road_segments_by_speed_limit(
    min_speed: Optional[float] = Query(
        None,
        description="Minimum speed limit in km/h (inclusive)",
    ),
    max_speed: Optional[float] = Query(
        None,
        description="Maximum speed limit in km/h (inclusive)",
    ),
    limit: Optional[int] = Query(
        None, ge=1, le=1000, description="Maximum number of results to return"
    ),
):
    """
    Query road segments by speed limit range.

    Examples:
        - Get segments with speed limit between 40 and 60 km/h: GET /by-speed-limit?min_speed=40&max_speed=60
        - Get segments with speed limit above 80 km/h: GET /by-speed-limit?min_speed=80
        - Get segments with speed limit below 30 km/h: GET /by-speed-limit?max_speed=30&limit=20
    """
    try:
        return await road_segment_service.get_by_speed_limit(
            min_speed=min_speed, max_speed=max_speed, limit=limit
        )
    except Exception as e:
        logger.error(f"Error querying by speed limit range: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to query by speed limit range: {str(e)}",
        ) from e


@router.get(
    "/by-length",
    response_model=List[Dict[str, Any]],
    summary="Query by Length Range",
    description="Retrieve RoadSegment entities filtered by length range.",
)
async def get_road_segments_by_length(
    min_length: Optional[float] = Query(
        None,
        description="Minimum length in km (inclusive)",
    ),
    max_length: Optional[float] = Query(
        None,
        description="Maximum length in km (inclusive)",
    ),
    limit: Optional[int] = Query(
        None, ge=1, le=1000, description="Maximum number of results to return"
    ),
):
    """
    Query road segments by length range.

    Examples:
        - Get segments between 1 and 5 km: GET /by-length?min_length=1&max_length=5
        - Get long segments above 10 km: GET /by-length?min_length=10
        - Get short segments below 1 km: GET /by-length?max_length=1&limit=50
    """
    try:
        return await road_segment_service.get_by_length_range(
            min_length=min_length, max_length=max_length, limit=limit
        )
    except Exception as e:
        logger.error(f"Error querying by length range: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to query by length range: {str(e)}",
        ) from e


@router.get(
    "/by-lane-count",
    response_model=List[Dict[str, Any]],
    summary="Query by Lane Count",
    description="Retrieve RoadSegment entities filtered by number of lanes.",
)
async def get_road_segments_by_lane_count(
    min_lanes: Optional[int] = Query(
        None,
        description="Minimum number of lanes (inclusive)",
    ),
    max_lanes: Optional[int] = Query(
        None,
        description="Maximum number of lanes (inclusive)",
    ),
    limit: Optional[int] = Query(
        None, ge=1, le=1000, description="Maximum number of results to return"
    ),
):
    """
    Query road segments by number of lanes.

    Examples:
        - Get segments with 4 lanes exactly: GET /by-lane-count?min_lanes=4&max_lanes=4
        - Get segments with 4 or more lanes: GET /by-lane-count?min_lanes=4
        - Get segments with 2 or fewer lanes: GET /by-lane-count?max_lanes=2&limit=50
    """
    try:
        return await road_segment_service.get_by_lane_count(
            min_lanes=min_lanes, max_lanes=max_lanes, limit=limit
        )
    except Exception as e:
        logger.error(f"Error querying by lane count: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to query by lane count: {str(e)}",
        ) from e


@router.get(
    "/by-road-name",
    response_model=List[Dict[str, Any]],
    summary="Query by Road Name",
    description="Retrieve RoadSegment entities filtered by road name.",
)
async def get_road_segments_by_name(
    road_name: str,
    exact_match: bool = Query(
        False,
        description="If true, uses exact match; if false, uses case-insensitive search",
    ),
    limit: Optional[int] = Query(
        None, ge=1, le=1000, description="Maximum number of results to return"
    ),
):
    """
    Query road segments by road name.

    Examples:
        - Get exact match for "Gran Via": GET /by-road-name/Gran Via?exact_match=true
        - Get case-insensitive search for "main": GET /by-road-name/main
        - Get roads containing "avenue": GET /by-road-name/avenue?limit=20
    """
    try:
        return await road_segment_service.get_by_road_name(
            road_name=road_name, exact_match=exact_match, limit=limit
        )
    except Exception as e:
        logger.error(f"Error querying by road name {road_name}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to query by road name: {str(e)}",
        ) from e


@router.get(
    "/by-status/{status}",
    response_model=List[Dict[str, Any]],
    summary="Query by Status",
    description="Retrieve RoadSegment entities filtered by status.",
)
async def get_road_segments_by_status(
    status: str,
    limit: Optional[int] = Query(
        None, ge=1, le=1000, description="Maximum number of results to return"
    ),
):
    """
    Query road segments by status.

    Examples:
        - Get open road segments: GET /by-status/open
        - Get closed road segments: GET /by-status/closed
        - Get limited access roads: GET /by-status/limited?limit=20
    """
    try:
        return await road_segment_service.get_by_status(status=status, limit=limit)
    except Exception as e:
        logger.error(f"Error querying by status {status}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to query by status: {str(e)}",
        ) from e


@router.get(
    "/by-vehicle-type/{vehicle_type}",
    response_model=List[Dict[str, Any]],
    summary="Query by Vehicle Type",
    description="Retrieve RoadSegment entities filtered by allowed vehicle type.",
)
async def get_road_segments_by_vehicle_type(
    vehicle_type: str,
    limit: Optional[int] = Query(
        None, ge=1, le=1000, description="Maximum number of results to return"
    ),
):
    """
    Query road segments by allowed vehicle type.

    Examples:
        - Get segments where cars are allowed: GET /by-vehicle-type/car
        - Get segments where buses are allowed: GET /by-vehicle-type/bus
        - Get segments where trucks are allowed: GET /by-vehicle-type/lorry
    """
    try:
        return await road_segment_service.get_by_vehicle_type(
            vehicle_type=vehicle_type, limit=limit
        )
    except Exception as e:
        logger.error(f"Error querying by vehicle type {vehicle_type}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to query by vehicle type: {str(e)}",
        ) from e
