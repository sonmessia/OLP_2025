---
sidebar_position: 1
title: API Documentation
---

# API Documentation

This document provides a comprehensive list of API endpoints available in the backend application.

## 1. AirQualityObserved

**Base Path:** `/api/v1/air-quality`

| Method   | Endpoint                              | Description                               | Input                                                                                                                                                  | Output                             |
| :------- | :------------------------------------ | :---------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------- | :--------------------------------- |
| `GET`    | `/`                                   | Query AirQualityObserved Entities         | Query Params: `id`, `q`, `pick`, `attrs`, `georel`, `geometry`, `coordinates`, `geoproperty`, `limit`, `offset`, `count`, `format`, `options`, `local` | `List[Dict]` or `int`              |
| `GET`    | `/{entity_id}`                        | Get AirQualityObserved Entity by ID       | Path: `entity_id`<br />Query Params: `pick`, `attrs`, `format`, `options`                                                                              | `Dict`                             |
| `POST`   | `/`                                   | Create AirQualityObserved Entity          | Body: `AirQualityObserved` model                                                                                                                       | `{"message": str, "id": str}`      |
| `PATCH`  | `/{entity_id}/attrs`                  | Update Entity Attributes (Partial Update) | Path: `entity_id`<br />Body: `Dict[str, NgsiLdAttributePatch]`                                                                                         | `None` (204 No Content)            |
| `PUT`    | `/{entity_id}`                        | Replace Entity (Full Update)              | Path: `entity_id`<br />Body: `AirQualityObserved` model                                                                                                | `None` (204 No Content)            |
| `DELETE` | `/{entity_id}`                        | Delete AirQualityObserved Entity          | Path: `entity_id`                                                                                                                                      | `None` (204 No Content)            |
| `DELETE` | `/{entity_id}/attrs/{attribute_name}` | Delete Entity Attribute                   | Path: `entity_id`, `attribute_name`                                                                                                                    | `None` (204 No Content)            |
| `POST`   | `/batch/create`                       | Batch Create Entities                     | Body: `BatchOperationRequest` (`entities`: List[Dict])                                                                                                 | `List[str]` or `{"success": True}` |
| `POST`   | `/batch/upsert`                       | Batch Upsert Entities                     | Body: `BatchOperationRequest`<br />Query Params: `options` ('update' or 'replace')                                                                     | `List[str]` or `{"success": True}` |
| `POST`   | `/batch/delete`                       | Batch Delete Entities                     | Body: `BatchDeleteRequest` (`entity_ids`: List[str])                                                                                                   | `None` (204 No Content)            |

## 2. Building

**Base Path:** `/api/v1/buildings`

| Method   | Endpoint                              | Description                    | Input                                                                                                                                                  | Output                             |
| :------- | :------------------------------------ | :----------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------- | :--------------------------------- |
| `GET`    | `/`                                   | Query Building Entities        | Query Params: `id`, `q`, `pick`, `attrs`, `georel`, `geometry`, `coordinates`, `geoproperty`, `limit`, `offset`, `count`, `format`, `options`, `local` | `List[Dict]` or `int`              |
| `GET`    | `/{entity_id}`                        | Get Building by ID             | Path: `entity_id`<br />Query Params: `pick`, `attrs`, `format`, `options`                                                                              | `Dict`                             |
| `POST`   | `/`                                   | Create Building                | Body: `Building` model                                                                                                                                 | `{"message": str, "id": str}`      |
| `PATCH`  | `/{entity_id}/attrs`                  | Update Building Attributes     | Path: `entity_id`<br />Body: `Dict[str, NgsiLdAttributePatch]`                                                                                         | `None` (204 No Content)            |
| `PUT`    | `/{entity_id}`                        | Replace Building               | Path: `entity_id`<br />Body: `Building` model                                                                                                          | `None` (204 No Content)            |
| `DELETE` | `/{entity_id}`                        | Delete Building                | Path: `entity_id`                                                                                                                                      | `None` (204 No Content)            |
| `DELETE` | `/{entity_id}/attrs/{attribute_name}` | Delete Building Attribute      | Path: `entity_id`, `attribute_name`                                                                                                                    | `None` (204 No Content)            |
| `POST`   | `/batch/create`                       | Batch Create Buildings         | Body: `BatchOperationRequest`                                                                                                                          | `List[str]` or `{"success": True}` |
| `POST`   | `/batch/upsert`                       | Batch Upsert Buildings         | Body: `BatchOperationRequest`<br />Query Params: `options`                                                                                             | `List[str]` or `{"success": True}` |
| `POST`   | `/batch/delete`                       | Batch Delete Buildings         | Body: `BatchDeleteRequest`                                                                                                                             | `None` (204 No Content)            |
| `GET`    | `/location/nearby`                    | Find buildings near a location | Query Params: `lon`, `lat`, `max_distance`, `limit`, `format`, `pick`                                                                                  | `List[Dict]`                       |
| `GET`    | `/category/{category}`                | Find buildings by category     | Path: `category`<br />Query Params: `limit`, `format`                                                                                                  | `List[Dict]`                       |
| `GET`    | `/tall`                               | Find tall buildings            | Query Params: `min_floors`, `limit`, `format`                                                                                                          | `List[Dict]`                       |

