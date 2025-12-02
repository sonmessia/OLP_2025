import requests
import sys
import time

def connect_sumo():
    url = "http://localhost:8000/sumo/connect"
    payload = {
        "host": "host.docker.internal",
        "port": 8813,
        "scenario": "Nga4ThuDuc"
    }
    
    print(f"🔌 Connecting to Backend at {url}...")
    print(f"   Payload: {payload}")
    print("   (This might take up to 10 seconds...)")
    
    try:
        # Set a timeout of 10 seconds
        response = requests.post(url, json=payload, timeout=10)
        
        if response.status_code == 200:
            print("\n✅ SUCCESS: Connected to SUMO!")
            print(response.json())
        else:
            print(f"\n❌ FAILED: Status {response.status_code}")
            print(response.text)
            
    except requests.exceptions.Timeout:
        print("\n❌ TIMEOUT: Backend did not respond in 10 seconds.")
        print("   Possible causes:")
        print("   1. Windows Firewall is blocking port 8813.")
        print("   2. SUMO is not running.")
        print("   3. Docker cannot reach host.docker.internal.")
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Could not connect to Backend (localhost:8000)")
        print("   Make sure Docker containers are running: docker-compose up -d")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")

if __name__ == "__main__":
    connect_sumo()
