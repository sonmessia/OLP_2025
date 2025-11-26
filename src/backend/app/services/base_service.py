# Copyright (c) 2025 Green Wave Team
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import logging
import os
from typing import Any, Dict, List, Optional, Union

import httpx
from pydantic import BaseModel

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class BaseService:
    """
    A comprehensive and robust base service for all FIWARE Orion-LD CRUD operations.
    It provides methods for single-entity, attribute-level, and batch operations.

    Usage:
        # Option 1: Context manager (recommended)
        async with BaseService() as service:
            await service.create_entity(data)

        # Option 2: Manual lifecycle
        service = BaseService()
        try:
            await service.create_entity(data)
        finally:
            await service.close()
    """

    def __init__(
        self, orion_url: Optional[str] = None, context_url: Optional[str] = None
    ):
        self.ORION_LD_URL = orion_url or os.getenv(
            "ORION_LD_URL", "http://fiware-orionld:1026/ngsi-ld/v1"
        )
        self.CONTEXT_URL = context_url or os.getenv(
            "CONTEXT_URL", "http://context/datamodels.context-ngsi.jsonld"
        )

        self.JSON_LD_CONTENT_HEADER = {"Content-Type": "application/ld+json"}
        self.JSON_CONTENT_HEADER = {"Content-Type": "application/json"}
        self.LINK_HEADER = {
            "Link": f'<{self.CONTEXT_URL}>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"'
        }

        # ✅ Reusable HTTP client
        self._client: Optional[httpx.AsyncClient] = None

        logger.debug(f"BaseService initialized for broker at {self.ORION_LD_URL}")

    async def _get_client(self) -> httpx.AsyncClient:
        """Get or create the async HTTP client with proper configuration."""
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(
                timeout=httpx.Timeout(30.0, connect=10.0),  # ✅ Add timeouts
                limits=httpx.Limits(
                    max_keepalive_connections=20,
                    max_connections=100,
                    keepalive_expiry=30.0,
                ),
                follow_redirects=True,
            )
        return self._client

    async def close(self):
        """Close the HTTP client and release resources."""
        if self._client and not self._client.is_closed:
            await self._client.aclose()
            logger.debug("HTTP client closed")

    async def __aenter__(self):
        """Async context manager entry."""
        await self._get_client()  # Initialize client
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()

    async def _make_request(
        self,
        method: str,
        endpoint: str,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        json_payload: Optional[Union[Dict, List]] = None,
    ) -> httpx.Response:
        """
        Make an async HTTP request to Orion-LD.

        Args:
            method: HTTP method (GET, POST, PATCH, DELETE, etc.)
            endpoint: API endpoint path
            headers: Optional HTTP headers
            params: Optional query parameters
            json_payload: Optional JSON body

        Returns:
            httpx.Response object

        Raises:
            httpx.HTTPStatusError: For HTTP error responses
            httpx.RequestError: For connection/request errors
        """
        # ✅ Remove leading slash from endpoint if present
        endpoint = endpoint.lstrip("/")
        full_url = f"{self.ORION_LD_URL}/{endpoint}"

        # Clean parameters (remove None, convert bool to string)
        clean_params = {}
        if params:
            for key, value in params.items():
                if value is None:
                    continue
                if isinstance(value, bool):
                    clean_params[key] = "true" if value else "false"
                else:
                    clean_params[key] = value

        # ✅ Use reusable client
        client = await self._get_client()

        try:
            logger.debug(f"{method} {full_url} | Params: {clean_params}")

            response = await client.request(
                method,
                full_url,
                headers=headers,
                params=clean_params,
                json=json_payload,
            )
            response.raise_for_status()

            logger.info(f"{method} {full_url} - Status: {response.status_code}")
            return response

        except httpx.HTTPStatusError as e:
            logger.error(
                f"HTTP Error {e.response.status_code} on {method} {full_url}: {e.response.text}"
            )
            raise

        except httpx.RequestError as e:
            logger.error(f"Connection Error on {method} {full_url}: {e}")
            raise

    # --- GROUP 1: SINGLE ENTITY OPERATIONS ---

    async def create_entity(self, entity_data: Dict[str, Any]) -> httpx.Response:
        """
        Creates a single new entity. (POST /entities)

        Args:
            entity_data: Entity data including type, id, and attributes

        Returns:
            httpx.Response with status 201 on success
        """
        entity_data.setdefault("@context", self.CONTEXT_URL)
        return await self._make_request(
            "POST",
            "entities",  # ✅ Removed trailing slash
            headers=self.JSON_LD_CONTENT_HEADER,
            json_payload=entity_data,
        )

    async def get_entity_by_id(
        self,
        entity_id: str,
        attrs: Optional[str] = None,
        options: Optional[str] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """
        Retrieves a single entity by its ID. (GET /entities/{id})

        Args:
            entity_id: The entity identifier (URI)
            attrs: Comma-separated list of attribute names to retrieve
            options: Query options (e.g., 'keyValues', 'sysAttrs')
            **kwargs: Additional query parameters

        Returns:
            Entity data as dictionary
        """
        params = kwargs.copy()
        if attrs:
            params["attrs"] = attrs
        if options:
            params["options"] = options

        response = await self._make_request(
            "GET", f"entities/{entity_id}", headers=self.LINK_HEADER, params=params
        )
        return response.json()

    async def replace_entity(
        self, entity_id: str, entity_data: Union[BaseModel, Dict[str, Any]]
    ) -> httpx.Response:
        """
        Replaces an entire entity. (PUT /entities/{id})

        Args:
            entity_id: The entity identifier
            entity_data: Complete entity data (Pydantic model or dictionary)

        Returns:
            httpx.Response with status 204 on success
        """
        # Convert Pydantic model to dictionary if needed and add context
        if isinstance(entity_data, BaseModel):
            entity_dict = entity_data.model_dump(exclude_unset=True)
        else:
            entity_dict = entity_data
        entity_dict.setdefault("@context", self.CONTEXT_URL)
        return await self._make_request(
            "PUT",
            f"entities/{entity_id}",
            headers=self.JSON_LD_CONTENT_HEADER,
            json_payload=entity_dict,
        )

    async def delete_entity(self, entity_id: str) -> httpx.Response:
        """
        Deletes a single entity. (DELETE /entities/{id})

        Args:
            entity_id: The entity identifier

        Returns:
            httpx.Response with status 204 on success
        """
        return await self._make_request("DELETE", f"entities/{entity_id}")

    # --- GROUP 2: ATTRIBUTE OPERATIONS ---

    async def update_entity_attributes(
        self, entity_id: str, attrs_data: Dict[str, Any]
    ) -> httpx.Response:
        """
        Updates attributes using Partial Update. (PATCH /entities/{id}/attrs)

        Args:
            entity_id: The entity identifier
            attrs_data: Attributes to update (without id and type)

        Returns:
            httpx.Response with status 204 on success
        """
        attrs_data.setdefault("@context", self.CONTEXT_URL)
        return await self._make_request(
            "PATCH",
            f"entities/{entity_id}/attrs",
            headers=self.JSON_LD_CONTENT_HEADER,
            json_payload=attrs_data,
        )

    async def delete_entity_attribute(
        self, entity_id: str, attr_name: str
    ) -> httpx.Response:
        """
        Deletes a specific attribute from an entity. (DELETE /entities/{id}/attrs/{attrName})

        Args:
            entity_id: The entity identifier
            attr_name: The attribute name to delete

        Returns:
            httpx.Response with status 204 on success
        """
        return await self._make_request(
            "DELETE", f"entities/{entity_id}/attrs/{attr_name}"
        )

    # --- GROUP 3: BATCH OPERATIONS ---

    async def batch_create(self, entities: List[Dict[str, Any]]) -> httpx.Response:
        """
        Creates multiple entities. (POST /entityOperations/create)

        Args:
            entities: List of entity data dictionaries

        Returns:
            httpx.Response with status 201/207 and success/error details
        """
        for entity in entities:
            entity.setdefault("@context", self.CONTEXT_URL)
        return await self._make_request(
            "POST",
            "entityOperations/create",
            headers=self.JSON_LD_CONTENT_HEADER,
            json_payload=entities,
        )

    async def batch_upsert(
        self, entities: List[Dict[str, Any]], options: str = "update"
    ) -> httpx.Response:
        """
        Creates or updates multiple entities. (POST /entityOperations/upsert)

        Args:
            entities: List of entity data dictionaries
            options: 'update' (default) or 'replace'

        Returns:
            httpx.Response with status 201/204/207
        """
        for entity in entities:
            entity.setdefault("@context", self.CONTEXT_URL)
        return await self._make_request(
            "POST",
            "entityOperations/upsert",
            headers=self.JSON_LD_CONTENT_HEADER,
            params={"options": options},
            json_payload=entities,
        )

    async def batch_update(
        self, entities: List[Dict[str, Any]], options: str = "update"
    ) -> httpx.Response:
        """
        Updates multiple entities. (POST /entityOperations/update)

        Args:
            entities: List of entity data dictionaries
            options: 'update' (default) or 'replace'

        Returns:
            httpx.Response with status 204/207
        """
        for entity in entities:
            entity.setdefault("@context", self.CONTEXT_URL)
        return await self._make_request(
            "POST",
            "entityOperations/update",
            headers=self.JSON_LD_CONTENT_HEADER,
            params={"options": options},
            json_payload=entities,
        )

    async def batch_delete(self, entity_ids: List[str]) -> httpx.Response:
        """
        Deletes multiple entities. (POST /entityOperations/delete)

        Args:
            entity_ids: List of entity identifiers (URIs)

        Returns:
            httpx.Response with status 204/207
        """
        return await self._make_request(
            "POST",
            "entityOperations/delete",
            headers=self.JSON_CONTENT_HEADER,
            json_payload=entity_ids,
        )

    # --- GROUP 4: QUERY OPERATIONS ---

    async def query_entities(
        self,
        # Entity filtering
        type: Optional[str] = None,
        id: Optional[str] = None,
        q: Optional[str] = None,
        # Attribute selection
        attrs: Optional[str] = None,  # Legacy
        pick: Optional[str] = None,  # Preferred
        # Geo-spatial queries
        georel: Optional[str] = None,
        geometry: Optional[str] = None,
        coordinates: Optional[str] = None,
        geoproperty: Optional[str] = None,  # Default is "location"
        # Pagination
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        # Result options
        count: Optional[bool] = None,
        options: Optional[str] = None,  # sysAttrs, keyValues, etc.
        format: Optional[str] = None,  # simplified
        # Federation
        local: Optional[bool] = None,
        # Temporal (if using temporal endpoint)
        timerel: Optional[str] = None,
        timeAt: Optional[str] = None,
        endTimeAt: Optional[str] = None,
        timeproperty: Optional[str] = None,  # Default is "observedAt"
        # Additional
        **kwargs,
    ) -> Union[List[Dict[str, Any]], int]:
        """
        Queries for a list of entities. (GET /entities)

        Args:
            type: Entity type filter
            id: Entity ID filter (comma-separated list)
            q: Query filter (e.g., "temperature>20", "controlledAsset==\"urn:...\")

            attrs: (Legacy) Attributes to include (comma-separated)
            pick: (Preferred) Attributes to select (comma-separated, includes id and type)

            georel: Geo-relationship (e.g., "near;maxDistance==2000")
            geometry: Geometry type (Point, LineString, Polygon, MultiPoint, MultiLineString, MultiPolygon)
            coordinates: Coordinates array as string
            geoproperty: Property to use for geo-queries (default: "location")

            limit: Maximum number of results (pagination)
            offset: Offset for pagination

            count: If True, returns only the count of matching entities (in header)
            options: Query options (e.g., 'sysAttrs', 'keyValues')
            format: Response format ('simplified' for key-value pairs)

            timerel: Temporal relationship ('before', 'after', 'between')
            timeAt: Timestamp in ISO8601 format
            endTimeAt: End timestamp (required for 'between')
            timeproperty: Property to use for temporal queries (default: "observedAt")

            **kwargs: Additional query parameters

        Returns:
            List of entities or count (int) if count=True

        Raises:
            ValueError: If query is too broad (no filters provided)

        Examples:
            # Basic query by type
            entities = await service.query_entities(type="TemperatureSensor")

            # Query with attribute selection (simplified format)
            entities = await service.query_entities(
                type="TemperatureSensor",
                pick="id,type,temperature",
                format="simplified"
            )

            # Query with filter
            hot_sensors = await service.query_entities(
                type="TemperatureSensor",
                q="temperature>30",
                limit=10
            )

            # Query by multiple IDs
            entities = await service.query_entities(
                id="urn:ngsi-ld:Sensor:001,urn:ngsi-ld:Sensor:002",
                pick="id,type,temperature",
                format="simplified"
            )

            # Get count only
            count = await service.query_entities(
                type="TemperatureSensor",
                q="temperature>20",
                count=True
            )

            # Query with system attributes
            entities = await service.query_entities(
                type="TemperatureSensor",
                options="sysAttrs"
            )

            # Geo-spatial query
            nearby = await service.query_entities(
                type="TemperatureSensor",
                georel="near;maxDistance==2000",
                geometry="Point",
                coordinates="[-8.5,41.2]"
            )

            # Find relationships
            count = await service.query_entities(
                type="TemperatureSensor",
                q='controlledAsset=="urn:ngsi-ld:Building:barn002"',
                limit=0,
                count=True
            )
        """
        # Build params dict
        params = {
            # Entity filtering
            "type": type,
            "id": id,
            "q": q,
            # Attribute selection
            "attrs": attrs,
            "pick": pick,
            # Geo-spatial
            "georel": georel,
            "geometry": geometry,
            "coordinates": coordinates,
            "geoproperty": geoproperty,
            # Pagination
            "limit": limit,
            "offset": offset,
            # Result options
            "count": count,
            "options": options,
            "format": format,
            # Federation
            "local": local,
            # Temporal
            "timerel": timerel,
            "timeAt": timeAt,
            "endTimeAt": endTimeAt,
            "timeproperty": timeproperty,
        }
        params.update(kwargs)

        # Remove None values
        params = {k: v for k, v in params.items() if v is not None}

        # Validate that at least one filter is provided
        filter_keys = {"type", "q", "id", "georel", "attrs", "local"}
        if not any(key in params for key in filter_keys):
            raise ValueError(
                "Query is too broad. Provide at least one filter: "
                "'type', 'q', 'id', 'georel', 'attrs', or 'local'."
            )

        response = await self._make_request(
            "GET", "entities", headers=self.LINK_HEADER, params=params
        )

        # Return count if requested
        if count:
            return int(response.headers.get("NGSILD-Results-Count", 0))

        return response.json()

    async def temporal_query(
        self,
        timerel: str,
        timeAt: str,
        endTimeAt: Optional[str] = None,
        type: Optional[str] = None,
        **kwargs,
    ) -> List[Dict[str, Any]]:
        """
        Performs a temporal query. (GET /temporal/entities)

        Args:
            timerel: Temporal relationship ('before', 'after', 'between')
            timeAt: Timestamp in ISO8601 format
            endTimeAt: End timestamp (required for 'between')
            type: Entity type filter
            **kwargs: Additional query parameters

        Returns:
            List of temporal entities
        """
        params = {
            "timerel": timerel,
            "timeAt": timeAt,
            "endTimeAt": endTimeAt,
            "type": type,
        }
        params.update(kwargs)
        params = {k: v for k, v in params.items() if v is not None}

        response = await self._make_request(
            "GET", "temporal/entities", headers=self.LINK_HEADER, params=params
        )
        return response.json()
