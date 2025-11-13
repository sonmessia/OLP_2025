import requests

ORION_LD_URL = "http://fiware-orionld:1026/ngsi-ld/v1"


class AirQualityService:
    @staticmethod
    def get_all_entities(local=True):
        url = f"{ORION_LD_URL}/entities"
        headers = {
            "Accept": "application/ld+json",
            "Link": '<http://context/datamodels.context-ngsi.jsonld>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"',
        }
        params = {"local": "true" if local else "false", "type": "AirQualityObserved"}
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching all entities: {e}")
            print(f"Response content: {response.text if response else 'No response'}")
            raise

    @staticmethod
    def get_entity_by_id(entity_id, local=True):
        url = f"{ORION_LD_URL}/entities/{entity_id}"
        headers = {
            "Accept": "application/ld+json",
            "Link": '<http://context/datamodels.context-ngsi.jsonld>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"',
        }
        params = {"local": local}
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching entity by ID {entity_id}: {e}")
            print(f"Response content: {response.text if response else 'No response'}")
            raise

    @staticmethod
    def create_entity(entity_data, local=True):
        url = f"{ORION_LD_URL}/entities"
        headers = {"Content-Type": "application/ld+json"}
        params = {"local": local}
        try:
            response = requests.post(
                url, json=entity_data, headers=headers, params=params
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error creating entity: {e}")
            print(f"Response content: {response.text if response else 'No response'}")
            raise

    @staticmethod
    def update_entity(entity_id, update_data, local=True):
        url = f"{ORION_LD_URL}/entities/{entity_id}/attrs"
        headers = {"Content-Type": "application/ld+json"}
        params = {"local": local}
        try:
            response = requests.patch(
                url, json=update_data, headers=headers, params=params
            )
            response.raise_for_status()
            return response.status_code
        except requests.exceptions.RequestException as e:
            print(f"Error updating entity {entity_id}: {e}")
            print(f"Response content: {response.text if response else 'No response'}")
            raise

    @staticmethod
    def delete_entity(entity_id, local=True):
        url = f"{ORION_LD_URL}/entities/{entity_id}"
        params = {"local": local}
        try:
            response = requests.delete(url, params=params)
            response.raise_for_status()
            return response.status_code
        except requests.exceptions.RequestException as e:
            print(f"Error deleting entity {entity_id}: {e}")
            print(f"Response content: {response.text if response else 'No response'}")
            raise
