from fastapi import APIRouter, HTTPException
from app.services.carbon_footprint_service import CarbonFootprintService
import requests

router = APIRouter(prefix="/api/v1/carbon-footprint", tags=["CarbonFootprint"])


@router.get("/")
def get_all_carbon_footprint():
    try:
        return CarbonFootprintService.get_all_entities()
    except requests.HTTPError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)


@router.get("/{entity_id}")
def get_carbon_footprint_by_id(entity_id: str):
    try:
        return CarbonFootprintService.get_entity_by_id(entity_id)
    except requests.HTTPError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)


@router.post("/")
def create_carbon_footprint(entity_data: dict):
    try:
        return CarbonFootprintService.create_entity(entity_data)
    except requests.HTTPError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)


@router.patch("/{entity_id}")
def update_carbon_footprint(entity_id: str, update_data: dict):
    try:
        return CarbonFootprintService.update_entity(entity_id, update_data)
    except requests.HTTPError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)


@router.delete("/{entity_id}")
def delete_carbon_footprint(entity_id: str):
    try:
        return CarbonFootprintService.delete_entity(entity_id)
    except requests.HTTPError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
