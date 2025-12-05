#!/usr/bin/env python3
"""
Unified script to generate synthetic data for all GreenWave environmental models.

Based on generate_synthetic_carbon_footprint.py pattern
Creates NGSI-LD compatible entities for:
- TrafficEnvironmentImpact
- AirQualityObserved
- CarbonFootprint
- WaterQualityObserved

Usage:
    python generate_all_synthetic_data.py --model air-quality
    python generate_all_synthetic_data.py --model all
    python generate_all_synthetic_data.py --model traffic-impact --count 3
"""

import argparse
import asyncio
import signal
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

# Add parent directory to Python path so we can import app modules
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import services
from app.services.air_quality_service import AirQualityService
from app.services.carbon_footprint_service import CarbonFootprintService
from app.services.traffic_enviroment_impact_service import (
    TrafficEnvironmentImpactService,
)
from app.services.water_quality_service import WaterQualityService


class SyntheticDataGenerator:
    """Generate synthetic NGSI-LD entities for all environmental models."""

    def __init__(self, seed: int = 42):
        """Initialize generator with seed for reproducible results."""
        self.seed = seed
        self.entity_counter = {
            "TrafficEnvironmentImpact": 0,
            "AirQualityObserved": 0,
            "CarbonFootprint": 0,
            "WaterQualityObserved": 0,
        }
        self.locations = {
            "Madrid": [-3.703790, 40.416775],
            "Barcelona": [2.183333, 41.383333],
            "Valencia": [-0.375823, 39.469907],
            "Seville": [-5.984459, 37.389092],
            "Bilbao": [-2.923441, 43.263012],
        }

    def _get_entity_id(self, model_type: str, location: str, suffix: str = "") -> str:
        """Generate unique entity ID following NGSI-LD pattern."""
        self.entity_counter[model_type] += 1
        counter = self.entity_counter[model_type]
        location_clean = location.replace(" ", "-")
        return f"urn:ngsi-ld:{model_type}:{location_clean}-{counter:03d}{suffix}"

    def _get_timestamp(self) -> str:
        """Get current ISO 8601 timestamp."""
        return datetime.now(timezone.utc).isoformat()

    def generate_traffic_entities(self, count: int = 5) -> List[Dict[str, Any]]:
        """Generate TrafficEnvironmentImpact entities."""
        entities = []
        current_time = self._get_timestamp()

        traffic_scenarios = [
            {
                "location": "Madrid Highway",
                "description": "High traffic intensity on Madrid's main highway",
                "co2_range": (450, 520),
                "intensity": 0.85,
                "vehicle_types": ["passenger_car", "heavy_truck"],
            },
            {
                "location": "Barcelona Coastal",
                "description": "Moderate traffic flow in Barcelona coastal area",
                "co2_range": (340, 400),
                "intensity": 0.72,
                "vehicle_types": ["passenger_car", "motorcycle"],
            },
            {
                "location": "Valencia Industrial",
                "description": "Heavy industrial traffic in Valencia's manufacturing zone",
                "co2_range": (500, 580),
                "intensity": 0.90,
                "vehicle_types": ["heavy_truck", "van"],
            },
            {
                "location": "Seville Residential",
                "description": "Light residential traffic in Seville suburbs",
                "co2_range": (280, 350),
                "intensity": 0.45,
                "vehicle_types": ["passenger_car", "bicycle"],
            },
            {
                "location": "Bilbao Green Zone",
                "description": "Eco-friendly traffic in Bilbao green zone",
                "co2_range": (250, 320),
                "intensity": 0.35,
                "vehicle_types": ["electric_vehicle", "bicycle", "pedestrian"],
            },
        ]

        for i in range(min(count, len(traffic_scenarios))):
            scenario = traffic_scenarios[i]
            coords = self.locations.get(scenario["location"].split()[0], [0, 0])

            co2_value = scenario["co2_range"][0] + (i * 10)

            entity = {
                "id": self._get_entity_id(
                    "TrafficEnvironmentImpact", scenario["location"], "-T"
                ),
                "type": "TrafficEnvironmentImpact",
                "dateObservedFrom": {
                    "type": "Property",
                    "value": {"@type": "DateTime", "@value": current_time},
                },
                "dateObservedTo": {
                    "type": "Property",
                    "value": {"@type": "DateTime", "@value": current_time},
                },
                "name": {
                    "type": "Property",
                    "value": f"{scenario['location']} Traffic Monitor",
                },
                "description": {"type": "Property", "value": scenario["description"]},
                "location": {
                    "type": "GeoProperty",
                    "value": {"type": "Point", "coordinates": coords},
                },
                "address": {
                    "type": "Property",
                    "value": {
                        "addressCountry": "Spain",
                        "addressLocality": scenario["location"].split()[0],
                    },
                },
                "areaServed": {"type": "Property", "value": scenario["location"]},
                "co2": {"type": "Property", "value": co2_value, "unitCode": "GQ"},
                "dataProvider": {
                    "type": "Property",
                    "value": "GreenWave Traffic Monitor",
                },
                "source": {
                    "type": "Property",
                    "value": "https://github.com/greenwave/traffic-monitor",
                },
                "refTrafficFlowObserved": {
                    "type": "Relationship",
                    "object": f"urn:ngsi-ld:TrafficFlowObserved:{scenario['location'].replace(' ', '-')}-{i}",
                },
                "vehicleClass": {
                    "type": "Property",
                    "value": scenario["vehicle_types"][0],
                },
                "intensity": {"type": "Property", "value": scenario["intensity"]},
                "averageSpeed": {
                    "type": "Property",
                    "value": 30 + (i * 5),
                    "unitCode": "KMH",
                },
                "occupancy": {"type": "Property", "value": scenario["intensity"] * 0.6},
            }
            entities.append(entity)

        return entities

    def generate_air_quality_entities(self, count: int = 5) -> List[Dict[str, Any]]:
        """Generate AirQualityObserved entities."""
        entities = []
        current_time = self._get_timestamp()

        air_quality_scenarios = [
            {
                "location": "Madrid City Center",
                "description": "Urban air quality monitoring in Madrid downtown",
                "aqi": 75,
                "level": "Moderate",
                "pollution_factor": 0.6,
            },
            {
                "location": "Barcelona Coastal",
                "description": "Coastal air quality monitoring in Barcelona",
                "aqi": 55,
                "level": "Fair",
                "pollution_factor": 0.4,
            },
            {
                "location": "Valencia Industrial",
                "description": "Industrial air quality monitoring in Valencia",
                "aqi": 125,
                "level": "Unhealthy for Sensitive Groups",
                "pollution_factor": 0.8,
            },
            {
                "location": "Seville Residential",
                "description": "Residential air quality monitoring in Seville",
                "aqi": 35,
                "level": "Good",
                "pollution_factor": 0.2,
            },
            {
                "location": "Bilbao Park",
                "description": "Green zone air quality monitoring in Bilbao park",
                "aqi": 18,
                "level": "Excellent",
                "pollution_factor": 0.1,
            },
        ]

        for i in range(min(count, len(air_quality_scenarios))):
            scenario = air_quality_scenarios[i]
            coords = self.locations.get(scenario["location"].split()[0], [0, 0])
            factor = scenario["pollution_factor"]

            entity = {
                "id": self._get_entity_id(
                    "AirQualityObserved", scenario["location"], "-AQ"
                ),
                "type": "AirQualityObserved",
                "dateObserved": {
                    "type": "Property",
                    "value": {"@type": "DateTime", "@value": current_time},
                },
                "name": {
                    "type": "Property",
                    "value": f"{scenario['location']} Air Quality Station",
                },
                "description": {"type": "Property", "value": scenario["description"]},
                "location": {
                    "type": "GeoProperty",
                    "value": {"type": "Point", "coordinates": coords},
                },
                "address": {
                    "type": "Property",
                    "value": {
                        "addressCountry": "Spain",
                        "addressLocality": scenario["location"].split()[0],
                    },
                },
                "areaServed": {"type": "Property", "value": scenario["location"]},
                "typeofLocation": {"type": "Property", "value": "outdoor"},
                "airQualityIndex": {
                    "type": "Property",
                    "value": scenario["aqi"],
                    "unitCode": "C62",
                },
                "airQualityLevel": {"type": "Property", "value": scenario["level"]},
                "pm25": {
                    "type": "Property",
                    "value": round(factor * 35 + (i * 2), 2),
                    "unitCode": "GQ",
                },
                "pm10": {
                    "type": "Property",
                    "value": round(factor * 50 + (i * 3), 2),
                    "unitCode": "GQ",
                },
                "no2": {
                    "type": "Property",
                    "value": round(factor * 40 + (i * 5), 2),
                    "unitCode": "GQ",
                },
                "o3": {
                    "type": "Property",
                    "value": round(factor * 60 + (i * 4), 2),
                    "unitCode": "GQ",
                },
                "co": {
                    "type": "Property",
                    "value": round(factor * 2 + (i * 0.1), 2),
                    "unitCode": "GP",
                },
                "so2": {
                    "type": "Property",
                    "value": round(factor * 10 + (i * 2), 2),
                    "unitCode": "GQ",
                },
                "co2": {
                    "type": "Property",
                    "value": round(400 + factor * 100 + (i * 10), 2),
                    "unitCode": "GQ",
                },
                "temperature": {
                    "type": "Property",
                    "value": round(20 + (i * 2), 1),
                    "unitCode": "CEL",
                },
                "relativeHumidity": {
                    "type": "Property",
                    "value": round(0.5 + (i * 0.05), 3),
                },
                "windSpeed": {
                    "type": "Property",
                    "value": round(3 + (i * 1), 1),
                    "unitCode": "MTS",
                },
                "windDirection": {
                    "type": "Property",
                    "value": round(i * 45, 1),
                    "unitCode": "DD",
                },
                "refAirQualityStation": {
                    "type": "Relationship",
                    "object": f"urn:ngsi-ld:AirQualityStation:{scenario['location'].replace(' ', '-')}-{i}",
                },
                "dataProvider": {
                    "type": "Property",
                    "value": "GreenWave Air Quality Monitor",
                },
                "source": {
                    "type": "Property",
                    "value": "https://github.com/greenwave/air-quality-monitor",
                },
            }
            entities.append(entity)

        return entities

    def generate_carbon_entities(self, count: int = 5) -> List[Dict[str, Any]]:
        """Generate CarbonFootprint entities."""
        entities = []
        current_time = self._get_timestamp()

        carbon_scenarios = [
            {
                "location": "Madrid Industrial",
                "description": "Industrial carbon emissions monitoring in Madrid",
                "source": "Industry",
                "co2eq": 158.7,
                "tags": ["industrial", "manufacturing", "heavy"],
            },
            {
                "location": "Barcelona Transport",
                "description": "Transport sector carbon monitoring at Barcelona hub",
                "source": "Transport",
                "co2eq": 87.4,
                "tags": ["urban", "transport", "medium"],
            },
            {
                "location": "Valencia Agriculture",
                "description": "Agricultural carbon emissions monitoring in Valencia",
                "source": "Agriculture",
                "co2eq": 34.2,
                "tags": ["rural", "agriculture", "low"],
            },
            {
                "location": "Seville Residential",
                "description": "Residential carbon monitoring in Seville suburbs",
                "source": "Residential",
                "co2eq": 58.9,
                "tags": ["suburban", "residential", "low-medium"],
            },
            {
                "location": "Bilbao Commercial",
                "description": "Commercial carbon monitoring in Bilbao shopping district",
                "source": "Commercial",
                "co2eq": 76.5,
                "tags": ["urban", "commercial", "medium"],
            },
        ]

        for i in range(min(count, len(carbon_scenarios))):
            scenario = carbon_scenarios[i]
            coords = self.locations.get(scenario["location"].split()[0], [0, 0])

            entity = {
                "id": self._get_entity_id(
                    "CarbonFootprint", scenario["location"], "-CF"
                ),
                "type": "CarbonFootprint",
                "dateCreated": {
                    "type": "Property",
                    "value": {"@type": "DateTime", "@value": current_time},
                },
                "dateModified": {
                    "type": "Property",
                    "value": {"@type": "DateTime", "@value": current_time},
                },
                "emissionDate": {
                    "type": "Property",
                    "value": {"@type": "DateTime", "@value": current_time},
                },
                "name": {
                    "type": "Property",
                    "value": f"{scenario['location']} Carbon Monitor",
                },
                "description": {"type": "Property", "value": scenario["description"]},
                "location": {
                    "type": "GeoProperty",
                    "value": {"type": "Point", "coordinates": coords},
                },
                "address": {
                    "type": "Property",
                    "value": {
                        "addressCountry": "Spain",
                        "addressLocality": scenario["location"].split()[0],
                    },
                },
                "areaServed": {"type": "Property", "value": scenario["location"]},
                "CO2eq": {
                    "type": "Property",
                    "value": scenario["co2eq"],
                    "unitCode": "KGM",
                },
                "emissionSource": {"type": "Property", "value": scenario["source"]},
                "dataProvider": {
                    "type": "Property",
                    "value": "GreenWave Carbon Monitor",
                },
                "source": {
                    "type": "Property",
                    "value": "https://github.com/greenwave/carbon-monitor",
                },
                "tags": {"type": "Property", "value": scenario["tags"]},
                "relatedSource": {
                    "type": "Relationship",
                    "object": f"urn:ngsi-ld:{scenario['source']}:{scenario['location'].replace(' ', '-')}-001",
                },
            }
            entities.append(entity)

        return entities

    def generate_water_entities(self, count: int = 5) -> List[Dict[str, Any]]:
        """Generate WaterQualityObserved entities."""
        entities = []
        current_time = self._get_timestamp()

        water_scenarios = [
            {
                "location": "Madrid River",
                "description": "River water quality monitoring in Madrid's Manzanares",
                "quality": "Poor",
                "temp": 18.7,
                "ph": 7.8,
                "do": 4.2,
            },
            {
                "location": "Barcelona Coastal",
                "description": "Coastal water quality monitoring at Barcelona beach",
                "quality": "Good",
                "temp": 22.5,
                "ph": 8.1,
                "do": 7.8,
            },
            {
                "location": "Valencia Reservoir",
                "description": "Freshwater reservoir quality monitoring in Valencia",
                "quality": "Moderate",
                "temp": 16.5,
                "ph": 7.5,
                "do": 6.8,
            },
            {
                "location": "Seville River",
                "description": "River water quality monitoring in Seville's Guadalquivir",
                "quality": "Fair",
                "temp": 21.5,
                "ph": 7.9,
                "do": 5.8,
            },
            {
                "location": "Bilbao Lake",
                "description": "Lake water quality monitoring in Bilbao's urban park",
                "quality": "Excellent",
                "temp": 14.5,
                "ph": 7.2,
                "do": 8.5,
            },
        ]

        for i in range(min(count, len(water_scenarios))):
            scenario = water_scenarios[i]
            coords = self.locations.get(scenario["location"].split()[0], [0, 0])

            # Quality factor for contaminant levels
            quality_factor = {
                "Excellent": 0.1,
                "Good": 0.3,
                "Fair": 0.5,
                "Moderate": 0.7,
                "Poor": 0.9,
            }[scenario["quality"]]

            entity = {
                "id": self._get_entity_id(
                    "WaterQualityObserved", scenario["location"], "-WQ"
                ),
                "type": "WaterQualityObserved",
                "dateObserved": {
                    "type": "Property",
                    "value": {"@type": "DateTime", "@value": current_time},
                },
                "name": {
                    "type": "Property",
                    "value": f"{scenario['location']} Water Station",
                },
                "description": {"type": "Property", "value": scenario["description"]},
                "location": {
                    "type": "GeoProperty",
                    "value": {"type": "Point", "coordinates": coords},
                },
                "address": {
                    "type": "Property",
                    "value": {
                        "addressCountry": "Spain",
                        "addressLocality": scenario["location"].split()[0],
                    },
                },
                "areaServed": {"type": "Property", "value": scenario["location"]},
                "temperature": {
                    "type": "Property",
                    "value": scenario["temp"],
                    "unitCode": "CEL",
                },
                "pH": {"type": "Property", "value": scenario["ph"], "unitCode": "C62"},
                "dissolvedOxygen": {
                    "type": "Property",
                    "value": scenario["do"],
                    "unitCode": "GQ",
                },
                "conductivity": {
                    "type": "Property",
                    "value": round(200 + quality_factor * 800, 1),
                    "unitCode": "C62",
                },
                "turbidity": {
                    "type": "Property",
                    "value": round(quality_factor * 20 + (i * 2), 1),
                    "unitCode": "NTU",
                },
                "alkalinity": {
                    "type": "Property",
                    "value": round(100 + (i * 10), 1),
                    "unitCode": "GQ",
                },
                "nitrates": {
                    "type": "Property",
                    "value": round(quality_factor * 10 + (i * 0.5), 2),
                    "unitCode": "GQ",
                },
                "phosphates": {
                    "type": "Property",
                    "value": round(quality_factor * 2 + (i * 0.2), 2),
                    "unitCode": "GQ",
                },
                "ammonia": {
                    "type": "Property",
                    "value": round(quality_factor * 1.5 + (i * 0.1), 2),
                    "unitCode": "GQ",
                },
                "lead": {
                    "type": "Property",
                    "value": round(quality_factor * 5 + (i * 0.5), 3),
                    "unitCode": "GQ",
                },
                "mercury": {
                    "type": "Property",
                    "value": round(quality_factor * 0.5 + (i * 0.02), 3),
                    "unitCode": "GQ",
                },
                "cadmium": {
                    "type": "Property",
                    "value": round(quality_factor * 1 + (i * 0.1), 3),
                    "unitCode": "GQ",
                },
                "arsenic": {
                    "type": "Property",
                    "value": round(quality_factor * 3 + (i * 0.3), 3),
                    "unitCode": "GQ",
                },
                "bod": {
                    "type": "Property",
                    "value": round(quality_factor * 8 + (i * 1), 1),
                    "unitCode": "GQ",
                },
                "cod": {
                    "type": "Property",
                    "value": round(quality_factor * 25 + (i * 3), 1),
                    "unitCode": "GQ",
                },
                "chlorides": {
                    "type": "Property",
                    "value": round(20 + (i * 8), 1),
                    "unitCode": "GQ",
                },
                "sulfates": {
                    "type": "Property",
                    "value": round(30 + (i * 10), 1),
                    "unitCode": "GQ",
                },
                "totalSuspendedSolids": {
                    "type": "Property",
                    "value": round(quality_factor * 25 + (i * 5), 1),
                    "unitCode": "GQ",
                },
                "measurand": {
                    "type": "Property",
                    "value": ["pH", "temperature", "dissolvedOxygen", "nitrates"],
                },
                "dataProvider": {
                    "type": "Property",
                    "value": "GreenWave Water Monitor",
                },
                "source": {
                    "type": "Property",
                    "value": "https://github.com/greenwave/water-monitor",
                },
                "refPointOfInterest": {
                    "type": "Relationship",
                    "object": f"urn:ngsi-ld:WaterPoint:{scenario['location'].replace(' ', '-')}-001",
                },
            }
            entities.append(entity)

        return entities


