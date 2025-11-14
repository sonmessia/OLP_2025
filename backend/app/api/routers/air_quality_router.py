from fastapi import APIRouter, HTTPException, Query, Body, Response
from typing import Optional, List, Dict, Any, Union
from pydantic import BaseModel, Field, model_validator
import httpx
import datetime

from app.services.air_quality_service import air_quality_service

router = APIRouter(prefix="/api/v1/air-quality", tags=["AirQualityObserved"])


class NgsiLdAttributePatch(BaseModel):
    """
    Model để xác thực cấu trúc của một thuộc tính khi cập nhật (PATCH).
    Đảm bảo payload gửi đến Orion-LD luôn hợp lệ.
    """

    type: str = Field(
        default="Property", pattern="^(Property|Relationship|GeoProperty)$"
    )
    value: Optional[Any] = None
    object: Optional[str] = None
    observedAt: Optional[str] = None
    unitCode: Optional[str] = None

    @model_validator(mode="after")
    def check_value_or_object_exists(self) -> "NgsiLdAttributePatch":
        if self.value is None and self.object is None:
            raise ValueError(
                'Either "value" or "object" must be provided for an attribute.'
            )
        return self


@router.get(
    "/",
    response_model=Union[List[Dict[str, Any]], int],
    summary="Query AirQualityObserved Entities",
)
async def get_all_air_quality(
    limit: Optional[int] = Query(
        None, description="Maximum number of results to return per page."
    ),
    offset: Optional[int] = Query(None, description="The number of results to skip."),
    attrs: Optional[str] = Query(
        None, description="Comma-separated list of attributes to return."
    ),
    q: Optional[str] = Query(
        None, description="NGSI-LD query filter string (e.g., CO>500;temperature<30)."
    ),
    count: bool = Query(
        False, description="If true, return only the total count of matching entities."
    ),
    format: str = Query(
        "normalized", description="Response format: 'keyValues' or 'normalized'."
    ),
    local: Optional[bool] = Query(True, description="Query only local entities."),
):
    """
    Retrieve a list of AirQualityObserved entities based on query parameters.
    """
    try:
        attrs_list = attrs.split(",") if attrs else None

        result = await air_quality_service.get_all(
            limit=limit,
            offset=offset,
            attrs=attrs_list,
            q=q,
            count=count,
            format=format,
            local=local,
        )
        return result
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code, detail=e.response.json()
        )
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=503, detail={"error": "Service Unavailable", "detail": str(e)}
        )


@router.get(
    "/{entity_id:path}",
    response_model=Dict[str, Any],
    summary="Get AirQualityObserved Entity by ID",
)
async def get_air_quality_by_id(
    entity_id: str,
    attrs: Optional[str] = Query(
        None, description="Comma-separated list of attributes to return."
    ),
    format: str = Query(
        "keyValues", description="Response format: 'keyValues' or 'normalized'."
    ),
):
    """
    Retrieve a single AirQualityObserved entity by its full URN.
    """
    try:
        attrs_list = attrs.split(",") if attrs else None
        return await air_quality_service.get_by_id(
            entity_id, attrs=attrs_list, format=format
        )
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code, detail=e.response.json()
        )


@router.post("/", status_code=201, summary="Create AirQualityObserved Entity")
async def create_air_quality(
    response: Response, entity_data: Dict[str, Any] = Body(...)
):
    """
    Create a new AirQualityObserved entity.
    """
    try:
        orion_response = await air_quality_service.create(entity_data)
        response.headers["Location"] = orion_response.headers.get("Location", "")
        return
    except httpx.HTTPStatusError as e:
        detail = e.response.json() if hasattr(e.response, "json") else str(e)
        status = e.response.status_code
        raise HTTPException(status_code=status, detail=detail)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))


@router.patch(
    "/{entity_id:path}/attrs",
    status_code=204,
    summary="Update Entity Attributes (Partial Update)",
)
async def update_air_quality_attributes(
    entity_id: str, update_data: Dict[str, NgsiLdAttributePatch]
):
    """
    Update one or more attributes of an AirQualityObserved entity using
    the NGSI-LD Partial Update specification (/attrs).
    """
    try:
        payload_to_send = {
            key: value.model_dump(exclude_unset=True)
            for key, value in update_data.items()
        }
        await air_quality_service.update_attrs(entity_id, payload_to_send)
        return
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code, detail=e.response.json()
        )


@router.delete(
    "/{entity_id:path}", status_code=204, summary="Delete AirQualityObserved Entity"
)
async def delete_air_quality(entity_id: str):
    """
    Delete an AirQualityObserved entity by its ID.
    """
    try:
        await air_quality_service.delete(entity_id)
        return
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code, detail=e.response.json()
        )
