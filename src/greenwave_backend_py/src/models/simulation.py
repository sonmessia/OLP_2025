"""
Data models for simulation
"""
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class VehicleData(BaseModel):
    """Vehicle data model"""
    id: str
    lat: float
    lon: float
    angle: float
    speed: float
    type: Optional[str] = None


class TrafficLightState(BaseModel):
    """Traffic light state model"""
    id: str
    state: str
    phase: int
    program: str = "default"


class TrafficFlowData(BaseModel):
    """Traffic flow data model"""
    queues: List[int]
    phase: int
    timestamp: int


class AirQualityData(BaseModel):
    """Air quality data model"""
    pm25: float
    timestamp: int


class SimulationState(BaseModel):
    """Complete simulation state"""
    vehicles: List[VehicleData] = []
    traffic_lights: List[TrafficLightState] = []
    traffic_flow: TrafficFlowData
    air_quality: AirQualityData
    reward: Optional[float] = None


class WebSocketMessage(BaseModel):
    """WebSocket message model"""
    type: str  # 'simulation_update', 'command', 'error', 'connection'
    data: dict
    timestamp: int


class CommandRequest(BaseModel):
    """Command request model"""
    phase: int
