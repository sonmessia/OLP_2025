"""
SUMO RL - Reinforcement Learning for Traffic Light Control
Integrated into FastAPI Backend
"""

__version__ = "1.0.0"
__author__ = "OLP 2025 Team"

# Export main components
from app.sumo_rl.agents.ai_agent import AIGreenWaveAgent
from app.sumo_rl.agents.iot_agent import IoTAgent
from app.sumo_rl.models.dqn_model import DQNModel

# from app.sumo_rl.environment.sumo_env import SumoEnvironment
# TODO: Create this file if needed

__all__ = [
    "AIGreenWaveAgent",
    "IoTAgent",
    # "SumoEnvironment",
    "DQNModel",
]
