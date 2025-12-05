#!/usr/bin/env python3
"""
Script to generate synthetic WaterQualityObserved entities for testing.

Based on create_air_quality_samples.py pattern
Generates realistic water quality data with NGSI-LD format
"""

import asyncio
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

# Import services
from app.services.water_quality_service import WaterQualityService

# Add parent directory to Python path so we can import app modules
sys.path.insert(0, str(Path(__file__).parent.parent))


def generate_sample_water_entities() -> List[Dict[str, Any]]:
    """
    Generate 5 diverse WaterQualityObserved entities.

    ⚠️ IMPORTANT: For batch operations, we need to send FULL NGSI-LD format
    but WITHOUT individual @context in each entity.
    """

    current_time = datetime.now(timezone.utc).isoformat()

    entities = [
        # 1. Madrid River - Poor water quality
        {
            "id": "urn:ngsi-ld:WaterQualityObserved:Madrid-River-001",
            "type": "WaterQualityObserved",
            "dateObserved": {
                "type": "Property",
                "value": {"@type": "DateTime", "@value": current_time},
            },
            "name": {"type": "Property", "value": "Madrid Manzanares River Station"},
            "description": {
                "type": "Property",
                "value": "Water quality monitoring station in Madrid's Manzanares River downstream",
            },
            "location": {
                "type": "GeoProperty",
                "value": {"type": "Point", "coordinates": [-3.712790, 40.406775]},
            },
            "address": {
                "type": "Property",
                "value": {
                    "addressCountry": "Spain",
                    "addressLocality": "Madrid",
                    "streetAddress": "Puente del Rey",
                },
            },
            "areaServed": {
                "type": "Property",
                "value": "Madrid Manzanares River Section",
            },
            "temperature": {"type": "Property", "value": 18.7, "unitCode": "CEL"},
            "pH": {"type": "Property", "value": 7.8, "unitCode": "C62"},
            "dissolvedOxygen": {"type": "Property", "value": 4.2, "unitCode": "GQ"},
            "conductivity": {"type": "Property", "value": 845.0, "unitCode": "C62"},
            "turbidity": {"type": "Property", "value": 15.8, "unitCode": "NTU"},
            "alkalinity": {"type": "Property", "value": 125.0, "unitCode": "GQ"},
            "nitrates": {"type": "Property", "value": 12.5, "unitCode": "GQ"},
            "phosphates": {"type": "Property", "value": 2.8, "unitCode": "GQ"},
            "ammonia": {"type": "Property", "value": 1.7, "unitCode": "GQ"},
            "lead": {"type": "Property", "value": 8.5, "unitCode": "GQ"},
            "mercury": {"type": "Property", "value": 0.8, "unitCode": "GQ"},
            "cadmium": {"type": "Property", "value": 1.2, "unitCode": "GQ"},
            "arsenic": {"type": "Property", "value": 3.7, "unitCode": "GQ"},
            "bod": {"type": "Property", "value": 12.5, "unitCode": "GQ"},
            "cod": {"type": "Property", "value": 35.8, "unitCode": "GQ"},
            "chlorides": {"type": "Property", "value": 45.0, "unitCode": "GQ"},
            "sulfates": {"type": "Property", "value": 65.0, "unitCode": "GQ"},
            "totalSuspendedSolids": {
                "type": "Property",
                "value": 38.5,
                "unitCode": "GQ",
            },
            "measurand": {
                "type": "Property",
                "value": [
                    "pH",
                    "temperature",
                    "dissolvedOxygen",
                    "nitrates",
                    "phosphates",
                ],
            },
            "dataProvider": {"type": "Property", "value": "GreenWave Water Monitor"},
            "source": {
                "type": "Property",
                "value": "https://github.com/greenwave/water-monitor",
            },
            "refPointOfInterest": {
                "type": "Property",
                "value": "urn:ngsi-ld:RiverMonitoring:Madrid-Manzanares-001",
            },
        },
        # 2. Barcelona Coastal - Good water quality
        {
            "id": "urn:ngsi-ld:WaterQualityObserved:Barcelona-Coastal-002",
            "type": "WaterQualityObserved",
            "dateObserved": {
                "type": "Property",
                "value": {"@type": "DateTime", "@value": current_time},
            },
            "name": {"type": "Property", "value": "Barcelona Beach Water Station"},
            "description": {
                "type": "Property",
                "value": "Coastal water quality monitoring station at Barcelona's main beach",
            },
            "location": {
                "type": "GeoProperty",
                "value": {"type": "Point", "coordinates": [2.193333, 41.363333]},
            },
            "address": {
                "type": "Property",
                "value": {
                    "addressCountry": "Spain",
                    "addressLocality": "Barcelona",
                    "addressRegion": "Catalonia",
                    "streetAddress": "Playa Barceloneta",
                },
            },
            "areaServed": {
                "type": "Property",
                "value": "Barcelona Mediterranean Coast",
            },
            "temperature": {"type": "Property", "value": 22.5, "unitCode": "CEL"},
            "pH": {"type": "Property", "value": 8.1, "unitCode": "C62"},
            "dissolvedOxygen": {"type": "Property", "value": 7.8, "unitCode": "GQ"},
            "conductivity": {"type": "Property", "value": 56500.0, "unitCode": "C62"},
            "turbidity": {"type": "Property", "value": 3.2, "unitCode": "NTU"},
            "alkalinity": {"type": "Property", "value": 115.0, "unitCode": "GQ"},
            "nitrates": {"type": "Property", "value": 0.8, "unitCode": "GQ"},
            "phosphates": {"type": "Property", "value": 0.3, "unitCode": "GQ"},
            "ammonia": {"type": "Property", "value": 0.1, "unitCode": "GQ"},
            "lead": {"type": "Property", "value": 0.5, "unitCode": "GQ"},
            "mercury": {"type": "Property", "value": 0.02, "unitCode": "GQ"},
            "cadmium": {"type": "Property", "value": 0.1, "unitCode": "GQ"},
            "arsenic": {"type": "Property", "value": 1.5, "unitCode": "GQ"},
            "bod": {"type": "Property", "value": 2.5, "unitCode": "GQ"},
            "cod": {"type": "Property", "value": 8.5, "unitCode": "GQ"},
            "chlorides": {"type": "Property", "value": 18500.0, "unitCode": "GQ"},
            "sulfates": {"type": "Property", "value": 2650.0, "unitCode": "GQ"},
            "totalSuspendedSolids": {
                "type": "Property",
                "value": 8.5,
                "unitCode": "GQ",
            },
            "measurand": {
                "type": "Property",
                "value": ["pH", "temperature", "dissolvedOxygen", "salinity"],
            },
            "salinity": {"type": "Property", "value": 35.5, "unitCode": "C62"},
            "dataProvider": {"type": "Property", "value": "GreenWave Water Monitor"},
            "source": {
                "type": "Property",
                "value": "https://github.com/greenwave/water-monitor",
            },
            "refPointOfInterest": {
                "type": "Property",
                "value": "urn:ngsi-ld:CoastalMonitoring:Barcelona-Barceloneta-002",
            },
        },
        # 3. Valencia Reservoir - Moderate water quality
        {
            "id": "urn:ngsi-ld:WaterQualityObserved:Valencia-Reservoir-003",
            "type": "WaterQualityObserved",
            "dateObserved": {
                "type": "Property",
                "value": {"@type": "DateTime", "@value": current_time},
            },
            "name": {"type": "Property", "value": "Valencia Reservoir Station"},
            "description": {
                "type": "Property",
                "value": "Freshwater reservoir quality monitoring station in Valencia's water supply",
            },
            "location": {
                "type": "GeoProperty",
                "value": {"type": "Point", "coordinates": [-0.365823, 39.439907]},
            },
            "address": {
                "type": "Property",
                "value": {
                    "addressCountry": "Spain",
                    "addressLocality": "Valencia",
                    "district": "Water Supply Zone",
                },
            },
            "areaServed": {
                "type": "Property",
                "value": "Valencia Water Supply District",
            },
            "temperature": {"type": "Property", "value": 16.5, "unitCode": "CEL"},
            "pH": {"type": "Property", "value": 7.5, "unitCode": "C62"},
            "dissolvedOxygen": {"type": "Property", "value": 6.8, "unitCode": "GQ"},
            "conductivity": {"type": "Property", "value": 285.0, "unitCode": "C62"},
            "turbidity": {"type": "Property", "value": 6.5, "unitCode": "NTU"},
            "alkalinity": {"type": "Property", "value": 145.0, "unitCode": "GQ"},
            "nitrates": {"type": "Property", "value": 4.2, "unitCode": "GQ"},
            "phosphates": {"type": "Property", "value": 1.2, "unitCode": "GQ"},
            "ammonia": {"type": "Property", "value": 0.4, "unitCode": "GQ"},
            "lead": {"type": "Property", "value": 2.8, "unitCode": "GQ"},
            "mercury": {"type": "Property", "value": 0.2, "unitCode": "GQ"},
            "cadmium": {"type": "Property", "value": 0.5, "unitCode": "GQ"},
            "arsenic": {"type": "Property", "value": 2.5, "unitCode": "GQ"},
            "bod": {"type": "Property", "value": 5.5, "unitCode": "GQ"},
            "cod": {"type": "Property", "value": 18.5, "unitCode": "GQ"},
            "chlorides": {"type": "Property", "value": 25.0, "unitCode": "GQ"},
            "sulfates": {"type": "Property", "value": 45.0, "unitCode": "GQ"},
            "totalSuspendedSolids": {
                "type": "Property",
                "value": 15.5,
                "unitCode": "GQ",
            },
            "measurand": {
                "type": "Property",
                "value": ["pH", "temperature", "dissolvedOxygen", "nitrates"],
            },
            "dataProvider": {"type": "Property", "value": "GreenWave Water Monitor"},
            "source": {
                "type": "Property",
                "value": "https://github.com/greenwave/water-monitor",
            },
            "refPointOfInterest": {
                "type": "Property",
                "value": "urn:ngsi-ld:ReservoirMonitoring:Valencia-Supply-003",
            },
        },
        # 4. Seville River - Fair water quality
        {
            "id": "urn:ngsi-ld:WaterQualityObserved:Seville-River-004",
            "type": "WaterQualityObserved",
            "dateObserved": {
                "type": "Property",
                "value": {"@type": "DateTime", "@value": current_time},
            },
            "name": {"type": "Property", "value": "Seville Guadalquivir River Station"},
            "description": {
                "type": "Property",
                "value": "River water quality monitoring station in Seville's Guadalquivir River",
            },
            "location": {
                "type": "GeoProperty",
                "value": {"type": "Point", "coordinates": [-5.994459, 37.379092]},
            },
            "address": {
                "type": "Property",
                "value": {
                    "addressCountry": "Spain",
                    "addressLocality": "Seville",
                    "addressRegion": "Andalusia",
                    "district": "Triana",
                    "streetAddress": "Puente de Triana",
                },
            },
            "areaServed": {
                "type": "Property",
                "value": "Seville Guadalquivir River District",
            },
            "temperature": {"type": "Property", "value": 21.5, "unitCode": "CEL"},
            "pH": {"type": "Property", "value": 7.9, "unitCode": "C62"},
            "dissolvedOxygen": {"type": "Property", "value": 5.8, "unitCode": "GQ"},
            "conductivity": {"type": "Property", "value": 685.0, "unitCode": "C62"},
            "turbidity": {"type": "Property", "value": 10.5, "unitCode": "NTU"},
            "alkalinity": {"type": "Property", "value": 135.0, "unitCode": "GQ"},
            "nitrates": {"type": "Property", "value": 8.5, "unitCode": "GQ"},
            "phosphates": {"type": "Property", "value": 1.8, "unitCode": "GQ"},
            "ammonia": {"type": "Property", "value": 0.8, "unitCode": "GQ"},
            "lead": {"type": "Property", "value": 4.5, "unitCode": "GQ"},
            "mercury": {"type": "Property", "value": 0.5, "unitCode": "GQ"},
            "cadmium": {"type": "Property", "value": 0.8, "unitCode": "GQ"},
            "arsenic": {"type": "Property", "value": 3.2, "unitCode": "GQ"},
            "bod": {"type": "Property", "value": 8.5, "unitCode": "GQ"},
            "cod": {"type": "Property", "value": 25.5, "unitCode": "GQ"},
            "chlorides": {"type": "Property", "value": 55.0, "unitCode": "GQ"},
            "sulfates": {"type": "Property", "value": 85.0, "unitCode": "GQ"},
            "totalSuspendedSolids": {
                "type": "Property",
                "value": 28.5,
                "unitCode": "GQ",
            },
            "measurand": {
                "type": "Property",
                "value": [
                    "pH",
                    "temperature",
                    "dissolvedOxygen",
                    "nitrates",
                    "phosphates",
                ],
            },
            "dataProvider": {"type": "Property", "value": "GreenWave Water Monitor"},
            "source": {
                "type": "Property",
                "value": "https://github.com/greenwave/water-monitor",
            },
            "refPointOfInterest": {
                "type": "Property",
                "value": "urn:ngsi-ld:RiverMonitoring:Seville-Guadalquivir-004",
            },
        },
        # 5. Bilbay Lake - Excellent water quality
        {
            "id": "urn:ngsi-ld:WaterQualityObserved:Bilbao-Lake-005",
            "type": "WaterQualityObserved",
            "dateObserved": {
                "type": "Property",
                "value": {"@type": "DateTime", "@value": current_time},
            },
            "name": {"type": "Property", "value": "Bilbao Park Lake Station"},
            "description": {
                "type": "Property",
                "value": "Freshwater lake quality monitoring station in Bilbao's urban park",
            },
            "location": {
                "type": "GeoProperty",
                "value": {"type": "Point", "coordinates": [-2.933441, 43.253012]},
            },
            "address": {
                "type": "Property",
                "value": {
                    "addressCountry": "Spain",
                    "addressLocality": "Bilbao",
                    "addressRegion": "Basque Country",
                    "district": "Parque del Casco Viejo",
                },
            },
            "areaServed": {"type": "Property", "value": "Bilbao Urban Park Zone"},
            "temperature": {"type": "Property", "value": 14.5, "unitCode": "CEL"},
            "pH": {"type": "Property", "value": 7.2, "unitCode": "C62"},
            "dissolvedOxygen": {"type": "Property", "value": 8.5, "unitCode": "GQ"},
            "conductivity": {"type": "Property", "value": 185.0, "unitCode": "C62"},
            "turbidity": {"type": "Property", "value": 2.5, "unitCode": "NTU"},
            "alkalinity": {"type": "Property", "value": 95.0, "unitCode": "GQ"},
            "nitrates": {"type": "Property", "value": 0.5, "unitCode": "GQ"},
            "phosphates": {"type": "Property", "value": 0.1, "unitCode": "GQ"},
            "ammonia": {"type": "Property", "value": 0.05, "unitCode": "GQ"},
            "lead": {"type": "Property", "value": 0.2, "unitCode": "GQ"},
            "mercury": {"type": "Property", "value": 0.01, "unitCode": "GQ"},
            "cadmium": {"type": "Property", "value": 0.05, "unitCode": "GQ"},
            "arsenic": {"type": "Property", "value": 0.8, "unitCode": "GQ"},
            "bod": {"type": "Property", "value": 1.5, "unitCode": "GQ"},
            "cod": {"type": "Property", "value": 4.5, "unitCode": "GQ"},
            "chlorides": {"type": "Property", "value": 12.0, "unitCode": "GQ"},
            "sulfates": {"type": "Property", "value": 18.0, "unitCode": "GQ"},
            "totalSuspendedSolids": {
                "type": "Property",
                "value": 5.5,
                "unitCode": "GQ",
            },
            "measurand": {
                "type": "Property",
                "value": ["pH", "temperature", "dissolvedOxygen", "transparency"],
            },
            "dataProvider": {"type": "Property", "value": "GreenWave Water Monitor"},
            "source": {
                "type": "Property",
                "value": "https://github.com/greenwave/water-monitor",
            },
            "refPointOfInterest": {
                "type": "Property",
                "value": "urn:ngsi-ld:LakeMonitoring:Bilbao-Park-005",
            },
        },
    ]

    return entities


