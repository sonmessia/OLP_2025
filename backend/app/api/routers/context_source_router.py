from fastapi import APIRouter, HTTPException
from app.services.context_source_service import ContextSourceService
import requests

router = APIRouter(prefix="/api/v1/csourceRegistrations", tags=["ContextSources"])


@router.post("/")
def create_context_source(context_source_data: dict):
    try:
        return ContextSourceService.create_context_source(context_source_data)
    except requests.HTTPError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)


@router.get("/")
def get_all_context_sources():
    try:
        return ContextSourceService.get_all_context_sources()
    except requests.HTTPError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)


@router.get("/{context_source_id}")
def get_context_source_by_id(context_source_id: str):
    try:
        return ContextSourceService.get_context_source_by_id(context_source_id)
    except requests.HTTPError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)


@router.patch("/{context_source_id}")
def update_context_source(context_source_id: str, update_data: dict):
    try:
        return ContextSourceService.update_context_source(
            context_source_id, update_data
        )
    except requests.HTTPError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)


@router.delete("/{context_source_id}")
def delete_context_source(context_source_id: str):
    try:
        return ContextSourceService.delete_context_source(context_source_id)
    except requests.HTTPError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
