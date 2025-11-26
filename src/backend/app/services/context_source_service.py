# Copyright (c) 2025 Green Wave Team
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

# app/services/context_source_service.py
import logging
from typing import Any, Dict, List, Optional

import httpx

from .base_service import BaseService

logger = logging.getLogger(__name__)


class ContextSourceService(BaseService):
    """
    Service layer for NGSI-LD Context Source Registrations.
    Provides high-level methods for managing federated data spaces.

    Context Source Registrations enable distributed NGSI-LD deployments
    where data can be sourced from multiple context brokers and providers.

    There are four types of registrations:
    - REDIRECT: All data for entity type is external (hierarchy of brokers)
    - INCLUSIVE: Data merged from local + external sources (federation)
    - EXCLUSIVE: Specific attributes proxy to single external source (IoT devices)
    - AUXILIARY: External data only used if not available locally (fallback)

    Usage:
        # Context manager (recommended)
        async with ContextSourceService() as service:
            registrations = await service.get_all()

        # Manual lifecycle
        service = ContextSourceService()
        try:
            reg = await service.create_registration(registration_data)
        finally:
            await service.close()

    Author: sonmessia
    Created: 2025-11-15
    Updated: 2025-11-15
    """

    def __init__(
        self, orion_url: Optional[str] = None, context_url: Optional[str] = None
    ):
        """
        Initialize ContextSourceService.

        Args:
            orion_url: Orion-LD broker URL (default from env: ORION_LD_URL)
            context_url: JSON-LD context URL (default from env: CONTEXT_URL)
        """
        super().__init__(orion_url, context_url)

    async def create_registration(
        self,
        description: str,
        entities: List[Dict[str, str]],
        endpoint: str,
        mode: str = "inclusive",
        operations: Optional[List[str]] = None,
        property_names: Optional[Any] = None,
        relationship_names: Optional[Any] = None,
        expires_at: Optional[str] = None,
        management_interval: Optional[int] = None,
        management_timeout: Optional[int] = None,
        context_source_info: Optional[Any] = None,
        tenant: Optional[str] = None,
    ) -> httpx.Response:
        """
        Create a new context source registration.

        Args:
            description: Human-readable description
            entities: List of entity patterns [{"type": "Device"}, {"id": "urn:..."}]
            endpoint: URI of the context source
            mode: Registration mode ('redirect', 'inclusive', 'exclusive', 'auxiliary')
            operations: List of operations or shorthand:
                       - 'federationOps': GET operations for federation
                       - 'redirectionOps': All CRUD operations
                       - 'retrieveOps': GET operations only
                       - Or explicit list: ['retrieveEntity', 'updateEntity', ...]
            property_names: Specific properties to register (for exclusive/auxiliary)
            relationship_names: Specific relationships to register
            expires_at: ISO8601 expiration timestamp
            management_interval: Refresh interval in seconds
            management_timeout: Request timeout in milliseconds
            context_source_info: Additional metadata (e.g., jsonldContext)
            tenant: NGSI-LD tenant

        Returns:
            httpx.Response with status 201 and Location header

        Examples:
            # REDIRECT: All Animal data from farmer subsystem
            await service.create_registration(
                description="Animal data from farmer",
                entities=[{"type": "Animal"}],
                endpoint="http://farmer-broker:1026",
                mode="redirect",
                operations=["redirectionOps"]
            )

            # INCLUSIVE: Federation with vet data
            await service.create_registration(
                description="Vet health records",
                entities=[{"type": "Animal"}],
                endpoint="http://vet-broker:1026",
                mode="inclusive",
                operations=["federationOps"]
            )

            # EXCLUSIVE: Live IoT device data
            await service.create_registration(
                description="Live sensor readings",
                entities=[{"type": "Animal", "id": "urn:ngsi-ld:Animal:cow001"}],
                endpoint="http://iot-agent:4041",
                mode="exclusive",
                operations=["retrieveOps"],
                property_names=["heartRate", "location"]
            )

            # AUXILIARY: Weather forecast as fallback
            await service.create_registration(
                description="Weather temperature fallback",
                entities=[{"type": "AgriParcel"}],
                endpoint="http://weather-service:1026",
                mode="auxiliary",
                operations=["retrieveOps"],
                property_names=["temperature"]
            )
        """
        registration_data: Dict[str, Any] = {
            "type": "ContextSourceRegistration",
            "description": description,
            "information": [{"entities": entities}],
            "endpoint": endpoint,
            "mode": mode,
        }

        # Add operations
        if operations:
            registration_data["operations"] = operations
        else:
            # Default operations based on mode
            if mode == "redirect":
                registration_data["operations"] = ["redirectionOps"]
            elif mode == "inclusive":
                registration_data["operations"] = ["federationOps"]
            elif mode in ["exclusive", "auxiliary"]:
                registration_data["operations"] = ["retrieveOps"]

        # Add property/relationship names for exclusive/auxiliary
        if property_names:
            registration_data["information"][0]["propertyNames"] = property_names

        if relationship_names:
            registration_data["information"][0][
                "relationshipNames"
            ] = relationship_names

        # Management settings
        if management_interval or management_timeout:
            registration_data["management"] = {}
            if management_interval:
                registration_data["management"]["interval"] = management_interval
            if management_timeout:
                registration_data["management"]["timeout"] = management_timeout

        # Expiration
        if expires_at:
            registration_data["expiresAt"] = expires_at

        # Context source info (e.g., for passing @context to external sources)
        if context_source_info:
            registration_data["contextSourceInfo"] = context_source_info

        # Prepare headers
        headers = self.LINK_HEADER.copy()
        if tenant:
            headers["NGSILD-Tenant"] = tenant

        logger.info(f"Creating {mode} registration: {description}")
        return await self._make_request(
            "POST",
            "csourceRegistrations",
            headers=headers,
            json_payload=registration_data,
        )

    async def get_all_registrations(
        self,
        entity_type: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        tenant: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Get all context source registrations.

        Args:
            entity_type: Filter by entity type
            limit: Maximum number of results
            offset: Offset for pagination
            tenant: NGSI-LD tenant

        Returns:
            List of registration objects

        Example:
            registrations = await service.get_all_registrations(
                entity_type="Animal"
            )
            for reg in registrations:
                print(f"{reg['description']}: {reg['mode']}")
        """
        params: Dict[str, Any] = {}
        if entity_type:
            params["type"] = entity_type
        if limit:
            params["limit"] = limit
        if offset:
            params["offset"] = offset

        headers = self.LINK_HEADER.copy()
        if tenant:
            headers["NGSILD-Tenant"] = tenant

        response = await self._make_request(
            "GET", "csourceRegistrations", headers=headers, params=params
        )

        return response.json()

    async def get_registration(
        self,
        registration_id: str,
        tenant: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Get details of a specific registration.

        Args:
            registration_id: Registration ID (URN)
            tenant: NGSI-LD tenant

        Returns:
            Registration object

        Example:
            reg = await service.get_registration(
                "urn:ngsi-ld:ContextSourceRegistration:12345"
            )
            print(f"Endpoint: {reg['endpoint']}")
            print(f"Mode: {reg['mode']}")
        """
        headers = self.LINK_HEADER.copy()
        if tenant:
            headers["NGSILD-Tenant"] = tenant

        response = await self._make_request(
            "GET", f"csourceRegistrations/{registration_id}", headers=headers
        )

        return response.json()

    async def update_registration(
        self,
        registration_id: str,
        update_data: Dict[str, Any],
        tenant: Optional[str] = None,
    ) -> int:
        """
        Update an existing registration.

        Args:
            registration_id: Registration ID (URN)
            update_data: Partial registration data to update
            tenant: NGSI-LD tenant

        Returns:
            HTTP status code (204 on success)

        Example:
            await service.update_registration(
                "urn:ngsi-ld:ContextSourceRegistration:12345",
                {
                    "endpoint": "http://new-endpoint:1026",
                    "management": {"timeout": 2000}
                }
            )
        """
        headers = {"Content-Type": "application/json"}
        if tenant:
            headers["NGSILD-Tenant"] = tenant

        response = await self._make_request(
            "PATCH",
            f"csourceRegistrations/{registration_id}",
            headers=headers,
            json_payload=update_data,
        )

        return response.status_code

    async def delete_registration(
        self,
        registration_id: str,
        tenant: Optional[str] = None,
    ) -> int:
        """
        Delete a registration.

        Args:
            registration_id: Registration ID (URN)
            tenant: NGSI-LD tenant

        Returns:
            HTTP status code (204 on success)

        Example:
            await service.delete_registration(
                "urn:ngsi-ld:ContextSourceRegistration:12345"
            )
        """
        headers = {}
        if tenant:
            headers["NGSILD-Tenant"] = tenant

        response = await self._make_request(
            "DELETE", f"csourceRegistrations/{registration_id}", headers=headers
        )

        return response.status_code

    # Helper methods for common registration patterns

    async def register_redirect(
        self,
        entity_type: str,
        endpoint: str,
        description: Optional[str] = None,
        tenant: Optional[str] = None,
    ) -> httpx.Response:
        """
        Create a redirect registration (hierarchy pattern).

        All data for the entity type is held externally. The primary
        broker holds no data and redirects all requests.

        Example:
            # All Animal data managed by farmer subsystem
            await service.register_redirect(
                entity_type="Animal",
                endpoint="http://farmer-broker:1026",
                description="Farmer manages all animal data"
            )
        """
        desc = description or f"Redirect {entity_type} to external source"

        return await self.create_registration(
            description=desc,
            entities=[{"type": entity_type}],
            endpoint=endpoint,
            mode="redirect",
            operations=["redirectionOps"],
            tenant=tenant,
        )

    async def register_federation(
        self,
        entity_type: str,
        endpoint: str,
        description: Optional[str] = None,
        tenant: Optional[str] = None,
    ) -> httpx.Response:
        """
        Create an inclusive federation registration.

        Data is merged from local broker and external source,
        using most recent observedAt timestamp.

        Example:
            # Merge Animal health data from vet
            await service.register_federation(
                entity_type="Animal",
                endpoint="http://vet-broker:1026",
                description="Vet health records"
            )
        """
        desc = description or f"Federation with external {entity_type} source"

        return await self.create_registration(
            description=desc,
            entities=[{"type": entity_type}],
            endpoint=endpoint,
            mode="inclusive",
            operations=["federationOps"],
            tenant=tenant,
        )

    async def register_device(
        self,
        entity_id: str,
        entity_type: str,
        properties: List[str],
        iot_agent_endpoint: str,
        description: Optional[str] = None,
        tenant: Optional[str] = None,
    ) -> httpx.Response:
        """
        Create an exclusive registration for IoT device.

        Specific attributes are always retrieved from the device
        via IoT Agent. No local caching.

        Example:
            # Live sensor data for cow collar
            await service.register_device(
                entity_id="urn:ngsi-ld:Animal:cow001",
                entity_type="Animal",
                properties=["heartRate", "location"],
                iot_agent_endpoint="http://iot-agent:4041",
                description="Live cow collar sensor"
            )
        """
        desc = description or f"Exclusive device registration for {entity_id}"

        return await self.create_registration(
            description=desc,
            entities=[{"type": entity_type, "id": entity_id}],
            endpoint=iot_agent_endpoint,
            mode="exclusive",
            operations=["retrieveOps"],
            property_names=properties,
            tenant=tenant,
        )

    async def register_fallback(
        self,
        entity_type: str,
        properties: List[str],
        endpoint: str,
        description: Optional[str] = None,
        tenant: Optional[str] = None,
    ) -> httpx.Response:
        """
        Create an auxiliary registration as fallback source.

        External data only used if not available locally.

        Example:
            # Weather forecast as fallback for field temperature
            await service.register_fallback(
                entity_type="AgriParcel",
                properties=["temperature"],
                endpoint="http://weather-service:1026",
                description="Weather forecast fallback"
            )
        """
        desc = description or f"Fallback {entity_type} source"

        return await self.create_registration(
            description=desc,
            entities=[{"type": entity_type}],
            endpoint=endpoint,
            mode="auxiliary",
            operations=["retrieveOps"],
            property_names=properties,
            tenant=tenant,
        )


# Singleton instance
context_source_service = ContextSourceService()
