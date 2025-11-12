import requests

ORION_LD_URL = "http://orion-ld:1026/ngsi-ld/v1"

class SubscriptionService:
    @staticmethod
    def create_subscription(subscription_data):
        url = f"{ORION_LD_URL}/subscriptions"
        headers = {
            "Content-Type": "application/ld+json"
        }
        response = requests.post(url, json=subscription_data, headers=headers)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def get_all_subscriptions():
        url = f"{ORION_LD_URL}/subscriptions"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def get_subscription_by_id(subscription_id):
        url = f"{ORION_LD_URL}/subscriptions/{subscription_id}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def update_subscription(subscription_id, update_data):
        url = f"{ORION_LD_URL}/subscriptions/{subscription_id}"
        headers = {
            "Content-Type": "application/ld+json"
        }
        response = requests.patch(url, json=update_data, headers=headers)
        response.raise_for_status()
        return response.status_code

    @staticmethod
    def delete_subscription(subscription_id):
        url = f"{ORION_LD_URL}/subscriptions/{subscription_id}"
        response = requests.delete(url)
        response.raise_for_status()
        return response.status_code