## 3. CarbonFootprint

**Base Path:** `/api/v1/carbon-footprint`

| Method   | Endpoint                              | Description                         | Input                                                                                                                                                  | Output                             |
| :------- | :------------------------------------ | :---------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------- | :--------------------------------- |
| `GET`    | `/`                                   | Query CarbonFootprint Entities      | Query Params: `id`, `q`, `pick`, `attrs`, `georel`, `geometry`, `coordinates`, `geoproperty`, `limit`, `offset`, `count`, `format`, `options`, `local` | `List[Dict]` or `int`              |
| `GET`    | `/{entity_id}`                        | Get CarbonFootprint by ID           | Path: `entity_id`<br />Query Params: `pick`, `attrs`, `format`, `options`                                                                              | `Dict`                             |
| `POST`   | `/`                                   | Create CarbonFootprint              | Body: `CarbonFootprint` model                                                                                                                          | `{"message": str, "id": str}`      |
| `PATCH`  | `/{entity_id}/attrs`                  | Update CarbonFootprint Attributes   | Path: `entity_id`<br />Body: `Dict[str, NgsiLdAttributePatch]`                                                                                         | `None` (204 No Content)            |
| `PUT`    | `/{entity_id}`                        | Replace CarbonFootprint             | Path: `entity_id`<br />Body: `CarbonFootprint` model                                                                                                   | `None` (204 No Content)            |
| `DELETE` | `/{entity_id}`                        | Delete CarbonFootprint              | Path: `entity_id`                                                                                                                                      | `None` (204 No Content)            |
| `DELETE` | `/{entity_id}/attrs/{attribute_name}` | Delete Attribute                    | Path: `entity_id`, `attribute_name`                                                                                                                    | `None` (204 No Content)            |
| `POST`   | `/batch/create`                       | Batch Create CarbonFootprint        | Body: `BatchOperationRequest`                                                                                                                          | `List[str]` or `{"success": True}` |
| `POST`   | `/batch/upsert`                       | Batch Upsert CarbonFootprint        | Body: `BatchOperationRequest`<br />Query Params: `options`                                                                                             | `List[str]` or `{"success": True}` |
| `POST`   | `/batch/delete`                       | Batch Delete CarbonFootprint        | Body: `BatchDeleteRequest`                                                                                                                             | `None` (204 No Content)            |
| `GET`    | `/source/{emission_source}`           | Find emissions by source type       | Path: `emission_source`<br />Query Params: `limit`, `format`                                                                                           | `List[Dict]`                       |
| `GET`    | `/high-emissions`                     | Find emissions exceeding threshold  | Query Params: `threshold`, `limit`, `format`                                                                                                           | `List[Dict]`                       |
| `GET`    | `/recent`                             | Get recent emission records         | Query Params: `since`, `limit`, `format`, `pick`                                                                                                       | `List[Dict]`                       |
| `GET`    | `/location/nearby`                    | Find emission records near location | Query Params: `lon`, `lat`, `max_distance`, `limit`, `format`, `pick`                                                                                  | `List[Dict]`                       |

