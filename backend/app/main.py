from fastapi import FastAPI
from app.api.routers import alerts

app = FastAPI(
    title="OLP 2025 Core Backend Service",
    description="Receives NGSI-LD notifications and handles business logic.",
    version="1.0.0",
)

app.include_router(alerts.router)


@app.get("/")
def read_root():
    """Endpoint cơ bản để kiểm tra service có đang chạy không"""
    return {"message": "Core Backend Service is running!"}
