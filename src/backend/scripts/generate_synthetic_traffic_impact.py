#!/usr/bin/env python3
# Copyright (c) 2025 Green Wave Team
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

"""
Script to generate synthetic TrafficEnvironmentImpact entities for testing.

Based on create_air_quality_samples.py pattern
Generates realistic traffic impact data with NGSI-LD format
"""

import asyncio
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

# Add parent directory to Python path so we can import app modules
sys.path.insert(0, str(Path(__file__).parent.parent))
# Import services
from app.services.traffic_enviroment_impact_service import (
    TrafficEnvironmentImpactService,
)


def generate_sample_traffic_entities() -> List[Dict[str, Any]]:
    """
    Generate 5 diverse TrafficEnvironmentImpact entities.

    ⚠️ IMPORTANT: For batch operations, we need to send FULL NGSI-LD format
    but WITHOUT individual @context in each entity.
    """

    current_time = datetime.now(timezone.utc).isoformat()

    entities = [
        # 1. Madrid Highway - High traffic impact
        {
            "id": "urn:ngsi-ld:TrafficEnvironmentImpact:Madrid-Highway-001",
            "type": "TrafficEnvironmentImpact",
            "dateObservedFrom": {
                "type": "Property",
                "value": {"@type": "DateTime", "@value": current_time},
            },
            "dateObservedTo": {
                "type": "Property",
                "value": {"@type": "DateTime", "@value": current_time},
            },
            "name": {"type": "Property", "value": "Madrid A-3 Highway Station"},
            "description": {
                "type": "Property",
                "value": "Traffic environmental impact monitoring on Madrid's main highway",
            },
            "location": {
                "type": "GeoProperty",
                "value": {"type": "Point", "coordinates": [-3.578790, 40.456775]},
            },
            "address": {
                "type": "Property",
                "value": {
                    "addressCountry": "Spain",
                    "addressLocality": "Madrid",
                    "streetAddress": "Autopista A-3",
                },
            },
            "areaServed": {"type": "Property", "value": "Madrid Highway Corridor"},
            "co2": {"type": "Property", "value": 485.2, "unitCode": "GQ"},
            "dataProvider": {"type": "Property", "value": "GreenWave Traffic Monitor"},
            "source": {
                "type": "Property",
                "value": "https://github.com/greenwave/traffic-monitor",
            },
            "traffic": [
                {
                    "type": "Property",
                    "value": {
                        "vehicleClass": "passenger_car",
                        "refTrafficFlowObserved": "urn:ngsi-ld:TrafficFlowObserved:Madrid-Highway-001-PC",
                        "intensity": 0.85,
                        "averageSpeed": 45.2,
                        "occupancy": 0.78,
                    },
                },
                {
                    "type": "Property",
                    "value": {
                        "vehicleClass": "heavy_truck",
                        "refTrafficFlowObserved": "urn:ngsi-ld:TrafficFlowObserved:Madrid-Highway-001-HT",
                        "intensity": 0.15,
                        "averageSpeed": 65.8,
                        "occupancy": 0.12,
                    },
                },
            ],
        },
        # 2. Barcelona Coastal - Moderate traffic impact
        {
            "id": "urn:ngsi-ld:TrafficEnvironmentImpact:Barcelona-Coastal-002",
            "type": "TrafficEnvironmentImpact",
            "dateObservedFrom": {
                "type": "Property",
                "value": {"@type": "DateTime", "@value": current_time},
            },
            "dateObservedTo": {
                "type": "Property",
                "value": {"@type": "DateTime", "@value": current_time},
            },
            "name": {"type": "Property", "value": "Barcelona Passeig Marítim Station"},
            "description": {
                "type": "Property",
                "value": "Coastal traffic environmental impact monitoring",
            },
            "location": {
                "type": "GeoProperty",
                "value": {"type": "Point", "coordinates": [2.183333, 41.383333]},
            },
            "address": {
                "type": "Property",
                "value": {
                    "addressCountry": "Spain",
                    "addressLocality": "Barcelona",
                    "addressRegion": "Catalonia",
                    "streetAddress": "Passeig Marítim",
                },
            },
            "areaServed": {"type": "Property", "value": "Barcelona Coastal Zone"},
            "co2": {"type": "Property", "value": 358.7, "unitCode": "GQ"},
            "dataProvider": {"type": "Property", "value": "GreenWave Traffic Monitor"},
            "source": {
                "type": "Property",
                "value": "https://github.com/greenwave/traffic-monitor",
            },
            "traffic": [
                {
                    "type": "Property",
                    "value": {
                        "vehicleClass": "passenger_car",
                        "refTrafficFlowObserved": "urn:ngsi-ld:TrafficFlowObserved:Barcelona-Coastal-002-PC",
                        "intensity": 0.72,
                        "averageSpeed": 38.5,
                        "occupancy": 0.65,
                    },
                },
                {
                    "type": "Property",
                    "value": {
                        "vehicleClass": "motorcycle",
                        "refTrafficFlowObserved": "urn:ngsi-ld:TrafficFlowObserved:Barcelona-Coastal-002-MC",
                        "intensity": 0.28,
                        "averageSpeed": 42.1,
                        "occupancy": 0.18,
                    },
                },
            ],
        },
        # 3. Valencia Industrial - Very high traffic impact
        {
            "id": "urn:ngsi-ld:TrafficEnvironmentImpact:Valencia-Industrial-003",
            "type": "TrafficEnvironmentImpact",
            "dateObservedFrom": {
                "type": "Property",
                "value": {"@type": "DateTime", "@value": current_time},
            },
            "dateObservedTo": {
                "type": "Property",
                "value": {"@type": "DateTime", "@value": current_time},
            },
            "name": {"type": "Property", "value": "Valencia Industrial Zone Station"},
            "description": {
                "type": "Property",
                "value": "Industrial area traffic environmental impact monitoring",
            },
            "location": {
                "type": "GeoProperty",
                "value": {"type": "Point", "coordinates": [-0.375823, 39.469907]},
            },
            "address": {
                "type": "Property",
                "value": {
                    "addressCountry": "Spain",
                    "addressLocality": "Valencia",
                    "district": "Industrial Zone",
                },
            },
            "areaServed": {"type": "Property", "value": "Valencia Industrial District"},
            "co2": {"type": "Property", "value": 542.3, "unitCode": "GQ"},
            "dataProvider": {"type": "Property", "value": "GreenWave Traffic Monitor"},
            "source": {
                "type": "Property",
                "value": "https://github.com/greenwave/traffic-monitor",
            },
            "traffic": [
                {
                    "type": "Property",
                    "value": {
                        "vehicleClass": "heavy_truck",
                        "refTrafficFlowObserved": "urn:ngsi-ld:TrafficFlowObserved:Valencia-Industrial-003-HT",
                        "intensity": 0.65,
                        "averageSpeed": 28.7,
                        "occupancy": 0.72,
                    },
                },
                {
                    "type": "Property",
                    "value": {
                        "vehicleClass": "van",
                        "refTrafficFlowObserved": "urn:ngsi-ld:TrafficFlowObserved:Valencia-Industrial-003-VN",
                        "intensity": 0.35,
                        "averageSpeed": 35.2,
                        "occupancy": 0.28,
                    },
                },
            ],
        },
        # 4. Seville Residential - Low traffic impact
        {
            "id": "urn:ngsi-ld:TrafficEnvironmentImpact:Seville-Residential-004",
            "type": "TrafficEnvironmentImpact",
            "dateObservedFrom": {
                "type": "Property",
                "value": {"@type": "DateTime", "@value": current_time},
            },
            "dateObservedTo": {
                "type": "Property",
                "value": {"@type": "DateTime", "@value": current_time},
            },
            "name": {"type": "Property", "value": "Seville Triana Station"},
            "description": {
                "type": "Property",
                "value": "Residential area traffic environmental impact monitoring",
            },
            "location": {
                "type": "GeoProperty",
                "value": {"type": "Point", "coordinates": [-5.984459, 37.389092]},
            },
            "address": {
                "type": "Property",
                "value": {
                    "addressCountry": "Spain",
                    "addressLocality": "Seville",
                    "addressRegion": "Andalusia",
                    "district": "Triana",
                },
            },
            "areaServed": {"type": "Property", "value": "Seville Residential District"},
            "co2": {"type": "Property", "value": 312.8, "unitCode": "GQ"},
            "dataProvider": {"type": "Property", "value": "GreenWave Traffic Monitor"},
            "source": {
                "type": "Property",
                "value": "https://github.com/greenwave/traffic-monitor",
            },
            "traffic": [
                {
                    "type": "Property",
                    "value": {
                        "vehicleClass": "passenger_car",
                        "refTrafficFlowObserved": "urn:ngsi-ld:TrafficFlowObserved:Seville-Residential-004-PC",
                        "intensity": 0.45,
                        "averageSpeed": 25.3,
                        "occupancy": 0.38,
                    },
                },
                {
                    "type": "Property",
                    "value": {
                        "vehicleClass": "bicycle",
                        "refTrafficFlowObserved": "urn:ngsi-ld:TrafficFlowObserved:Seville-Residential-004-BC",
                        "intensity": 0.25,
                        "averageSpeed": 18.5,
                        "occupancy": 0.15,
                    },
                },
            ],
        },
        # 5. Bilbao Green Zone - Excellent traffic conditions
        {
            "id": "urn:ngsi-ld:TrafficEnvironmentImpact:Bilbao-Green-005",
            "type": "TrafficEnvironmentImpact",
            "dateObservedFrom": {
                "type": "Property",
                "value": {"@type": "DateTime", "@value": current_time},
            },
            "dateObservedTo": {
                "type": "Property",
                "value": {"@type": "DateTime", "@value": current_time},
            },
            "name": {"type": "Property", "value": "Bilbao Park Station"},
            "description": {
                "type": "Property",
                "value": "Green zone traffic environmental impact monitoring",
            },
            "location": {
                "type": "GeoProperty",
                "value": {"type": "Point", "coordinates": [-2.923441, 43.263012]},
            },
            "address": {
                "type": "Property",
                "value": {
                    "addressCountry": "Spain",
                    "addressLocality": "Bilbao",
                    "addressRegion": "Basque Country",
                },
            },
            "areaServed": {"type": "Property", "value": "Bilbao Green Zone"},
            "co2": {"type": "Property", "value": 285.4, "unitCode": "GQ"},
            "dataProvider": {"type": "Property", "value": "GreenWave Traffic Monitor"},
            "source": {
                "type": "Property",
                "value": "https://github.com/greenwave/traffic-monitor",
            },
            "traffic": [
                {
                    "type": "Property",
                    "value": {
                        "vehicleClass": "electric_vehicle",
                        "refTrafficFlowObserved": "urn:ngsi-ld:TrafficFlowObserved:Bilbao-Green-005-EV",
                        "intensity": 0.35,
                        "averageSpeed": 22.8,
                        "occupancy": 0.25,
                    },
                },
                {
                    "type": "Property",
                    "value": {
                        "vehicleClass": "bicycle",
                        "refTrafficFlowObserved": "urn:ngsi-ld:TrafficFlowObserved:Bilbao-Green-005-BC",
                        "intensity": 0.45,
                        "averageSpeed": 15.2,
                        "occupancy": 0.18,
                    },
                },
                {
                    "type": "Property",
                    "value": {
                        "vehicleClass": "pedestrian",
                        "refTrafficFlowObserved": "urn:ngsi-ld:TrafficFlowObserved:Bilbao-Green-005-PE",
                        "intensity": 0.20,
                        "averageSpeed": 5.5,
                        "occupancy": 0.08,
                    },
                },
            ],
        },
    ]

    return entities


