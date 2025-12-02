"""
Configuration for SUMO RL System
"""
import os
from pydantic_settings import BaseSettings


class SumoRLConfig(BaseSettings):
    """SUMO RL Configuration"""
    
    # Orion-LD Configuration
    orion_url: str = "http://localhost:1026/ngsi-ld/v1"
    
    # Traffic Light Configuration
    tls_id: str = "4066470692"  # Nga4ThuDuc junction
    num_phases: int = 2
    min_green_steps: int = 100
    
    # SUMO Configuration
    sumo_config_path: str = "sumo_files/Nga4ThuDuc/Nga4ThuDuc.sumocfg"
    edge_ids: list = ["720360980", "720360983#1", "1106838009#1"]
    detector_ids: list = ["e2_0", "e2_2"]
    
    # DQN Model Configuration
    model_path: str = "dqn_model.keras"
    state_size: int = 4
    action_size: int = 2
    
    # Training Configuration
    gamma: float = 0.95
    epsilon_start: float = 1.0
    epsilon_end: float = 0.01
    epsilon_decay_steps: int = 7000
    learning_rate: float = 0.0005
    replay_buffer_size: int = 10000
    batch_size: int = 64
    target_update_freq: int = 200
    
    # Reward Weights
    w_traffic: float = 0.6  # Traffic flow priority
    w_env: float = 0.4      # Environmental priority
    
    # Agent Configuration
    ai_agent_host: str = "0.0.0.0"
    ai_agent_port: int = 5000
    iot_agent_host: str = "0.0.0.0"
    iot_agent_port: int = 4041
    
    class Config:
        env_file = ".env"
        env_prefix = "SUMO_RL_"


# Global config instance
config = SumoRLConfig()
