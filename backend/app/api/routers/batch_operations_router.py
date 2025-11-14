import httpx
from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from pydantic import BaseModel
from app.services.batch_operations_service import BatchOperationsService

router = APIRouter(prefix="/api/v1/batch", tags=["Batch Operations"])


class BatchCreateRequest(BaseModel):
    entities: List[Dict[str, Any]]
    local: bool = True


class BatchUpsertRequest(BaseModel):
    entities: List[Dict[str, Any]]
    local: bool = True


class BatchUpdateRequest(BaseModel):
    entities: List[Dict[str, Any]]
    local: bool = True


class BatchDeleteRequest(BaseModel):
    entity_ids: List[str]
    local: bool = True


@router.post("/create")
async def create_entities(request: BatchCreateRequest):
    """Create multiple entities"""
    try:
        return BatchOperationsService.create_entities(
            entities_data=request.entities, local=request.local
        )
    except httpx.HTTPError as e:
        raise HTTPException(
            status_code=getattr(e.response, "status_code", 500), detail=str(e)
        )


@router.post("/upsert")
async def upsert_entities(request: BatchUpsertRequest):
    """Create new entities or update existing ones"""
    try:
        return BatchOperationsService.upsert_entities(
            entities_data=request.entities, local=request.local
        )
    except httpx.HTTPError as e:
        raise HTTPException(
            status_code=getattr(e.response, "status_code", 500), detail=str(e)
        )


@router.post("/update")
async def update_entities(request: BatchUpdateRequest):
    """Update multiple entities"""
    try:
        return BatchOperationsService.update_entities(
            entities_data=request.entities, local=request.local
        )
    except httpx.HTTPError as e:
        raise HTTPException(
            status_code=getattr(e.response, "status_code", 500), detail=str(e)
        )


@router.post("/delete")
async def delete_entities(request: BatchDeleteRequest):
    """Delete multiple entities"""
    try:
        return BatchOperationsService.delete_entities(
            entity_ids=request.entity_ids, local=request.local
        )
    except httpx.HTTPError as e:
        raise HTTPException(
            status_code=getattr(e.response, "status_code", 500), detail=str(e)
        )