## 4. ContextSourceRegistrations

**Base Path:** `/api/v1/csourceRegistrations`

| Method   | Endpoint             | Description                              | Input                                                                                        | Output                                     |
| :------- | :------------------- | :--------------------------------------- | :------------------------------------------------------------------------------------------- | :----------------------------------------- |
| `POST`   | `/`                  | Create a new context source registration | Body: `RegistrationCreate`<br />Query Params: `tenant`                                       | `{"message": str, "id": str, "mode": str}` |
| `GET`    | `/`                  | Get all context source registrations     | Query Params: `entity_type`, `limit`, `offset`, `tenant`                                     | `List[Dict]`                               |
| `GET`    | `/{registration_id}` | Get details of a registration            | Path: `registration_id`<br />Query Params: `tenant`                                          | `Dict`                                     |
| `PATCH`  | `/{registration_id}` | Update a registration                    | Path: `registration_id`<br />Body: `RegistrationUpdate`<br />Query Params: `tenant`          | `None` (204 No Content)                    |
| `DELETE` | `/{registration_id}` | Delete a registration                    | Path: `registration_id`<br />Query Params: `tenant`                                          | `None` (204 No Content)                    |
| `POST`   | `/quick/redirect`    | Quick redirect registration              | Query Params: `entity_type`, `endpoint`, `description`, `tenant`                             | `{"message": str, "id": str}`              |
| `POST`   | `/quick/federation`  | Quick federation registration            | Query Params: `entity_type`, `endpoint`, `description`, `tenant`                             | `{"message": str, "id": str}`              |
| `POST`   | `/quick/device`      | Quick device registration                | Query Params: `entity_id`, `entity_type`, `properties`, `iot_agent`, `description`, `tenant` | `{"message": str, "id": str}`              |

## 5. Device

**Base Path:** `/api/v1/devices`

| Method   | Endpoint                              | Description                   | Input                                                                                                                                                  | Output                             |
| :------- | :------------------------------------ | :---------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------- | :--------------------------------- |
| `GET`    | `/`                                   | Query Device Entities         | Query Params: `id`, `q`, `pick`, `attrs`, `georel`, `geometry`, `coordinates`, `geoproperty`, `limit`, `offset`, `count`, `format`, `options`, `local` | `List[Dict]` or `int`              |
| `GET`    | `/{entity_id}`                        | Get Device by ID              | Path: `entity_id`<br />Query Params: `pick`, `attrs`, `format`, `options`                                                                              | `Dict`                             |
| `POST`   | `/`                                   | Create Device                 | Body: `Device` model                                                                                                                                   | `{"message": str, "id": str}`      |
| `PATCH`  | `/{entity_id}/attrs`                  | Update Device Attributes      | Path: `entity_id`<br />Body: `Dict[str, NgsiLdAttributePatch]`                                                                                         | `None` (204 No Content)            |
| `PUT`    | `/{entity_id}`                        | Replace Device                | Path: `entity_id`<br />Body: `Device` model                                                                                                            | `None` (204 No Content)            |
| `DELETE` | `/{entity_id}`                        | Delete Device                 | Path: `entity_id`                                                                                                                                      | `None` (204 No Content)            |
| `DELETE` | `/{entity_id}/attrs/{attribute_name}` | Delete Device Attribute       | Path: `entity_id`, `attribute_name`                                                                                                                    | `None` (204 No Content)            |
| `POST`   | `/batch/create`                       | Batch Create Devices          | Body: `BatchOperationRequest`                                                                                                                          | `List[str]` or `{"success": True}` |
| `POST`   | `/batch/upsert`                       | Batch Upsert Devices          | Body: `BatchOperationRequest`<br />Query Params: `options`                                                                                             | `List[str]` or `{"success": True}` |
| `POST`   | `/batch/delete`                       | Batch Delete Devices          | Body: `BatchDeleteRequest`                                                                                                                             | `None` (204 No Content)            |
| `GET`    | `/category/{category}`                | Find devices by category      | Path: `category`<br />Query Params: `limit`, `format`                                                                                                  | `List[Dict]`                       |
| `GET`    | `/low-battery`                        | Find devices with low battery | Query Params: `threshold`, `limit`, `format`                                                                                                           | `List[Dict]`                       |
| `GET`    | `/state/{device_state}`               | Find devices by state         | Path: `device_state`<br />Query Params: `limit`, `format`                                                                                              | `List[Dict]`                       |
| `GET`    | `/property/{controlled_property}`     | Find devices by property      | Path: `controlled_property`<br />Query Params: `limit`, `format`                                                                                       | `List[Dict]`                       |
| `GET`    | `/inactive`                           | Find inactive devices         | Query Params: `days`, `limit`, `format`                                                                                                                | `List[Dict]`                       |
| `GET`    | `/location/nearby`                    | Find devices near location    | Query Params: `lon`, `lat`, `max_distance`, `limit`, `format`, `pick`                                                                                  | `List[Dict]`                       |

