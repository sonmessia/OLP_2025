"""
Script to create 5 sample AirQualityObserved entities for testing.

Author: sonmessia
Created: 2025-11-15
"""

import asyncio
from datetime import datetime, timezone
from typing import List, Dict, Any
from backend.app.services.air_quality_service import AirQualityService


def generate_sample_entities() -> List[Dict[str, Any]]:
    """
    Generate 5 diverse AirQualityObserved entities.

    ⚠️ IMPORTANT: For batch operations, we need to send FULL NGSI-LD format
    but WITHOUT individual @context in each entity.
    """

    current_time = datetime.now(timezone.utc).isoformat()

    entities = [
        # 1. Madrid City Center - High pollution
        {
            "id": "urn:ngsi-ld:AirQualityObserved:Madrid-CityCenter-001",
            "type": "AirQualityObserved",
            "dateObserved": {
                "type": "Property",
                "value": {"@type": "DateTime", "@value": current_time},
            },
            "name": {"type": "Property", "value": "Madrid City Center Station"},
            "description": {
                "type": "Property",
                "value": "Air quality monitoring station in Madrid downtown area",
            },
            "location": {
                "type": "GeoProperty",
                "value": {"type": "Point", "coordinates": [-3.703790, 40.416775]},
            },
            "address": {
                "type": "Property",
                "value": {
                    "addressCountry": "Spain",
                    "addressLocality": "Madrid",
                    "streetAddress": "Plaza Mayor",
                },
            },
            "areaServed": {"type": "Property", "value": "Madrid Downtown"},
            "typeofLocation": {"type": "Property", "value": "outdoor"},
            "airQualityIndex": {"type": "Property", "value": 75, "unitCode": "C62"},
            "airQualityLevel": {"type": "Property", "value": "Moderate"},
            "pm25": {"type": "Property", "value": 35.2, "unitCode": "GQ"},
            "pm10": {"type": "Property", "value": 58.7, "unitCode": "GQ"},
            "no2": {"type": "Property", "value": 42.3, "unitCode": "GQ"},
            "o3": {"type": "Property", "value": 68.5, "unitCode": "GQ"},
            "co": {"type": "Property", "value": 0.8, "unitCode": "GP"},
            "so2": {"type": "Property", "value": 12.4, "unitCode": "GQ"},
            "temperature": {"type": "Property", "value": 22.5, "unitCode": "CEL"},
            "relativeHumidity": {"type": "Property", "value": 0.65, "unitCode": "C62"},
            "windSpeed": {"type": "Property", "value": 3.2, "unitCode": "MTS"},
            "windDirection": {"type": "Property", "value": 45.0, "unitCode": "DD"},
            "reliability": {"type": "Property", "value": 0.95},
        },
        # 2. Barcelona Coastal - Moderate pollution
        {
            "id": "urn:ngsi-ld:AirQualityObserved:Barcelona-Coastal-002",
            "type": "AirQualityObserved",
            "dateObserved": {
                "type": "Property",
                "value": {"@type": "DateTime", "@value": current_time},
            },
            "name": {"type": "Property", "value": "Barcelona Coastal Station"},
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
            "typeofLocation": {"type": "Property", "value": "outdoor"},
            "airQualityIndex": {"type": "Property", "value": 55},
            "airQualityLevel": {"type": "Property", "value": "Fair"},
            "pm25": {"type": "Property", "value": 22.8, "unitCode": "GQ"},
            "pm10": {"type": "Property", "value": 38.5, "unitCode": "GQ"},
            "no2": {"type": "Property", "value": 28.7, "unitCode": "GQ"},
            "o3": {"type": "Property", "value": 72.3, "unitCode": "GQ"},
            "co": {"type": "Property", "value": 0.5, "unitCode": "GP"},
            "so2": {"type": "Property", "value": 8.2, "unitCode": "GQ"},
            "temperature": {"type": "Property", "value": 24.8, "unitCode": "CEL"},
            "relativeHumidity": {"type": "Property", "value": 0.72},
            "windSpeed": {"type": "Property", "value": 5.8, "unitCode": "MTS"},
            "windDirection": {"type": "Property", "value": 90.0, "unitCode": "DD"},
        },
        # 3. Valencia Industrial - Very high pollution
        {
            "id": "urn:ngsi-ld:AirQualityObserved:Valencia-Industrial-003",
            "type": "AirQualityObserved",
            "dateObserved": {
                "type": "Property",
                "value": {"@type": "DateTime", "@value": current_time},
            },
            "name": {"type": "Property", "value": "Valencia Industrial Zone Station"},
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
            "typeofLocation": {"type": "Property", "value": "outdoor"},
            "airQualityIndex": {"type": "Property", "value": 125},
            "airQualityLevel": {
                "type": "Property",
                "value": "Unhealthy for Sensitive Groups",
            },
            "pm25": {"type": "Property", "value": 65.4, "unitCode": "GQ"},
            "pm10": {"type": "Property", "value": 98.2, "unitCode": "GQ"},
            "pm1": {"type": "Property", "value": 42.1, "unitCode": "GQ"},
            "no2": {"type": "Property", "value": 78.9, "unitCode": "GQ"},
            "nox": {"type": "Property", "value": 125.3, "unitCode": "GQ"},
            "o3": {"type": "Property", "value": 45.2, "unitCode": "GQ"},
            "co": {"type": "Property", "value": 1.8, "unitCode": "GP"},
            "co2": {"type": "Property", "value": 425.0, "unitCode": "GQ"},
            "so2": {"type": "Property", "value": 28.7, "unitCode": "GQ"},
            "temperature": {"type": "Property", "value": 26.3, "unitCode": "CEL"},
            "relativeHumidity": {"type": "Property", "value": 0.58},
            "windSpeed": {"type": "Property", "value": 2.1, "unitCode": "MTS"},
        },
        # 4. Seville Residential - Low pollution
        {
            "id": "urn:ngsi-ld:AirQualityObserved:Seville-Residential-004",
            "type": "AirQualityObserved",
            "dateObserved": {
                "type": "Property",
                "value": {"@type": "DateTime", "@value": current_time},
            },
            "name": {"type": "Property", "value": "Seville Residential Area Station"},
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
            "typeofLocation": {"type": "Property", "value": "outdoor"},
            "airQualityIndex": {"type": "Property", "value": 35},
            "airQualityLevel": {"type": "Property", "value": "Good"},
            "pm25": {"type": "Property", "value": 12.3, "unitCode": "GQ"},
            "pm10": {"type": "Property", "value": 24.8, "unitCode": "GQ"},
            "no2": {"type": "Property", "value": 18.5, "unitCode": "GQ"},
            "o3": {"type": "Property", "value": 82.4, "unitCode": "GQ"},
            "temperature": {"type": "Property", "value": 28.7, "unitCode": "CEL"},
            "relativeHumidity": {"type": "Property", "value": 0.48},
            "windSpeed": {"type": "Property", "value": 4.3, "unitCode": "MTS"},
        },
        # 5. Bilbao Park - Excellent air quality
        {
            "id": "urn:ngsi-ld:AirQualityObserved:Bilbao-Park-005",
            "type": "AirQualityObserved",
            "dateObserved": {
                "type": "Property",
                "value": {"@type": "DateTime", "@value": current_time},
            },
            "name": {"type": "Property", "value": "Bilbao Park Station"},
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
            "typeofLocation": {"type": "Property", "value": "outdoor"},
            "airQualityIndex": {"type": "Property", "value": 18},
            "airQualityLevel": {"type": "Property", "value": "Excellent"},
            "pm25": {"type": "Property", "value": 5.2, "unitCode": "GQ"},
            "pm10": {"type": "Property", "value": 12.4, "unitCode": "GQ"},
            "no2": {"type": "Property", "value": 8.3, "unitCode": "GQ"},
            "o3": {"type": "Property", "value": 95.7, "unitCode": "GQ"},
            "temperature": {"type": "Property", "value": 19.8, "unitCode": "CEL"},
            "relativeHumidity": {"type": "Property", "value": 0.82},
            "windSpeed": {"type": "Property", "value": 6.2, "unitCode": "MTS"},
            "precipitation": {"type": "Property", "value": 2.3, "unitCode": "MMT"},
        },
    ]

    return entities


