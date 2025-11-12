import requests

ORION_LD_URL = "http://orion-ld:1026/ngsi-ld/v1"

class DeviceService:
    @staticmethod
    def get_all_entities():
        url = f"{ORION_LD_URL}/entities"
        headers = {
            "Accept": "application/ld+json",
            "Link": '<http://context-url>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def get_entity_by_id(entity_id):
        url = f"{ORION_LD_URL}/entities/{entity_id}"
        headers = {
            "Accept": "application/ld+json",
            "Link": '<http://context-url>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def create_entity(entity_data):
        url = f"{ORION_LD_URL}/entities"
        headers = {
            "Content-Type": "application/ld+json"
        }
        response = requests.post(url, json=entity_data, headers=headers)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def update_entity(entity_id, update_data):
        url = f"{ORION_LD_URL}/entities/{entity_id}/attrs"
        headers = {
            "Content-Type": "application/ld+json"
        }
        response = requests.patch(url, json=update_data, headers=headers)
        response.raise_for_status()
        return response.status_code

    @staticmethod
    def delete_entity(entity_id):
        url = f"{ORION_LD_URL}/entities/{entity_id}"
        response = requests.delete(url)
        response.raise_for_status()
        return response.status_code