"""
Configuration settings for GreenWave Backend
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings"""
    
    # Server
    port: int = 3001
    host: str = "0.0.0.0"
    
    # Orion Context Broker
    orion_url: str = "http://localhost:1026/ngsi-ld/v1"
    
    # WebSocket
    ws_port: int = 8765
    
    # Traffic Light
    tls_id: str = "4066470692"
    
    # Simulation
    update_interval: int = 2000  # milliseconds
    
    # AI Settings
    ai_enabled: bool = False
    ai_model_path: str = "models/dqn_model.h5"
    ai_num_phases: int = 2
    ai_min_green_steps: int = 100  # 10 seconds at 0.1s step length
    
    # SUMO Settings
    sumo_enabled: bool = False
    sumo_config_path: str = "sumo_files/Nga4ThuDuc/Nga4ThuDuc.sumocfg"
    sumo_use_gui: bool = False
    sumo_step_length: float = 1.0
    sumo_detector_ids: str = "e2_0,e2_2"  # Comma-separated
    sumo_edge_ids: str = "1106838009#1,720360980,720360983#1,720360983#2"  # Comma-separated
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
