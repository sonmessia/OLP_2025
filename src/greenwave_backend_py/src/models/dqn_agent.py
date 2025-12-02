"""
DQN Agent for traffic light control
"""
import os
import numpy as np
from typing import Optional, List
import logging

logger = logging.getLogger(__name__)


class DQNAgent:
    """Deep Q-Network Agent for traffic light control"""
    
    def __init__(
        self,
        model_path: str,
        state_size: int = 4,
        num_actions: int = 2,
        use_random_fallback: bool = True
    ):
        """
        Initialize DQN Agent
        
        Args:
            model_path: Path to the trained model file (.h5)
            state_size: Size of state vector (default: 4 for 2 queues + phase + pm25)
            num_actions: Number of possible actions (default: 2 for keep/change phase)
            use_random_fallback: Use random action if model not available
        """
        self.model_path = model_path
        self.state_size = state_size
        self.num_actions = num_actions
        self.use_random_fallback = use_random_fallback
        self.model: Optional[any] = None
        self.is_loaded = False
        
        self._load_model()
    
    def _load_model(self):
        """Load the DQN model from file"""
        try:
            import tensorflow as tf
            from tensorflow import keras
            
            if os.path.exists(self.model_path):
                logger.info(f"Loading DQN model from {self.model_path}")
                self.model = keras.models.load_model(self.model_path, compile=False)
                self.is_loaded = True
                logger.info("DQN model loaded successfully")
            else:
                logger.warning(f"Model file not found: {self.model_path}")
                if self.use_random_fallback:
                    logger.info("Will use random action selection as fallback")
                else:
                    raise FileNotFoundError(f"Model file not found: {self.model_path}")
        except ImportError as e:
            logger.error(f"TensorFlow/Keras not available: {e}")
            if not self.use_random_fallback:
                raise
            logger.info("Will use random action selection as fallback")
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            if not self.use_random_fallback:
                raise
            logger.info("Will use random action selection as fallback")
    
    def get_action(self, state: List[float]) -> int:
        """
        Get action from the agent given current state
        
        Args:
            state: Current state vector [queue1, queue2, phase, pm25]
        
        Returns:
            Action index (0: keep phase, 1: change phase)
        """
        if self.is_loaded and self.model is not None:
            try:
                # Prepare state for prediction
                state_array = np.array(state, dtype=np.float32).reshape((1, -1))
                
                # Get Q-values from model
                q_values = self.model.predict(state_array, verbose=0)[0]
                
                # Return action with highest Q-value
                action = int(np.argmax(q_values))
                
                logger.debug(f"State: {state}, Q-values: {q_values}, Action: {action}")
                return action
            except Exception as e:
                logger.error(f"Error during prediction: {e}")
                if self.use_random_fallback:
                    return self._random_action()
                raise
        else:
            # Fallback to random action
            return self._random_action()
    
    def _random_action(self) -> int:
        """Get random action"""
        import random
        action = random.choice(range(self.num_actions))
        logger.debug(f"Random action: {action}")
        return action
    
    def reload_model(self):
        """Reload the model from file"""
        logger.info("Reloading DQN model...")
        self.is_loaded = False
        self.model = None
        self._load_model()
    
    def get_info(self) -> dict:
        """Get agent information"""
        return {
            "model_path": self.model_path,
            "is_loaded": self.is_loaded,
            "state_size": self.state_size,
            "num_actions": self.num_actions,
            "use_random_fallback": self.use_random_fallback,
            "model_exists": os.path.exists(self.model_path)
        }
