from typing import Dict, Any, List, Optional
from .base_service import BaseService


class ApiDiscoveryService(BaseService):
    """Service for API Discovery following FIWARE Orion-LD API"""
    
    @staticmethod
    def get_all_types(limit: Optional[int] = None,
                     offset: Optional[int] = None,
                     count: bool = False):
        """List all entity types in the Broker"""
        url = BaseService._get_url("types")
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
    def get_all_attributes(limit: Optional[int] = None,
                           offset: Optional[int] = None,
                           count: bool = False):
        """List all attribute names in the Broker"""
        url = BaseService._get_url("attributes")
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


class SystemService(BaseService):
    """Service for System endpoints following FIWARE Orion-LD API"""
    
    @staticmethod
    def get_version():
        """Get Broker version and uptime information"""
        url = BaseService._get_url("../version")
        
        response = BaseService._make_request("GET", url)
        return response.json()
