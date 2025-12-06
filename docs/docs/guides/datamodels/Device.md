<!--
 Copyright (c) 2025 Green Wave Team
 
 This software is released under the MIT License.
 https://opensource.org/licenses/MIT
-->

---
sidebar_position: 3
title: Device
---

# Device

## Entity Description

The `Device` entity represents a physical hardware unit (IoT device) such as a sensor, actuator, or meter. It is the source of raw data in the system.

### JSON Structure

A typical `Device` entity in NGSI-LD format looks like this:

```json
{
  "id": "urn:ngsi-ld:Device:Sensor-001",
  "type": "Device",
  "category": {
    "type": "Property",
    "value": ["sensor"]
  },
  "controlledProperty": {
    "type": "Property",
    "value": ["airPollution", "temperature"]
  },
  "batteryLevel": {
    "type": "Property",
    "value": 0.95
  },
  "ipAddress": {
    "type": "Property",
    "value": ["192.168.1.10"]
  },
  "location": {
    "type": "GeoProperty",
    "value": {
      "type": "Point",
      "coordinates": [-3.70379, 40.416775]
    }
  },
  "deviceState": {
    "type": "Property",
    "value": "ok"
  }
}
```

### Key Fields

- **id**: Unique identifier for the device.
- **type**: Entity type, must be `Device`.
- **category**: The category of the device (e.g., `sensor`, `actuator`, `meter`).
- **controlledProperty**: List of properties the device monitors or controls (e.g., `airPollution`, `trafficFlow`).
- **batteryLevel**: Current battery level (0.0 to 1.0).
- **deviceState**: Operational state of the device (e.g., `ok`, `error`).
- **ipAddress**: Network address of the device.

## Smart Data Models

This data model follows the [Smart Data Models](https://smart-data-models.github.io/dataModel.Device/Device/) standard for Devices. It aligns with the SAREF (Smart Appliances REFerence) ontology.

## Application

### Data Validation

The `openAPI/smartmodels.yaml` ensures:

- **Categories**: `category` values must match the allowed enum list (e.g., `sensor`, `actuator`).
- **Properties**: `controlledProperty` must be valid strings from the standard list.

### Documentation

- **IoT Integration**: Helps IoT engineers understand how to register new devices into the system.
- **Maintenance**: Operations teams can use fields like `batteryLevel` and `deviceState` to monitor fleet health.

### Uniqueness & Linked Data

- **Uniqueness**: `batteryLevel` is defined as `fiware:batteryLevel`, ensuring consistent interpretation across different device manufacturers.
- **Linked Data**: Devices are linked to the observations they generate (via `refDevice` in `AirQualityObserved`) and potentially to the assets they control (via `controlledAsset`).

### Intelligent Query Support

- **Maintenance Queries**: "Find all devices with `batteryLevel` below 0.2."
- **Capability Queries**: "List all devices capable of measuring `airPollution` in the 'Downtown' district."
