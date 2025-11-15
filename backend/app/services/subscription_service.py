# app/services/subscription_service.py
from typing import Optional, Dict, Any, List
from .base_service import BaseService
import httpx
import logging

logger = logging.getLogger(__name__)


class SubscriptionService(BaseService):
    """
    Service layer for NGSI-LD Subscriptions.
    Provides high-level methods for managing context subscriptions.

    Subscriptions allow applications to be notified asynchronously when
    context data changes, reducing the need for constant polling.

    Usage:
        # Context manager (recommended)
        async with SubscriptionService() as service:
            subscriptions = await service.get_all()

        # Manual lifecycle
        service = SubscriptionService()
        try:
            sub = await service.create_subscription(subscription_data)
        finally:
            await service.close()

    Author: sonmessia
    Created: 2025-11-15
    """

    def __init__(
        self, orion_url: Optional[str] = None, context_url: Optional[str] = None
    ):
        """
        Initialize SubscriptionService.

        Args:
            orion_url: Orion-LD broker URL (default from env: ORION_LD_URL)
            context_url: JSON-LD context URL (default from env: CONTEXT_URL)
        """
        super().__init__(orion_url, context_url)

    async def create_subscription(
        self,
        description: str,
        entities: List[Dict[str, str]],
        notification_uri: str,
        watched_attributes: Optional[List[str]] = None,
        q: Optional[str] = None,
        notification_format: str = "normalized",
        notification_accept: str = "application/json",
        notifier_info: Optional[List[Dict[str, str]]] = None,
        expires_at: Optional[str] = None,
        throttling: Optional[int] = None,
        tenant: Optional[str] = None,
    ) -> httpx.Response:
        """
        Create a new subscription.

        Args:
            description: Human-readable description of the subscription
            entities: List of entity type/id patterns to watch
                     [{"type": "Device"}, {"id": "urn:ngsi-ld:Device:001"}]
            notification_uri: URI where notifications will be sent
            watched_attributes: Specific attributes to watch for changes
            q: Query filter (e.g., "temperature>25")
            notification_format: Format of notification payload
                               ('normalized', 'keyValues', 'x-ngsiv2-normalized')
            notification_accept: Accept header for notifications
            notifier_info: Additional notification metadata (for MQTT QoS, etc.)
            expires_at: ISO8601 timestamp when subscription expires
            throttling: Minimum time (seconds) between notifications
            tenant: NGSI-LD tenant (if using multi-tenancy)

        Returns:
            httpx.Response with status 201 and Location header

        Examples:
            # Simple subscription for device changes
            response = await service.create_subscription(
                description="Notify on device battery level changes",
                entities=[{"type": "Device"}],
                notification_uri="http://myapp:3000/notifications/devices",
                watched_attributes=["batteryLevel"],
                q="batteryLevel<0.2"
            )

            # Subscription with MQTT endpoint
            response = await service.create_subscription(
                description="Notify via MQTT",
                entities=[{"type": "WaterQualityObserved"}],
                notification_uri="mqtt://mosquitto:1883/water-quality",
                watched_attributes=["pH", "turbidity"],
                notification_format="keyValues",
                notifier_info=[{"key": "MQTT-QoS", "value": "1"}]
            )
        """
        subscription_data = {
            "type": "Subscription",
            "description": description,
            "entities": entities,
            "notification": {
                "format": notification_format,
                "endpoint": {"uri": notification_uri, "accept": notification_accept},
            },
        }

        # Optional: watched attributes
        if watched_attributes:
            subscription_data["watchedAttributes"] = watched_attributes

        # Optional: query filter
        if q:
            subscription_data["q"] = q

        # Optional: notification attributes
        if watched_attributes:
            subscription_data["notification"]["attributes"] = watched_attributes

        # Optional: notifier info (for MQTT QoS, etc.)
        if notifier_info:
            subscription_data["notification"]["endpoint"][
                "notifierInfo"
            ] = notifier_info

        # Optional: expiration
        if expires_at:
            subscription_data["expiresAt"] = expires_at

        # Optional: throttling
        if throttling:
            subscription_data["throttling"] = throttling

        # Prepare headers
        headers = self.LINK_HEADER.copy()
        if tenant:
            headers["NGSILD-Tenant"] = tenant

        logger.info(f"Creating subscription: {description}")
        return await self._make_request(
            "POST", "subscriptions", headers=headers, json_payload=subscription_data
        )

    async def get_all_subscriptions(
        self,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        tenant: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Get all subscriptions.

        Args:
            limit: Maximum number of results
            offset: Offset for pagination
            tenant: NGSI-LD tenant

        Returns:
            List of subscription objects

        Example:
            subscriptions = await service.get_all_subscriptions()
            for sub in subscriptions:
                print(f"{sub['description']}: {sub['id']}")
        """
        params = {}
        if limit:
            params["limit"] = limit
        if offset:
            params["offset"] = offset

        headers = {}
        if tenant:
            headers["NGSILD-Tenant"] = tenant

        response = await self._make_request(
            "GET", "subscriptions", headers=headers, params=params
        )

        return response.json()

    async def get_subscription(
        self,
        subscription_id: str,
        tenant: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Get details of a specific subscription.

        Args:
            subscription_id: Subscription ID (URN)
            tenant: NGSI-LD tenant

        Returns:
            Subscription object with notification status

        Example:
            sub = await service.get_subscription(
                "urn:ngsi-ld:Subscription:5fd228838b9b83697b855a72"
            )
            print(f"Last notification: {sub['notification'].get('lastNotification')}")
        """
        headers = {}
        if tenant:
            headers["NGSILD-Tenant"] = tenant

        response = await self._make_request(
            "GET", f"subscriptions/{subscription_id}", headers=headers
        )

        return response.json()

    async def update_subscription(
        self,
        subscription_id: str,
        update_data: Dict[str, Any],
        tenant: Optional[str] = None,
    ) -> int:
        """
        Update an existing subscription.

        Args:
            subscription_id: Subscription ID (URN)
            update_data: Partial subscription data to update
            tenant: NGSI-LD tenant

        Returns:
            HTTP status code (204 on success)

        Example:
            # Update notification endpoint
            await service.update_subscription(
                "urn:ngsi-ld:Subscription:5fd228838b9b83697b855a72",
                {
                    "notification": {
                        "endpoint": {
                            "uri": "http://newserver:3000/notifications"
                        }
                    }
                }
            )
        """
        headers = {"Content-Type": "application/json"}
        if tenant:
            headers["NGSILD-Tenant"] = tenant

        response = await self._make_request(
            "PATCH",
            f"subscriptions/{subscription_id}",
            headers=headers,
            json_payload=update_data,
        )

        return response.status_code

    async def delete_subscription(
        self,
        subscription_id: str,
        tenant: Optional[str] = None,
    ) -> int:
        """
        Delete a subscription.

        Args:
            subscription_id: Subscription ID (URN)
            tenant: NGSI-LD tenant

        Returns:
            HTTP status code (204 on success)

        Example:
            await service.delete_subscription(
                "urn:ngsi-ld:Subscription:5fd228838b9b83697b855a72"
            )
        """
        headers = {}
        if tenant:
            headers["NGSILD-Tenant"] = tenant

        response = await self._make_request(
            "DELETE", f"subscriptions/{subscription_id}", headers=headers
        )

        return response.status_code

    # Helper methods for common subscription patterns

    async def subscribe_to_entity_changes(
        self,
        entity_type: str,
        notification_uri: str,
        attributes: Optional[List[str]] = None,
        q: Optional[str] = None,
        description: Optional[str] = None,
    ) -> httpx.Response:
        """
        Create a subscription for entity type changes.

        Args:
            entity_type: Entity type to watch
            notification_uri: Where to send notifications
            attributes: Specific attributes to watch
            q: Query filter
            description: Subscription description

        Returns:
            httpx.Response with subscription ID

        Example:
            # Watch for low battery devices
            await service.subscribe_to_entity_changes(
                entity_type="Device",
                notification_uri="http://myapp:3000/low-battery",
                attributes=["batteryLevel"],
                q="batteryLevel<0.2",
                description="Low battery alert"
            )
        """
        desc = description or f"Subscribe to {entity_type} changes"

        return await self.create_subscription(
            description=desc,
            entities=[{"type": entity_type}],
            notification_uri=notification_uri,
            watched_attributes=attributes,
            q=q,
        )

    async def subscribe_to_specific_entity(
        self,
        entity_id: str,
        notification_uri: str,
        attributes: Optional[List[str]] = None,
        description: Optional[str] = None,
    ) -> httpx.Response:
        """
        Create a subscription for a specific entity.

        Args:
            entity_id: Specific entity ID to watch
            notification_uri: Where to send notifications
            attributes: Specific attributes to watch
            description: Subscription description

        Returns:
            httpx.Response with subscription ID

        Example:
            await service.subscribe_to_specific_entity(
                entity_id="urn:ngsi-ld:Device:sensor001",
                notification_uri="http://myapp:3000/sensor001-updates",
                attributes=["temperature", "humidity"]
            )
        """
        desc = description or f"Subscribe to {entity_id} changes"

        return await self.create_subscription(
            description=desc,
            entities=[{"id": entity_id}],
            notification_uri=notification_uri,
            watched_attributes=attributes,
        )

    async def subscribe_with_mqtt(
        self,
        entity_type: str,
        mqtt_broker: str,
        mqtt_topic: str,
        mqtt_qos: str = "1",
        attributes: Optional[List[str]] = None,
        q: Optional[str] = None,
        description: Optional[str] = None,
    ) -> httpx.Response:
        """
        Create an MQTT subscription.

        Args:
            entity_type: Entity type to watch
            mqtt_broker: MQTT broker address (e.g., "mosquitto:1883")
            mqtt_topic: MQTT topic to publish to
            mqtt_qos: MQTT Quality of Service level
            attributes: Specific attributes to watch
            q: Query filter
            description: Subscription description

        Returns:
            httpx.Response with subscription ID

        Example:
            await service.subscribe_with_mqtt(
                entity_type="WaterQualityObserved",
                mqtt_broker="mosquitto:1883",
                mqtt_topic="/water-quality/alerts",
                mqtt_qos="1",
                attributes=["pH", "turbidity"],
                q="pH<6.5|pH>8.5"
            )
        """
        desc = description or f"MQTT subscription for {entity_type}"
        mqtt_uri = f"mqtt://{mqtt_broker}/{mqtt_topic}"

        return await self.create_subscription(
            description=desc,
            entities=[{"type": entity_type}],
            notification_uri=mqtt_uri,
            watched_attributes=attributes,
            q=q,
            notification_format="keyValues",
            notifier_info=[{"key": "MQTT-QoS", "value": mqtt_qos}],
        )


# Singleton instance
subscription_service = SubscriptionService()
