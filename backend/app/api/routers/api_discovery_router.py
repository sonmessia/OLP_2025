import httpx
from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from app.services.api_discovery_service import ApiDiscoveryService, SystemService

router = APIRouter(prefix="/api/v1/discovery", tags=["API Discovery"])


@router.get("/types")
async def get_all_types(
    limit: Optional[int] = Query(
        None, description="Maximum number of results to return"
    ),
    offset: Optional[int] = Query(None, description="Number of results to skip"),
    count: bool = Query(False, description="Return total count in headers"),
):
    """List all entity types in the Broker"""
    try:
        return ApiDiscoveryService.get_all_types(
            limit=limit, offset=offset, count=count
        )
    except httpx.HTTPError as e:
        raise HTTPException(status_code=getattr(e.response, 'status_code', 500), detail=str(e))


@router.get("/attributes")
async def get_all_attributes(
    limit: Optional[int] = Query(
        None, description="Maximum number of results to return"
    ),
    offset: Optional[int] = Query(None, description="Number of results to skip"),
    count: bool = Query(False, description="Return total count in headers"),
):
    """List all attribute names in the Broker"""
    try:
        return ApiDiscoveryService.get_all_attributes(
            limit=limit, offset=offset, count=count
        )
    except httpx.HTTPError as e:
        raise HTTPException(status_code=getattr(e.response, 'status_code', 500), detail=str(e))


@router.get("/version")
async def get_version():
    """Get Broker version and uptime information"""
    try:
        return SystemService.get_version()
    except httpx.HTTPError as e:
        raise HTTPException(status_code=getattr(e.response, 'status_code', 500), detail=str(e))
