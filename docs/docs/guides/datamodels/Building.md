<!--
 Copyright (c) 2025 Green Wave Team
 
 This software is released under the MIT License.
 https://opensource.org/licenses/MIT
-->

---
sidebar_position: 5
title: Building
---

# Building

## Entity Description

The `Building` entity represents a building or structure. In the context of GreenWave, it is often used to associate energy consumption or carbon footprint data with specific physical structures.

### JSON Structure

A typical `Building` entity in NGSI-LD format looks like this:

```json
{
  "id": "urn:ngsi-ld:Building:Office-001",
  "type": "Building",
  "category": {
    "type": "Property",
    "value": ["office"]
  },
  "address": {
    "type": "Property",
    "value": {
      "streetAddress": "123 Innovation Drive",
      "addressLocality": "Smart City",
      "addressCountry": "US"
    }
  },
  "floorsAboveGround": {
    "type": "Property",
    "value": 10
  },
  "location": {
    "type": "GeoProperty",
    "value": {
      "type": "Polygon",
      "coordinates": [
        [
          [-3.703, 40.416],
          [-3.703, 40.417],
          [-3.704, 40.417],
          [-3.704, 40.416],
          [-3.703, 40.416]
        ]
      ]
    }
  },
  "mapUrl": {
    "type": "Property",
    "value": "http://maps.example.com/building/123"
  }
}
```

### Key Fields

- **id**: Unique identifier for the building.
- **type**: Entity type, must be `Building`.
- **category**: Category of the building (e.g., `office`, `residential`, `industrial`).
- **address**: Structured address of the building.
- **location**: GeoJSON Polygon representing the building's footprint.
- **floorsAboveGround**: Number of floors.

## Smart Data Models

This data model complies with the [Smart Data Models](https://smart-data-models.github.io/dataModel.Building/Building/) standard. It is useful for urban planning and energy management applications.

## Application

### Data Validation

- **Structure**: Ensures `address` follows the standard schema (street, locality, country).
- **Geometry**: Validates that `location` is a closed `Polygon`.

### Documentation

- **Urban Planning**: Provides data on building density and types for city planners.
- **Energy Management**: Serves as the reference object for `CarbonFootprint` entities (linked via `refBuilding`), allowing analysis of emissions per building.

### Uniqueness & Linked Data

- **Uniqueness**: `category` is mapped to `fiware:category`, ensuring consistent building classification.
- **Linked Data**: Buildings are linked to `CarbonFootprint` entities. This enables the creation of a "Digital Twin" of the city where physical structures are connected to their dynamic environmental performance data.

### Intelligent Query Support

- **Spatial Queries**: "Find all `office` buildings in the 'Tech Park' district."
- **Sustainability Queries**: "List buildings with the highest carbon footprint per square meter."