async def create_entities_batch():
    """Create entities using batch operation."""
    print("🚀 Creating 5 WaterQualityObserved entities via batch operation...")
    print(f"⏰ Timestamp: {datetime.now(timezone.utc).isoformat()}\n")

    async with WaterQualityService() as service:
        entities = generate_sample_water_entities()

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
                temp = entity.get("temperature", {}).get("value", "N/A")
                ph = entity.get("pH", {}).get("value", "N/A")
                do = entity.get("dissolvedOxygen", {}).get("value", "N/A")
                coords = (
                    entity.get("location", {}).get("value", {}).get("coordinates", [])
                )

                print(f"   {i}. {name}")
                print(f"      ID: {entity['id']}")
                print(f"      Location: {coords}")
                print(f"      Temperature: {temp}°C")
                print(f"      pH: {ph}")
                print(f"      Dissolved O2: {do} mg/L")
                print()

        except Exception as e:
            print(f"❌ Batch create failed: {str(e)}")
            import traceback

            traceback.print_exc()


async def verify_entities():
    """Verify that entities were created."""
    print("\n🔍 Verifying created entities...")

    async with WaterQualityService() as service:
        try:
            entities = await service.get_all(
                limit=10,
                format="simplified",
                pick="id,name,temperature,pH,dissolvedOxygen,turbidity",
            )

            if isinstance(entities, int):
                print(f"✅ Found {entities} WaterQualityObserved entities total\n")
                return

            for entity in entities:
                print(f"   📍 {entity.get('name', 'N/A')}")
                print(f"      ID: {entity['id']}")
                print(f"      Temperature: {entity.get('temperature', 'N/A')}°C")
                print(f"      pH: {entity.get('pH', 'N/A')}")
                print(
                    f"      Dissolved O2: {entity.get('dissolvedOxygen', 'N/A')} mg/L"
                )
                print(f"      Turbidity: {entity.get('turbidity', 'N/A')} NTU")
                print()

        except Exception as e:
            print(f"❌ Verification failed: {str(e)}")


async def main():
    print("=" * 80)
    print("  WaterQualityObserved Synthetic Data Creator")
    print("  Author: GreenWave Team")
    print(f"  Date: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print("=" * 80)
    print()

    await create_entities_batch()
    await verify_entities()

    print("\n✨ Done!")


if __name__ == "__main__":
    asyncio.run(main())
