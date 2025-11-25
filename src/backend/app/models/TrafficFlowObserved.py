from __future__ import annotations

from typing import List, Optional, Union

from pydantic import AnyUrl, AwareDatetime, BaseModel, Field


class TrafficFlowObserved(BaseModel):
    """Minimal TrafficFlowObserved model for SUMO-derived traffic metrics.

    This model is intentionally small and focuses on the attributes produced by
    the SUMO simulation used in the project: queues, vehicleCount and avgSpeed.
    """

    id: Optional[Union[str, AnyUrl]] = Field(None, description="Unique identifier")
    type: Optional[str] = Field(None, description="NGSI Entity type (TrafficFlowObserved)")
    dateObservedFrom: Optional[AwareDatetime] = Field(None, description="Observation start time")
    dateObservedTo: Optional[AwareDatetime] = Field(None, description="Observation end time")
    queues: Optional[List[int]] = Field(None, description="Queue lengths per lane/direction")
    vehicleCount: Optional[int] = Field(None, description="Total vehicles observed", ge=0)
    avgSpeed: Optional[float] = Field(None, description="Average speed in m/s", ge=0.0)
    refRoadSegment: Optional[Union[str, AnyUrl]] = Field(None, description="Reference to RoadSegment entity")

    class Config:
        schema_extra = {
            "example": {
                "id": "urn:ngsi-ld:TrafficFlowObserved:4066470692",
                "type": "TrafficFlowObserved",
                "dateObservedFrom": "2025-11-24T10:00:00Z",
                "dateObservedTo": "2025-11-24T10:01:00Z",
                "queues": [0, 1],
                "vehicleCount": 3,
                "avgSpeed": 5.2,
                "refRoadSegment": "urn:ngsi-ld:RoadSegment:4066470692",
            }
        }