## 6. RoadSegment

**Base Path:** `/api/v1/road-segments`

| Method   | Endpoint                          | Description                       | Input                                                                                                                                                  | Output                |
| :------- | :-------------------------------- | :-------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------- | :-------------------- |
| `GET`    | `/`                               | Query RoadSegment Entities        | Query Params: `id`, `q`, `pick`, `attrs`, `georel`, `geometry`, `coordinates`, `geoproperty`, `limit`, `offset`, `count`, `format`, `options`, `local` | `List[Dict]` or `int` |
| `GET`    | `/{entity_id}`                    | Get RoadSegment by ID             | Path: `entity_id`<br />Query Params: `attrs`, `options`                                                                                                | `Dict`                |
| `POST`   | `/`                               | Create RoadSegment Entity         | Body: `Dict`                                                                                                                                           | `Response`            |
| `PATCH`  | `/{entity_id}`                    | Update RoadSegment Entity         | Path: `entity_id`<br />Body: `Dict[str, NgsiLdAttributePatch]`                                                                                         | `Response`            |
| `PUT`    | `/{entity_id}`                    | Replace RoadSegment Entity        | Path: `entity_id`<br />Body: `RoadSegment` or `Dict`                                                                                                   | `Response`            |
| `DELETE` | `/{entity_id}`                    | Delete RoadSegment Entity         | Path: `entity_id`                                                                                                                                      | `Response`            |
| `POST`   | `/batch/create`                   | Batch Create RoadSegment Entities | Body: `BatchOperationRequest`                                                                                                                          | `Response`            |
| `POST`   | `/batch/upsert`                   | Batch Upsert RoadSegment Entities | Body: `BatchOperationRequest`<br />Query Params: `options`                                                                                             | `Response`            |
| `POST`   | `/batch/update`                   | Batch Update RoadSegment Entities | Body: `BatchOperationRequest`<br />Query Params: `options`                                                                                             | `Response`            |
| `POST`   | `/batch/delete`                   | Batch Delete RoadSegment Entities | Body: `BatchDeleteRequest`                                                                                                                             | `Response`            |
| `GET`    | `/by-road-class/{road_class}`     | Query by Road Class               | Path: `road_class`<br />Query Params: `limit`                                                                                                          | `List[Dict]`          |
| `GET`    | `/by-speed-limit`                 | Query by Speed Limit Range        | Query Params: `min_speed`, `max_speed`, `limit`                                                                                                        | `List[Dict]`          |
| `GET`    | `/by-length`                      | Query by Length Range             | Query Params: `min_length`, `max_length`, `limit`                                                                                                      | `List[Dict]`          |
| `GET`    | `/by-lane-count`                  | Query by Lane Count               | Query Params: `min_lanes`, `max_lanes`, `limit`                                                                                                        | `List[Dict]`          |
| `GET`    | `/by-road-name`                   | Query by Road Name                | Query Params: `road_name`, `exact_match`, `limit`                                                                                                      | `List[Dict]`          |
| `GET`    | `/by-status/{status}`             | Query by Status                   | Path: `status`<br />Query Params: `limit`                                                                                                              | `List[Dict]`          |
| `GET`    | `/by-vehicle-type/{vehicle_type}` | Query by Vehicle Type             | Path: `vehicle_type`<br />Query Params: `limit`                                                                                                        | `List[Dict]`          |

