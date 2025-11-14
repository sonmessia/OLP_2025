from fastapi import APIRouter, HTTPException, Query, Body, Response
from typing import Optional, List, Dict, Any, Union
import httpx

from app.services.subscription_service import subscription_service

router = APIRouter(prefix="/api/v1/subscriptions", tags=["Subscriptions"])


@router.post("/", status_code=201, summary="Create a new Subscription")
async def create_subscription(
    response: Response, subscription_data: Dict[str, Any] = Body(...)
):
    """
    Create a new subscription for event-driven notifications.

    The subscription payload should include:
    - type: Always "Subscription"
    - description: Human-readable description (optional)
    - entities: Array defining entities to monitor (required)
      Example: [{"type": "AirQualityObserved"}]
    - watchedAttributes: List of attributes to monitor (optional)
      Example: ["CO", "NO2"]
    - q: Filter condition (optional)
      Example: "CO > 800"
    - notification: Notification configuration (required)
      - attributes: Attributes to include in notification (optional)
      - format: "keyValues" or "normalized" (optional)
      - endpoint: Destination configuration (required)
        - uri: Notification URL (required)
        - accept: Content-Type for notification (optional)

    Returns Location header with the subscription ID.
    """
    try:
        orion_response = await subscription_service.create_subscription(
            subscription_data
        )
        # Thiết lập header Location
        response.headers["Location"] = orion_response.headers.get("Location", "")
        return
    except httpx.HTTPStatusError as e:
        detail = e.response.json() if hasattr(e.response, "json") else str(e)
        status = e.response.status_code
        raise HTTPException(status_code=status, detail=detail)
    except httpx.RequestError as e:
        raise HTTPException(status_code=422, detail=str(e))


@router.get(
    "/",
    response_model=Union[List[Dict[str, Any]], int],
    summary="List all Subscriptions",
)
async def get_all_subscriptions(
    limit: Optional[int] = Query(
        None, description="Maximum number of results to return per page."
    ),
    offset: Optional[int] = Query(None, description="The number of results to skip."),
    count: bool = Query(
        False, description="If true, return only the total count of subscriptions."
    ),
):
    """
    Retrieve a list of all active subscriptions.

    Use limit and offset for pagination.
    Set count=true to get only the total count of subscriptions.
    """
    try:
        result = await subscription_service.get_all_subscriptions(
            limit=limit, offset=offset, count=count
        )
        return result
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code, detail=e.response.json()
        )
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=503, detail={"error": "Service Unavailable", "detail": str(e)}
        )


@router.get(
    "/{subscription_id:path}",
    response_model=Dict[str, Any],
    summary="Get Subscription by ID",
)
async def get_subscription_by_id(subscription_id: str):
    """
    Retrieve details of a specific subscription.

    Useful for debugging as the response includes diagnostic information:
    - status: Current status of the subscription
    - timesSent: Number of notifications sent
    - lastFailure: Timestamp of last failed notification
    - lastSuccess: Timestamp of last successful notification
    - lastFailureReason: Reason for last failure
    """
    try:
        return await subscription_service.get_subscription_by_id(subscription_id)
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code, detail=e.response.json()
        )


@router.patch(
    "/{subscription_id:path}",
    status_code=204,
    summary="Update Subscription (Partial Update)",
)
async def update_subscription(
    subscription_id: str, update_data: Dict[str, Any] = Body(...)
):
    """
    Update an existing subscription.

    You only need to send the fields you want to change.
    Common updates:
    - description: Update the description
    - notification.endpoint.uri: Change the notification URL
    - watchedAttributes: Modify monitored attributes
    - q: Update filter conditions

    Example:
    {
      "description": "Updated description",
      "notification": {
        "endpoint": {
          "uri": "http://new-url/notifications"
        }
      }
    }
    """
    try:
        await subscription_service.update_subscription(subscription_id, update_data)
        return
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code, detail=e.response.json()
        )


@router.delete(
    "/{subscription_id:path}", status_code=204, summary="Delete Subscription"
)
async def delete_subscription(subscription_id: str):
    """
    Delete (cancel) a subscription.

    After deletion, no more notifications will be sent for this subscription.
    """
    try:
        await subscription_service.delete_subscription(subscription_id)
        return
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code, detail=e.response.json()
        )
