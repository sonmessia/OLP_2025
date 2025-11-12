import requests
from fastapi import APIRouter, HTTPException
from backend.app.services.air_quality_service import AirQualityService

router = APIRouter(prefix="/api/air-quality", tags=["AirQualityObserved"])

@router.get("/")
def get_all_air_quality():
    try:
        return AirQualityService.get_all_entities()
    except requests.HTTPError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)

@router.get("/{entity_id}")
def get_air_quality_by_id(entity_id: str):
    try:
        return AirQualityService.get_entity_by_id(entity_id)
    except requests.HTTPError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)

@router.post("/")
def create_air_quality(entity_data: dict):
    try:
        return AirQualityService.create_entity(entity_data)
    except requests.HTTPError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)

@router.patch("/{entity_id}")
def update_air_quality(entity_id: str, update_data: dict):
    try:
        return AirQualityService.update_entity(entity_id, update_data)
    except requests.HTTPError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)

@router.delete("/{entity_id}")
def delete_air_quality(entity_id: str):
    try:
        return AirQualityService.delete_entity(entity_id)
    except requests.HTTPError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)