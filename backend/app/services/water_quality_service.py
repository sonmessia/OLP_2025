# water_quality_service.py
from typing import Optional, Dict, Any, List, Union
from .base_service import BaseService
import httpx
import logging

logger = logging.getLogger(__name__)


class WaterQualityService(BaseService):
    """
    Service layer for WaterQualityObserved entities.
    Provides high-level methods for CRUD operations on water quality monitoring data.

    This service is designed to work with FIWARE Orion-LD context broker
    following NGSI-LD specifications for water quality observations.

    Usage:
        # Context manager (recommended)
        async with WaterQualityService() as service:
            observations = await service.get_all(limit=10)

        # Manual lifecycle
        service = WaterQualityService()
        try:
            observation = await service.get_by_id("urn:ngsi-ld:WaterQualityObserved:001")
        finally:
            await service.close()

    Author: sonmessia
    Created: 2025-11-15
    """

    def __init__(
        self, orion_url: Optional[str] = None, context_url: Optional[str] = None
    ):
        """
        Initialize WaterQualityService.

        Args:
            orion_url: Orion-LD broker URL (default from env: ORION_LD_URL)
            context_url: JSON-LD context URL (default from env: CONTEXT_URL)
        """
        super().__init__(orion_url, context_url)
        self.entity_type = "WaterQualityObserved"

    async def create(self, entity_data: Dict[str, Any]) -> httpx.Response:
        """
        Create a new WaterQualityObserved entity.

        Args:
            entity_data: Dictionary containing entity attributes.
                        Must include 'id' and 'dateObserved' at minimum.

        Returns:
            httpx.Response with status 201 on success

        Raises:
            ValueError: If required dateObserved field is missing
            httpx.HTTPStatusError: If the entity already exists (409)

        Example:
            observation = {
                "id": "urn:ngsi-ld:WaterQualityObserved:River-Madrid-001",
                "dateObserved": "2025-11-15T12:37:09Z",
                "pH": {
                    "type": "Property",
                    "value": 7.2
                },
                "temperature": {
                    "type": "Property",
                    "value": 15.3,
                    "unitCode": "CEL"
                },
                "conductivity": {
                    "type": "Property",
                    "value": 450.5,
                    "unitCode": "D63"
                },
                "location": {
                    "type": "GeoProperty",
                    "value": {
                        "type": "Point",
                        "coordinates": [-3.703790, 40.416775]
                    }
                }
            }
            response = await service.create(observation)
        """
        if "dateObserved" not in entity_data:
            raise ValueError(
                "dateObserved attribute is required for WaterQualityObserved entity."
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
        Query for WaterQualityObserved entities.
        Automatically adds the 'type=WaterQualityObserved' filter to all queries.

        Args:
            id: Filter by entity ID(s), comma-separated
            q: Query filter (e.g., "pH>7", "temperature<20", "turbidity>5")

            pick: Preferred - Attributes to select (comma-separated)
            attrs: Legacy - Attributes to include (comma-separated)

            georel: Geo-relationship (e.g., "near;maxDistance==5000")
            geometry: Geometry type (Point, LineString, Polygon, etc.)
            coordinates: Coordinates array as string
            geoproperty: Property to use for geo-queries (default: "location")

            limit: Maximum number of results
            offset: Offset for pagination

            count: If True, returns only the count of matching entities
            format: Response format ('simplified' for key-value pairs)
            options: Query options (e.g., 'sysAttrs' for system attributes)

            local: If True, query only local entities (not federated)

            **kwargs: Additional query parameters

        Returns:
            List of WaterQualityObserved entities or count (int) if count=True

        Examples:
            # Get all water quality observations (up to 100)
            observations = await service.get_all(limit=100)

            # Get observations with pH above 8 (alkaline)
            alkaline = await service.get_all(
                q="pH>8",
                format="simplified",
                limit=10
            )

            # Get observations with high turbidity
            turbid = await service.get_all(
                q="turbidity>10",
                pick="id,type,turbidity,dateObserved,location",
                format="simplified",
                limit=20
            )

            # Count total observations
            count = await service.get_all(count=True)

            # Geo-spatial query - find monitoring stations in area
            nearby = await service.get_all(
                georel="near;maxDistance==5000",
                geometry="Point",
                coordinates="[-3.703790,40.416775]",
                limit=10
            )

            # Get recent high-temperature readings
            warm_water = await service.get_all(
                q="temperature>25;dateObserved>'2025-11-14T00:00:00Z'",
                format="simplified",
                limit=20
            )
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
        Retrieve a specific WaterQualityObserved entity by ID.

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
            # Get full observation
            observation = await service.get_by_id(
                "urn:ngsi-ld:WaterQualityObserved:River-Madrid-001"
            )

            # Get specific parameters in simplified format
            data = await service.get_by_id(
                "urn:ngsi-ld:WaterQualityObserved:River-Madrid-001",
                pick="id,type,pH,temperature,conductivity,dateObserved",
                format="simplified"
            )
            # Returns: {"id": "...", "pH": 7.2, "temperature": 15.3, ...}
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
        Update specific attributes of a WaterQualityObserved entity.

        Args:
            entity_id: The entity identifier
            update_data: Dictionary with attributes to update

        Returns:
            HTTP status code (204 on success)

        Example:
            status = await service.update_attrs(
                "urn:ngsi-ld:WaterQualityObserved:River-Madrid-001",
                {
                    "pH": {
                        "type": "Property",
                        "value": 7.5
                    },
                    "temperature": {
                        "type": "Property",
                        "value": 16.2,
                        "unitCode": "CEL"
                    },
                    "dateObserved": {
                        "type": "Property",
                        "value": "2025-11-15T12:37:09Z"
                    }
                }
            )
        """
        response = await super().update_entity_attributes(entity_id, update_data)
        return response.status_code

    async def replace(self, entity_id: str, entity_data: Dict[str, Any]) -> int:
        """
        Replace an entire WaterQualityObserved entity.

        Args:
            entity_id: The entity identifier
            entity_data: Complete entity data (will replace all attributes)

        Returns:
            HTTP status code (204 on success)
        """
        entity_data["type"] = self.entity_type
        response = await super().replace_entity(entity_id, entity_data)
        return response.status_code

    async def delete(self, entity_id: str) -> int:
        """
        Delete a WaterQualityObserved entity.

        Args:
            entity_id: The entity identifier

        Returns:
            HTTP status code (204 on success)
        """
        response = await super().delete_entity(entity_id)
        return response.status_code

    async def delete_attribute(self, entity_id: str, attribute_name: str) -> int:
        """
        Delete a specific attribute from a WaterQualityObserved entity.

        Args:
            entity_id: The entity identifier
            attribute_name: Name of the attribute to delete

        Returns:
            HTTP status code (204 on success)

        Example:
            status = await service.delete_attribute(
                "urn:ngsi-ld:WaterQualityObserved:River-Madrid-001",
                "turbidity"
            )
        """
        response = await super().delete_entity_attribute(entity_id, attribute_name)
        return response.status_code

    async def batch_upsert(
        self, entities: List[Dict[str, Any]], options: str = "update"
    ) -> httpx.Response:
        """
        Create or update a list of WaterQualityObserved entities.

        Args:
            entities: List of entity dictionaries
            options: 'update' (default) or 'replace'

        Returns:
            httpx.Response with status 201/204/207
        """
        for entity in entities:
            entity["type"] = self.entity_type

        return await super().batch_upsert(entities, options)

    async def batch_create(self, entities: List[Dict[str, Any]]) -> httpx.Response:
        """
        Create multiple WaterQualityObserved entities.

        Args:
            entities: List of entity dictionaries

        Returns:
            httpx.Response with created entity IDs or errors
        """
        for entity in entities:
            entity["type"] = self.entity_type

        return await super().batch_create(entities)

    async def batch_delete(self, entity_ids: List[str]) -> httpx.Response:
        """
        Delete multiple WaterQualityObserved entities.

        Args:
            entity_ids: List of entity identifiers (URNs)

        Returns:
            httpx.Response with status 204/207
        """
        return await super().batch_delete(entity_ids)

    async def find_poor_quality(
        self,
        parameter: str = "pH",
        min_value: Optional[float] = None,
        max_value: Optional[float] = None,
        limit: Optional[int] = None,
        format: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Find water quality observations outside acceptable ranges.

        Args:
            parameter: Water quality parameter (pH, turbidity, etc.)
            min_value: Minimum acceptable value
            max_value: Maximum acceptable value
            limit: Maximum number of results
            format: Response format

        Returns:
            List of observations with poor quality

        Examples:
            # Find acidic water (pH < 6.5)
            acidic = await service.find_poor_quality(
                parameter="pH",
                max_value=6.5,
                limit=20,
                format="simplified"
            )

            # Find alkaline water (pH > 8.5)
            alkaline = await service.find_poor_quality(
                parameter="pH",
                min_value=8.5,
                limit=20,
                format="simplified"
            )

            # Find high turbidity (> 10 NTU)
            turbid = await service.find_poor_quality(
                parameter="turbidity",
                min_value=10,
                limit=20,
                format="simplified"
            )
        """
        if min_value is not None and max_value is not None:
            # Out of range (too low OR too high)
            q = f"{parameter}<{min_value}|{parameter}>{max_value}"
        elif min_value is not None:
            q = f"{parameter}>{min_value}"
        elif max_value is not None:
            q = f"{parameter}<{max_value}"
        else:
            raise ValueError("Either min_value or max_value must be specified")

        result = await self.get_all(q=q, limit=limit, format=format, count=False)
        if isinstance(result, int):
            return []
        return result

    async def get_recent(
        self,
        since: str,
        limit: Optional[int] = None,
        format: Optional[str] = None,
        pick: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Get recent WaterQualityObserved entities since a specific time.

        Args:
            since: ISO8601 timestamp (e.g., "2025-11-15T00:00:00Z")
            limit: Maximum number of results
            format: Response format
            pick: Attributes to select

        Returns:
            List of recent observations

        Example:
            recent = await service.get_recent(
                since="2025-11-15T00:00:00Z",
                limit=50,
                format="simplified",
                pick="id,type,dateObserved,pH,temperature,turbidity"
            )
        """
        q = f"dateObserved>'{since}'"
        result = await self.get_all(
            q=q, limit=limit, format=format, pick=pick, count=False
        )
        if isinstance(result, int):
            return []
        return result

    async def find_by_location(
        self,
        coordinates: str,
        max_distance: int = 5000,
        limit: Optional[int] = None,
        format: Optional[str] = None,
        pick: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Find WaterQualityObserved entities near a specific location.

        Args:
            coordinates: Coordinates as string "[lon,lat]"
            max_distance: Maximum distance in meters (default: 5000m)
            limit: Maximum number of results
            format: Response format
            pick: Attributes to select

        Returns:
            List of nearby observations

        Example:
            nearby = await service.find_by_location(
                coordinates="[-3.703790,40.416775]",
                max_distance=5000,
                limit=10,
                pick="id,type,pH,temperature,location",
                format="simplified"
            )
        """
        result = await self.get_all(
            georel=f"near;maxDistance=={max_distance}",
            geometry="Point",
            coordinates=coordinates,
            limit=limit,
            format=format,
            pick=pick,
            count=False,
        )
        if isinstance(result, int):
            return []
        return result

    async def find_contaminated(
        self,
        contaminant: str,
        threshold: float,
        limit: Optional[int] = None,
        format: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Find water samples with high contaminant levels.

        Args:
            contaminant: Contaminant name (e.g., 'Pb', 'Hg', 'Cd', 'escherichiaColi')
            threshold: Threshold value
            limit: Maximum number of results
            format: Response format

        Returns:
            List of contaminated samples

        Examples:
            # Find high lead levels
            lead_contamination = await service.find_contaminated(
                contaminant="Pb",
                threshold=0.015,  # EPA action level
                limit=20,
                format="simplified"
            )

            # Find E. coli contamination
            ecoli = await service.find_contaminated(
                contaminant="escherichiaColi",
                threshold=126,  # EPA threshold (CFU/100ml)
                limit=20,
                format="simplified"
            )
        """
        result = await self.get_all(
            q=f"{contaminant}>{threshold}", limit=limit, format=format, count=False
        )
        if isinstance(result, int):
            return []
        return result


# Singleton instance for convenience (optional)
water_quality_service = WaterQualityService()
