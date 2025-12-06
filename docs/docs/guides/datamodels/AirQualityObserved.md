---
sidebar_position: 1
title: AirQualityObserved
---

# AirQualityObserved

## Entity Description

The `AirQualityObserved` entity represents an observation of air quality conditions at a specific location and time. It is a key component in monitoring environmental health and pollution levels.

### JSON Structure

A typical `AirQualityObserved` entity in NGSI-LD format looks like this:

```json
{
  "id": "urn:ngsi-ld:AirQualityObserved:Madrid-AmbientObserved-28079004-2016-03-15T11:00:00",
  "type": "AirQualityObserved",
  "dateObserved": {
    "type": "Property",
    "value": "2016-03-15T11:00:00Z"
  },
  "airQualityLevel": {
    "type": "Property",
    "value": "moderate"
  },
  "co2": {
    "type": "Property",
    "value": 450
  },
  "no2": {
    "type": "Property",
    "value": 45
  },
  "location": {
    "type": "GeoProperty",
    "value": {
      "type": "Point",
      "coordinates": [-3.70379, 40.416775]
    }
  },
  "refDevice": {
    "type": "Relationship",
    "object": "urn:ngsi-ld:Device:Device-01"
  }
}
```

### Key Fields

- **id**: Unique identifier for the entity (e.g., `urn:ngsi-ld:AirQualityObserved:001`).
- **type**: Entity type, must be `AirQualityObserved`.
- **dateObserved**: The date and time of the observation.
- **location**: GeoJSON representation of the location (Point, Polygon, etc.).
- **co2, no2, pm10, pm25**: Measured values for various pollutants.
- **airQualityLevel**: Qualitative assessment of air quality (e.g., "good", "moderate", "hazardous").
- **refDevice**: A relationship link to the `Device` that captured this observation.

## Smart Data Models

This data model is fully compliant with the [Smart Data Models](https://smart-data-models.github.io/dataModel.Environment/AirQualityObserved/) standard for Environment. This ensures interoperability with other systems and adherence to international standards for smart city data.

## Application

### Data Validation

Using the `openAPI/smartmodels.yaml` file, the system enforces strict validation rules. For example:

- **Mandatory Fields**: `id`, `type`, and `dateObserved` must be present.
- **Data Types**: `co2` must be a number; sending a string will trigger a validation error.
- **Enum Values**: `airQualityLevel` must match one of the predefined values (e.g., "good", "moderate").

### Documentation

This model serves as a reference for Frontend and Mobile (Flutter) developers:

- **API Integration**: Developers know exactly which endpoints to call and what JSON structure to expect.
- **UI Binding**: Fields like `co2` and `airQualityLevel` can be directly mapped to UI widgets (charts, status indicators).

### Uniqueness & Linked Data

The `ld-context-files` provide a JSON-LD context that maps short terms to unique URIs:

- **Uniqueness**: `co2` becomes `fiware:co2` (e.g., `https://uri.fiware.org/ns/data-models#co2`), distinguishing it from other definitions of CO2 in different domains.
- **Linked Data**: The `refDevice` field is not just a string but a link to a `Device` entity. This allows the Context Broker to build a **Knowledge Graph**, connecting air quality data to the specific sensor hardware.

### Intelligent Query Support

The semantic definition enables powerful queries:

- **Geo-queries**: "Find all air quality observations within 500m of the city center."
- **Relationship queries**: "Retrieve all air quality records captured by devices manufactured by 'Samsung'."
