"""
AI Service for intelligent traffic light control
"""
import logging
from typing import Optional, Callable, Dict, Any
from ..models.dqn_agent import DQNAgent

logger = logging.getLogger(__name__)


class AIService:
    """Service for AI-powered traffic light control"""
    
    def __init__(
        self,
        model_path: str,
        tls_id: str,
        num_phases: int = 2,
        min_green_steps: int = 100,
        enabled: bool = False
    ):
        """
        Initialize AI Service
        
        Args:
            model_path: Path to DQN model file
            tls_id: Traffic light system ID
            num_phases: Number of traffic light phases
            min_green_steps: Minimum green time in steps (10 steps = 1 second)
            enabled: Whether AI is enabled by default
        """
        self.tls_id = tls_id
        self.num_phases = num_phases
        self.min_green_steps = min_green_steps
        self.enabled = enabled
        
        # Initialize DQN agent
        self.agent = DQNAgent(
            model_path=model_path,
            state_size=4,  # [queue1, queue2, phase, pm25]
            num_actions=2,  # [keep, change]
            use_random_fallback=True
        )
        
        # Callback for sending phase change commands
        self.phase_change_callback: Optional[Callable[[int], None]] = None
        
        # State tracking
        self.current_phase = 0
        self.steps_in_phase = 0
        
        logger.info(f"AI Service initialized for TLS {tls_id}")
        logger.info(f"AI enabled: {enabled}")
    
    def set_phase_change_callback(self, callback: Callable[[int], None]):
        """Set callback function for phase changes"""
        self.phase_change_callback = callback
    
    def process_state(self, state_data: Dict[str, Any]) -> Optional[int]:
        """
        Process current state and decide action
        
        Args:
            state_data: Dictionary containing:
                - queues: List[float] - Queue lengths
                - phase: int - Current phase
                - pm25: float - Air quality (PM2.5)
        
        Returns:
            New phase number if change is needed, None otherwise
        """
        if not self.enabled:
            return None
        
        try:
            # Extract state components
            queues = state_data.get('queues', [0, 0])
            phase = state_data.get('phase', 0)
            pm25 = state_data.get('pm25', 0)
            
            # Build state vector
            state = [*queues, phase, pm25]
            
            # Update tracking
            self.current_phase = phase
            self.steps_in_phase += 1
            
            # Get action from agent
            action = self.agent.get_action(state)
            
            logger.debug(f"State: {state}, Action: {action}, Steps in phase: {self.steps_in_phase}")
            
            # Action 1 = change phase
            if action == 1 and self.steps_in_phase >= self.min_green_steps:
                next_phase = (phase + 1) % self.num_phases
                self.steps_in_phase = 0  # Reset counter
                
                logger.info(f"AI decision: Change phase from {phase} to {next_phase}")
                
                # Execute phase change via callback
                if self.phase_change_callback:
                    self.phase_change_callback(next_phase)
                
                return next_phase
            
            return None
            
        except Exception as e:
            logger.error(f"Error processing state: {e}")
            return None
    
    def enable(self):
        """Enable AI control"""
        self.enabled = True
        logger.info("AI control enabled")
    
    def disable(self):
        """Disable AI control"""
        self.enabled = False
        logger.info("AI control disabled")
    
    def toggle(self) -> bool:
        """Toggle AI control"""
        self.enabled = not self.enabled
        logger.info(f"AI control {'enabled' if self.enabled else 'disabled'}")
        return self.enabled
    
    def reload_model(self):
        """Reload the AI model"""
        logger.info("Reloading AI model...")
        self.agent.reload_model()
    
    def get_status(self) -> dict:
        """Get AI service status"""
        return {
            "enabled": self.enabled,
            "tls_id": self.tls_id,
            "num_phases": self.num_phases,
            "min_green_steps": self.min_green_steps,
            "current_phase": self.current_phase,
            "steps_in_phase": self.steps_in_phase,
            "agent_info": self.agent.get_info()
        }
