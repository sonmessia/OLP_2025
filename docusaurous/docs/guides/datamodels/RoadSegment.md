---
sidebar_position: 4
title: RoadSegment
---

<!--
 Copyright (c) 2025 Green Wave Team

 This software is released under the MIT License.
 https://opensource.org/licenses/MIT
-->

# RoadSegment

## Entity Description

The `RoadSegment` entity represents a specific section of a road. It is used to map traffic data and environmental impacts to physical infrastructure.

### JSON Structure

A typical `RoadSegment` entity in NGSI-LD format looks like this:

```json
{
  "id": "urn:ngsi-ld:RoadSegment:Segment-A",
  "type": "RoadSegment",
  "name": {
    "type": "Property",
    "value": "Main Street - Block 1"
  },
  "roadClass": {
    "type": "Property",
    "value": "MAJOR_CITY_ROAD"
  },
  "allowedVehicleType": {
    "type": "Property",
    "value": ["car", "bus", "bicycle"]
  },
  "maximumAllowedSpeed": {
    "type": "Property",
    "value": 50
  },
  "totalLaneNumber": {
    "type": "Property",
    "value": 2
  },
  "location": {
    "type": "GeoProperty",
    "value": {
      "type": "LineString",
      "coordinates": [
        [-3.703, 40.416],
        [-3.704, 40.417]
      ]
    }
  }
}
```

### Key Fields

- **id**: Unique identifier for the road segment.
- **type**: Entity type, must be `RoadSegment`.
- **name**: Human-readable name of the segment.
- **roadClass**: Classification of the road (e.g., `motorway`, `primary`, `residential`).
- **allowedVehicleType**: List of vehicle types allowed on this segment.
- **maximumAllowedSpeed**: Speed limit for the segment.
- **location**: GeoJSON LineString representing the path of the road segment.

## Smart Data Models

This data model adheres to the [Smart Data Models](https://smart-data-models.github.io/dataModel.Transportation/RoadSegment/) standard for Transportation. It is compatible with DATEX II and OpenStreetMap standards.

## Application

### Data Validation

- **Geometry**: The `location` is typically a `LineString`, validated to ensure it contains valid coordinates.
- **Enums**: `roadClass` and `allowedVehicleType` are validated against standard lists to ensure consistency.

### Documentation

- **Map Rendering**: Frontend applications use the `location` field to draw the road network on maps.
- **Routing**: Navigation algorithms use `maximumAllowedSpeed` and `allowedVehicleType` to calculate optimal routes.

### Uniqueness & Linked Data

- **Uniqueness**: `roadClass` is mapped to `fiware:roadClass`, standardizing road types across the platform.
- **Linked Data**: `RoadSegment` acts as a hub. `TrafficEnvironmentImpact` and `TrafficFlowObserved` entities link to it via `refRoadSegment`, allowing data aggregation by location.

### Intelligent Query Support

- **Spatial Queries**: "Find all road segments within a specific polygon."
- **Attribute Queries**: "Identify all `MAJOR_CITY_ROAD` segments where the speed limit is greater than 50 km/h."
- **Impact Correlation**: "Show road segments with high traffic density but low air quality."
