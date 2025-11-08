from pysmartdatamodels import pysmartdatamodels as sdm
import subprocess
import json

# --------------------------
# 1️⃣ Thông tin cấu hình
# --------------------------
serverUrl = "http://localhost:1026"
dataModel = "CarbonFootprint"
subject = "dataModel.Environment"

# --------------------------
# 2️⃣ Dữ liệu nhiều thuộc tính cùng lúc
# --------------------------
attributes = {
    "emissionSource": "Transport",
    "CO2eq": 25.5,
    "emissionDate": "2025-05-12T10:00:00Z",
    "relatedSource": "urn:ngsi-ld:Source:001",
}

# --------------------------
# 3️⃣ Gửi toàn bộ thuộc tính trong một lần
# --------------------------
# Thực thi cập nhật tới Orion-LD broker

for key, value in attributes.items():
    print(f"Thuộc tính '{key}': {json.dumps(value)}")
    print(
        sdm.update_broker(
            dataModel,
            subject,
            key,
            value,
            serverUrl=serverUrl,
            updateThenCreate=True,
        )
    )

# --------------------------
# 4️⃣ Kiểm tra kết quả
# --------------------------
print("\nKiểm tra các entity hiện có trong broker:")
command = [
    "curl",
    "-X",
    "GET",
    "http://localhost:1026/ngsi-ld/v1/entities?local=true&limit=1000",
]
try:
    result = subprocess.run(command, capture_output=True, text=True, check=True)
    print(result.stdout)
except subprocess.CalledProcessError as e:
    print(f"Error executing curl command: {e}")
    print(f"stderr: {e.stderr}")