## 7. Subscriptions

**Base Path:** `/api/v1/subscriptions`

| Method   | Endpoint             | Description                       | Input                                                                                       | Output                        |
| :------- | :------------------- | :-------------------------------- | :------------------------------------------------------------------------------------------ | :---------------------------- |
| `POST`   | `/`                  | Create a new subscription         | Body: `SubscriptionCreate`<br />Query Params: `tenant`                                      | `{"message": str, "id": str}` |
| `GET`    | `/`                  | Get all subscriptions             | Query Params: `limit`, `offset`, `tenant`                                                   | `List[Dict]`                  |
| `GET`    | `/{subscription_id}` | Get details of a subscription     | Path: `subscription_id`<br />Query Params: `tenant`                                         | `Dict`                        |
| `PATCH`  | `/{subscription_id}` | Update a subscription             | Path: `subscription_id`<br />Body: `SubscriptionUpdate`<br />Query Params: `tenant`         | `None` (204 No Content)       |
| `DELETE` | `/{subscription_id}` | Delete a subscription             | Path: `subscription_id`<br />Query Params: `tenant`                                         | `None` (204 No Content)       |
| `POST`   | `/quick/entity-type` | Quick subscription to entity type | Query Params: `entity_type`, `notification_uri`, `attributes`, `q`, `description`, `tenant` | `{"message": str, "id": str}` |

## 8. TrafficEnvironmentImpact

**Base Path:** `/api/v1/traffic-environment-impact`

| Method   | Endpoint                             | Description                             | Input                                                                                                                                                  | Output                |
| :------- | :----------------------------------- | :-------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------- | :-------------------- |
| `GET`    | `/`                                  | Query TrafficEnvironmentImpact Entities | Query Params: `id`, `q`, `pick`, `attrs`, `georel`, `geometry`, `coordinates`, `geoproperty`, `limit`, `offset`, `count`, `format`, `options`, `local` | `List[Dict]` or `int` |
| `GET`    | `/{entity_id}`                       | Get TrafficEnvironmentImpact by ID      | Path: `entity_id`<br />Query Params: `attrs`, `options`                                                                                                | `Dict`                |
| `POST`   | `/`                                  | Create TrafficEnvironmentImpact Entity  | Body: `Dict`                                                                                                                                           | `Response`            |
| `PATCH`  | `/{entity_id}`                       | Update TrafficEnvironmentImpact Entity  | Path: `entity_id`<br />Body: `Dict[str, NgsiLdAttributePatch]`                                                                                         | `Response`            |
| `PUT`    | `/{entity_id}`                       | Replace TrafficEnvironmentImpact Entity | Path: `entity_id`<br />Body: `TrafficEnvironmentImpact` or `Dict`                                                                                      | `Response`            |
| `DELETE` | `/{entity_id}`                       | Delete TrafficEnvironmentImpact Entity  | Path: `entity_id`                                                                                                                                      | `Response`            |
| `POST`   | `/batch/create`                      | Batch Create Entities                   | Body: `BatchOperationRequest`                                                                                                                          | `Response`            |
| `POST`   | `/batch/upsert`                      | Batch Upsert Entities                   | Body: `BatchOperationRequest`<br />Query Params: `options`                                                                                             | `Response`            |
| `POST`   | `/batch/update`                      | Batch Update Entities                   | Body: `BatchOperationRequest`<br />Query Params: `options`                                                                                             | `Response`            |
| `POST`   | `/batch/delete`                      | Batch Delete Entities                   | Body: `BatchDeleteRequest`                                                                                                                             | `Response`            |
| `GET`    | `/by-co2-range`                      | Query by CO2 Range                      | Query Params: `min_co2`, `max_co2`, `limit`                                                                                                            | `List[Dict]`          |
| `GET`    | `/by-time-range`                     | Query by Time Range                     | Query Params: `start_time`, `end_time`, `limit`                                                                                                        | `List[Dict]`          |
| `GET`    | `/by-vehicle-class/{vehicle_class}`  | Query by Vehicle Class                  | Path: `vehicle_class`<br />Query Params: `limit`                                                                                                       | `List[Dict]`          |
| `GET`    | `/by-traffic-flow/{traffic_flow_id}` | Query by Traffic Flow Reference         | Path: `traffic_flow_id`<br />Query Params: `limit`                                                                                                     | `List[Dict]`          |

