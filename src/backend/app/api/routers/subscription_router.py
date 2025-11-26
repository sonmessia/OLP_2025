# Copyright (c) 2025 Green Wave Team
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import logging
from typing import Any, Dict, List, Optional

import httpx
from fastapi import APIRouter, HTTPException, Query, Response, status
from pydantic import BaseModel, Field

from app.services.subscription_service import subscription_service

router = APIRouter(prefix="/api/v1/subscriptions", tags=["Subscriptions"])
logger = logging.getLogger(__name__)


class EntityPattern(BaseModel):
    """Entity pattern for subscription."""

    id: Optional[str] = Field(None, description="Specific entity ID")
    type: Optional[str] = Field(None, description="Entity type")


class NotificationEndpoint(BaseModel):
    """Notification endpoint configuration."""

    uri: str = Field(..., description="Notification URI (HTTP or MQTT)")
    accept: str = Field("application/json", description="Accept header")
    notifierInfo: Optional[List[Dict[str, str]]] = Field(
        None, description="Additional notifier info (e.g., MQTT QoS)"
    )


class SubscriptionCreate(BaseModel):
    """Model for creating a subscription."""

    description: str = Field(..., description="Subscription description")
    entities: List[EntityPattern] = Field(..., description="Entity patterns to watch")
    watchedAttributes: Optional[List[str]] = Field(
        None, description="Attributes to watch"
    )
    q: Optional[str] = Field(None, description="Query filter")
    notificationFormat: str = Field("normalized", description="Notification format")
    notificationUri: str = Field(..., description="Where to send notifications")
    notificationAccept: str = Field("application/json")
    notifierInfo: Optional[List[Dict[str, str]]] = None
    expiresAt: Optional[str] = Field(None, description="ISO8601 expiration timestamp")
    throttling: Optional[int] = Field(
        None, description="Min seconds between notifications"
    )


class SubscriptionUpdate(BaseModel):
    """Model for updating a subscription."""

    description: Optional[str] = None
    watchedAttributes: Optional[List[str]] = None
    q: Optional[str] = None
    notification: Optional[Dict[str, Any]] = None
    expiresAt: Optional[str] = None
    throttling: Optional[int] = None


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_subscription(
    response: Response,
    subscription: SubscriptionCreate,
    tenant: Optional[str] = Query(None, description="NGSI-LD tenant"),
):
    """
    Create a new subscription.

    The subscription will trigger notifications when the specified
    entities change according to the watch criteria.

    Examples:
        # HTTP notification
        {
            "description": "Low battery alert",
            "entities": [{"type": "Device"}],
            "watchedAttributes": ["batteryLevel"],
            "q": "batteryLevel<0.2",
            "notificationFormat": "keyValues",
            "notificationUri": "http://myapp:3000/low-battery"
        }

        # MQTT notification
        {
            "description": "Water quality alerts",
            "entities": [{"type": "WaterQualityObserved"}],
            "watchedAttributes": ["pH"],
            "q": "pH<6.5|pH>8.5",
            "notificationFormat": "keyValues",
            "notificationUri": "mqtt://mosquitto:1883/water-alerts",
            "notifierInfo": [{"key": "MQTT-QoS", "value": "1"}]
        }
    """
    try:
        orion_response = await subscription_service.create_subscription(
            description=subscription.description,
            entities=[e.model_dump(exclude_none=True) for e in subscription.entities],
            notification_uri=subscription.notificationUri,
            watched_attributes=subscription.watchedAttributes,
            q=subscription.q,
            notification_format=subscription.notificationFormat,
            notification_accept=subscription.notificationAccept,
            notifier_info=subscription.notifierInfo,
            expires_at=subscription.expiresAt,
            throttling=subscription.throttling,
            tenant=tenant,
        )

        response.headers["Location"] = orion_response.headers.get("Location", "")
        subscription_id = orion_response.headers.get("Location", "").split("/")[-1]

        return {"message": "Subscription created successfully", "id": subscription_id}

    except httpx.HTTPStatusError as e:
        logger.error(f"Failed to create subscription: {e.response.text}")
        raise HTTPException(
            status_code=e.response.status_code,
            detail=(
                e.response.json()
                if e.response.headers.get("content-type") == "application/json"
                else {"error": e.response.text}
            ),
        ) from e


@router.get("/", response_model=List[Dict[str, Any]])
async def get_all_subscriptions(
    limit: Optional[int] = Query(None, ge=1, le=1000),
    offset: Optional[int] = Query(None, ge=0),
    tenant: Optional[str] = Query(None),
):
    """
    Get all subscriptions.

    Returns a list of all active subscriptions including their
    notification status (last notification time, success/failure).
    """
    try:
        return await subscription_service.get_all_subscriptions(
            limit=limit, offset=offset, tenant=tenant
        )
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code, detail=e.response.json()
        ) from e


@router.get("/{subscription_id}", response_model=Dict[str, Any])
async def get_subscription(subscription_id: str, tenant: Optional[str] = Query(None)):
    """
    Get details of a specific subscription.

    Includes notification statistics like last notification time,
    number of notifications sent, and success/failure status.
    """
    try:
        return await subscription_service.get_subscription(
            subscription_id=subscription_id, tenant=tenant
        )
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"error": "Subscription not found"},
            ) from e
        raise HTTPException(
            status_code=e.response.status_code, detail=e.response.json()
        ) from e


@router.patch("/{subscription_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_subscription(
    subscription_id: str,
    update_data: SubscriptionUpdate,
    tenant: Optional[str] = Query(None),
):
    """
    Update an existing subscription.

    You can update the notification endpoint, watched attributes,
    query filter, or other subscription parameters.
    """
    try:
        await subscription_service.update_subscription(
            subscription_id=subscription_id,
            update_data=update_data.model_dump(exclude_none=True),
            tenant=tenant,
        )
        return
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"error": "Subscription not found"},
            ) from e
        raise HTTPException(
            status_code=e.response.status_code, detail=e.response.json()
        ) from e


@router.delete("/{subscription_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_subscription(
    subscription_id: str, tenant: Optional[str] = Query(None)
):
    """Delete a subscription."""
    try:
        await subscription_service.delete_subscription(
            subscription_id=subscription_id, tenant=tenant
        )
        return
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"error": "Subscription not found"},
            ) from e
        raise HTTPException(
            status_code=e.response.status_code, detail=e.response.json()
        ) from e


# Convenience endpoints


@router.post("/quick/entity-type", status_code=status.HTTP_201_CREATED)
async def quick_subscribe_entity_type(
    response: Response,
    entity_type: str = Query(..., description="Entity type to watch"),
    notification_uri: str = Query(..., description="Notification endpoint"),
    attributes: Optional[str] = Query(None, description="Comma-separated attributes"),
    q: Optional[str] = Query(None, description="Query filter"),
    description: Optional[str] = Query(None),
    tenant: Optional[str] = Query(None),
):
    """
    Quick subscription to an entity type.

    Example: /api/v1/subscriptions/quick/entity-type?entity_type=Device&notification_uri=http://myapp:3000/alerts&attributes=batteryLevel&q=batteryLevel<0.2
    """
    try:
        attrs_list = attributes.split(",") if attributes else None

        orion_response = await subscription_service.subscribe_to_entity_changes(
            entity_type=entity_type,
            notification_uri=notification_uri,
            attributes=attrs_list,
            q=q,
            description=description,
        )

        response.headers["Location"] = orion_response.headers.get("Location", "")
        subscription_id = orion_response.headers.get("Location", "").split("/")[-1]

        return {"message": "Subscription created", "id": subscription_id}

    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code, detail=e.response.json()
        ) from e
