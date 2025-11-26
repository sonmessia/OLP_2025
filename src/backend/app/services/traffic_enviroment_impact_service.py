# Copyright (c) 2025 Green Wave Team
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import logging
from typing import Any, Dict, List, Optional, Union

import httpx

from app.models.TrafficEnvironmentImpact import TrafficEnvironmentImpact

from .base_service import BaseService

logger = logging.getLogger(__name__)


class TrafficEnvironmentImpactService(BaseService):
    """
    Service layer for TrafficEnvironmentImpact entities.
    Provides high-level methods for CRUD operations on traffic environment impact data.

    This service is designed to work with FIWARE Orion-LD context broker
    following NGSI-LD specifications for traffic environmental impact monitoring.

    Usage as singleton:
        from app.services.traffic_enviroment_impact_service import traffic_environment_impact_service
        await traffic_environment_impact_service.initialize()
        try:
            entities = await traffic_environment_impact_service.get_all(limit=10)
        finally:
            await traffic_environment_impact_service.close()

    Author: sonmessia
    Created: 2025-11-17
    """

    _instance: Optional["TrafficEnvironmentImpactService"] = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(
        self, orion_url: Optional[str] = None, context_url: Optional[str] = None
    ):
        # Initialize only once
        if not hasattr(self, "_initialized"):
            super().__init__(orion_url, context_url)
            self.entity_type = "TrafficEnvironmentImpact"
            self._initialized = True

    async def initialize(self):
        """Initialize the singleton service with HTTP client."""
        await self._get_client()
        logger.debug("TrafficEnvironmentImpactService singleton initialized")

    async def create(self, entity_data: Dict[str, Any]) -> httpx.Response:
        """
        Create a new TrafficEnvironmentImpact entity.

        Args:
            entity_data: Dictionary containing entity attributes.
                        Must include 'id' and 'dateObservedFrom' at minimum.

        Returns:
            httpx.Response with status 201 on success

        Raises:
            ValueError: If required dateObservedFrom field is missing
            httpx.HTTPStatusError: If the entity already exists (409)

        Example:
            entity = {
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
                        "type": "Property",
                        "value": {
                            "refTrafficFlowObserved": "urn:ngsi-ld:TrafficFlowObserved:001",
                            "vehicleClass": "passengerCar"
                        }
                    }
                ]
            }
            response = await service.create(entity)
        """
        if "dateObservedFrom" not in entity_data:
            raise ValueError(
                "dateObservedFrom attribute is required for TrafficEnvironmentImpact entity."
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
        Query for TrafficEnvironmentImpact entities.
        Automatically adds the 'type=TrafficEnvironmentImpact' filter to all queries.

        Args:
            id: Filter by entity ID(s), comma-separated
            q: Query filter (e.g., "co2>100", "dateObservedFrom>2025-11-17")

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
            List of TrafficEnvironmentImpact entities or count (int) if count=True

        Examples:
            # Get all traffic environment impacts (up to 100)
            entities = await service.get_all(limit=100)

            # Get impacts with high CO2 levels
            high_co2 = await service.get_all(
                q="co2>100",
                limit=50
            )

            # Get impacts from specific date
            recent = await service.get_all(
                q="dateObservedFrom>2025-11-16T00:00:00Z",
                pick="id,type,co2,dateObservedFrom",
                format="simplified",
                limit=20
            )

            # Get count of all entities
            total_count = await service.get_all(count=True)

            # Get specific entities by ID
            entities = await service.get_all(
                id="urn:ngsi-ld:TrafficEnvironmentImpact:001,urn:ngsi-ld:TrafficEnvironmentImpact:002",
                pick="id,type,co2",
                format="simplified"
            )

            # Geo-spatial query for impacts in an area
            nearby = await service.get_all(
                georel="near;maxDistance==5000",
                geometry="Point",
                coordinates="[-3.7167,40.3833]",  # Madrid coordinates
                limit=10
            )
        """
        return await super().query_entities(
            type=self.entity_type,
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
            **kwargs,
        )

    async def get_by_id(
        self,
        entity_id: str,
        attrs: Optional[str] = None,
        options: Optional[str] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """
        Retrieve a TrafficEnvironmentImpact entity by its ID.

        Args:
            entity_id: The entity identifier (URI)
            attrs: Comma-separated list of attribute names to retrieve
            options: Query options (e.g., 'keyValues', 'sysAttrs')
            **kwargs: Additional query parameters

        Returns:
            TrafficEnvironmentImpact entity data as dictionary

        Example:
            entity = await service.get_by_id(
                "urn:ngsi-ld:TrafficEnvironmentImpact:Madrid-001",
                attrs="id,type,co2,dateObservedFrom"
            )
        """
        return await super().get_entity_by_id(
            entity_id=entity_id, attrs=attrs, options=options, **kwargs
        )

    async def update(
        self, entity_id: str, attrs_data: Dict[str, Any]
    ) -> httpx.Response:
        """
        Update specific attributes of a TrafficEnvironmentImpact entity.

        Args:
            entity_id: The entity identifier
            attrs_data: Dictionary of attributes to update

        Returns:
            httpx.Response with status 204 on success

        Example:
            await service.update(
                "urn:ngsi-ld:TrafficEnvironmentImpact:Madrid-001",
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
            )
        """
        return await super().update_entity_attributes(entity_id, attrs_data)

    async def replace(
        self,
        entity_id: str,
        entity_data: Union[TrafficEnvironmentImpact, Dict[str, Any]],
    ) -> httpx.Response:
        """
        Replace an entire TrafficEnvironmentImpact entity.

        Args:
            entity_id: The entity identifier
            entity_data: Complete entity data (Pydantic model or dictionary)

        Returns:
            httpx.Response with status 204 on success

        Example:
            new_data = {
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
            await service.replace("urn:ngsi-ld:TrafficEnvironmentImpact:Madrid-001", new_data)
        """
        if isinstance(entity_data, TrafficEnvironmentImpact):
            entity_data = entity_data.model_dump(exclude_unset=True)

        entity_data["type"] = self.entity_type
        return await super().replace_entity(entity_id, entity_data)

    async def delete(self, entity_id: str) -> httpx.Response:
        """
        Delete a TrafficEnvironmentImpact entity.

        Args:
            entity_id: The entity identifier

        Returns:
            httpx.Response with status 204 on success

        Example:
            await service.delete("urn:ngsi-ld:TrafficEnvironmentImpact:Madrid-001")
        """
        return await super().delete_entity(entity_id)

    async def batch_create(self, entities: List[Dict[str, Any]]) -> httpx.Response:
        """
        Create multiple TrafficEnvironmentImpact entities in batch.

        Args:
            entities: List of entity dictionaries with required fields

        Returns:
            httpx.Response with status 201/207 and success/error details

        Example:
            entities = [
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
            response = await service.batch_create(entities)
        """
        for entity in entities:
            if "dateObservedFrom" not in entity:
                raise ValueError(
                    "dateObservedFrom attribute is required for all entities in batch create."
                )
            entity["type"] = self.entity_type

        return await super().batch_create(entities)

    async def batch_upsert(
        self, entities: List[Dict[str, Any]], options: str = "update"
    ) -> httpx.Response:
        """
        Create or update multiple TrafficEnvironmentImpact entities in batch.

        Args:
            entities: List of entity dictionaries
            options: 'update' (default) or 'replace'

        Returns:
            httpx.Response with status 201/204/207

        Example:
            entities = [
                {
                    "id": "urn:ngsi-ld:TrafficEnvironmentImpact:001",
                    "dateObservedFrom": "2025-11-17T10:00:00Z",
                    "co2": {"type": "Property", "value": 105.2, "unitCode": "GQ"}
                }
            ]
            response = await service.batch_upsert(entities)
        """
        for entity in entities:
            entity["type"] = self.entity_type

        return await super().batch_upsert(entities, options=options)

    async def batch_update(
        self, entities: List[Dict[str, Any]], options: str = "update"
    ) -> httpx.Response:
        """
        Update multiple TrafficEnvironmentImpact entities in batch.

        Args:
            entities: List of entity dictionaries with updates
            options: 'update' (default) or 'replace'

        Returns:
            httpx.Response with status 204/207

        Example:
            entities = [
                {
                    "id": "urn:ngsi-ld:TrafficEnvironmentImpact:001",
                    "co2": {"type": "Property", "value": 130.7, "unitCode": "GQ"}
                }
            ]
            response = await service.batch_update(entities)
        """
        for entity in entities:
            entity["type"] = self.entity_type

        return await super().batch_update(entities, options=options)

    async def batch_delete(self, entity_ids: List[str]) -> httpx.Response:
        """
        Delete multiple TrafficEnvironmentImpact entities in batch.

        Args:
            entity_ids: List of entity identifiers (URIs)

        Returns:
            httpx.Response with status 204/207

        Example:
            entity_ids = [
                "urn:ngsi-ld:TrafficEnvironmentImpact:001",
                "urn:ngsi-ld:TrafficEnvironmentImpact:002"
            ]
            response = await service.batch_delete(entity_ids)
        """
        return await super().batch_delete(entity_ids)

    async def get_by_co2_range(
        self,
        min_co2: Optional[float] = None,
        max_co2: Optional[float] = None,
        limit: Optional[int] = None,
        **kwargs,
    ) -> Union[List[Dict[str, Any]], int]:
        """
        Query traffic environment impacts by CO2 emission range.

        Args:
            min_co2: Minimum CO2 value (inclusive)
            max_co2: Maximum CO2 value (inclusive)
            limit: Maximum number of results
            **kwargs: Additional query parameters

        Returns:
            List of TrafficEnvironmentImpact entities

        Examples:
            # Get entities with CO2 between 50 and 150
            entities = await service.get_by_co2_range(min_co2=50, max_co2=150)

            # Get entities with CO2 above 100
            high_co2 = await service.get_by_co2_range(min_co2=100)

            # Get entities with CO2 below 75
            low_co2 = await service.get_by_co2_range(max_co2=75, limit=20)
        """
        query_parts = []
        if min_co2 is not None:
            query_parts.append(f"co2>={min_co2}")
        if max_co2 is not None:
            query_parts.append(f"co2<={max_co2}")

        q = ";".join(query_parts) if query_parts else None

        return await self.get_all(q=q, limit=limit, **kwargs)

    async def get_by_time_range(
        self,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        limit: Optional[int] = None,
        **kwargs,
    ) -> Union[List[Dict[str, Any]], int]:
        """
        Query traffic environment impacts by observation time range.

        Args:
            start_time: Start time in ISO8601 format (inclusive)
            end_time: End time in ISO8601 format (inclusive)
            limit: Maximum number of results
            **kwargs: Additional query parameters

        Returns:
            List of TrafficEnvironmentImpact entities

        Examples:
            # Get entities from last 24 hours
            entities = await service.get_by_time_range(
                start_time="2025-11-16T10:00:00Z",
                end_time="2025-11-17T10:00:00Z"
            )

            # Get entities observed after a specific time
            recent = await service.get_by_time_range(start_time="2025-11-17T08:00:00Z")
        """
        query_parts = []
        if start_time is not None:
            query_parts.append(f'dateObservedFrom>="{start_time}"')
        if end_time is not None:
            query_parts.append(f'dateObservedTo<="{end_time}"')

        q = ";".join(query_parts) if query_parts else None

        return await self.get_all(q=q, limit=limit, **kwargs)

    async def get_by_vehicle_class(
        self, vehicle_class: str, limit: Optional[int] = None, **kwargs
    ) -> Union[List[Dict[str, Any]], int]:
        """
        Query traffic environment impacts by vehicle class.

        Args:
            vehicle_class: The vehicle class to filter by
            limit: Maximum number of results
            **kwargs: Additional query parameters

        Returns:
            List of TrafficEnvironmentImpact entities

        Example:
            # Get impacts for passenger cars
            passenger_cars = await service.get_by_vehicle_class("passengerCar", limit=50)
        """
        q = f'traffic.vehicleClass=="{vehicle_class}"'
        return await self.get_all(q=q, limit=limit, **kwargs)

    async def get_by_traffic_flow_reference(
        self,
        traffic_flow_id: str,
        limit: Optional[int] = None,
        **kwargs,
    ) -> Union[List[Dict[str, Any]], int]:
        """
        Query traffic environment impacts by traffic flow reference.

        Args:
            traffic_flow_id: The traffic flow observed entity ID
            limit: Maximum number of results
            **kwargs: Additional query parameters

        Returns:
            List of TrafficEnvironmentImpact entities

        Example:
            entities = await service.get_by_traffic_flow_reference(
                "urn:ngsi-ld:TrafficFlowObserved:001",
                limit=20
            )
        """
        q = f'traffic.refTrafficFlowObserved=="{traffic_flow_id}"'
        return await self.get_all(q=q, limit=limit, **kwargs)


traffic_environment_impact_service = TrafficEnvironmentImpactService()
