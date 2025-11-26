# Copyright (c) 2025 Green Wave Team
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import logging
from typing import Any, Dict, List, Optional, Union

import httpx

from app.models.AirQualityObserved import AirQualityObserved

from .base_service import BaseService

logger = logging.getLogger(__name__)


class AirQualityService(BaseService):
    """
    Service layer for AirQualityObserved entities.
    Provides high-level methods for CRUD operations on air quality data.

    This service is designed to work with FIWARE Orion-LD context broker
    following NGSI-LD specifications for air quality monitoring.

    Usage:
        # Context manager (recommended)
        async with AirQualityService() as service:
            entities = await service.get_all(limit=10)

        # Manual lifecycle
        service = AirQualityService()
        try:
            entity = await service.get_by_id("urn:ngsi-ld:AirQualityObserved:001")
        finally:
            await service.close()

    Author: sonmessia
    Created: 2025-11-15
    """

    def __init__(
        self, orion_url: Optional[str] = None, context_url: Optional[str] = None
    ):
        """
        Initialize AirQualityService.

        Args:
            orion_url: Orion-LD broker URL (default from env: ORION_LD_URL)
            context_url: JSON-LD context URL (default from env: CONTEXT_URL)
        """
        super().__init__(orion_url, context_url)
        self.entity_type = "AirQualityObserved"

    async def create(self, entity_data: Dict[str, Any]) -> httpx.Response:
        """
        Create a new AirQualityObserved entity.

        Args:
            entity_data: Dictionary containing entity attributes.
                        Must include 'id' and 'dateObserved' at minimum.

        Returns:
            httpx.Response with status 201 on success

        Raises:
            ValueError: If required dateObserved field is missing
            httpx.HTTPStatusError: If the entity already exists (409)

        Example:
            entity = {
                "id": "urn:ngsi-ld:AirQualityObserved:Madrid-001",
                "dateObserved": "2025-11-15T10:25:52Z",
                "temperature": {
                    "type": "Property",
                    "value": 25.5,
                    "unitCode": "CEL"
                },
                "pm25": {
                    "type": "Property",
                    "value": 35.2,
                    "unitCode": "GQ"
                }
            }
            response = await service.create(entity)
        """
        if "dateObserved" not in entity_data:
            raise ValueError(
                "dateObserved attribute is required for AirQualityObserved entity."
            )

        entity_data["type"] = self.entity_type
        return await super().create_entity(entity_data)

    async def get_all(
        self,
        # Filtering
        id: Optional[str] = None,
        q: Optional[str] = None,
        # Attribute selection
        pick: Optional[str] = None,
        attrs: Optional[str] = None,  # Legacy
        # Geo-spatial
        georel: Optional[str] = None,
        geometry: Optional[str] = None,
        coordinates: Optional[str] = None,
        geoproperty: Optional[str] = None,
        # Pagination
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        # Result options
        count: Optional[bool] = None,
        format: Optional[str] = None,
        options: Optional[str] = None,
        # Federation
        local: Optional[bool] = None,
        **kwargs,
    ) -> Union[List[Dict[str, Any]], int]:
        """
        Query for AirQualityObserved entities.
        Automatically adds the 'type=AirQualityObserved' filter to all queries.

        Args:
            id: Filter by entity ID(s), comma-separated
            q: Query filter (e.g., "temperature>25", "pm25<50")

            pick: Preferred - Attributes to select (comma-separated)
            attrs: Legacy - Attributes to include (comma-separated)

            georel: Geo-relationship (e.g., "near;maxDistance==2000")
            geometry: Geometry type (Point, LineString, Polygon, etc.)
            coordinates: Coordinates array as string (e.g., "[-8.5,41.2]")
            geoproperty: Property to use for geo-queries (default: "location")

            limit: Maximum number of results
            offset: Offset for pagination

            count: If True, returns only the count of matching entities
            format: Response format ('simplified' for key-value pairs)
            options: Query options (e.g., 'sysAttrs' for system attributes)

            local: If True, query only local entities (not federated)

            **kwargs: Additional query parameters

        Returns:
            List of AirQualityObserved entities or count (int) if count=True

        Examples:
            # Get all air quality observations (up to 100)
            entities = await service.get_all(limit=100)

            # Get observations with high PM2.5 levels
            polluted = await service.get_all(
                q="pm25>50",
                format="simplified",
                limit=10
            )

            # Get specific attributes only
            temps = await service.get_all(
                pick="id,type,temperature,dateObserved",
                format="simplified",
                limit=20
            )

            # Count observations in last hour
            count = await service.get_all(
                q="dateObserved>'2025-11-15T09:00:00Z'",
                count=True
            )

            # Geo-spatial query - find nearby sensors
            nearby = await service.get_all(
                georel="near;maxDistance==5000",
                geometry="Point",
                coordinates="[-3.703790,40.416775]",  # Madrid
                limit=5
            )

            # Get with system attributes
            with_meta = await service.get_all(
                limit=10,
                options="sysAttrs"
            )

            # Local entities only (skip federation)
            local_only = await service.get_all(local=True, limit=50)
        """
        kwargs["type"] = self.entity_type

        if id is not None:
            kwargs["id"] = id
        if q is not None:
            kwargs["q"] = q
        if pick is not None:
            kwargs["pick"] = pick
        if attrs is not None:
            kwargs["attrs"] = attrs
        if georel is not None:
            kwargs["georel"] = georel
        if geometry is not None:
            kwargs["geometry"] = geometry
        if coordinates is not None:
            kwargs["coordinates"] = coordinates
        if geoproperty is not None:
            kwargs["geoproperty"] = geoproperty
        if limit is not None:
            kwargs["limit"] = limit
        if offset is not None:
            kwargs["offset"] = offset
        if count is not None:
            kwargs["count"] = count
        if format is not None:
            kwargs["format"] = format
        if options is not None:
            kwargs["options"] = options
        if local is not None:
            kwargs["local"] = local

        return await self.query_entities(**kwargs)

    async def get_by_id(
        self,
        entity_id: str,
        pick: Optional[str] = None,
        attrs: Optional[str] = None,
        format: Optional[str] = None,
        options: Optional[str] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """
        Retrieve a specific AirQualityObserved entity by ID.

        Args:
            entity_id: The entity identifier (URN)
            pick: Attributes to select (comma-separated)
            attrs: Legacy - Attributes to include
            format: Response format ('simplified' for key-value pairs)
            options: Query options (e.g., 'sysAttrs')
            **kwargs: Additional query parameters

        Returns:
            Entity data as dictionary

        Examples:
            # Get full entity
            entity = await service.get_by_id(
                "urn:ngsi-ld:AirQualityObserved:Madrid-001"
            )

            # Get specific attributes in simplified format
            data = await service.get_by_id(
                "urn:ngsi-ld:AirQualityObserved:Madrid-001",
                pick="id,type,temperature,pm25,dateObserved",
                format="simplified"
            )
            # Returns: {"id": "...", "temperature": 25.5, "pm25": 35.2, ...}

            # Get with system metadata
            entity = await service.get_by_id(
                "urn:ngsi-ld:AirQualityObserved:Madrid-001",
                options="sysAttrs"
            )
        """
        if pick is not None:
            kwargs["pick"] = pick
        if attrs is not None:
            kwargs["attrs"] = attrs
        if format is not None:
            kwargs["format"] = format
        if options is not None:
            kwargs["options"] = options

        return await super().get_entity_by_id(entity_id, **kwargs)

    async def update_attrs(self, entity_id: str, update_data: Dict[str, Any]) -> int:
        """
        Update specific attributes of an AirQualityObserved entity.

        Args:
            entity_id: The entity identifier
            update_data: Dictionary with attributes to update

        Returns:
            HTTP status code (204 on success)

        Example:
            # Update temperature and PM2.5 readings
            status = await service.update_attrs(
                "urn:ngsi-ld:AirQualityObserved:Madrid-001",
                {
                    "temperature": {
                        "type": "Property",
                        "value": 26.8,
                        "unitCode": "CEL"
                    },
                    "pm25": {
                        "type": "Property",
                        "value": 42.1,
                        "unitCode": "GQ"
                    },
                    "dateObserved": {
                        "type": "Property",
                        "value": "2025-11-15T10:25:52Z"
                    }
                }
            )
        """
        response = await super().update_entity_attributes(entity_id, update_data)
        return response.status_code

    async def replace(
        self, entity_id: str, entity_data: Union[Dict[str, Any], AirQualityObserved]
    ) -> int:
        """
        Replace an entire AirQualityObserved entity.

        Args:
            entity_id: The entity identifier
            entity_data: Complete entity data (will replace all attributes)

        Returns:
            HTTP status code (204 on success)

        Example:
            new_data = {
                "dateObserved": "2025-11-15T10:25:52Z",
                "temperature": {
                    "type": "Property",
                    "value": 28.0,
                    "unitCode": "CEL"
                },
                "pm25": {
                    "type": "Property",
                    "value": 38.5,
                    "unitCode": "GQ"
                }
            }
            status = await service.replace(
                "urn:ngsi-ld:AirQualityObserved:Madrid-001",
                new_data
            )
        """
        if isinstance(entity_data, AirQualityObserved):
            entity_dict = entity_data.model_dump(exclude_unset=True)
        else:
            entity_dict = entity_data

        entity_dict["type"] = self.entity_type
        response = await super().replace_entity(entity_id, entity_dict)
        return response.status_code

    async def delete(self, entity_id: str) -> int:
        """
        Delete an AirQualityObserved entity.

        Args:
            entity_id: The entity identifier

        Returns:
            HTTP status code (204 on success)

        Example:
            status = await service.delete(
                "urn:ngsi-ld:AirQualityObserved:Madrid-001"
            )
        """
        response = await super().delete_entity(entity_id)
        return response.status_code

    async def delete_attribute(self, entity_id: str, attribute_name: str) -> int:
        """
        Delete a specific attribute from an AirQualityObserved entity.

        Args:
            entity_id: The entity identifier
            attribute_name: Name of the attribute to delete

        Returns:
            HTTP status code (204 on success)

        Example:
            # Remove the 'relativeHumidity' attribute
            status = await service.delete_attribute(
                "urn:ngsi-ld:AirQualityObserved:Madrid-001",
                "relativeHumidity"
            )
        """
        response = await super().delete_entity_attribute(entity_id, attribute_name)
        return response.status_code

    async def batch_upsert(
        self, entities: List[Dict[str, Any]], options: str = "update"
    ) -> httpx.Response:
        """
        Create or update a list of AirQualityObserved entities.
        Automatically sets the 'type' for each entity in the batch.

        Args:
            entities: List of entity dictionaries
            options: 'update' (default, keep existing attrs) or 'replace' (remove unlisted attrs)

        Returns:
            httpx.Response with status 201/204/207

        Example:
            entities = [
                {
                    "id": "urn:ngsi-ld:AirQualityObserved:Madrid-001",
                    "dateObserved": "2025-11-15T10:25:52Z",
                    "temperature": {"type": "Property", "value": 25.5, "unitCode": "CEL"},
                    "pm25": {"type": "Property", "value": 35.2, "unitCode": "GQ"}
                },
                {
                    "id": "urn:ngsi-ld:AirQualityObserved:Madrid-002",
                    "dateObserved": "2025-11-15T10:25:52Z",
                    "temperature": {"type": "Property", "value": 26.1, "unitCode": "CEL"},
                    "pm25": {"type": "Property", "value": 42.8, "unitCode": "GQ"}
                }
            ]
            response = await service.batch_upsert(entities, options="update")
        """
        for entity in entities:
            entity["type"] = self.entity_type

        return await super().batch_upsert(entities, options)

    async def batch_create(self, entities: List[Dict[str, Any]]) -> httpx.Response:
        """
        Create multiple AirQualityObserved entities.
        Fails if any entity already exists.

        Args:
            entities: List of entity dictionaries

        Returns:
            httpx.Response with created entity IDs or errors

        Example:
            entities = [
                {
                    "id": "urn:ngsi-ld:AirQualityObserved:Madrid-003",
                    "dateObserved": "2025-11-15T10:25:52Z",
                    "temperature": {"type": "Property", "value": 24.2, "unitCode": "CEL"}
                },
                {
                    "id": "urn:ngsi-ld:AirQualityObserved:Madrid-004",
                    "dateObserved": "2025-11-15T10:25:52Z",
                    "temperature": {"type": "Property", "value": 27.8, "unitCode": "CEL"}
                }
            ]
            response = await service.batch_create(entities)
        """
        for entity in entities:
            entity["type"] = self.entity_type

        return await super().batch_create(entities)

    async def batch_delete(self, entity_ids: List[str]) -> httpx.Response:
        """
        Delete multiple AirQualityObserved entities.

        Args:
            entity_ids: List of entity identifiers (URNs)

        Returns:
            httpx.Response with status 204/207

        Example:
            ids = [
                "urn:ngsi-ld:AirQualityObserved:Madrid-001",
                "urn:ngsi-ld:AirQualityObserved:Madrid-002"
            ]
            response = await service.batch_delete(ids)
        """
        return await super().batch_delete(entity_ids)


# Singleton instance for convenience (optional)
air_quality_service = AirQualityService()
