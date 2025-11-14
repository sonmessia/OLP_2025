from typing import Dict, Any, List
from .base_service import BaseService


class BatchOperationsService(BaseService):
    """Service for Batch Operations following FIWARE Orion-LD API"""

    @staticmethod
    def create_entities(entities_data: Dict[str, Any], local: bool = True):
        """Create multiple entities"""
        url = BaseService._get_url("entityOperations/create")
        headers = BaseService.JSON_LD_HEADERS
        params = BaseService._prepare_params(local=local)

        response = BaseService._make_request(
            "POST", url, headers=headers, params=params, json_data=entities_data
        )
        return response.json()

    @staticmethod
    def upsert_entities(entities_data: Dict[str, Any], local: bool = True):
        """Create new entities or update existing ones"""
        url = BaseService._get_url("entityOperations/upsert")
        headers = BaseService.JSON_LD_HEADERS
        params = BaseService._prepare_params(local=local)

        response = BaseService._make_request(
            "POST", url, headers=headers, params=params, json_data=entities_data
        )
        return response.json()

    @staticmethod
    def update_entities(entities_data: Dict[str, Any], local: bool = True):
        """Update multiple entities"""
        url = BaseService._get_url("entityOperations/update")
        headers = BaseService.JSON_LD_HEADERS
        params = BaseService._prepare_params(local=local)

        response = BaseService._make_request(
            "POST", url, headers=headers, params=params, json_data=entities_data
        )
        return response.json()

    @staticmethod
    def delete_entities(entity_ids: List[str], local: bool = True):
        """Delete multiple entities"""
        url = BaseService._get_url("entityOperations/")
        params = BaseService._prepare_params(local=local)

        response = BaseService._make_request(
            "DELETE", url, params=params, json_data=entity_ids
        )
        return response.status_code
