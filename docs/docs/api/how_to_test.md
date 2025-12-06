---
sidebar_position: 2
title: How To Test
---

# How To Test

This guide provides instructions on how to test the GreenWave API using Postman. It covers setting up the environment, configuring authorization, and constructing requests.

## Prerequisites

1. Download and install Postman.
2. Ensure the backend server is running and accessible.

## 1. Environment Setup

Using environments in Postman allows you to switch between different setups (e.g., Local, Development, Production) easily without changing the request URLs manually.

1. Open Postman and go to the **Environments** tab on the left sidebar.
2. Click **Create Environment**.
3. Name the environment (e.g., `GreenWave Local`).
4. Add the following variable:

| Variable  | Type    | Initial Value           | Current Value           |
| :-------- | :------ | :---------------------- | :---------------------- |
| `baseUrl` | Default | `http://localhost:8000` | `http://localhost:8000` |

5. Click **Save**.
6. Select this environment from the environment dropdown in the top right corner.

## 2. Authorization

If the API requires authentication, configure it at the Collection level so it applies to all requests.

1. Create a new Collection in Postman (e.g., `GreenWave API`).
2. Select the Collection and go to the **Authorization** tab.
3. Select the appropriate Type (e.g., **Bearer Token** or **API Key**).
4. Enter your token or key.
   - If using a variable, enter `{{authToken}}` in the Token field and add `authToken` to your Environment variables.
5. Click **Save**.

## 3. Constructing Requests

When creating requests, use the `{{baseUrl}}` variable followed by the specific endpoint path.

### GET Request

Used to retrieve data.

**Example: Query AirQualityObserved Entities**

1. Create a new request.
2. Set the method to **GET**.
3. Enter the URL: `{{baseUrl}}/api/v1/air-quality`
4. **Params** (Optional): Add query parameters to filter results.
   - Key: `limit`, Value: `10`
   - Key: `format`, Value: `keyValues`
5. Click **Send**.

### POST Request

Used to create new entities. Requires a JSON body.

**Example: Create AirQualityObserved Entity**

1. Create a new request.
2. Set the method to **POST**.
3. Enter the URL: `{{baseUrl}}/api/v1/air-quality`
4. Go to the **Body** tab.
5. Select **raw** and choose **JSON** from the dropdown.
6. Enter the JSON payload:

```json
{
  "id": "urn:ngsi-ld:AirQualityObserved:001",
  "type": "AirQualityObserved",
  "dateObserved": {
    "type": "Property",
    "value": "2023-10-01T12:00:00Z"
  },
  "NO2": {
    "type": "Property",
    "value": 45
  },
  "location": {
    "type": "GeoProperty",
    "value": {
      "type": "Point",
      "coordinates": [-3.70379, 40.416775]
    }
  }
}
```

7. Click **Send**.

### PATCH Request

Used to update existing entities partially.

**Example: Update Entity Attributes**

1. Create a new request.
2. Set the method to **PATCH**.
3. Enter the URL: `{{baseUrl}}/api/v1/air-quality/urn:ngsi-ld:AirQualityObserved:001/attrs`
4. Go to the **Body** tab.
5. Select **raw** and choose **JSON**.
6. Enter the JSON payload (NGSI-LD Attribute Patch):

```json
{
  "NO2": {
    "type": "Property",
    "value": 50
  }
}
```

7. Click **Send**.

### DELETE Request

Used to remove entities.

**Example: Delete AirQualityObserved Entity**

1. Create a new request.
2. Set the method to **DELETE**.
3. Enter the URL: `{{baseUrl}}/api/v1/air-quality/urn:ngsi-ld:AirQualityObserved:001`
4. Click **Send**.

## 4. Batch Operations

For bulk actions, use the batch endpoints.

**Example: Batch Create Entities**

1. Create a new request.
2. Set the method to **POST**.
3. Enter the URL: `{{baseUrl}}/api/v1/air-quality/batch/create`
4. Body (JSON):

```json
{
  "entities": [
    {
      "id": "urn:ngsi-ld:AirQualityObserved:002",
      "type": "AirQualityObserved",
      "NO2": { "type": "Property", "value": 30 }
    },
    {
      "id": "urn:ngsi-ld:AirQualityObserved:003",
      "type": "AirQualityObserved",
      "NO2": { "type": "Property", "value": 25 }
    }
  ]
}
```

## 5. Testing Workflow Example

To verify the lifecycle of an entity, follow this sequence:

1. **Create**: Send a POST request to create a new entity. Verify the response is `201 Created` or returns the ID.
2. **Read**: Send a GET request using the ID from the previous step. Verify the returned data matches what was sent.
3. **Update**: Send a PATCH request to modify a property. Verify the response is `204 No Content`.
4. **Verify Update**: Send a GET request again. Verify the property value has changed.
5. **Delete**: Send a DELETE request. Verify the response is `204 No Content`.
6. **Verify Delete**: Send a GET request. Verify the response is `404 Not Found`.
