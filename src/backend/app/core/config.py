# Copyright (c) 2025 Green Wave Team
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "OLP 2025 Core Backend Service"
    app_version: str = "1.0.0"

    class Config:
        env_file = ".env"


settings = Settings()