async def create_entities_batch(entities: List[Dict[str, Any]], service_name: str):
    """Create entities using batch operation for specified service."""
    print(f"🚀 Creating {len(entities)} {service_name} entities via batch operation...")
    print(f"⏰ Timestamp: {datetime.now(timezone.utc).isoformat()}\n")

    service_map = {
        "TrafficEnvironmentImpact": TrafficEnvironmentImpactService,
        "AirQualityObserved": AirQualityService,
        "CarbonFootprint": CarbonFootprintService,
        "WaterQualityObserved": WaterQualityService,
    }

    service_class = service_map.get(service_name)
    if not service_class:
        print(f"❌ Unknown service: {service_name}")
        return

    async with service_class() as service:
        try:
            response = await service.batch_create(entities)
            print("✅ Batch create successful!")
            print(f"   Status: {response.status_code}")

            if response.content:
                result = response.json()
                if "success" in result and result["success"]:
                    print(
                        f"   ✅ Successfully created: {len(result['success'])} entities"
                    )
                    for entity_id in result["success"]:
                        print(f"      - {entity_id}")

                if "errors" in result and result["errors"]:
                    print(f"   ❌ Errors: {len(result['errors'])}")
                    for error in result["errors"]:
                        print(f"      - {error['entityId']}: {error['error']['title']}")

            # Show summary
            print(f"\n📊 {service_name} entities created:")
            for i, entity in enumerate(entities, 1):
                name = entity.get("name", {}).get("value", "N/A")
                print(f"   {i}. {name}")
                print(f"      ID: {entity['id']}")

                # Show key fields based on entity type
                if service_name == "TrafficEnvironmentImpact":
                    co2 = entity.get("co2", {}).get("value", "N/A")
                    intensity = entity.get("intensity", {}).get("value", "N/A")
                    avg_speed = entity.get("averageSpeed", {}).get("value", "N/A")
                    print(
                        f"      CO2: {co2} ppm, Intensity: {intensity}, Avg Speed: {avg_speed} km/h"
                    )
                elif service_name == "AirQualityObserved":
                    aqi = entity.get("airQualityIndex", {}).get("value", "N/A")
                    level = entity.get("airQualityLevel", {}).get("value", "N/A")
                    pm25 = entity.get("pm25", {}).get("value", "N/A")
                    print(f"      AQI: {aqi} ({level}), PM2.5: {pm25} µg/m³")
                elif service_name == "CarbonFootprint":
                    co2eq = entity.get("CO2eq", {}).get("value", "N/A")
                    source = entity.get("emissionSource", {}).get("value", "N/A")
                    tags = entity.get("tags", {}).get("value", [])
                    print(
                        f"      CO2eq: {co2eq} kg/h from {source}, Tags: {', '.join(tags)}"
                    )
                elif service_name == "WaterQualityObserved":
                    temp = entity.get("temperature", {}).get("value", "N/A")
                    ph = entity.get("pH", {}).get("value", "N/A")
                    do = entity.get("dissolvedOxygen", {}).get("value", "N/A")
                    turbidity = entity.get("turbidity", {}).get("value", "N/A")
                    print(
                        f"      Temperature: {temp}°C, pH: {ph}, DO: {do} mg/L, Turbidity: {turbidity} NTU"
                    )
                print()

        except Exception as e:
            print(f"❌ Batch create failed: {str(e)}")
            import traceback

            traceback.print_exc()


