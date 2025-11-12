import requests

ORION_LD_URL = "http://orion-ld:1026/ngsi-ld/v1"

class ContextSourceService:
    @staticmethod
    def create_context_source(context_source_data):
        url = f"{ORION_LD_URL}/csourceRegistrations"
        headers = {
            "Content-Type": "application/ld+json"
        }
        response = requests.post(url, json=context_source_data, headers=headers)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def get_all_context_sources():
        url = f"{ORION_LD_URL}/csourceRegistrations"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def get_context_source_by_id(context_source_id):
        url = f"{ORION_LD_URL}/csourceRegistrations/{context_source_id}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def update_context_source(context_source_id, update_data):
        url = f"{ORION_LD_URL}/csourceRegistrations/{context_source_id}"
        headers = {
            "Content-Type": "application/ld+json"
        }
        response = requests.patch(url, json=update_data, headers=headers)
        response.raise_for_status()
        return response.status_code

    @staticmethod
    def delete_context_source(context_source_id):
        url = f"{ORION_LD_URL}/csourceRegistrations/{context_source_id}"
        response = requests.delete(url)
        response.raise_for_status()
        return response.status_code