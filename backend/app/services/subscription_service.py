from typing import Dict, Any, List, Optional
from .base_service import BaseService


class SubscriptionService(BaseService):
    """Service for Subscription management following FIWARE Orion-LD API"""
    
    @staticmethod
    def create_subscription(subscription_data: Dict[str, Any]):
        """Create a new subscription"""
        url = BaseService._get_url("subscriptions")
        headers = BaseService.JSON_LD_HEADERS
        
        response = BaseService._make_request("POST", url, headers=headers, json_data=subscription_data)
        return response.json()

    @staticmethod
    def get_all_subscriptions(limit: Optional[int] = None, 
                             offset: Optional[int] = None,
                             count: bool = False):
        """List all subscriptions"""
        url = BaseService._get_url("subscriptions")
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
    def get_subscription_by_id(subscription_id: str):
        """Get subscription by ID"""
        url = BaseService._get_url(f"subscriptions/{subscription_id}")
        headers = BaseService.DEFAULT_HEADERS
        
        response = BaseService._make_request("GET", url, headers=headers)
        return response.json()

    @staticmethod
    def update_subscription(subscription_id: str, update_data: Dict[str, Any]):
        """Update subscription (PATCH)"""
        url = BaseService._get_url(f"subscriptions/{subscription_id}")
        headers = BaseService.JSON_LD_HEADERS
        
        response = BaseService._make_request("PATCH", url, headers=headers, json_data=update_data)
        return response.status_code

    @staticmethod
    def delete_subscription(subscription_id: str):
        """Delete subscription"""
        url = BaseService._get_url(f"subscriptions/{subscription_id}")
        
        response = BaseService._make_request("DELETE", url)
        return response.status_code