async def create_entities_batch():
    """Create entities using batch operation."""
    print("🚀 Creating 5 AirQualityObserved entities via batch operation...")
    print(f"⏰ Timestamp: {datetime.now(timezone.utc).isoformat()}\n")

    async with AirQualityService() as service:
        entities = generate_sample_entities()

        try:
            response = await service.batch_create(entities)
            print(f"✅ Batch create successful!")
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
                aqi = entity.get("airQualityIndex", {}).get("value", "N/A")
                level = entity.get("airQualityLevel", {}).get("value", "N/A")
                pm25 = entity.get("pm25", {}).get("value", "N/A")
                coords = (
                    entity.get("location", {}).get("value", {}).get("coordinates", [])
                )

                print(f"   {i}. {name}")
                print(f"      ID: {entity['id']}")
                print(f"      Location: {coords}")
                print(f"      AQI: {aqi} ({level})")
                print(f"      PM2.5: {pm25} µg/m³")
                print()

        except Exception as e:
            print(f"❌ Batch create failed: {str(e)}")
            import traceback

            traceback.print_exc()


async def verify_entities():
    """Verify that entities were created."""
    print("\n🔍 Verifying created entities...")

    async with AirQualityService() as service:
        try:
            entities = await service.get_all(
                limit=10,
                format="simplified",
                pick="id,name,airQualityIndex,airQualityLevel,pm25",
            )

            if isinstance(entities, int):
                print(f"✅ Found {entities} AirQualityObserved entities total\n")
                return
            for entity in entities:
                print(f"   📍 {entity.get('name', 'N/A')}")
                print(f"      ID: {entity['id']}")
                print(f"      AQI: {entity.get('airQualityIndex', 'N/A')}")
                print(f"      Level: {entity.get('airQualityLevel', 'N/A')}")
                print(f"      PM2.5: {entity.get('pm25', 'N/A')} µg/m³")
                print()

        except Exception as e:
            print(f"❌ Verification failed: {str(e)}")


async def main():
    print("=" * 80)
    print("  AirQualityObserved Sample Data Creator")
    print("  Author: sonmessia")
    print(f"  Date: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print("=" * 80)
    print()

    await create_entities_batch()
    await verify_entities()

    print("\n✨ Done!")


if __name__ == "__main__":
    asyncio.run(main())