## 9. WaterQualityObserved

**Base Path:** `/api/v1/water-quality`

| Method   | Endpoint                              | Description                            | Input                                                                                                                                                  | Output                             |
| :------- | :------------------------------------ | :------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------- | :--------------------------------- |
| `GET`    | `/`                                   | Query WaterQualityObserved Entities    | Query Params: `id`, `q`, `pick`, `attrs`, `georel`, `geometry`, `coordinates`, `geoproperty`, `limit`, `offset`, `count`, `format`, `options`, `local` | `List[Dict]` or `int`              |
| `GET`    | `/{entity_id}`                        | Get WaterQualityObserved by ID         | Path: `entity_id`<br />Query Params: `pick`, `attrs`, `format`, `options`                                                                              | `Dict`                             |
| `POST`   | `/`                                   | Create WaterQualityObserved            | Body: `WaterQualityObserved` model                                                                                                                     | `{"message": str, "id": str}`      |
| `PATCH`  | `/{entity_id}/attrs`                  | Update WaterQualityObserved Attributes | Path: `entity_id`<br />Body: `Dict[str, NgsiLdAttributePatch]`                                                                                         | `None` (204 No Content)            |
| `PUT`    | `/{entity_id}`                        | Replace WaterQualityObserved           | Path: `entity_id`<br />Body: `WaterQualityObserved` model                                                                                              | `None` (204 No Content)            |
| `DELETE` | `/{entity_id}`                        | Delete WaterQualityObserved            | Path: `entity_id`                                                                                                                                      | `None` (204 No Content)            |
| `DELETE` | `/{entity_id}/attrs/{attribute_name}` | Delete Attribute                       | Path: `entity_id`, `attribute_name`                                                                                                                    | `None` (204 No Content)            |
| `POST`   | `/batch/create`                       | Batch Create WaterQualityObserved      | Body: `BatchOperationRequest`                                                                                                                          | `List[str]` or `{"success": True}` |
| `POST`   | `/batch/upsert`                       | Batch Upsert WaterQualityObserved      | Body: `BatchOperationRequest`<br />Query Params: `options`                                                                                             | `List[str]` or `{"success": True}` |
| `POST`   | `/batch/delete`                       | Batch Delete WaterQualityObserved      | Body: `BatchDeleteRequest`                                                                                                                             | `None` (204 No Content)            |
| `GET`    | `/poor-quality/{parameter}`           | Find poor quality water                | Path: `parameter`<br />Query Params: `min_value`, `max_value`, `limit`, `format`                                                                       | `List[Dict]`                       |
| `GET`    | `/contaminated/{contaminant}`         | Find contaminated water                | Path: `contaminant`<br />Query Params: `threshold`, `limit`, `format`                                                                                  | `List[Dict]`                       |
| `GET`    | `/recent`                             | Get recent observations                | Query Params: `since`, `limit`, `format`, `pick`                                                                                                       | `List[Dict]`                       |
| `GET`    | `/location/nearby`                    | Find observations near location        | Query Params: `lon`, `lat`, `max_distance`, `limit`, `format`, `pick`                                                                                  | `List[Dict]`                       |
