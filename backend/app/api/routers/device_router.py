from fastapi import APIRouter, HTTPException
from backend.app.services.device_service import DeviceService
import requests

router = APIRouter(prefix="/api/device", tags=["Device"])

@router.get("/")
def get_all_devices():
    try:
        return DeviceService.get_all_entities()
    except requests.HTTPError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)

@router.get("/{entity_id}")
def get_device_by_id(entity_id: str):
    try:
        return DeviceService.get_entity_by_id(entity_id)
    except requests.HTTPError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)

@router.post("/")
def create_device(entity_data: dict):
    try:
        return DeviceService.create_entity(entity_data)
    except requests.HTTPError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)

@router.patch("/{entity_id}")
def update_device(entity_id: str, update_data: dict):
    try:
        return DeviceService.update_entity(entity_id, update_data)
    except requests.HTTPError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)

@router.delete("/{entity_id}")
def delete_device(entity_id: str):
    try:
        return DeviceService.delete_entity(entity_id)
    except requests.HTTPError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)