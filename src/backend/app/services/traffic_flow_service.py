import logging
from typing import Any, Dict, List, Optional, Union

import httpx

from app.models.TrafficFlowObserved import TrafficFlowObserved

from .base_service import BaseService

logger = logging.getLogger(__name__)


class TrafficFlowObservedService(BaseService):
    """Service layer for TrafficFlowObserved entities.

    Provides simple CRUD wrapper around the BaseService HTTP client.
    """

    _instance: Optional["TrafficFlowObservedService"] = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, orion_url: Optional[str] = None, context_url: Optional[str] = None):
        if not hasattr(self, "_initialized"):
            super().__init__(orion_url, context_url)
            self.entity_type = "TrafficFlowObserved"
            self._initialized = True

    async def initialize(self):
        await self._get_client()
        logger.debug("TrafficFlowObservedService initialized")

    async def create(self, entity_data: Dict[str, Any]) -> httpx.Response:
        entity_data["type"] = self.entity_type
        return await super().create_entity(entity_data)

    async def get_all(self, **kwargs) -> Union[List[Dict[str, Any]], int]:
        return await super().query_entities(type=self.entity_type, **kwargs)

    async def get_by_id(self, entity_id: str, **kwargs) -> Dict[str, Any]:
        return await super().get_entity_by_id(entity_id=entity_id, **kwargs)

    async def update(self, entity_id: str, attrs_data: Dict[str, Any]) -> httpx.Response:
        return await super().update_entity_attributes(entity_id, attrs_data)

    async def replace(self, entity_id: str, entity_data: Union[TrafficFlowObserved, Dict[str, Any]]) -> httpx.Response:
        if isinstance(entity_data, TrafficFlowObserved):
            entity_data = entity_data.model_dump(exclude_unset=True)
        entity_data["type"] = self.entity_type
        return await super().replace_entity(entity_id, entity_data)

    async def delete(self, entity_id: str) -> httpx.Response:
        return await super().delete_entity(entity_id)


traffic_flow_service = TrafficFlowObservedService()
