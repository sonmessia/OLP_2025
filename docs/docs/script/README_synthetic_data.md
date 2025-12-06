# GreenWave Synthetic Data Generation Scripts

This directory contains scripts to generate synthetic NGSI-LD entities for all GreenWave environmental monitoring models.

## Scripts Overview

### Individual Model Scripts

- **`create_air_quality_samples.py`** (existing) - AirQualityObserved entities
- **`generate_synthetic_traffic_impact.py`** - TrafficEnvironmentImpact entities
- **`generate_synthetic_carbon_footprint.py`** - CarbonFootprint entities
- **`generate_synthetic_water_quality.py`** - WaterQualityObserved entities

### Unified Script

- **`generate_all_synthetic_data.py`** - All models in one script with CLI options

## Usage

### Prerequisites

1. Ensure FIWARE Orion-LD is running (http://localhost:1026)
2. Set PYTHONPATH correctly: `export PYTHONPATH=/path/to/GreenWave/src/backend`
3. Docker services running: `docker-compose up`

### Individual Scripts

```bash
# Generate Air Quality data (5 entities)
python scripts/create_air_quality_samples.py

# Generate Traffic Impact data (5 entities)
python scripts/generate_synthetic_traffic_impact.py

# Generate Carbon Footprint data (5 entities)
python scripts/generate_synthetic_carbon_footprint.py

# Generate Water Quality data (5 entities)
python scripts/generate_synthetic_water_quality.py
```

### Unified Script (Recommended)

```bash
# Generate data for ALL models (default: 5 entities each)
python scripts/generate_all_synthetic_data.py

# Generate data for specific model
python scripts/generate_all_synthetic_data.py --model air-quality
python scripts/generate_all_synthetic_data.py --model traffic-impact
python scripts/generate_all_synthetic_data.py --model carbon-footprint
python scripts/generate_all_synthetic_data.py --model water-quality

# Generate custom number of entities
python scripts/generate_all_synthetic_data.py --model all --count 3

# Generate and verify entities
python scripts/generate_all_synthetic_data.py --model air-quality --verify
```

## Entity Characteristics

### TrafficEnvironmentImpact

- **Locations**: Madrid Highway, Barcelona Coastal, Valencia Industrial, Seville Residential, Bilbao Green Zone
- **CO₂ Levels**: 250-580 ppm based on traffic intensity
- **Vehicle Types**: passenger cars, heavy trucks, electric vehicles, bicycles, pedestrians
- **Metrics**: traffic intensity, average speed, occupancy

### AirQualityObserved

- **Locations**: Madrid City Center, Barcelona Coastal, Valencia Industrial, Seville Residential, Bilbao Park
- **AQI Range**: 18-125 (Excellent to Unhealthy for Sensitive Groups)
- **Pollutants**: PM2.5, PM10, NO₂, O₃, CO, SO₂, CO₂
- **Weather**: Temperature, humidity, wind speed/direction

### CarbonFootprint

- **Locations**: Madrid Industrial, Barcelona Transport, Valencia Agriculture, Seville Residential, Bilbao Commercial
- **CO₂eq Range**: 34-159 kg/hour by sector
- **Emission Sources**: Industry, Transport, Agriculture, Residential, Commercial
- **Tags**: urban, industrial, residential, etc.

### WaterQualityObserved

- **Locations**: Madrid River, Barcelona Coastal, Valencia Reservoir, Seville River, Bilbao Lake
- **Quality Levels**: Excellent, Good, Fair, Moderate, Poor
- **Parameters**: pH, temperature, dissolved oxygen, nitrates, phosphates
- **Contaminants**: Heavy metals (lead, mercury, cadmium, arsenic), organic matter (BOD, COD)

## Output Example

```
================================================================================
  GreenWave Synthetic Data Generator
  NGSI-LD Compatible Entity Creation
  Author: GreenWave Team
  Date: 2025-11-29 14:30:58 UTC
================================================================================

🌍 Processing TrafficEnvironmentImpact entities...
🚀 Creating 5 TrafficEnvironmentImpact entities via batch operation...
⏰ Timestamp: 2025-11-29T14:30:58.321859+00:00

✅ Batch create successful!
   Status: 201
   ✅ Successfully created: 5 entities
      - urn:ngsi-ld:TrafficEnvironmentImpact:Madrid-Highway-001-T
      - urn:ngsi-ld:TrafficEnvironmentImpact:Barcelona-Coastal-002-T
      - urn:ngsi-ld:TrafficEnvironmentImpact:Valencia-Industrial-003-T
      - urn:ngsi-ld:TrafficEnvironmentImpact:Seville-Residential-004-T
      - urn:ngsi-ld:TrafficEnvironmentImpact:Bilbao-Green-005-T

📊 TrafficEnvironmentImpact entities created:
   1. Madrid Highway Traffic Monitor
      ID: urn:ngsi-ld:TrafficEnvironmentImpact:Madrid-Highway-001-T
      Location: [-3.57879, 40.456775]
      CO2: 450.0 ppm
   ...

🔍 Verifying TrafficEnvironmentImpact entities...
   📍 Madrid Highway Traffic Monitor
      ID: urn:ngsi-ld:TrafficEnvironmentImpact:Madrid-Highway-001-T
   ...

✨ Generation complete!
```

## NGSI-LD Format

All generated entities follow the FIWARE NGSI-LD standard:

```json
{
  "id": "urn:ngsi-ld:AirQualityObserved:Madrid-CityCenter-001",
  "type": "AirQualityObserved",
  "dateObserved": {
    "type": "Property",
    "value": {
      "@type": "DateTime",
      "@value": "2025-11-29T14:30:58.321859+00:00"
    }
  },
  "location": {
    "type": "GeoProperty",
    "value": { "type": "Point", "coordinates": [-3.70379, 40.416775] }
  },
  "airQualityIndex": {
    "type": "Property",
    "value": 75,
    "unitCode": "C62"
  }
  // ... additional properties
}
```

## Integration with GreenWave Backend

These scripts integrate seamlessly with your existing GreenWave infrastructure:

1. **Services**: Use the same service classes as the main application
2. **Batch Operations**: Leverage FIWARE Orion-LD batch creation endpoints
3. **Error Handling**: Proper exception handling and verification
4. **NGSI-LD Compliance**: Full compatibility with Smart Data Models

## Extending the Scripts

To add new models or modify existing ones:

1. **Create Service**: Add new service class in `app/services/`
2. **Update Generator**: Modify generation logic in the scripts
3. **Add CLI Option**: Update `generate_all_synthetic_data.py` arguments
4. **Test**: Verify with `python scripts/generate_all_synthetic_data.py --model your-new-model`

## Troubleshooting

### Import Errors

```bash
# Ensure correct Python path
export PYTHONPATH=/path/to/GreenWave/src/backend:$PYTHONPATH

# Test imports
python scripts/generate_all_synthetic_data.py --help
```

### Connection Errors

```bash
# Verify FIWARE services running
docker-compose ps

# Check Orion-LD health
curl http://localhost:1026/version
```

### Entity Creation Errors

- Check FIWARE Orion-LD logs: `docker logs fiware-orionld`
- Verify NGSI-LD context files are accessible
- Ensure entity IDs follow NGSI-LD format: `urn:ngsi-ld:Type:Location-Number`
