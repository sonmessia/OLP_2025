from typing import Any, Dict, Optional

import httpx
from fastapi import APIRouter, HTTPException, Query

from app.services.context_source_service import ContextSourceService

router = APIRouter(prefix="/api/v1/csourceRegistrations", tags=["ContextSources"])


@router.post("/")
async def create_context_source(context_source_data: Dict[str, Any]):
    try:
        return ContextSourceService.create_context_source(context_source_data)
    except httpx.HTTPError as e:
        raise HTTPException(
            status_code=getattr(e.response, "status_code", 500), detail=str(e)
        )


@router.get("/")
async def get_all_context_sources(
    limit: Optional[int] = Query(None, description="Maximum number of results"),
    offset: Optional[int] = Query(None, description="Number of results to skip"),
    count: bool = Query(False, description="Return total count"),
):
    try:
        return ContextSourceService.get_all_context_sources(
            limit=limit, offset=offset, count=count
        )
    except httpx.HTTPError as e:
        raise HTTPException(
            status_code=getattr(e.response, "status_code", 500), detail=str(e)
        )


@router.get("/{context_source_id}")
async def get_context_source_by_id(context_source_id: str):
    try:
        return ContextSourceService.get_context_source_by_id(context_source_id)
    except httpx.HTTPError as e:
        raise HTTPException(
            status_code=getattr(e.response, "status_code", 500), detail=str(e)
        )


@router.patch("/{context_source_id}")
async def update_context_source(context_source_id: str, update_data: Dict[str, Any]):
    try:
        return ContextSourceService.update_context_source(
            context_source_id, update_data
        )
    except httpx.HTTPError as e:
        raise HTTPException(
            status_code=getattr(e.response, "status_code", 500), detail=str(e)
        )


@router.delete("/{context_source_id}")
async def delete_context_source(context_source_id: str):
    try:
        return ContextSourceService.delete_context_source(context_source_id)
    except httpx.HTTPError as e:
        raise HTTPException(
            status_code=getattr(e.response, "status_code", 500), detail=str(e)
        )
