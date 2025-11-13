from typing import Dict, Any, List, Optional
from .base_service import BaseService


class ContextSourceService(BaseService):
    """Service for Context Source Registrations following FIWARE Orion-LD API"""
    
    @staticmethod
    def create_context_source(context_source_data: Dict[str, Any]):
        """Create a new context source registration"""
        url = BaseService._get_url("csourceRegistrations")
        headers = BaseService.JSON_LD_HEADERS
        
        response = BaseService._make_request("POST", url, headers=headers, json_data=context_source_data)
        return response.json()

    @staticmethod
    def get_all_context_sources(limit: Optional[int] = None,
                                offset: Optional[int] = None,
                                count: bool = False):
        """List all context source registrations"""
        url = BaseService._get_url("csourceRegistrations")
        headers = BaseService.DEFAULT_HEADERS
        
        params = {}
        if limit:
            params["limit"] = limit
        if offset:
            params["offset"] = offset
        if count:
            params["count"] = "true"
            
        response = BaseService._make_request("GET", url, headers=headers, params=params)
        return response.json() if not count else response.headers.get('X-Total-Count', 0)

    @staticmethod
    def get_context_source_by_id(context_source_id: str):
        """Get context source registration by ID"""
        url = BaseService._get_url(f"csourceRegistrations/{context_source_id}")
        headers = BaseService.DEFAULT_HEADERS
        
        response = BaseService._make_request("GET", url, headers=headers)
        return response.json()

    @staticmethod
    def update_context_source(context_source_id: str, update_data: Dict[str, Any]):
        """Update context source registration (PATCH)"""
        url = BaseService._get_url(f"csourceRegistrations/{context_source_id}")
        headers = BaseService.JSON_LD_HEADERS
        
        response = BaseService._make_request("PATCH", url, headers=headers, json_data=update_data)
        return response.status_code

    @staticmethod
    def delete_context_source(context_source_id: str):
        """Delete context source registration"""
        url = BaseService._get_url(f"csourceRegistrations/{context_source_id}")
        
        response = BaseService._make_request("DELETE", url)
        return response.status_code