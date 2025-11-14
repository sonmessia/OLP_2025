import requests
import httpx
import json
from typing import Optional, Dict, Any, List, Union
import logging
import os

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class BaseService:
    """
    A comprehensive and robust base service for all FIWARE Orion-LD CRUD operations.
    It provides methods for single-entity, attribute-level, and batch operations.
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
        self.JSON_CONTENT_HEADER = {
            "Content-Type": "application/json"
        }  # Dùng cho batch ops
        self.LINK_HEADER = {
            "Link": f'<{self.CONTEXT_URL}>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"'
        }

        logger.debug(f"BaseService initialized for broker at {self.ORION_LD_URL}")

    async def _make_request(
        self,
        method: str,
        endpoint: str,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        json_payload: Optional[Union[Dict, List]] = None,
    ) -> requests.Response:
        full_url = f"{self.ORION_LD_URL}/{endpoint}"
        clean_params = {}
        if params:
            for key, value in params.items():
                if value is None:
                    continue
                if isinstance(value, bool):
                    if value:
                        clean_params[key] = "true"
                else:
                    clean_params[key] = value

        async with httpx.AsyncClient() as client:
            try:
                response = requests.request(
                    method,
                    full_url,
                    headers=headers,
                    params=clean_params,
                    json=json_payload,
                )
                response.raise_for_status()
                return response
            except requests.exceptions.HTTPError as e:
                logger.error(
                    f"HTTP Error {e.response.status_code} on {method} {full_url}: {e.response.text}"
                )
                raise
            except requests.exceptions.RequestException as e:
                logger.error(f"Connection Error on {method} {full_url}: {e}")
                raise

    # --- NHÓM 1: THAO TÁC TRÊN THỰC THỂ DUY NHẤT ---

    async def create_entity(self, entity_data: Dict[str, Any]) -> requests.Response:
        """Creates a single new entity. (POST /entities)"""
        entity_data.setdefault("@context", self.CONTEXT_URL)
        return await self._make_request(
            "POST",
            "entities/",
            headers=self.JSON_LD_CONTENT_HEADER,
            json_payload=entity_data,
        )

    async def get_entity_by_id(self, entity_id: str, **kwargs) -> Dict[str, Any]:
        """Retrieves a single entity by its ID. (GET /entities/{id})"""
        response = await self._make_request(
            "GET", f"entities/{entity_id}", headers=self.LINK_HEADER, params=kwargs
        )
        return response.json()

    async def replace_entity(
        self, entity_id: str, entity_data: Dict[str, Any]
    ) -> requests.Response:
        """Replaces an entire entity. (PUT /entities/{id})"""
        entity_data.setdefault("@context", self.CONTEXT_URL)
        return await self._make_request(
            "PUT",
            f"entities/{entity_id}",
            headers=self.JSON_LD_CONTENT_HEADER,
            json_payload=entity_data,
        )

    async def delete_entity(self, entity_id: str) -> requests.Response:
        """Deletes a single entity. (DELETE /entities/{id})"""
        return await self._make_request("DELETE", f"entities/{entity_id}")

    # --- NHÓM 2: THAO TÁC TRÊN THUỘC TÍNH ---

    async def update_entity_attributes(
        self, entity_id: str, attrs_data: Dict[str, Any]
    ) -> requests.Response:
        """Updates attributes using Partial Update. (PATCH /entities/{id}/attrs)"""
        attrs_data.setdefault("@context", self.CONTEXT_URL)
        return await self._make_request(
            "PATCH",
            f"entities/{entity_id}/attrs",
            headers=self.JSON_LD_CONTENT_HEADER,
            json_payload=attrs_data,
        )

    # --- NHÓM 3: THAO TÁC HÀNG LOẠT (BATCH OPERATIONS) ---

    async def batch_create(self, entities: List[Dict[str, Any]]) -> requests.Response:
        """Creates multiple entities. (POST /entityOperations/create)"""
        for entity in entities:
            entity.setdefault("@context", self.CONTEXT_URL)
        return await self._make_request(
            "POST",
            "entityOperations/create",
            headers=self.JSON_CONTENT_HEADER,
            json_payload=entities,
        )

    async def batch_upsert(
        self, entities: List[Dict[str, Any]], options: str = "update"
    ) -> requests.Response:
        """Creates or updates multiple entities. (POST /entityOperations/upsert)"""
        for entity in entities:
            entity.setdefault("@context", self.CONTEXT_URL)
        return await self._make_request(
            "POST",
            "entityOperations/upsert",
            headers=self.JSON_CONTENT_HEADER,
            params={"options": options},
            json_payload=entities,
        )

    async def batch_update(
        self, entities: List[Dict[str, Any]], options: str = "update"
    ) -> requests.Response:
        """Updates multiple entities. (POST /entityOperations/update)"""
        for entity in entities:
            entity.setdefault("@context", self.CONTEXT_URL)
        return await self._make_request(
            "POST",
            "entityOperations/update",
            headers=self.JSON_CONTENT_HEADER,
            params={"options": options},
            json_payload=entities,
        )

    async def batch_delete(self, entity_ids: List[str]) -> requests.Response:
        """Deletes multiple entities. (POST /entityOperations/delete)"""
        return await self._make_request(
            "POST",
            "entityOperations/delete",
            headers=self.JSON_CONTENT_HEADER,
            json_payload=entity_ids,
        )

    # --- NHÓM 4: TRUY VẤN TẬP HỢP ---

    async def query_entities(self, **kwargs) -> Union[List[Dict[str, Any]], int]:
        """Queries for a list of entities. (GET /entities)"""
        if not any(
            key in kwargs for key in ["type", "q", "id", "georel", "attrs", "local"]
        ):
            raise ValueError(
                "Query is too broad. Provide at least one filter: 'type', 'q', 'id', 'georel', 'local', or 'attrs'."
            )

        response = await self._make_request(
            "GET", "entities/", headers=self.LINK_HEADER, params=kwargs
        )

        if kwargs.get("count") == "true" or kwargs.get("count") is True:
            return int(response.headers.get("NGSILD-Results-Count", 0))
        return response.json()
