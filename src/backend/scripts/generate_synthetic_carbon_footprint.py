#!/usr/bin/env python3
"""
Script to generate synthetic CarbonFootprint entities for testing.

Based on create_air_quality_samples.py pattern
Generates realistic carbon footprint data with NGSI-LD format
"""

import asyncio
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

# Add parent directory to Python path so we can import app modules
sys.path.insert(0, str(Path(__file__).parent.parent))
# Import services
from app.services.carbon_footprint_service import CarbonFootprintService


def generate_sample_carbon_entities() -> List[Dict[str, Any]]:
    """
    Generate 5 diverse CarbonFootprint entities.

    ⚠️ IMPORTANT: For batch operations, we need to send FULL NGSI-LD format
    but WITHOUT individual @context in each entity.
    """

    current_time = datetime.now(timezone.utc).isoformat()

    entities = [
        # 1. Madrid Industrial Zone - High emissions
        {
            "id": "urn:ngsi-ld:CarbonFootprint:Madrid-Industrial-001",
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
            "name": {"type": "Property", "value": "Madrid Industrial Carbon Monitor"},
            "description": {
                "type": "Property",
                "value": "Industrial carbon footprint monitoring in Madrid's manufacturing district",
            },
            "location": {
                "type": "GeoProperty",
                "value": {"type": "Point", "coordinates": [-3.628790, 40.426775]},
            },
            "address": {
                "type": "Property",
                "value": {
                    "addressCountry": "Spain",
                    "addressLocality": "Madrid",
                    "district": "Industrial Zone",
                    "streetAddress": "Polígono Industrial",
                },
            },
            "areaServed": {"type": "Property", "value": "Madrid Industrial District"},
            "CO2eq": {"type": "Property", "value": 158.7, "unitCode": "KGM"},
            "emissionSource": {"type": "Property", "value": "Industry"},
            "dataProvider": {"type": "Property", "value": "GreenWave Carbon Monitor"},
            "source": {
                "type": "Property",
                "value": "https://github.com/greenwave/carbon-monitor",
            },
            "tags": {
                "type": "Property",
                "value": ["industrial", "manufacturing", "heavy"],
            },
            "relatedSource": {
                "type": "Property",
                "value": "urn:ngsi-ld:Factory:Madrid-Plant-001",
            },
        },
        # 2. Barcelona Transport Hub - Medium emissions
        {
            "id": "urn:ngsi-ld:CarbonFootprint:Barcelona-Transport-002",
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
            "name": {"type": "Property", "value": "Barcelona Transport Carbon Monitor"},
            "description": {
                "type": "Property",
                "value": "Transport sector carbon footprint monitoring at Barcelona's main transport hub",
            },
            "location": {
                "type": "GeoProperty",
                "value": {"type": "Point", "coordinates": [2.123333, 41.353333]},
            },
            "address": {
                "type": "Property",
                "value": {
                    "addressCountry": "Spain",
                    "addressLocality": "Barcelona",
                    "addressRegion": "Catalonia",
                    "streetAddress": "Estació Central",
                },
            },
            "areaServed": {"type": "Property", "value": "Barcelona Transport Zone"},
            "CO2eq": {"type": "Property", "value": 87.4, "unitCode": "KGM"},
            "emissionSource": {"type": "Property", "value": "Transport"},
            "dataProvider": {"type": "Property", "value": "GreenWave Carbon Monitor"},
            "source": {
                "type": "Property",
                "value": "https://github.com/greenwave/carbon-monitor",
            },
            "tags": {"type": "Property", "value": ["urban", "transport", "medium"]},
            "relatedSource": {
                "type": "Property",
                "value": "urn:ngsi-ld:BusStation:Barcelona-Central-002",
            },
        },
        # 3. Valencia Agriculture - Low emissions
        {
            "id": "urn:ngsi-ld:CarbonFootprint:Valencia-Agriculture-003",
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
                "value": "Valencia Agriculture Carbon Monitor",
            },
            "description": {
                "type": "Property",
                "value": "Agricultural sector carbon footprint monitoring in Valencia's farming region",
            },
            "location": {
                "type": "GeoProperty",
                "value": {"type": "Point", "coordinates": [-0.395823, 39.439907]},
            },
            "address": {
                "type": "Property",
                "value": {
                    "addressCountry": "Spain",
                    "addressLocality": "Valencia",
                    "district": "Agricultural Zone",
                    "streetAddress": "Finca Modelo",
                },
            },
            "areaServed": {
                "type": "Property",
                "value": "Valencia Agricultural District",
            },
            "CO2eq": {"type": "Property", "value": 34.2, "unitCode": "KGM"},
            "emissionSource": {"type": "Property", "value": "Agriculture"},
            "dataProvider": {"type": "Property", "value": "GreenWave Carbon Monitor"},
            "source": {
                "type": "Property",
                "value": "https://github.com/greenwave/carbon-monitor",
            },
            "tags": {"type": "Property", "value": ["rural", "agriculture", "low"]},
            "relatedSource": {
                "type": "Property",
                "value": "urn:ngsi-ld:Farm:Valencia-Region-003",
            },
        },
        # 4. Seville Residential - Low-Medium emissions
        {
            "id": "urn:ngsi-ld:CarbonFootprint:Seville-Residential-004",
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
            "name": {"type": "Property", "value": "Seville Residential Carbon Monitor"},
            "description": {
                "type": "Property",
                "value": "Residential sector carbon footprint monitoring in Seville's suburban area",
            },
            "location": {
                "type": "GeoProperty",
                "value": {"type": "Point", "coordinates": [-5.974459, 37.359092]},
            },
            "address": {
                "type": "Property",
                "value": {
                    "addressCountry": "Spain",
                    "addressLocality": "Seville",
                    "addressRegion": "Andalusia",
                    "district": "Residencial Norte",
                },
            },
            "areaServed": {"type": "Property", "value": "Seville Residential District"},
            "CO2eq": {"type": "Property", "value": 58.9, "unitCode": "KGM"},
            "emissionSource": {"type": "Property", "value": "Residential"},
            "dataProvider": {"type": "Property", "value": "GreenWave Carbon Monitor"},
            "source": {
                "type": "Property",
                "value": "https://github.com/greenwave/carbon-monitor",
            },
            "tags": {
                "type": "Property",
                "value": ["suburban", "residential", "low-medium"],
            },
            "relatedSource": {
                "type": "Property",
                "value": "urn:ngsi-ld:Residential:Seville-Norte-004",
            },
        },
        # 5. Bilbao Commercial - Medium emissions
        {
            "id": "urn:ngsi-ld:CarbonFootprint:Bilbao-Commercial-005",
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
            "name": {"type": "Property", "value": "Bilbao Commercial Carbon Monitor"},
            "description": {
                "type": "Property",
                "value": "Commercial sector carbon footprint monitoring in Bilbao's shopping district",
            },
            "location": {
                "type": "GeoProperty",
                "value": {"type": "Point", "coordinates": [-2.913441, 43.233012]},
            },
            "address": {
                "type": "Property",
                "value": {
                    "addressCountry": "Spain",
                    "addressLocality": "Bilbao",
                    "addressRegion": "Basque Country",
                    "streetAddress": "Gran Vía Comercial",
                },
            },
            "areaServed": {"type": "Property", "value": "Bilbao Commercial District"},
            "CO2eq": {"type": "Property", "value": 76.5, "unitCode": "KGM"},
            "emissionSource": {"type": "Property", "value": "Commercial"},
            "dataProvider": {"type": "Property", "value": "GreenWave Carbon Monitor"},
            "source": {
                "type": "Property",
                "value": "https://github.com/greenwave/carbon-monitor",
            },
            "tags": {"type": "Property", "value": ["urban", "commercial", "medium"]},
            "relatedSource": {
                "type": "Property",
                "value": "urn:ngsi-ld:Mall:Bilbao-Center-005",
            },
        },
    ]

    return entities


