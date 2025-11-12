from fastapi import APIRouter, HTTPException
from app.services.building_service import BuildingService
import requests

router = APIRouter(prefix="/api/building", tags=["Building"])

@router.get("/")
def get_all_buildings():
    try:
        return BuildingService.get_all_entities()
    except requests.HTTPError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)

@router.get("/{entity_id}")
def get_building_by_id(entity_id: str):
    try:
        return BuildingService.get_entity_by_id(entity_id)
    except requests.HTTPError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)

@router.post("/")
def create_building(entity_data: dict):
    try:
        return BuildingService.create_entity(entity_data)
    except requests.HTTPError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)

@router.patch("/{entity_id}")
def update_building(entity_id: str, update_data: dict):
    try:
        return BuildingService.update_entity(entity_id, update_data)
    except requests.HTTPError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)

@router.delete("/{entity_id}")
def delete_building(entity_id: str):
    try:
        return BuildingService.delete_entity(entity_id)
    except requests.HTTPError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)