async def verify_entities(service_name: str, limit: int = 10):
    """Verify that entities were created for specified service."""
    print(f"\n🔍 Verifying {service_name} entities...")

    service_map = {
        "TrafficEnvironmentImpact": TrafficEnvironmentImpactService,
        "AirQualityObserved": AirQualityService,
        "CarbonFootprint": CarbonFootprintService,
        "WaterQualityObserved": WaterQualityService,
    }

    service_class = service_map.get(service_name)
    if not service_class:
        print(f"❌ Unknown service: {service_name}")
        return

    async with service_class() as service:
        try:
            entities = await service.get_all(
                limit=limit, format="simplified", pick="id,name"
            )

            if isinstance(entities, int):
                print(f"✅ Found {entities} {service_name} entities total\n")
                return

            for entity in entities:
                print(f"   📍 {entity.get('name', 'N/A')}")
                print(f"      ID: {entity['id']}")
                print()

        except Exception as e:
            print(f"❌ Verification failed: {str(e)}")


def handle_signal(signum: int, frame) -> None:
    """Handle shutdown signals gracefully."""
    print(f"\n\n⚠️  Received signal {signum}. Shutting down gracefully...")
    sys.exit(0)


async def continuous_generation(generator, models_to_process, interval_seconds):
    """Generate synthetic data continuously at specified intervals."""
    print(f"🚀 Starting continuous generation every {interval_seconds} second(s)")
    print("Press Ctrl+C to stop gracefully")
    print("=" * 80)

    try:
        while True:
            start_time = time.time()

            # Generate data for all configured models
            all_entities = {}
            for model_name, generate_func in models_to_process:
                print(f"\n🌍 Generating {model_name} data...")
                entities = generate_func(1)  # Generate 1 entity per model per cycle
                all_entities[model_name] = entities

                # Save to database
                try:
                    await create_entities_batch(entities, model_name)
                except Exception as e:
                    print(f"❌ Failed to save {model_name}: {e}")

            # Display summary
            timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
            print(f"\n{'='*80}")
            print(f"🌍 GreenWave Continuous Data Generation - {timestamp}")
            print(f"{'='*80}")

            for model_name, entities in all_entities.items():
                print(f"\n📊 {model_name}: {len(entities)} entities generated")

                # Show key metrics for each entity type
                for _i, entity in enumerate(
                    entities[:1], 1
                ):  # Show first entity details
                    if model_name == "TrafficEnvironmentImpact":
                        co2 = entity.get("co2", {}).get("value", "N/A")
                        intensity = entity.get("intensity", {}).get("value", "N/A")
                        print(f"   CO2: {co2} ppm, Intensity: {intensity}")
                    elif model_name == "AirQualityObserved":
                        aqi = entity.get("airQualityIndex", {}).get("value", "N/A")
                        pm25 = entity.get("pm25", {}).get("value", "N/A")
                        print(f"   AQI: {aqi}, PM2.5: {pm25} µg/m³")
                    elif model_name == "CarbonFootprint":
                        co2eq = entity.get("CO2eq", {}).get("value", "N/A")
                        source = entity.get("emissionSource", {}).get("value", "N/A")
                        print(f"   CO2eq: {co2eq} kg/h from {source}")
                    elif model_name == "WaterQualityObserved":
                        temp = entity.get("temperature", {}).get("value", "N/A")
                        ph = entity.get("pH", {}).get("value", "N/A")
                        do = entity.get("dissolvedOxygen", {}).get("value", "N/A")
                        print(f"   Temp: {temp}°C, pH: {ph}, DO: {do} mg/L")

            # Calculate sleep time to maintain consistent interval
            elapsed = time.time() - start_time
            sleep_time = max(0, interval_seconds - elapsed)

            if sleep_time > 0:
                print(f"\n⏰ Waiting {sleep_time:.1f}s before next generation...")
                time.sleep(sleep_time)
            else:
                print(f"\n⚠️ Generation took {elapsed:.1f}s, running immediately...")

    except KeyboardInterrupt:
        print("\n\n🛑 Continuous generation stopped gracefully")
        return


