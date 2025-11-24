"""
Service for interacting with Orion Context Broker (NGSI-LD)
"""
import httpx
from typing import Optional, Dict, Any
import logging

from ..models.simulation import TrafficFlowData, AirQualityData

logger = logging.getLogger(__name__)


class OrionService:
    """Orion Context Broker service"""
    
    def __init__(self, orion_url: str):
        self.base_url = orion_url
        self.client = httpx.AsyncClient(
            base_url=orion_url,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json"
            },
            timeout=10.0
        )
    
    async def get_traffic_flow(self, tls_id: str) -> Optional[TrafficFlowData]:
        """Get traffic flow data from Orion"""
        try:
            response = await self.client.get(
                f"/entities/urn:ngsi-ld:TrafficFlowObserved:{tls_id}"
            )
            
            if response.status_code == 200:
                entity = response.json()
                return TrafficFlowData(
                    queues=entity.get("queues", {}).get("value", [0, 0]),
                    phase=entity.get("phase", {}).get("value", 0),
                    timestamp=int(entity.get("timestamp", 0))
                )
            else:
                logger.warning(f"Failed to get traffic flow: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Error fetching traffic flow: {e}")
            return None
    
    async def get_air_quality(self, tls_id: str) -> Optional[AirQualityData]:
        """Get air quality data from Orion"""
        try:
            response = await self.client.get(
                f"/entities/urn:ngsi-ld:AirQualityObserved:{tls_id}"
            )
            
            if response.status_code == 200:
                entity = response.json()
                return AirQualityData(
                    pm25=entity.get("pm25", {}).get("value", 0.0),
                    timestamp=int(entity.get("timestamp", 0))
                )
            else:
                logger.warning(f"Failed to get air quality: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Error fetching air quality: {e}")
            return None
    
    async def set_traffic_light_phase(self, tls_id: str, phase: int) -> bool:
        """Send phase change command to traffic light"""
        try:
            response = await self.client.patch(
                f"/entities/urn:ngsi-ld:TrafficLight:{tls_id}/attrs",
                json={
                    "forcePhase": {
                        "type": "Property",
                        "value": phase
                    }
                }
            )
            
            if response.status_code in [200, 204]:
                logger.info(f"Set traffic light {tls_id} to phase {phase}")
                return True
            else:
                logger.error(f"Failed to set phase: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"Error setting traffic light phase: {e}")
            return False
    
    async def get_entity(self, entity_id: str) -> Optional[Dict[str, Any]]:
        """Get entity by ID"""
        try:
            response = await self.client.get(f"/entities/{entity_id}")
            
            if response.status_code == 200:
                return response.json()
            else:
                return None
                
        except Exception as e:
            logger.error(f"Error fetching entity {entity_id}: {e}")
            return None
    
    async def upsert_entity(self, entity: Dict[str, Any]) -> bool:
        """Create or update entity"""
        try:
            entity_id = entity.get("id")
            entity_type = entity.get("type")
            attrs = {k: v for k, v in entity.items() if k not in ["id", "type"]}
            
            # Try to update first
            response = await self.client.patch(
                f"/entities/{entity_id}/attrs",
                json=attrs
            )
            
            if response.status_code == 404:
                # Entity doesn't exist, create it
                response = await self.client.post(
                    "/entities",
                    json=entity
                )
            
            return response.status_code in [200, 201, 204]
            
        except Exception as e:
            logger.error(f"Error upserting entity: {e}")
            return False
    
    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()
