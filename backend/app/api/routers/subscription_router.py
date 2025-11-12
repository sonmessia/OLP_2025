from fastapi import APIRouter, HTTPException
from app.services.subscription_service import SubscriptionService
import requests

router = APIRouter(prefix="/api/subscriptions", tags=["Subscriptions"])

@router.post("/")
def create_subscription(subscription_data: dict):
    try:
        return SubscriptionService.create_subscription(subscription_data)
    except requests.HTTPError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)

@router.get("/")
def get_all_subscriptions():
    try:
        return SubscriptionService.get_all_subscriptions()
    except requests.HTTPError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)

@router.get("/{subscription_id}")
def get_subscription_by_id(subscription_id: str):
    try:
        return SubscriptionService.get_subscription_by_id(subscription_id)
    except requests.HTTPError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)

@router.patch("/{subscription_id}")
def update_subscription(subscription_id: str, update_data: dict):
    try:
        return SubscriptionService.update_subscription(subscription_id, update_data)
    except requests.HTTPError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)

@router.delete("/{subscription_id}")
def delete_subscription(subscription_id: str):
    try:
        return SubscriptionService.delete_subscription(subscription_id)
    except requests.HTTPError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)