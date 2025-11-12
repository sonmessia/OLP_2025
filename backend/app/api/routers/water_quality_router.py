from fastapi import APIRouter, HTTPException
from app.services.water_quality_service import WaterQualityService
import requests

router = APIRouter(prefix="/api/v1/water-quality", tags=["WaterQualityObserved"])


@router.get("/")
def get_all_water_quality():
    try:
        return WaterQualityService.get_all_entities()
    except requests.HTTPError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)


@router.get("/{entity_id}")
def get_water_quality_by_id(entity_id: str):
    try:
        return WaterQualityService.get_entity_by_id(entity_id)
    except requests.HTTPError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)


@router.post("/")
def create_water_quality(entity_data: dict):
    try:
        return WaterQualityService.create_entity(entity_data)
    except requests.HTTPError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)


@router.patch("/{entity_id}")
def update_water_quality(entity_id: str, update_data: dict):
    try:
        return WaterQualityService.update_entity(entity_id, update_data)
    except requests.HTTPError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)


@router.delete("/{entity_id}")
def delete_water_quality(entity_id: str):
    try:
        return WaterQualityService.delete_entity(entity_id)
    except requests.HTTPError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