async def main():
    parser = argparse.ArgumentParser(
        description="Generate synthetic NGSI-LD entities for GreenWave models"
    )
    parser.add_argument(
        "--model",
        choices=[
            "traffic-impact",
            "air-quality",
            "carbon-footprint",
            "water-quality",
            "all",
        ],
        default="all",
        help="Specify which model to generate data for (default: all)",
    )
    parser.add_argument(
        "--count",
        type=int,
        default=5,
        help="Number of entities to generate per model (default: 5)",
    )
    parser.add_argument(
        "--verify", action="store_true", help="Verify created entities after generation"
    )
    parser.add_argument(
        "--continuous",
        action="store_true",
        help="Generate data continuously every second",
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=1,
        help="Generation interval in seconds for continuous mode (default: 1)",
    )

    args = parser.parse_args()

    # Set up signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)

    print("=" * 80)
    print("  GreenWave Synthetic Data Generator")
    print("  NGSI-LD Compatible Entity Creation")
    print("  Author: GreenWave Team")
    print(f"  Date: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print("=" * 80)
    print()

    generator = SyntheticDataGenerator()

    model_mapping = {
        "traffic-impact": (
            "TrafficEnvironmentImpact",
            generator.generate_traffic_entities,
        ),
        "air-quality": ("AirQualityObserved", generator.generate_air_quality_entities),
        "carbon-footprint": ("CarbonFootprint", generator.generate_carbon_entities),
        "water-quality": ("WaterQualityObserved", generator.generate_water_entities),
    }

    if args.model == "all":
        models_to_process = [
            (model_name, func) for model_name, func in model_mapping.values()
        ]
    else:
        model_name, generate_func = model_mapping[args.model]
        models_to_process = [(model_name, generate_func)]

    # Handle continuous vs batch mode
    if args.continuous:
        await continuous_generation(generator, models_to_process, args.interval)
    else:
        # Original batch mode
        for model_name, generate_func in models_to_process:
            print(f"🌍 Processing {model_name} entities...")
            entities = generate_func(args.count)
            await create_entities_batch(entities, model_name)

            if args.verify:
                await verify_entities(model_name)

        print("\n✨ Generation complete!")


if __name__ == "__main__":
    asyncio.run(main())
