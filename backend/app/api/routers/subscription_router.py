import httpx
from fastapi import APIRouter, HTTPException, Query
from typing import Optional, Dict, Any
from app.services.subscription_service import SubscriptionService

router = APIRouter(prefix="/api/v1/subscriptions", tags=["Subscriptions"])


@router.post("/")
async def create_subscription(subscription_data: Dict[str, Any]):
    try:
        return SubscriptionService.create_subscription(subscription_data)
    except httpx.HTTPError as e:
        raise HTTPException(status_code=getattr(e.response, 'status_code', 500), detail=str(e))


@router.get("/")
async def get_all_subscriptions(
    limit: Optional[int] = Query(None, description="Maximum number of results"),
    offset: Optional[int] = Query(None, description="Number of results to skip"),
    count: bool = Query(False, description="Return total count"),
):
    try:
        return SubscriptionService.get_all_subscriptions(
            limit=limit, offset=offset, count=count
        )
    except httpx.HTTPError as e:
        raise HTTPException(status_code=getattr(e.response, 'status_code', 500), detail=str(e))


@router.get("/{subscription_id}")
async def get_subscription_by_id(subscription_id: str):
    try:
        return SubscriptionService.get_subscription_by_id(subscription_id)
    except httpx.HTTPError as e:
        raise HTTPException(status_code=getattr(e.response, 'status_code', 500), detail=str(e))


@router.patch("/{subscription_id}")
async def update_subscription(subscription_id: str, update_data: Dict[str, Any]):
    try:
        return SubscriptionService.update_subscription(subscription_id, update_data)
    except httpx.HTTPError as e:
        raise HTTPException(status_code=getattr(e.response, 'status_code', 500), detail=str(e))


@router.delete("/{subscription_id}")
async def delete_subscription(subscription_id: str):
    try:
        return SubscriptionService.delete_subscription(subscription_id)
    except httpx.HTTPError as e:
        raise HTTPException(status_code=getattr(e.response, 'status_code', 500), detail=str(e))
