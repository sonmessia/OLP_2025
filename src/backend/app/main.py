from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routers.air_quality_router import router as air_quality_router
from app.api.routers.building_router import router as building_router
from app.api.routers.carbon_footprint_router import (
    router as carbon_footprint_router,
)
from app.api.routers.context_source_router import (
    router as context_source_router,
)
from app.api.routers.device_router import router as device_router
from app.api.routers.road_segment_router import router as road_segment_router
from app.api.routers.subscription_router import router as subscription_router
from app.api.routers.traffic_environment_impact_router import (
    router as traffic_environment_impact_router,
)
from app.api.routers.traffic_flow_router import router as traffic_flow_router
from app.api.routers.traffic_light_router import router as traffic_light_router
from app.api.routers.water_quality_router import router as water_quality_router
from app.api.routers.sumo_control_router import router as sumo_control_router

app = FastAPI(
    title="GreenWave Core Backend Service",
    description="Receives NGSI-LD notifications and handles business logic.",
    version="1.0.0",
)

# Enable CORS for Dashboard support
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(air_quality_router)
app.include_router(carbon_footprint_router)
app.include_router(traffic_environment_impact_router)
app.include_router(traffic_flow_router)
app.include_router(water_quality_router)
app.include_router(device_router)
app.include_router(building_router)
app.include_router(subscription_router)
app.include_router(context_source_router)
app.include_router(road_segment_router)
app.include_router(traffic_light_router)  # SUMO RL Integration
app.include_router(sumo_control_router)  # SUMO Control & Real-time Data


@app.get("/")
def read_root():
    """Endpoint cơ bản để kiểm tra service có đang chạy không"""
    return {"message": "Core Backend Service is running!"}
