# app/routers/context_source_router.py
from fastapi import APIRouter, HTTPException, Query, Response, status
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
import httpx
import logging

from app.services.context_source_service import context_source_service

router = APIRouter(
    prefix="/api/v1/csourceRegistrations", tags=["ContextSourceRegistrations"]
)
logger = logging.getLogger(__name__)


class EntityInfo(BaseModel):
    """Entity information for registration."""

    type: Optional[str] = Field(None, description="Entity type")
    id: Optional[str] = Field(None, description="Specific entity ID")


class RegistrationInfo(BaseModel):
    """Information block for registration."""

    entities: List[EntityInfo]
    propertyNames: Optional[List[str]] = Field(
        None, description="Properties to register"
    )
    relationshipNames: Optional[List[str]] = Field(
        None, description="Relationships to register"
    )


class ManagementInfo(BaseModel):
    """Management settings for registration."""

    interval: Optional[int] = Field(None, description="Refresh interval (seconds)")
    timeout: Optional[int] = Field(None, description="Request timeout (milliseconds)")


class RegistrationCreate(BaseModel):
    """Model for creating a context source registration."""

    description: str = Field(..., description="Registration description")
    entities: List[EntityInfo] = Field(..., description="Entity patterns")
    endpoint: str = Field(..., description="Context source endpoint URI")
    mode: str = Field(
        "inclusive",
        description="Registration mode: redirect, inclusive, exclusive, auxiliary",
    )
    operations: Optional[List[str]] = Field(
        None,
        description="Operations: federationOps, redirectionOps, retrieveOps, or explicit list",
    )
    propertyNames: Optional[List[str]] = None
    relationshipNames: Optional[List[str]] = None
    expiresAt: Optional[str] = Field(None, description="ISO8601 expiration")
    management: Optional[ManagementInfo] = None
    contextSourceInfo: Optional[List[Dict[str, str]]] = None


class RegistrationUpdate(BaseModel):
    """Model for updating a registration."""

    description: Optional[str] = None
    endpoint: Optional[str] = None
    expiresAt: Optional[str] = None
    management: Optional[ManagementInfo] = None
    contextSourceInfo: Optional[List[Dict[str, str]]] = None


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_registration(
    response: Response,
    registration: RegistrationCreate,
    tenant: Optional[str] = Query(None, description="NGSI-LD tenant"),
):
    """
    Create a new context source registration.

    Registrations enable federated data spaces by connecting multiple
    context sources together. Four modes are available:

    - **redirect**: All entity data is external (broker hierarchy)
    - **inclusive**: Data merged from local + external (federation)
    - **exclusive**: Specific attributes from single source (IoT devices)
    - **auxiliary**: External data as fallback only

    Examples:
        # REDIRECT: All Animal data from farmer
        {
            "description": "Farmer manages animals",
            "entities": [{"type": "Animal"}],
            "endpoint": "http://farmer-broker:1026",
            "mode": "redirect",
            "operations": ["redirectionOps"]
        }

        # INCLUSIVE: Merge vet health records
        {
            "description": "Vet health data",
            "entities": [{"type": "Animal"}],
            "endpoint": "http://vet-broker:1026",
            "mode": "inclusive",
            "operations": ["federationOps"]
        }

        # EXCLUSIVE: Live IoT sensor
        {
            "description": "Cow collar sensor",
            "entities": [{"type": "Animal", "id": "urn:ngsi-ld:Animal:cow001"}],
            "endpoint": "http://iot-agent:4041",
            "mode": "exclusive",
            "operations": ["retrieveOps"],
            "propertyNames": ["heartRate", "location"]
        }

        # AUXILIARY: Weather fallback
        {
            "description": "Weather forecast",
            "entities": [{"type": "AgriParcel"}],
            "endpoint": "http://weather:1026",
            "mode": "auxiliary",
            "operations": ["retrieveOps"],
            "propertyNames": ["temperature"]
        }
    """
    try:
        orion_response = await context_source_service.create_registration(
            description=registration.description,
            entities=[e.model_dump(exclude_none=True) for e in registration.entities],
            endpoint=registration.endpoint,
            mode=registration.mode,
            operations=registration.operations,
            property_names=registration.propertyNames,
            relationship_names=registration.relationshipNames,
            expires_at=registration.expiresAt,
            management_interval=(
                registration.management.interval if registration.management else None
            ),
            management_timeout=(
                registration.management.timeout if registration.management else None
            ),
            context_source_info=registration.contextSourceInfo,
            tenant=tenant,
        )

        response.headers["Location"] = orion_response.headers.get("Location", "")
        registration_id = orion_response.headers.get("Location", "").split("/")[-1]

        return {
            "message": "Context source registration created successfully",
            "id": registration_id,
            "mode": registration.mode,
        }

    except httpx.HTTPStatusError as e:
        logger.error(f"Failed to create registration: {e.response.text}")
        raise HTTPException(
            status_code=e.response.status_code,
            detail=(
                e.response.json()
                if e.response.headers.get("content-type") == "application/json"
                else {"error": e.response.text}
            ),
        )