async def create_entities_batch():
    """Create entities using batch operation."""
    print("🚀 Creating 5 TrafficEnvironmentImpact entities via batch operation...")
    print(f"⏰ Timestamp: {datetime.now(timezone.utc).isoformat()}\n")

    async with TrafficEnvironmentImpactService() as service:
        entities = generate_sample_traffic_entities()

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

            # Summary
            print("\n📊 Summary of entities to create:")
            for i, entity in enumerate(entities, 1):
                name = entity.get("name", {}).get("value", "N/A")
                co2 = entity.get("co2", {}).get("value", "N/A")
                coords = (
                    entity.get("location", {}).get("value", {}).get("coordinates", [])
                )

                print(f"   {i}. {name}")
                print(f"      ID: {entity['id']}")
                print(f"      Location: {coords}")
                print(f"      CO2: {co2} ppm")
                print()

        except Exception as e:
            print(f"❌ Batch create failed: {str(e)}")
            import traceback

            traceback.print_exc()


async def verify_entities():
    """Verify that entities were created."""
    print("\n🔍 Verifying created entities...")

    async with TrafficEnvironmentImpactService() as service:
        try:
            entities = await service.get_all(
                limit=10, format="simplified", pick="id,name,co2,areaServed"
            )

            if isinstance(entities, int):
                print(f"✅ Found {entities} TrafficEnvironmentImpact entities total\n")
                return

            for entity in entities:
                print(f"   📍 {entity.get('name', 'N/A')}")
                print(f"      ID: {entity['id']}")
                print(f"      CO2: {entity.get('co2', 'N/A')} ppm")
                print(f"      Area: {entity.get('areaServed', 'N/A')}")
                print()

        except Exception as e:
            print(f"❌ Verification failed: {str(e)}")


async def main():
    print("=" * 80)
    print("  TrafficEnvironmentImpact Synthetic Data Creator")
    print("  Author: GreenWave Team")
    print(f"  Date: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print("=" * 80)
    print()

    await create_entities_batch()
    await verify_entities()

    print("\n✨ Done!")


if __name__ == "__main__":
    asyncio.run(main())
