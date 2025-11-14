import httpx
from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from app.services.building_service import BuildingService

router = APIRouter(prefix="/api/v1/building", tags=["Building"])


class AttributeRequest(BaseModel):
    value: Any
    type: Optional[str] = None


@router.get("/")
async def get_all_buildings(
    local: bool = Query(True, description="Include local entities"),
    limit: Optional[int] = Query(None, description="Maximum number of results"),
    offset: Optional[int] = Query(None, description="Number of results to skip"),
    attrs: Optional[List[str]] = Query(None, description="Attributes to return"),
    q: Optional[str] = Query(None, description="Query filter"),
    count: bool = Query(False, description="Return total count"),
):
    try:
        return BuildingService.get_all_entities(
            local=local, limit=limit, offset=offset, attrs=attrs, q=q, count=count
        )
    except httpx.HTTPError as e:
        raise HTTPException(status_code=getattr(e.response, 'status_code', 500), detail=str(e))


@router.get("/{entity_id}")
async def get_building_by_id(
    entity_id: str,
    local: bool = Query(True, description="Include local entities"),
    attrs: Optional[List[str]] = Query(None, description="Attributes to return"),
):
    try:
        return BuildingService.get_entity_by_id(entity_id, local=local, attrs=attrs)
    except httpx.HTTPError as e:
        raise HTTPException(status_code=getattr(e.response, 'status_code', 500), detail=str(e))


@router.post("/")
async def create_building(
    entity_data: Dict[str, Any],
    local: bool = Query(True, description="Create local entity"),
):
    try:
        return BuildingService.create_entity(entity_data, local=local)
    except httpx.HTTPError as e:
        raise HTTPException(status_code=getattr(e.response, 'status_code', 500), detail=str(e))


@router.patch("/{entity_id}")
async def update_building_attributes(
    entity_id: str,
    update_data: Dict[str, Any],
    local: bool = Query(True, description="Update local entity"),
):
    try:
        return BuildingService.update_entity_attributes(
            entity_id, update_data, local=local
        )
    except httpx.HTTPError as e:
        raise HTTPException(status_code=getattr(e.response, 'status_code', 500), detail=str(e))


@router.put("/{entity_id}")
async def replace_building(
    entity_id: str,
    entity_data: Dict[str, Any],
    local: bool = Query(True, description="Replace local entity"),
):
    try:
        return BuildingService.replace_entity(entity_id, entity_data, local=local)
    except httpx.HTTPError as e:
        raise HTTPException(status_code=getattr(e.response, 'status_code', 500), detail=str(e))


@router.post("/{entity_id}/attrs")
async def add_building_attributes(
    entity_id: str,
    attributes_data: Dict[str, Any],
    local: bool = Query(True, description="Add to local entity"),
):
    try:
        return BuildingService.add_attributes(entity_id, attributes_data, local=local)
    except httpx.HTTPError as e:
        raise HTTPException(status_code=getattr(e.response, 'status_code', 500), detail=str(e))


@router.get("/{entity_id}/attrs/{attr_name}")
async def get_building_attribute(
    entity_id: str,
    attr_name: str,
    local: bool = Query(True, description="Get from local entity"),
):
    try:
        return BuildingService.get_attribute_by_id(entity_id, attr_name, local=local)
    except httpx.HTTPError as e:
        raise HTTPException(status_code=getattr(e.response, 'status_code', 500), detail=str(e))


@router.patch("/{entity_id}/attrs/{attr_name}")
async def update_building_attribute(
    entity_id: str,
    attr_name: str,
    attr_data: AttributeRequest,
    local: bool = Query(True, description="Update local entity"),
):
    try:
        return BuildingService.update_attribute(
            entity_id, attr_name, attr_data.dict(), local=local
        )
    except httpx.HTTPError as e:
        raise HTTPException(status_code=getattr(e.response, 'status_code', 500), detail=str(e))


@router.delete("/{entity_id}/attrs/{attr_name}")
async def delete_building_attribute(
    entity_id: str,
    attr_name: str,
    local: bool = Query(True, description="Delete from local entity"),
):
    try:
        return BuildingService.delete_attribute(entity_id, attr_name, local=local)
    except httpx.HTTPError as e:
        raise HTTPException(status_code=getattr(e.response, 'status_code', 500), detail=str(e))


@router.delete("/{entity_id}")
async def delete_building(
    entity_id: str, local: bool = Query(True, description="Delete local entity")
):
    try:
        return BuildingService.delete_entity(entity_id, local=local)
    except httpx.HTTPError as e:
        raise HTTPException(status_code=getattr(e.response, 'status_code', 500), detail=str(e))
