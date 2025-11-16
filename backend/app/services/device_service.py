# device_service.py
import logging
from typing import Any, Dict, List, Optional, Union

import httpx

from .base_service import BaseService

logger = logging.getLogger(__name__)


class DeviceService(BaseService):
    """
    Service layer for Device entities.
    Provides high-level methods for CRUD operations on IoT devices and sensors.

    This service is designed to work with FIWARE Orion-LD context broker
    following NGSI-LD specifications for device management.

    Usage:
        # Context manager (recommended)
        async with DeviceService() as service:
            devices = await service.get_all(limit=10)

        # Manual lifecycle
        service = DeviceService()
        try:
            device = await service.get_by_id("urn:ngsi-ld:Device:001")
        finally:
            await service.close()

    Author: sonmessia
    Created: 2025-11-15
    """

    def __init__(
        self, orion_url: Optional[str] = None, context_url: Optional[str] = None
    ):
        """
        Initialize DeviceService.

        Args:
            orion_url: Orion-LD broker URL (default from env: ORION_LD_URL)
            context_url: JSON-LD context URL (default from env: CONTEXT_URL)
        """
        super().__init__(orion_url, context_url)
        self.entity_type = "Device"

    async def create(self, entity_data: Dict[str, Any]) -> httpx.Response:
        """
        Create a new Device entity.

        Args:
            entity_data: Dictionary containing entity attributes.
                        Must include 'id' at minimum.

        Returns:
            httpx.Response with status 201 on success

        Raises:
            httpx.HTTPStatusError: If the entity already exists (409)

        Example:
            device = {
                "id": "urn:ngsi-ld:Device:Sensor-Madrid-001",
                "category": {
                    "type": "Property",
                    "value": ["sensor"]
                },
                "controlledProperty": {
                    "type": "Property",
                    "value": ["temperature", "humidity"]
                },
                "deviceState": {
                    "type": "Property",
                    "value": "active"
                },
                "batteryLevel": {
                    "type": "Property",
                    "value": 0.85
                },
                "serialNumber": {
                    "type": "Property",
                    "value": "SN-12345"
                },
                "location": {
                    "type": "GeoProperty",
                    "value": {
                        "type": "Point",
                        "coordinates": [-3.703790, 40.416775]
                    }
                }
            }
            response = await service.create(device)
        """
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
        Query for Device entities.
        Automatically adds the 'type=Device' filter to all queries.

        Args:
            id: Filter by entity ID(s), comma-separated
            q: Query filter (e.g., "batteryLevel<0.2", "deviceState==active")

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
            List of Device entities or count (int) if count=True

        Examples:
            # Get all devices (up to 100)
            devices = await service.get_all(limit=100)

            # Get devices with low battery
            low_battery = await service.get_all(
                q="batteryLevel<0.2",
                format="simplified",
                limit=10
            )

            # Get sensors only
            sensors = await service.get_all(
                q="category==sensor",
                pick="id,type,serialNumber,batteryLevel,deviceState",
                format="simplified",
                limit=20
            )

            # Count total devices
            count = await service.get_all(count=True)

            # Geo-spatial query - find devices in area
            nearby = await service.get_all(
                georel="near;maxDistance==1000",
                geometry="Point",
                coordinates="[-3.703790,40.416775]",
                limit=10
            )

            # Get active temperature sensors
            temp_sensors = await service.get_all(
                q="controlledProperty==temperature;deviceState==active",
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
        Retrieve a specific Device entity by ID.

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
            # Get full device
            device = await service.get_by_id(
                "urn:ngsi-ld:Device:Sensor-Madrid-001"
            )

            # Get specific attributes in simplified format
            data = await service.get_by_id(
                "urn:ngsi-ld:Device:Sensor-Madrid-001",
                pick="id,type,serialNumber,batteryLevel,deviceState",
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
        Update specific attributes of a Device entity.

        Args:
            entity_id: The entity identifier
            update_data: Dictionary with attributes to update

        Returns:
            HTTP status code (204 on success)

        Example:
            status = await service.update_attrs(
                "urn:ngsi-ld:Device:Sensor-Madrid-001",
                {
                    "batteryLevel": {
                        "type": "Property",
                        "value": 0.75
                    },
                    "deviceState": {
                        "type": "Property",
                        "value": "active"
                    },
                    "dateLastValueReported": {
                        "type": "Property",
                        "value": "2025-11-15T12:45:25Z"
                    }
                }
            )
        """
        response = await super().update_entity_attributes(entity_id, update_data)
        return response.status_code

    async def replace(self, entity_id: str, entity_data: Dict[str, Any]) -> int:
        """
        Replace an entire Device entity.

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
        Delete a Device entity.

        Args:
            entity_id: The entity identifier

        Returns:
            HTTP status code (204 on success)
        """
        response = await super().delete_entity(entity_id)
        return response.status_code

    async def delete_attribute(self, entity_id: str, attribute_name: str) -> int:
        """
        Delete a specific attribute from a Device entity.

        Args:
            entity_id: The entity identifier
            attribute_name: Name of the attribute to delete

        Returns:
            HTTP status code (204 on success)

        Example:
            status = await service.delete_attribute(
                "urn:ngsi-ld:Device:Sensor-Madrid-001",
                "rssi"
            )
        """
        response = await super().delete_entity_attribute(entity_id, attribute_name)
        return response.status_code

    async def batch_upsert(
        self, entities: List[Dict[str, Any]], options: str = "update"
    ) -> httpx.Response:
        """
        Create or update a list of Device entities.

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
        Create multiple Device entities.

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
        Delete multiple Device entities.

        Args:
            entity_ids: List of entity identifiers (URNs)

        Returns:
            httpx.Response with status 204/207
        """
        return await super().batch_delete(entity_ids)

    async def find_by_category(
        self, category: str, limit: Optional[int] = None, format: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Find Device entities by category.

        Args:
            category: Device category (sensor, actuator, meter, HVAC, network, etc.)
            limit: Maximum number of results
            format: Response format

        Returns:
            List of devices matching the category

        Example:
            sensors = await service.find_by_category(
                category="sensor",
                limit=50,
                format="simplified"
            )
        """
        result = await self.get_all(
            q=f"category=={category}", limit=limit, format=format, count=False
        )
        if isinstance(result, int):
            return []
        return result

    async def find_low_battery(
        self,
        threshold: float = 0.2,
        limit: Optional[int] = None,
        format: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Find devices with low battery levels.

        Args:
            threshold: Battery level threshold (0.0 to 1.0, default: 0.2 = 20%)
            limit: Maximum number of results
            format: Response format

        Returns:
            List of devices with low battery

        Example:
            low_battery = await service.find_low_battery(
                threshold=0.15,
                limit=20,
                format="simplified"
            )
        """
        result = await self.get_all(
            q=f"batteryLevel<{threshold}", limit=limit, format=format, count=False
        )
        if isinstance(result, int):
            return []
        return result

    async def find_by_state(
        self,
        device_state: str,
        limit: Optional[int] = None,
        format: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Find devices by operational state.

        Args:
            device_state: Device state (active, inactive, error, maintenance, etc.)
            limit: Maximum number of results
            format: Response format

        Returns:
            List of devices in the specified state

        Example:
            inactive = await service.find_by_state(
                device_state="inactive",
                limit=20,
                format="simplified"
            )
        """
        result = await self.get_all(
            q=f"deviceState=={device_state}", limit=limit, format=format, count=False
        )
        if isinstance(result, int):
            return []
        return result

    async def find_by_controlled_property(
        self,
        controlled_property: str,
        limit: Optional[int] = None,
        format: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Find devices that control/sense a specific property.

        Args:
            controlled_property: Property name (temperature, humidity, pressure, etc.)
            limit: Maximum number of results
            format: Response format

        Returns:
            List of devices that control/sense the property

        Example:
            temp_devices = await service.find_by_controlled_property(
                controlled_property="temperature",
                limit=30,
                format="simplified"
            )
        """
        result = await self.get_all(
            q=f"controlledProperty=={controlled_property}",
            limit=limit,
            format=format,
            count=False,
        )
        if isinstance(result, int):
            return []
        return result

    async def find_by_location(
        self,
        coordinates: str,
        max_distance: int = 1000,
        limit: Optional[int] = None,
        format: Optional[str] = None,
        pick: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Find Device entities near a specific location.

        Args:
            coordinates: Coordinates as string "[lon,lat]"
            max_distance: Maximum distance in meters (default: 1000m)
            limit: Maximum number of results
            format: Response format
            pick: Attributes to select

        Returns:
            List of nearby devices

        Example:
            nearby = await service.find_by_location(
                coordinates="[-3.703790,40.416775]",
                max_distance=1000,
                limit=10,
                pick="id,type,serialNumber,category,location",
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

    async def find_inactive_devices(
        self,
        days_inactive: int = 7,
        limit: Optional[int] = None,
        format: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Find devices that haven't reported data recently.

        Args:
            days_inactive: Number of days without data (default: 7)
            limit: Maximum number of results
            format: Response format

        Returns:
            List of inactive devices

        Example:
            inactive = await service.find_inactive_devices(
                days_inactive=14,
                limit=20,
                format="simplified"
            )
        """
        from datetime import datetime, timedelta, timezone

        cutoff_date = (
            datetime.now(timezone.utc) - timedelta(days=days_inactive)
        ).isoformat()

        result = await self.get_all(
            q=f"dateLastValueReported<'{cutoff_date}'",
            limit=limit,
            format=format,
            count=False,
        )
        if isinstance(result, int):
            return []
        return result


# Singleton instance for convenience (optional)
device_service = DeviceService()