@router.get("/", response_model=List[Dict[str, Any]])
async def get_all_registrations(
    entity_type: Optional[str] = Query(None, description="Filter by entity type"),
    limit: Optional[int] = Query(None, ge=1, le=1000),
    offset: Optional[int] = Query(None, ge=0),
    tenant: Optional[str] = Query(None),
):
    """
    Get all context source registrations.

    Returns a list of all active registrations including their
    mode, endpoint, and entity information.
    """
    try:
        return await context_source_service.get_all_registrations(
            entity_type=entity_type, limit=limit, offset=offset, tenant=tenant
        )
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code, detail=e.response.json()
        )


@router.get("/{registration_id}", response_model=Dict[str, Any])
async def get_registration(registration_id: str, tenant: Optional[str] = Query(None)):
    """
    Get details of a specific context source registration.
    """
    try:
        return await context_source_service.get_registration(
            registration_id=registration_id, tenant=tenant
        )
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"error": "Registration not found"},
            )
        raise HTTPException(
            status_code=e.response.status_code, detail=e.response.json()
        )


@router.patch("/{registration_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_registration(
    registration_id: str,
    update_data: RegistrationUpdate,
    tenant: Optional[str] = Query(None),
):
    """
    Update an existing context source registration.

    You can update the endpoint, expiration, or management settings.
    """
    try:
        await context_source_service.update_registration(
            registration_id=registration_id,
            update_data=update_data.model_dump(exclude_none=True),
            tenant=tenant,
        )
        return
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"error": "Registration not found"},
            )
        raise HTTPException(
            status_code=e.response.status_code, detail=e.response.json()
        )


@router.delete("/{registration_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_registration(
    registration_id: str, tenant: Optional[str] = Query(None)
):
    """Delete a context source registration."""
    try:
        await context_source_service.delete_registration(
            registration_id=registration_id, tenant=tenant
        )
        return
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"error": "Registration not found"},
            )
        raise HTTPException(
            status_code=e.response.status_code, detail=e.response.json()
        )


# Quick registration endpoints


@router.post("/quick/redirect", status_code=status.HTTP_201_CREATED)
async def quick_redirect_registration(
    response: Response,
    entity_type: str = Query(..., description="Entity type to redirect"),
    endpoint: str = Query(..., description="External endpoint"),
    description: Optional[str] = Query(None),
    tenant: Optional[str] = Query(None),
):
    """
    Quick redirect registration (hierarchy pattern).

    Example: /api/v1/csourceRegistrations/quick/redirect?entity_type=Animal&endpoint=http://farmer:1026
    """
    try:
        orion_response = await context_source_service.register_redirect(
            entity_type=entity_type,
            endpoint=endpoint,
            description=description,
            tenant=tenant,
        )

        response.headers["Location"] = orion_response.headers.get("Location", "")
        registration_id = orion_response.headers.get("Location", "").split("/")[-1]

        return {"message": "Redirect registration created", "id": registration_id}

    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code, detail=e.response.json()
        )


@router.post("/quick/federation", status_code=status.HTTP_201_CREATED)
async def quick_federation_registration(
    response: Response,
    entity_type: str = Query(..., description="Entity type to federate"),
    endpoint: str = Query(..., description="Federation endpoint"),
    description: Optional[str] = Query(None),
    tenant: Optional[str] = Query(None),
):
    """
    Quick federation registration (inclusive pattern).

    Example: /api/v1/csourceRegistrations/quick/federation?entity_type=Animal&endpoint=http://vet:1026
    """
    try:
        orion_response = await context_source_service.register_federation(
            entity_type=entity_type,
            endpoint=endpoint,
            description=description,
            tenant=tenant,
        )

        response.headers["Location"] = orion_response.headers.get("Location", "")
        registration_id = orion_response.headers.get("Location", "").split("/")[-1]

        return {"message": "Federation registration created", "id": registration_id}

    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code, detail=e.response.json()
        )


@router.post("/quick/device", status_code=status.HTTP_201_CREATED)
async def quick_device_registration(
    response: Response,
    entity_id: str = Query(..., description="Device entity ID"),
    entity_type: str = Query(..., description="Entity type"),
    properties: str = Query(..., description="Comma-separated property names"),
    iot_agent: str = Query(..., description="IoT Agent endpoint"),
    description: Optional[str] = Query(None),
    tenant: Optional[str] = Query(None),
):
    """
    Quick device registration (exclusive pattern).

    Example: /api/v1/csourceRegistrations/quick/device?entity_id=urn:ngsi-ld:Animal:cow001&entity_type=Animal&properties=heartRate,location&iot_agent=http://iot-agent:4041
    """
    try:
        props_list = properties.split(",")

        orion_response = await context_source_service.register_device(
            entity_id=entity_id,
            entity_type=entity_type,
            properties=props_list,
            iot_agent_endpoint=iot_agent,
            description=description,
            tenant=tenant,
        )

        response.headers["Location"] = orion_response.headers.get("Location", "")
        registration_id = orion_response.headers.get("Location", "").split("/")[-1]

        return {"message": "Device registration created", "id": registration_id}

    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code, detail=e.response.json()
        )
