# Copyright (c) 2025 Green Wave Team
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import logging
from typing import Any, Dict, List, Optional, Union

import httpx
from fastapi import APIRouter, HTTPException, Query, Response, status
from pydantic import BaseModel, Field, model_validator

from app.models.TrafficEnvironmentImpact import TrafficEnvironmentImpact
from app.services.traffic_enviroment_impact_service import (
    traffic_environment_impact_service,
)

router = APIRouter(
    prefix="/api/v1/traffic-environment-impact", tags=["TrafficEnvironmentImpact"]
)
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
    summary="Query TrafficEnvironmentImpact Entities",
    description="Retrieve a list of TrafficEnvironmentImpact entities with advanced filtering, pagination, and formatting options.",
)
async def get_all_traffic_environment_impact(
    # Filtering
    id: Optional[str] = Query(
        None,
        description="Filter by entity ID(s), comma-separated (e.g., 'urn:ngsi-ld:TrafficEnvironmentImpact:001,urn:ngsi-ld:TrafficEnvironmentImpact:002')",
    ),
    q: Optional[str] = Query(
        None,
        description="NGSI-LD query filter string (e.g., 'co2>100', 'dateObservedFrom>2025-11-17')",
    ),
    # Attribute selection
    pick: Optional[str] = Query(
        None,
        description="Preferred - Comma-separated list of attributes to select (e.g., 'id,type,co2,dateObservedFrom')",
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
        description="Coordinates for geo-spatial queries as JSON array string (e.g., '[-8.5,41.2]' or '[[-8.5,41.2],[-8.6,41.3]]')",
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
    Get TrafficEnvironmentImpact entities with comprehensive filtering and pagination.

    Examples:
        - Get all entities: GET /
        - Get entities by ID: GET /?id=urn:ngsi-ld:TrafficEnvironmentImpact:001
        - Get entities with high CO2: GET /?q=co2>100
        - Get entities from time range: GET /?q=dateObservedFrom>2025-11-17T00:00:00Z
        - Get entities with pagination: GET /?limit=20&offset=40
        - Get count only: GET /?count=true
        - Get simplified format: GET /?format=simplified&pick=id,type,co2
        - Geo-spatial query: GET /?georel=near;maxDistance==2000&geometry=Point&coordinates=[-8.5,41.2]
    """
    try:
        return await traffic_environment_impact_service.get_all(
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
        logger.error(
            f"HTTP error retrieving traffic environment impacts: {e.response.text}"
        )
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"Failed to retrieve traffic environment impacts: {e.response.text}",
        ) from e
    except Exception as e:
        logger.error(
            f"Unexpected error retrieving traffic environment impacts: {str(e)}"
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}",
        ) from e


@router.get(
    "/{entity_id}",
    response_model=Dict[str, Any],
    summary="Get TrafficEnvironmentImpact by ID",
    description="Retrieve a specific TrafficEnvironmentImpact entity by its unique identifier.",
)
async def get_traffic_environment_impact_by_id(
    entity_id: str,
    attrs: Optional[str] = Query(
        None,
        description="Comma-separated list of attribute names to retrieve (e.g., 'id,type,co2,dateObservedFrom')",
    ),
    options: Optional[str] = Query(
        None,
        description="Query options (e.g., 'keyValues' for key-value format, 'sysAttrs' for system attributes)",
    ),
):
    """
    Get a specific TrafficEnvironmentImpact entity by its ID.

    Examples:
        - Get full entity: GET /urn:ngsi-ld:TrafficEnvironmentImpact:001
        - Get specific attributes: GET /urn:ngsi-ld:TrafficEnvironmentImpact:001?attrs=id,type,co2
        - Get in key-value format: GET /urn:ngsi-ld:TrafficEnvironmentImpact:001?option=keyValues
    """
    try:
        return await traffic_environment_impact_service.get_by_id(
            entity_id=entity_id, attrs=attrs, options=options
        )
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"TrafficEnvironmentImpact entity with ID '{entity_id}' not found",
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
    summary="Create TrafficEnvironmentImpact Entity",
    description="Create a new TrafficEnvironmentImpact entity with the provided data.",
)
async def create_traffic_environment_impact(
    entity_data: Dict[str, Any],
):
    """
    Create a new TrafficEnvironmentImpact entity.

    Required fields:
        - id: Unique identifier (URN format recommended)
        - dateObservedFrom: Start date of observation (ISO 8601 format)

    Optional fields:
        - dateObservedTo: End date of observation
        - co2: CO2 emission concentration with unitCode
        - traffic: Array of traffic items with vehicle class and references
        - location: GeoJSON location data
        - address: Address information
        - Any other standard NGSI-LD attributes

    Example:
    {
        "id": "urn:ngsi-ld:TrafficEnvironmentImpact:Madrid-001",
        "dateObservedFrom": "2025-11-17T10:25:52Z",
        "dateObservedTo": "2025-11-17T10:30:52Z",
        "co2": {
            "type": "Property",
            "value": 125.5,
            "unitCode": "GQ"
        },
        "traffic": [
            {
                "refTrafficFlowObserved": "urn:ngsi-ld:TrafficFlowObserved:001",
                "vehicleClass": "passengerCar"
            }
        ]
    }
    """
    try:
        response = await traffic_environment_impact_service.create(entity_data)
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
                detail=f"TrafficEnvironmentImpact entity already exists: {e.response.text}",
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
    summary="Update TrafficEnvironmentImpact Entity",
    description="Update specific attributes of an existing TrafficEnvironmentImpact entity.",
)
async def update_traffic_environment_impact(
    entity_id: str,
    attributes: Dict[str, NgsiLdAttributePatch],
):
    """
    Update specific attributes of a TrafficEnvironmentImpact entity.

    Provide only the attributes you want to update in the request body.

    Example:
    {
        "co2": {
            "type": "Property",
            "value": 150.8,
            "unitCode": "GQ"
        },
        "dateModified": {
            "type": "Property",
            "value": "2025-11-17T15:30:00Z"
        }
    }
    """
    try:
        # Convert Pydantic models to dictionaries
        attrs_data = {
            key: attr.model_dump(exclude_unset=True) for key, attr in attributes.items()
        }

        response = await traffic_environment_impact_service.update(
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
                detail=f"TrafficEnvironmentImpact entity with ID '{entity_id}' not found",
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
    summary="Replace TrafficEnvironmentImpact Entity",
    description="Replace an entire TrafficEnvironmentImpact entity with new data.",
)
async def replace_traffic_environment_impact(
    entity_id: str,
    entity_data: Union[TrafficEnvironmentImpact, Dict[str, Any]],
):
    """
    Replace an entire TrafficEnvironmentImpact entity.

    Provide the complete entity data including type and all required attributes.

    Example:
    {
        "id": "urn:ngsi-ld:TrafficEnvironmentImpact:Madrid-001",
        "type": "TrafficEnvironmentImpact",
        "dateObservedFrom": "2025-11-17T10:25:52Z",
        "dateObservedTo": "2025-11-17T10:30:52Z",
        "co2": {
            "type": "Property",
            "value": 145.3,
            "unitCode": "GQ"
        }
    }
    """
    try:
        response = await traffic_environment_impact_service.replace(
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
                detail=f"TrafficEnvironmentImpact entity with ID '{entity_id}' not found",
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
    summary="Delete TrafficEnvironmentImpact Entity",
    description="Delete a TrafficEnvironmentImpact entity by its ID.",
)
async def delete_traffic_environment_impact(entity_id: str):
    """
    Delete a TrafficEnvironmentImpact entity.

    Example: DELETE /urn:ngsi-ld:TrafficEnvironmentImpact:001
    """
    try:
        response = await traffic_environment_impact_service.delete(entity_id=entity_id)
        return Response(
            content=response.content,
            status_code=response.status_code,
            headers=dict(response.headers),
        )
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"TrafficEnvironmentImpact entity with ID '{entity_id}' not found",
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
    summary="Batch Create TrafficEnvironmentImpact Entities",
    description="Create multiple TrafficEnvironmentImpact entities in a single request.",
)
async def batch_create_traffic_environment_impact(
    request: BatchOperationRequest,
):
    """
    Create multiple TrafficEnvironmentImpact entities in batch.

    Each entity must include at least:
        - id: Unique identifier
        - dateObservedFrom: Start date of observation

    Example:
    {
        "entities": [
            {
                "id": "urn:ngsi-ld:TrafficEnvironmentImpact:001",
                "dateObservedFrom": "2025-11-17T10:00:00Z",
                "co2": {"type": "Property", "value": 100.5, "unitCode": "GQ"}
            },
            {
                "id": "urn:ngsi-ld:TrafficEnvironmentImpact:002",
                "dateObservedFrom": "2025-11-17T10:05:00Z",
                "co2": {"type": "Property", "value": 120.3, "unitCode": "GQ"}
            }
        ]
    }
    """
    try:
        response = await traffic_environment_impact_service.batch_create(
            request.entities
        )
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
    summary="Batch Upsert TrafficEnvironmentImpact Entities",
    description="Create or update multiple TrafficEnvironmentImpact entities in a single request.",
)
async def batch_upsert_traffic_environment_impact(
    request: BatchOperationRequest,
    options: str = Query(
        "update",
        description="Upsert option: 'update' (default) to modify existing entities, or 'replace' to completely replace them",
    ),
):
    """
    Create or update multiple TrafficEnvironmentImpact entities in batch.

    The request body format is the same as batch create.
    Use the 'options' parameter to control how existing entities are handled.
    """
    try:
        response = await traffic_environment_impact_service.batch_upsert(
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
    summary="Batch Update TrafficEnvironmentImpact Entities",
    description="Update multiple TrafficEnvironmentImpact entities in a single request.",
)
async def batch_update_traffic_environment_impact(
    request: BatchOperationRequest,
    options: str = Query(
        "update",
        description="Update option: 'update' (default) to modify existing attributes, or 'replace' to replace entire entities",
    ),
):
    """
    Update multiple TrafficEnvironmentImpact entities in batch.

    Each entity in the request should include the 'id' and the attributes to update.
    """
    try:
        response = await traffic_environment_impact_service.batch_update(
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
    summary="Batch Delete TrafficEnvironmentImpact Entities",
    description="Delete multiple TrafficEnvironmentImpact entities in a single request.",
)
async def batch_delete_traffic_environment_impact(
    request: BatchDeleteRequest,
):
    """
    Delete multiple TrafficEnvironmentImpact entities by their IDs.

    Example:
    {
        "entity_ids": [
            "urn:ngsi-ld:TrafficEnvironmentImpact:001",
            "urn:ngsi-ld:TrafficEnvironmentImpact:002"
        ]
    }
    """
    try:
        response = await traffic_environment_impact_service.batch_delete(
            request.entity_ids
        )
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
    "/by-co2-range",
    response_model=List[Dict[str, Any]],
    summary="Query by CO2 Range",
    description="Retrieve TrafficEnvironmentImpact entities filtered by CO2 emission range.",
)
async def get_traffic_environment_impact_by_co2_range(
    min_co2: Optional[float] = Query(
        None,
        description="Minimum CO2 value (inclusive)",
    ),
    max_co2: Optional[float] = Query(
        None,
        description="Maximum CO2 value (inclusive)",
    ),
    limit: Optional[int] = Query(
        None, ge=1, le=1000, description="Maximum number of results to return"
    ),
):
    """
    Query traffic environment impacts by CO2 emission range.

    Examples:
        - Get entities with CO2 between 50 and 150: GET /by-co2-range?min_co2=50&max_co2=150
        - Get entities with CO2 above 100: GET /by-co2-range?min_co2=100
        - Get entities with CO2 below 75: GET /by-co2-range?max_co2=75&limit=20
    """
    try:
        return await traffic_environment_impact_service.get_by_co2_range(
            min_co2=min_co2, max_co2=max_co2, limit=limit
        )
    except Exception as e:
        logger.error(f"Error querying by CO2 range: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to query by CO2 range: {str(e)}",
        ) from e


@router.get(
    "/by-time-range",
    response_model=List[Dict[str, Any]],
    summary="Query by Time Range",
    description="Retrieve TrafficEnvironmentImpact entities filtered by observation time range.",
)
async def get_traffic_environment_impact_by_time_range(
    start_time: Optional[str] = Query(
        None,
        description="Start time in ISO8601 format (inclusive)",
    ),
    end_time: Optional[str] = Query(
        None,
        description="End time in ISO8601 format (inclusive)",
    ),
    limit: Optional[int] = Query(
        None, ge=1, le=1000, description="Maximum number of results to return"
    ),
):
    """
    Query traffic environment impacts by observation time range.

    Examples:
        - Get entities from last 24 hours: GET /by-time-range?start_time=2025-11-16T10:00:00Z&end_time=2025-11-17T10:00:00Z
        - Get entities observed after a specific time: GET /by-time-range?start_time=2025-11-17T08:00:00Z
    """
    try:
        return await traffic_environment_impact_service.get_by_time_range(
            start_time=start_time, end_time=end_time, limit=limit
        )
    except Exception as e:
        logger.error(f"Error querying by time range: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to query by time range: {str(e)}",
        ) from e


@router.get(
    "/by-vehicle-class/{vehicle_class}",
    response_model=List[Dict[str, Any]],
    summary="Query by Vehicle Class",
    description="Retrieve TrafficEnvironmentImpact entities filtered by vehicle class.",
)
async def get_traffic_environment_impact_by_vehicle_class(
    vehicle_class: str,
    limit: Optional[int] = Query(
        None, ge=1, le=1000, description="Maximum number of results to return"
    ),
):
    """
    Query traffic environment impacts by vehicle class.

    Examples:
        - Get impacts for passenger cars: GET /by-vehicle-class/passengerCar
        - Get impacts for heavy vehicles: GET /by-vehicle-class/heavyVehicle
    """
    try:
        return await traffic_environment_impact_service.get_by_vehicle_class(
            vehicle_class=vehicle_class, limit=limit
        )
    except Exception as e:
        logger.error(f"Error querying by vehicle class {vehicle_class}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to query by vehicle class: {str(e)}",
        ) from e


@router.get(
    "/by-traffic-flow/{traffic_flow_id}",
    response_model=List[Dict[str, Any]],
    summary="Query by Traffic Flow Reference",
    description="Retrieve TrafficEnvironmentImpact entities filtered by traffic flow observed reference.",
)
async def get_traffic_environment_impact_by_traffic_flow(
    traffic_flow_id: str,
    limit: Optional[int] = Query(
        None, ge=1, le=1000, description="Maximum number of results to return"
    ),
):
    """
    Query traffic environment impacts by traffic flow observed reference.

    Examples:
        - Get impacts for a specific traffic flow: GET /by-traffic-flow/urn:ngsi-ld:TrafficFlowObserved:001
    """
    try:
        return await traffic_environment_impact_service.get_by_traffic_flow_reference(
            traffic_flow_id=traffic_flow_id, limit=limit
        )
    except Exception as e:
        logger.error(f"Error querying by traffic flow {traffic_flow_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to query by traffic flow: {str(e)}",
        ) from e
