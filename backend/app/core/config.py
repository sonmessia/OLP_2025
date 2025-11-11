from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "OLP 2025 Core Backend Service"
    app_version: str = "1.0.0"

    class Config:
        env_file = ".env"


settings = Settings()
