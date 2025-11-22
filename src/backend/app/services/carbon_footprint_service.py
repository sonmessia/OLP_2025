# carbon_footprint_service.py
import logging
from typing import Any, Dict, List, Optional, Union

import httpx

from app.models.CarbonFootprint import CarbonFootprint

from .base_service import BaseService

logger = logging.getLogger(__name__)


class CarbonFootprintService(BaseService):
    """
    Service layer for CarbonFootprint entities.
    Provides high-level methods for CRUD operations on carbon emissions data.

    This service is designed to work with FIWARE Orion-LD context broker
    following NGSI-LD specifications for carbon footprint tracking.

    Usage:
        # Context manager (recommended)
        async with CarbonFootprintService() as service:
            emissions = await service.get_all(limit=10)

        # Manual lifecycle
        service = CarbonFootprintService()
        try:
            emission = await service.get_by_id("urn:ngsi-ld:CarbonFootprint:001")
        finally:
            await service.close()

    Author: sonmessia
    Created: 2025-11-15
    """

    def __init__(
        self, orion_url: Optional[str] = None, context_url: Optional[str] = None
    ):
        """
        Initialize CarbonFootprintService.

        Args:
            orion_url: Orion-LD broker URL (default from env: ORION_LD_URL)
            context_url: JSON-LD context URL (default from env: CONTEXT_URL)
        """
        super().__init__(orion_url, context_url)
        self.entity_type = "CarbonFootprint"

    async def create(self, entity_data: Dict[str, Any]) -> httpx.Response:
        """
        Create a new CarbonFootprint entity.

        Args:
            entity_data: Dictionary containing entity attributes.
                        Must include 'id' and 'emissionDate' at minimum.

        Returns:
            httpx.Response with status 201 on success

        Raises:
            ValueError: If required emissionDate field is missing
            httpx.HTTPStatusError: If the entity already exists (409)

        Example:
            emission = {
                "id": "urn:ngsi-ld:CarbonFootprint:Transport-Madrid-001",
                "emissionDate": "2025-11-15T12:30:00Z",
                "CO2eq": {
                    "type": "Property",
                    "value": 125.5,
                    "unitCode": "KGM"
                },
                "emissionSource": {
                    "type": "Property",
                    "value": "Transport"
                },
                "location": {
                    "type": "GeoProperty",
                    "value": {
                        "type": "Point",
                        "coordinates": [-3.703790, 40.416775]
                    }
                }
            }
            response = await service.create(emission)
        """
        if "emissionDate" not in entity_data:
            raise ValueError(
                "emissionDate attribute is required for CarbonFootprint entity."
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
        Query for CarbonFootprint entities.
        Automatically adds the 'type=CarbonFootprint' filter to all queries.

        Args:
            id: Filter by entity ID(s), comma-separated
            q: Query filter (e.g., "CO2eq>100", "emissionSource==Transport")

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
            List of CarbonFootprint entities or count (int) if count=True

        Examples:
            # Get all emissions (up to 100)
            emissions = await service.get_all(limit=100)

            # Get high CO2 emissions
            high_emissions = await service.get_all(
                q="CO2eq>100",
                format="simplified",
                limit=10
            )

            # Get emissions from specific source
            transport = await service.get_all(
                q="emissionSource==Transport",
                pick="id,type,CO2eq,emissionDate,emissionSource",
                format="simplified",
                limit=20
            )

            # Count total emissions
            count = await service.get_all(count=True)

            # Geo-spatial query - find emissions in area
            nearby = await service.get_all(
                georel="near;maxDistance==5000",
                geometry="Point",
                coordinates="[-3.703790,40.416775]",
                limit=10
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
        Retrieve a specific CarbonFootprint entity by ID.

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
            # Get full emission record
            emission = await service.get_by_id(
                "urn:ngsi-ld:CarbonFootprint:Transport-Madrid-001"
            )

            # Get specific attributes in simplified format
            data = await service.get_by_id(
                "urn:ngsi-ld:CarbonFootprint:Transport-Madrid-001",
                pick="id,type,CO2eq,emissionDate,emissionSource",
                format="simplified"
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
        Update specific attributes of a CarbonFootprint entity.

        Args:
            entity_id: The entity identifier
            update_data: Dictionary with attributes to update

        Returns:
            HTTP status code (204 on success)

        Example:
            status = await service.update_attrs(
                "urn:ngsi-ld:CarbonFootprint:Transport-Madrid-001",
                {
                    "CO2eq": {
                        "type": "Property",
                        "value": 130.2,
                        "unitCode": "KGM"
                    },
                    "tags": {
                        "type": "Property",
                        "value": ["vehicle", "urban", "daily"]
                    }
                }
            )
        """
        response = await super().update_entity_attributes(entity_id, update_data)
        return response.status_code

    async def replace(
        self, entity_id: str, entity_data: Union[Dict[str, Any], CarbonFootprint]
    ) -> int:
        """
        Replace an entire CarbonFootprint entity.

        Args:
            entity_id: The entity identifier
            entity_data: Complete entity data (will replace all attributes)

        Returns:
            HTTP status code (204 on success)
        """
        if isinstance(entity_data, CarbonFootprint):
            entity_dict = entity_data.model_dump(exclude_unset=True)
        else:
            entity_dict = entity_data

        entity_dict["type"] = self.entity_type
        response = await super().replace_entity(entity_id, entity_dict)
        return response.status_code

    async def delete(self, entity_id: str) -> int:
        """
        Delete a CarbonFootprint entity.

        Args:
            entity_id: The entity identifier

        Returns:
            HTTP status code (204 on success)
        """
        response = await super().delete_entity(entity_id)
        return response.status_code

    async def delete_attribute(self, entity_id: str, attribute_name: str) -> int:
        """
        Delete a specific attribute from a CarbonFootprint entity.

        Args:
            entity_id: The entity identifier
            attribute_name: Name of the attribute to delete

        Returns:
            HTTP status code (204 on success)
        """
        response = await super().delete_entity_attribute(entity_id, attribute_name)
        return response.status_code

    async def batch_upsert(
        self, entities: List[Dict[str, Any]], options: str = "update"
    ) -> httpx.Response:
        """
        Create or update a list of CarbonFootprint entities.

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
        Create multiple CarbonFootprint entities.

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
        Delete multiple CarbonFootprint entities.

        Args:
            entity_ids: List of entity identifiers (URNs)

        Returns:
            httpx.Response with status 204/207
        """
        return await super().batch_delete(entity_ids)

    async def find_by_source(
        self,
        emission_source: str,
        limit: Optional[int] = None,
        format: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Find CarbonFootprint entities by emission source.

        Args:
            emission_source: Source type (Transport, Industry, Agriculture, etc.)
            limit: Maximum number of results
            format: Response format

        Returns:
            List of emissions from the specified source

        Example:
            transport = await service.find_by_source(
                emission_source="Transport",
                limit=50,
                format="simplified"
            )
        """
        result = await self.get_all(
            q=f"emissionSource=={emission_source}",
            limit=limit,
            format=format,
            count=False,
        )
        if isinstance(result, int):
            return []
        return result

    async def find_high_emissions(
        self,
        threshold: float = 100.0,
        limit: Optional[int] = None,
        format: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Find emissions exceeding a CO2eq threshold.

        Args:
            threshold: CO2eq threshold value (kg)
            limit: Maximum number of results
            format: Response format

        Returns:
            List of high emission records

        Example:
            high = await service.find_high_emissions(
                threshold=150.0,
                limit=20,
                format="simplified"
            )
        """
        result = await self.get_all(
            q=f"CO2eq>{threshold}", limit=limit, format=format, count=False
        )
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
        Get recent CarbonFootprint entities since a specific time.

        Args:
            since: ISO8601 timestamp (e.g., "2025-11-15T10:00:00Z")
            limit: Maximum number of results
            format: Response format
            pick: Attributes to select

        Returns:
            List of recent emissions

        Example:
            recent = await service.get_recent(
                since="2025-11-15T00:00:00Z",
                limit=50,
                format="simplified",
                pick="id,type,emissionDate,CO2eq,emissionSource"
            )
        """
        q = f"emissionDate>'{since}'"
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
        Find CarbonFootprint entities near a specific location.

        Args:
            coordinates: Coordinates as string "[lon,lat]"
            max_distance: Maximum distance in meters (default: 5000m)
            limit: Maximum number of results
            format: Response format
            pick: Attributes to select

        Returns:
            List of nearby emissions

        Example:
            nearby = await service.find_by_location(
                coordinates="[-3.703790,40.416775]",
                max_distance=5000,
                limit=10,
                pick="id,type,CO2eq,emissionSource,location",
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


# Singleton instance for convenience (optional)
carbon_footprint_service = CarbonFootprintService()
