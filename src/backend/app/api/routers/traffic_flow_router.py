# Copyright (c) 2025 Green Wave Team
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import logging
from typing import Any, Dict, List, Optional, Union

import httpx
from fastapi import APIRouter, HTTPException, Query, Response, status

from app.services.traffic_flow_service import traffic_flow_service

router = APIRouter(prefix="/api/v1/traffic-flow", tags=["TrafficFlowObserved"])
logger = logging.getLogger(__name__)


@router.get("/", response_model=Union[List[Dict[str, Any]], int])
async def get_all_traffic_flow(
    id: Optional[str] = Query(None),
    q: Optional[str] = Query(None),
    pick: Optional[str] = Query(None),
    limit: Optional[int] = Query(None, ge=1, le=1000),
    offset: Optional[int] = Query(None, ge=0),
    count: Optional[bool] = Query(False),
    format: Optional[str] = Query(None),
    options: Optional[str] = Query(None),
    local: Optional[bool] = Query(None),
):
    try:
        return await traffic_flow_service.get_all(
            id=id,
            q=q,
            pick=pick,
            limit=limit,
            offset=offset,
            count=count,
            format=format,
            options=options,
            local=local,
        )
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error retrieving traffic flow entities: {e.response.text}")
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text) from e
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e


@router.get("/{entity_id}", response_model=Dict[str, Any])
async def get_traffic_flow_by_id(entity_id: str):
    try:
        return await traffic_flow_service.get_by_id(entity_id=entity_id)
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"TrafficFlowObserved {entity_id} not found") from e
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text) from e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_traffic_flow(entity_data: Dict[str, Any]):
    try:
        response = await traffic_flow_service.create(entity_data)
        return Response(status_code=response.status_code, content=response.text)
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text) from e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e


@router.patch("/{entity_id}", status_code=status.HTTP_204_NO_CONTENT)
async def patch_traffic_flow(entity_id: str, attrs: Dict[str, Any]):
    try:
        response = await traffic_flow_service.update(entity_id, attrs)
        return Response(status_code=response.status_code, content=response.text)
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text) from e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e


@router.delete("/{entity_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_traffic_flow(entity_id: str):
    try:
        response = await traffic_flow_service.delete(entity_id)
        return Response(status_code=response.status_code, content=response.text)
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text) from e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e
