from typing import Optional, Dict, Any, List
from .base_service import BaseService


class CarbonFootprintService(BaseService):
    """Service for Carbon Footprint entities following FIWARE Orion-LD API"""
    
    @staticmethod
    def get_all_entities(local: bool = True, limit: Optional[int] = None, 
                        offset: Optional[int] = None, attrs: Optional[List[str]] = None,
                        q: Optional[str] = None, count: bool = False):
        """Get all Carbon Footprint entities with advanced filtering"""
        url = BaseService._get_url("entities")
        headers = BaseService.DEFAULT_HEADERS
        
        params = BaseService._prepare_params(
            local=local,
            type="CarbonFootprint",
            limit=limit,
            offset=offset,
            **({"attrs": ",".join(attrs)} if attrs else {}),
            **({"q": q} if q else {}),
            **({"count": "true"} if count else {})
        )
        
        response = BaseService._make_request("GET", url, headers=headers, params=params)
        return response.json() if not count else response.headers.get('X-Total-Count', 0)

    @staticmethod
    def get_entity_by_id(entity_id: str, local: bool = True, 
                        attrs: Optional[List[str]] = None):
        """Get Carbon Footprint entity by ID"""
        url = BaseService._get_url(f"entities/{entity_id}")
        headers = BaseService.DEFAULT_HEADERS
        
        params = BaseService._prepare_params(
            local=local,
            **({"attrs": ",".join(attrs)} if attrs else {})
        )
        
        response = BaseService._make_request("GET", url, headers=headers, params=params)
        return response.json()

    @staticmethod
    def create_entity(entity_data: Dict[str, Any], local: bool = True):
        """Create new Carbon Footprint entity"""
        url = BaseService._get_url("entities")
        headers = BaseService.JSON_LD_HEADERS
        params = BaseService._prepare_params(local=local)
        
        response = BaseService._make_request("POST", url, headers=headers, params=params, json_data=entity_data)
        return response.json()

    @staticmethod
    def update_entity_attributes(entity_id: str, update_data: Dict[str, Any], local: bool = True):
        """Update specific attributes of Carbon Footprint entity (PATCH)"""
        url = BaseService._get_url(f"entities/{entity_id}/attrs")
        headers = BaseService.JSON_LD_HEADERS
        params = BaseService._prepare_params(local=local)
        
        response = BaseService._make_request("PATCH", url, headers=headers, params=params, json_data=update_data)
        return response.status_code

    @staticmethod
    def replace_entity(entity_id: str, entity_data: Dict[str, Any], local: bool = True):
        """Replace entire Carbon Footprint entity (PUT)"""
        url = BaseService._get_url(f"entities/{entity_id}")
        headers = BaseService.JSON_LD_HEADERS
        params = BaseService._prepare_params(local=local)
        
        response = BaseService._make_request("PUT", url, headers=headers, params=params, json_data=entity_data)
        return response.status_code

    @staticmethod
    def add_attributes(entity_id: str, attributes_data: Dict[str, Any], local: bool = True):
        """Add new attributes to Carbon Footprint entity"""
        url = BaseService._get_url(f"entities/{entity_id}/attrs")
        headers = BaseService.JSON_LD_HEADERS
        params = BaseService._prepare_params(local=local)
        
        response = BaseService._make_request("POST", url, headers=headers, params=params, json_data=attributes_data)
        return response.status_code

    @staticmethod
    def get_attribute_by_id(entity_id: str, attr_name: str, local: bool = True):
        """Get specific attribute of Carbon Footprint entity"""
        url = BaseService._get_url(f"entities/{entity_id}/attrs/{attr_name}")
        headers = BaseService.DEFAULT_HEADERS
        params = BaseService._prepare_params(local=local)
        
        response = BaseService._make_request("GET", url, headers=headers, params=params)
        return response.json()

    @staticmethod
    def update_attribute(entity_id: str, attr_name: str, attr_data: Dict[str, Any], local: bool = True):
        """Update specific attribute of Carbon Footprint entity"""
        url = BaseService._get_url(f"entities/{entity_id}/attrs/{attr_name}")
        headers = BaseService.JSON_LD_HEADERS
        params = BaseService._prepare_params(local=local)
        
        response = BaseService._make_request("PATCH", url, headers=headers, params=params, json_data=attr_data)
        return response.status_code

    @staticmethod
    def delete_attribute(entity_id: str, attr_name: str, local: bool = True):
        """Delete specific attribute from Carbon Footprint entity"""
        url = BaseService._get_url(f"entities/{entity_id}/attrs/{attr_name}")
        params = BaseService._prepare_params(local=local)
        
        response = BaseService._make_request("DELETE", url, params=params)
        return response.status_code

    @staticmethod
    def delete_entity(entity_id: str, local: bool = True):
        """Delete Carbon Footprint entity"""
        url = BaseService._get_url(f"entities/{entity_id}")
        params = BaseService._prepare_params(local=local)
        
        response = BaseService._make_request("DELETE", url, params=params)
        return response.status_code
