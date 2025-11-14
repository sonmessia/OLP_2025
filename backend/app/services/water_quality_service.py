from typing import Optional, Dict, Any, List, Union
from .base_service import BaseService
import requests


class WaterQualityService(BaseService):
    """
    Service layer for WaterQualityObserved entities.
    Provides high-level methods for CRUD operations.
    """

    def __init__(
        self, orion_url: Optional[str] = None, context_url: Optional[str] = None
    ):
        super().__init__(orion_url, context_url)
        self.entity_type = "WaterQualityObserved"

    async def create(self, entity_data: Dict[str, Any]) -> requests.Response:
        """
        Create a new WaterQualityObserved entity.
        """
        entity_data["type"] = self.entity_type
        return await super().create_entity(entity_data)

    async def get_all(self, **kwargs) -> Union[List[Dict[str, Any]], int]:
        """
        Queries for WaterQualityObserved entities.
        It automatically adds the 'type=WaterQualityObserved' filter to all queries.
        """
        kwargs["type"] = self.entity_type

        return await self.query_entities(**kwargs)

    async def batch_upsert(
        self, entities: List[Dict[str, Any]], options: str = "update"
    ) -> requests.Response:
        """
        Creates or updates a list of WaterQualityObserved entities.
        It automatically sets the 'type' for each entity in the batch.
        """
        for entity in entities:
            entity["type"] = self.entity_type

        return await super().batch_upsert(entities, options)

    async def get_by_id(self, entity_id: str, **kwargs) -> Dict[str, Any]:
        """Alias for the inherited get_entity_by_id method."""
        return await super().get_entity_by_id(entity_id, **kwargs)

    async def update_attrs(self, entity_id: str, update_data: Dict[str, Any]) -> int:
        """Alias for the inherited update_entity_attributes method."""
        response = await super().update_entity_attributes(entity_id, update_data)
        return response.status_code

    async def replace(self, entity_id: str, entity_data: Dict[str, Any]) -> int:
        """Alias for the inherited replace_entity method."""
        entity_data["type"] = self.entity_type
        response = await super().replace_entity(entity_id, entity_data)
        return response.status_code

    async def delete(self, entity_id: str) -> int:
        """Alias for the inherited delete_entity method."""
        response = await super().delete_entity(entity_id)
        return response.status_code


water_quality_service = WaterQualityService()
