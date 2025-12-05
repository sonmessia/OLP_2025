"""
DQN Model Architecture and Management
"""
import logging
import os
from typing import Optional, Tuple

import numpy as np

logger = logging.getLogger(__name__)


class DQNModel:
    """Deep Q-Network Model Wrapper"""
    
    def __init__(self, model_path: Optional[str] = None, state_size: int = 4, action_size: int = 2):
        self.model_path = model_path or "dqn_model.keras"
        self.state_size = state_size
        self.action_size = action_size
        self.model = None
        self.loaded = False
        
        # Try to load model
        if os.path.exists(self.model_path):
            self.load_model()
    
    def build_model(self, learning_rate: float = 0.0005):
        """
        Build DQN model architecture
        128-128-64 with Dropout(0.2)
        """
        try:
            from tensorflow import keras
            from tensorflow.keras import layers
            
            model = keras.Sequential([
                layers.Input(shape=(self.state_size,)),
                layers.Dense(128, activation='relu', kernel_initializer='he_normal'),
                layers.Dropout(0.2),
                layers.Dense(128, activation='relu', kernel_initializer='he_normal'),
                layers.Dropout(0.2),
                layers.Dense(64, activation='relu', kernel_initializer='he_normal'),
                layers.Dense(self.action_size, activation='linear')
            ])
            
            model.compile(
                loss='mse',
                optimizer=keras.optimizers.Adam(learning_rate=learning_rate)
            )
            
            self.model = model
            logger.info("[DQN] Model built successfully")
            return model
            
        except ImportError as e:
            logger.error(f"[DQN] TensorFlow not available: {e}")
            return None
    
    def load_model(self):
        """Load pre-trained model from file"""
        try:
            from tensorflow import keras
            
            logger.info(f"[DQN] Loading model from {self.model_path}...")
            self.model = keras.models.load_model(self.model_path, compile=False)
            self.loaded = True
            logger.info("[DQN] ✅ Model loaded successfully")
            
            # Log architecture
            total_params = sum([np.prod(w.shape) for w in self.model.get_weights()])
            logger.info(f"[DQN] Total parameters: {total_params:,}")
            
            return True
            
        except ImportError:
            logger.warning("[DQN] TensorFlow not available - running in random mode")
            return False
        except Exception as e:
            logger.error(f"[DQN] Error loading model: {e}")
            return False
    
    def save_model(self, path: Optional[str] = None):
        """Save model to file"""
        if self.model is None:
            logger.warning("[DQN] No model to save")
            return False
        
        save_path = path or self.model_path
        
        try:
            self.model.save(save_path)
            logger.info(f"[DQN] Model saved to {save_path}")
            return True
        except Exception as e:
            logger.error(f"[DQN] Error saving model: {e}")
            return False
    
    def predict(self, state: Tuple) -> int:
        """
        Predict best action for given state
        
        Args:
            state: (queue_1, queue_2, current_phase, pm25)
        
        Returns:
            action: 0 (hold) or 1 (switch)
        """
        if self.model is None or not self.loaded:
            # Fallback to random
            import random
            action = random.choice([0, 1])
            logger.debug(f"[DQN] Random action: {action}")
            return action
        
        try:
            state_array = np.array(state, dtype=np.float32).reshape((1, -1))
            q_values = self.model.predict(state_array, verbose=0)[0]
            action = int(np.argmax(q_values))
            logger.debug(f"[DQN] State: {state} → Q: {q_values} → Action: {action}")
            return action
            
        except Exception as e:
            logger.error(f"[DQN] Prediction error: {e}")
            import random
            return random.choice([0, 1])
    
    def get_q_values(self, state: Tuple) -> Optional[np.ndarray]:
        """Get Q-values for state"""
        if self.model is None:
            return None
        
        try:
            state_array = np.array(state, dtype=np.float32).reshape((1, -1))
            return self.model.predict(state_array, verbose=0)[0]
        except Exception as e:
            logger.error(f"[DQN] Error getting Q-values: {e}")
            return None
    
    def get_info(self) -> dict:
        """Get model information"""
        if not self.loaded or self.model is None:
            return {
                "loaded": False,
                "mode": "random",
                "message": "Running in random mode (no model loaded)"
            }
        
        try:
            total_params = sum([np.prod(w.shape) for w in self.model.get_weights()])
            
            return {
                "loaded": True,
                "mode": "dqn",
                "path": self.model_path,
                "total_parameters": int(total_params),
                "input_shape": str(self.model.input_shape),
                "output_shape": str(self.model.output_shape),
                "state_size": self.state_size,
                "action_size": self.action_size
            }
        except Exception as e:
            return {
                "loaded": True,
                "mode": "dqn",
                "error": str(e)
            }