async def create_entities_batch():
    """Create entities using batch operation."""
    print("🚀 Creating 5 CarbonFootprint entities via batch operation...")
    print(f"⏰ Timestamp: {datetime.now(timezone.utc).isoformat()}\n")

    async with CarbonFootprintService() as service:
        entities = generate_sample_carbon_entities()

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
                co2eq = entity.get("CO2eq", {}).get("value", "N/A")
                source = entity.get("emissionSource", {}).get("value", "N/A")
                coords = (
                    entity.get("location", {}).get("value", {}).get("coordinates", [])
                )
                tags = entity.get("tags", {}).get("value", [])

                print(f"   {i}. {name}")
                print(f"      ID: {entity['id']}")
                print(f"      Location: {coords}")
                print(f"      CO2eq: {co2eq} kg/h")
                print(f"      Source: {source}")
                print(f"      Tags: {', '.join(tags) if tags else 'N/A'}")
                print()

        except Exception as e:
            print(f"❌ Batch create failed: {str(e)}")
            import traceback

            traceback.print_exc()


async def verify_entities():
    """Verify that entities were created."""
    print("\n🔍 Verifying created entities...")

    async with CarbonFootprintService() as service:
        try:
            entities = await service.get_all(
                limit=10, format="simplified", pick="id,name,CO2eq,emissionSource,tags"
            )

            if isinstance(entities, int):
                print(f"✅ Found {entities} CarbonFootprint entities total\n")
                return

            for entity in entities:
                print(f"   📍 {entity.get('name', 'N/A')}")
                print(f"      ID: {entity['id']}")
                print(f"      CO2eq: {entity.get('CO2eq', 'N/A')} kg/h")
                print(f"      Source: {entity.get('emissionSource', 'N/A')}")
                tags = entity.get("tags", "N/A")
                print(
                    f"      Tags: {', '.join(tags) if isinstance(tags, list) else tags}"
                )
                print()

        except Exception as e:
            print(f"❌ Verification failed: {str(e)}")


async def main():
    print("=" * 80)
    print("  CarbonFootprint Synthetic Data Creator")
    print("  Author: GreenWave Team")
    print(f"  Date: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print("=" * 80)
    print()

    await create_entities_batch()
    await verify_entities()

    print("\n✨ Done!")


if __name__ == "__main__":
    asyncio.run(main())
