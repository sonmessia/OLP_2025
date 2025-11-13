import requests
from typing import Optional, Dict, Any, List, Union
import logging

logger = logging.getLogger(__name__)


class BaseService:
    """Base service class for FIWARE Orion-LD API operations"""
    
    # Base URL for Orion-LD
    ORION_LD_URL = "http://fiware-orionld:1026/ngsi-ld/v1"
    
    # Common headers
    DEFAULT_HEADERS = {
        "Accept": "application/ld+json",
        "Link": '<http://context/datamodels.context-ngsi.jsonld>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"',
    }
    
    JSON_LD_HEADERS = {
        "Content-Type": "application/ld+json",
        "Accept": "application/ld+json",
        "Link": '<http://context/datamodels.context-ngsi.jsonld>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"',
    }
    
    JSON_HEADERS = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    
    @staticmethod
    def _make_request(method: str, url: str, headers: Optional[Dict[str, str]] = None, 
                      params: Optional[Dict[str, Any]] = None, json_data: Optional[Dict[str, Any]] = None) -> requests.Response:
        """Make HTTP request with error handling"""
        try:
            response = requests.request(method, url, headers=headers, params=params, json=json_data)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            logger.error(f"Error in {method} request to {url}: {e}")
            if hasattr(e, 'response') and e.response is not None:
                logger.error(f"Response content: {e.response.text}")
            raise
    
    @staticmethod
    def _get_url(endpoint: str) -> str:
        """Get full URL for endpoint"""
        return f"{BaseService.ORION_LD_URL}/{endpoint}"
    
    @staticmethod
    def _prepare_params(local: bool = True, **additional_params) -> Dict[str, Any]:
        """Prepare request parameters"""
        params = {"local": "true" if local else "false"}
        params.update(additional_params)
        return params
    
    @staticmethod
    def _merge_headers(*header_dicts) -> Dict[str, str]:
        """Merge multiple header dictionaries"""
        merged = {}
        for headers in header_dicts:
            if headers:
                merged.update(headers)
        return merged
