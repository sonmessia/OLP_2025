from typing import Dict, Any, List, Optional, Union
import requests
from .base_service import BaseService


class SubscriptionService(BaseService):
    """
    Service for NGSI-LD Subscription management.

    Subscriptions are the publish/subscribe (pub/sub) mechanism of NGSI-LD.
    Instead of polling, applications can subscribe to events of interest and
    receive notifications automatically when those events occur.
    """

    async def create_subscription(
        self, subscription_data: Dict[str, Any]
    ) -> requests.Response:
        """
        Creates a new subscription. (POST /subscriptions/)

        The subscription payload should include:
        - type: Always "Subscription"
        - description: Human-readable description (optional)
        - entities: Array of entities to monitor (required)
        - watchedAttributes: Attributes to monitor (optional)
        - q: Filter condition (optional)
        - notification: Notification configuration (required)
        - @context: Context URL (required)

        Returns:
            Response with status 201 and Location header containing subscription ID
        """
        subscription_data.setdefault("@context", self.CONTEXT_URL)
        subscription_data.setdefault("type", "Subscription")

        return await self._make_request(
            "POST",
            "subscriptions/",
            headers=self.JSON_LD_CONTENT_HEADER,
            json_payload=subscription_data,
        )

    async def get_all_subscriptions(
        self,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        count: bool = False,
    ) -> Union[List[Dict[str, Any]], int]:
        """
        Retrieves a list of all active subscriptions. (GET /subscriptions/)

        Args:
            limit: Maximum number of results to return per page
            offset: Number of results to skip (for pagination)
            count: If True, return only the count of subscriptions

        Returns:
            List of subscription objects or count (if count=True)
        """
        params = {}
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        if count:
            params["count"] = count

        response = await self._make_request(
            "GET", "subscriptions/", headers=self.LINK_HEADER, params=params
        )

        if count:
            return int(response.headers.get("NGSILD-Results-Count", 0))
        return response.json()

    async def get_subscription_by_id(self, subscription_id: str) -> Dict[str, Any]:
        """
        Retrieves details of a specific subscription. (GET /subscriptions/{id})

        This is useful for debugging as the response includes diagnostic information:
        - status: Current status of the subscription
        - timesSent: Number of notifications sent
        - lastFailure: Timestamp of last failed notification
        - lastSuccess: Timestamp of last successful notification
        - lastFailureReason: Reason for last failure

        Args:
            subscription_id: The ID of the subscription to retrieve

        Returns:
            Subscription object with diagnostic information
        """
        response = await self._make_request(
            "GET", f"subscriptions/{subscription_id}", headers=self.LINK_HEADER
        )
        return response.json()

    async def update_subscription(
        self, subscription_id: str, update_data: Dict[str, Any]
    ) -> requests.Response:
        """
        Updates an existing subscription. (PATCH /subscriptions/{id})

        You only need to send the fields you want to change.
        Common updates:
        - description: Update the description
        - notification.endpoint.uri: Change the notification URL
        - watchedAttributes: Modify monitored attributes
        - q: Update filter conditions

        Args:
            subscription_id: The ID of the subscription to update
            update_data: JSON-LD object with fields to update

        Returns:
            Response with status 204 No Content
        """
        update_data.setdefault("@context", self.CONTEXT_URL)

        return await self._make_request(
            "PATCH",
            f"subscriptions/{subscription_id}",
            headers=self.JSON_LD_CONTENT_HEADER,
            json_payload=update_data,
        )

    async def delete_subscription(self, subscription_id: str) -> requests.Response:
        """
        Deletes (cancels) a subscription. (DELETE /subscriptions/{id})

        After deletion, no more notifications will be sent for this subscription.

        Args:
            subscription_id: The ID of the subscription to delete

        Returns:
            Response with status 204 No Content
        """
        return await self._make_request("DELETE", f"subscriptions/{subscription_id}")


subscription_service = SubscriptionService()
