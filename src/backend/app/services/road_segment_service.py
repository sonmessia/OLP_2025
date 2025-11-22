import logging
from typing import Any, Dict, List, Optional, Union

import httpx

from app.models.RoadSegment import RoadSegment

from .base_service import BaseService

logger = logging.getLogger(__name__)


class RoadSegmentService(BaseService):
    """
    Service layer for RoadSegment entities.
    Provides high-level methods for CRUD operations on road segment data.

    This service is designed to work with FIWARE Orion-LD context broker
    following NGSI-LD specifications for road segment monitoring and management.

    Usage as singleton:
        from app.services.road_segment_service import road_segment_service
        await road_segment_service.initialize()
        try:
            entities = await road_segment_service.get_all(limit=10)
        finally:
            await road_segment_service.close()

    Author: sonmessia
    Created: 2025-11-22
    """

    _instance: Optional["RoadSegmentService"] = None

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
            self.entity_type = "RoadSegment"
            self._initialized = True

    async def initialize(self):
        """Initialize the singleton service with HTTP client."""
        await self._get_client()
        logger.debug("RoadSegmentService singleton initialized")

    async def create(self, entity_data: Dict[str, Any]) -> httpx.Response:
        """
        Create a new RoadSegment entity.

        Args:
            entity_data: Dictionary containing entity attributes.
                        Must include 'id' at minimum.

        Returns:
            httpx.Response with status 201 on success

        Raises:
            ValueError: If required id field is missing
            httpx.HTTPStatusError: If the entity already exists (409)

        Example:
            entity = {
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
            response = await service.create(entity)
        """
        if "id" not in entity_data:
            raise ValueError("id attribute is required for RoadSegment entity.")

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
        Query for RoadSegment entities.
        Automatically adds the 'type=RoadSegment' filter to all queries.

        Args:
            id: Filter by entity ID(s), comma-separated
            q: Query filter (e.g., "roadClass==MAJOR_CITY_ROAD", "length>5.0")

            pick: Preferred - Attributes to select (comma-separated)
            attrs: Legacy - Attributes to include (comma-separated)

            georel: Geo-relationship (e.g., "near;maxDistance==2000")
            geometry: Geometry type (Point, LineString, Polygon, etc.)
            coordinates: Coordinates array as string (e.g., "[-3.7038, 40.4168]")
            geoproperty: Property to use for geo-queries (default: "location")

            limit: Maximum number of results
            offset: Offset for pagination

            count: If True, returns only the count of matching entities
            format: Response format ('simplified' for key-value pairs)
            options: Query options (e.g., 'sysAttrs' for system attributes)

            local: If True, query only local entities (not federated)

            **kwargs: Additional query parameters

        Returns:
            List of RoadSegment entities or count (int) if count=True

        Examples:
            # Get all road segments (up to 100)
            entities = await service.get_all(limit=100)

            # Get major city roads
            major_roads = await service.get_all(
                q="roadClass==MAJOR_CITY_ROAD",
                limit=50
            )

            # Get road segments with specific attributes
            roads = await service.get_all(
                pick="id,type,roadName,roadClass,length,location",
                format="simplified",
                limit=20
            )

            # Get count of all entities
            total_count = await service.get_all(count=True)

            # Get specific entities by ID
            entities = await service.get_all(
                id="urn:ngsi-ld:RoadSegment:001,urn:ngsi-ld:RoadSegment:002",
                pick="id,type,roadName",
                format="simplified"
            )

            # Geo-spatial query for road segments in an area
            nearby = await service.get_all(
                georel="near;maxDistance==5000",
                geometry="Point",
                coordinates="[-3.7038,40.4168]",  # Madrid coordinates
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
        Retrieve a RoadSegment entity by its ID.

        Args:
            entity_id: The entity identifier (URI)
            attrs: Comma-separated list of attribute names to retrieve
            options: Query options (e.g., 'keyValues', 'sysAttrs')
            **kwargs: Additional query parameters

        Returns:
            RoadSegment entity data as dictionary

        Example:
            entity = await service.get_by_id(
                "urn:ngsi-ld:RoadSegment:Madrid-001",
                attrs="id,type,roadName,roadClass,length"
            )
        """
        return await super().get_entity_by_id(
            entity_id=entity_id, attrs=attrs, options=options, **kwargs
        )

    async def update(
        self, entity_id: str, attrs_data: Dict[str, Any]
    ) -> httpx.Response:
        """
        Update specific attributes of a RoadSegment entity.

        Args:
            entity_id: The entity identifier
            attrs_data: Dictionary of attributes to update

        Returns:
            httpx.Response with status 204 on success

        Example:
            await service.update(
                "urn:ngsi-ld:RoadSegment:Madrid-001",
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
            )
        """
        return await super().update_entity_attributes(entity_id, attrs_data)

    async def replace(
        self,
        entity_id: str,
        entity_data: Union[RoadSegment, Dict[str, Any]],
    ) -> httpx.Response:
        """
        Replace an entire RoadSegment entity.

        Args:
            entity_id: The entity identifier
            entity_data: Complete entity data (Pydantic model or dictionary)

        Returns:
            httpx.Response with status 204 on success

        Example:
            new_data = {
                "id": "urn:ngsi-ld:RoadSegment:Madrid-001",
                "type": "RoadSegment",
                "roadName": "Gran Via",
                "roadClass": "MAJOR_CITY_ROAD",
                "length": 2.8,
                "width": 14.0,
                "totalLaneNumber": 6,
                "maximumAllowedSpeed": 50.0
            }
            await service.replace("urn:ngsi-ld:RoadSegment:Madrid-001", new_data)
        """
        if isinstance(entity_data, RoadSegment):
            entity_data = entity_data.model_dump(exclude_unset=True)

        entity_data["type"] = self.entity_type
        return await super().replace_entity(entity_id, entity_data)

    async def delete(self, entity_id: str) -> httpx.Response:
        """
        Delete a RoadSegment entity.

        Args:
            entity_id: The entity identifier

        Returns:
            httpx.Response with status 204 on success

        Example:
            await service.delete("urn:ngsi-ld:RoadSegment:Madrid-001")
        """
        return await super().delete_entity(entity_id)

    async def batch_create(self, entities: List[Dict[str, Any]]) -> httpx.Response:
        """
        Create multiple RoadSegment entities in batch.

        Args:
            entities: List of entity dictionaries with required fields

        Returns:
            httpx.Response with status 201/207 and success/error details

        Example:
            entities = [
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
            response = await service.batch_create(entities)
        """
        for entity in entities:
            if "id" not in entity:
                raise ValueError(
                    "id attribute is required for all entities in batch create."
                )
            entity["type"] = self.entity_type

        return await super().batch_create(entities)

    async def batch_upsert(
        self, entities: List[Dict[str, Any]], options: str = "update"
    ) -> httpx.Response:
        """
        Create or update multiple RoadSegment entities in batch.

        Args:
            entities: List of entity dictionaries
            options: 'update' (default) or 'replace'

        Returns:
            httpx.Response with status 201/204/207

        Example:
            entities = [
                {
                    "id": "urn:ngsi-ld:RoadSegment:001",
                    "roadName": "Main Street",
                    "roadClass": "MAJOR_CITY_ROAD",
                    "length": 1.6
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
        Update multiple RoadSegment entities in batch.

        Args:
            entities: List of entity dictionaries with updates
            options: 'update' (default) or 'replace'

        Returns:
            httpx.Response with status 204/207

        Example:
            entities = [
                {
                    "id": "urn:ngsi-ld:RoadSegment:001",
                    "maximumAllowedSpeed": {"type": "Property", "value": 45.0}
                }
            ]
            response = await service.batch_update(entities)
        """
        for entity in entities:
            entity["type"] = self.entity_type

        return await super().batch_update(entities, options=options)

    async def batch_delete(self, entity_ids: List[str]) -> httpx.Response:
        """
        Delete multiple RoadSegment entities in batch.

        Args:
            entity_ids: List of entity identifiers (URIs)

        Returns:
            httpx.Response with status 204/207

        Example:
            entity_ids = [
                "urn:ngsi-ld:RoadSegment:001",
                "urn:ngsi-ld:RoadSegment:002"
            ]
            response = await service.batch_delete(entity_ids)
        """
        return await super().batch_delete(entity_ids)

    async def get_by_road_class(
        self, road_class: str, limit: Optional[int] = None, **kwargs
    ) -> Union[List[Dict[str, Any]], int]:
        """
        Query road segments by road class.

        Args:
            road_class: The road class to filter by (e.g., "MAJOR_CITY_ROAD")
            limit: Maximum number of results
            **kwargs: Additional query parameters

        Returns:
            List of RoadSegment entities

        Example:
            # Get major city roads
            major_roads = await service.get_by_road_class("MAJOR_CITY_ROAD", limit=50)
        """
        q = f'roadClass=="{road_class}"'
        return await self.get_all(q=q, limit=limit, **kwargs)

    async def get_by_speed_limit(
        self,
        min_speed: Optional[float] = None,
        max_speed: Optional[float] = None,
        limit: Optional[int] = None,
        **kwargs,
    ) -> Union[List[Dict[str, Any]], int]:
        """
        Query road segments by speed limit range.

        Args:
            min_speed: Minimum speed limit in km/h (inclusive)
            max_speed: Maximum speed limit in km/h (inclusive)
            limit: Maximum number of results
            **kwargs: Additional query parameters

        Returns:
            List of RoadSegment entities

        Examples:
            # Get roads with speed limit between 40 and 60 km/h
            roads = await service.get_by_speed_limit(min_speed=40, max_speed=60)

            # Get roads with speed limit above 80 km/h
            high_speed_roads = await service.get_by_speed_limit(min_speed=80)

            # Get roads with speed limit below 30 km/h
            low_speed_roads = await service.get_by_speed_limit(max_speed=30, limit=20)
        """
        query_parts = []
        if min_speed is not None:
            query_parts.append(f"maximumAllowedSpeed>={min_speed}")
        if max_speed is not None:
            query_parts.append(f"maximumAllowedSpeed<={max_speed}")

        q = ";".join(query_parts) if query_parts else None

        return await self.get_all(q=q, limit=limit, **kwargs)

    async def get_by_length_range(
        self,
        min_length: Optional[float] = None,
        max_length: Optional[float] = None,
        limit: Optional[int] = None,
        **kwargs,
    ) -> Union[List[Dict[str, Any]], int]:
        """
        Query road segments by length range.

        Args:
            min_length: Minimum length in km (inclusive)
            max_length: Maximum length in km (inclusive)
            limit: Maximum number of results
            **kwargs: Additional query parameters

        Returns:
            List of RoadSegment entities

        Examples:
            # Get segments between 1 and 5 km
            segments = await service.get_by_length_range(min_length=1, max_length=5)

            # Get long segments above 10 km
            long_segments = await service.get_by_length_range(min_length=10)

            # Get short segments below 1 km
            short_segments = await service.get_by_length_range(max_length=1, limit=50)
        """
        query_parts = []
        if min_length is not None:
            query_parts.append(f"length>={min_length}")
        if max_length is not None:
            query_parts.append(f"length<={max_length}")

        q = ";".join(query_parts) if query_parts else None

        return await self.get_all(q=q, limit=limit, **kwargs)

    async def get_by_lane_count(
        self,
        min_lanes: Optional[int] = None,
        max_lanes: Optional[int] = None,
        limit: Optional[int] = None,
        **kwargs,
    ) -> Union[List[Dict[str, Any]], int]:
        """
        Query road segments by number of lanes.

        Args:
            min_lanes: Minimum number of lanes (inclusive)
            max_lanes: Maximum number of lanes (inclusive)
            limit: Maximum number of results
            **kwargs: Additional query parameters

        Returns:
            List of RoadSegment entities

        Examples:
            # Get segments with 4 lanes exactly
            segments = await service.get_by_lane_count(min_lanes=4, max_lanes=4)

            # Get segments with 4 or more lanes
            multi_lane = await service.get_by_lane_count(min_lanes=4)

            # Get segments with 2 or fewer lanes
            few_lanes = await service.get_by_lane_count(max_lanes=2, limit=50)
        """
        query_parts = []
        if min_lanes is not None:
            query_parts.append(f"totalLaneNumber>={min_lanes}")
        if max_lanes is not None:
            query_parts.append(f"totalLaneNumber<={max_lanes}")

        q = ";".join(query_parts) if query_parts else None

        return await self.get_all(q=q, limit=limit, **kwargs)

    async def get_by_road_name(
        self,
        road_name: str,
        exact_match: bool = False,
        limit: Optional[int] = None,
        **kwargs,
    ) -> Union[List[Dict[str, Any]], int]:
        """
        Query road segments by road name.

        Args:
            road_name: The road name to search for
            exact_match: If True, uses exact match; if False, uses case-insensitive search
            limit: Maximum number of results
            **kwargs: Additional query parameters

        Returns:
            List of RoadSegment entities

        Examples:
            # Get exact match for "Gran Via"
            gran_via = await service.get_by_road_name("Gran Via", exact_match=True)

            # Get case-insensitive search for "main"
            main_streets = await service.get_by_road_name("main", exact_match=False)
        """
        if exact_match:
            q = f'roadName=="{road_name}"'
        else:
            # Case-insensitive search
            q = f'roadName=~"(?i).*{road_name}.*"'

        return await self.get_all(q=q, limit=limit, **kwargs)

    async def get_by_status(
        self, status: str, limit: Optional[int] = None, **kwargs
    ) -> Union[List[Dict[str, Any]], int]:
        """
        Query road segments by status.

        Args:
            status: The status to filter by ("open", "closed", "limited")
            limit: Maximum number of results
            **kwargs: Additional query parameters

        Returns:
            List of RoadSegment entities

        Example:
            # Get closed road segments
            closed_roads = await service.get_by_status("closed", limit=20)
        """
        q = f'status=="{status}"'
        return await self.get_all(q=q, limit=limit, **kwargs)

    async def get_by_vehicle_type(
        self, vehicle_type: str, limit: Optional[int] = None, **kwargs
    ) -> Union[List[Dict[str, Any]], int]:
        """
        Query road segments by allowed vehicle type.

        Args:
            vehicle_type: The vehicle type to filter by (e.g., "car", "bus", "truck")
            limit: Maximum number of results
            **kwargs: Additional query parameters

        Returns:
            List of RoadSegment entities

        Example:
            # Get segments where buses are allowed
            bus_roads = await service.get_by_vehicle_type("bus", limit=50)
        """
        q = f'allowedVehicleType=="{vehicle_type}"'
        return await self.get_all(q=q, limit=limit, **kwargs)


road_segment_service = RoadSegmentService()
