"""
Smart Traffic Light Controller
Thuật toán điều hướng giao thông ĐÚNG:
- Phân tích từng traffic light độc lập
- Chọn phase dựa trên mật độ xe thực tế
- Đảm bảo không xung đột (không cho tất cả đèn xanh cùng lúc!)
"""
import logging
from typing import Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)

try:
    import traci
    _TRACI_AVAILABLE = True
except ImportError:
    _TRACI_AVAILABLE = False
    logger.warning("TraCI not available")


class SmartTrafficController:
    """
    Controller thông minh cho giao thông
    
    Nguyên lý:
    1. Thu thập dữ liệu: occupancy, queue length từ các lanes
    2. Tính điểm ưu tiên cho mỗi hướng
    3. Chọn phase cho đèn xanh ở hướng ưu tiên cao nhất
    4. Đảm bảo thời gian tối thiểu cho mỗi phase (tránh nhấp nháy)
    """
    
    def __init__(self, tls_id: str, min_green_time: int = 10):
        """
        Args:
            tls_id: Traffic light system ID
            min_green_time: Thời gian tối thiểu cho đèn xanh (giây)
        """
        self.tls_id = tls_id
        self.min_green_time = min_green_time
        self.current_phase = 0
        self.phase_start_time = 0
        
    def get_lane_metrics(self, lane_id: str) -> Dict:
        """Lấy metrics của một lane"""
        if not _TRACI_AVAILABLE:
            return {}
            
        try:
            return {
                'occupancy': traci.lane.getLastStepOccupancy(lane_id),
                'queue_length': traci.lane.getLastStepHaltingNumber(lane_id),
                'waiting_time': traci.lane.getWaitingTime(lane_id),
                'vehicle_count': traci.lane.getLastStepVehicleNumber(lane_id)
            }
        except Exception as e:
            logger.error(f"Failed to get metrics for lane {lane_id}: {e}")
            return {}
    
    def calculate_phase_priority(self, phase_index: int) -> float:
        """Tính độ ưu tiên của một phase dựa trên traffic metrics"""
        if not _TRACI_AVAILABLE:
            return 0.0
            
        try:
            logic = traci.trafficlight.getAllProgramLogics(self.tls_id)[0]
            phase = logic.phases[phase_index]
            state = phase.state
            
            controlled_lanes = traci.trafficlight.getControlledLanes(self.tls_id)
            green_lanes = [
                lane for i, lane in enumerate(controlled_lanes) 
                if i < len(state) and state[i] in ['G', 'g']
            ]
            
            if not green_lanes:
                return 0.0
            
            total_occupancy = 0
            total_queue = 0
            total_waiting = 0
            valid_lanes = 0
            
            for lane in green_lanes:
                metrics = self.get_lane_metrics(lane)
                if metrics:
                    total_occupancy += metrics.get('occupancy', 0)
                    total_queue += metrics.get('queue_length', 0)
                    total_waiting += metrics.get('waiting_time', 0)
                    valid_lanes += 1
            
            if valid_lanes == 0:
                return 0.0
            
            avg_occupancy = total_occupancy / valid_lanes
            avg_queue = min(total_queue / (valid_lanes * 10), 1.0)
            avg_waiting = min(total_waiting / (valid_lanes * 60), 1.0)
            
            priority = 0.30 * avg_occupancy + 0.40 * avg_queue + 0.30 * avg_waiting
            
            logger.debug(f"Phase {phase_index} priority: {priority:.2f}")
            
            return priority
            
        except Exception as e:
            logger.error(f"Failed to calculate priority for phase {phase_index}: {e}")
            return 0.0
    
    def select_best_phase(self) -> int:
        """Chọn phase tối ưu dựa trên traffic conditions"""
        if not _TRACI_AVAILABLE:
            return 0
            
        try:
            current_time = traci.simulation.getTime()
            time_in_phase = current_time - self.phase_start_time
            
            if time_in_phase < self.min_green_time:
                logger.debug(f"Keeping phase {self.current_phase} (only {time_in_phase}s elapsed)")
                return self.current_phase
            
            logic = traci.trafficlight.getAllProgramLogics(self.tls_id)[0]
            num_phases = len(logic.phases)
            
            priorities = {}
            for i in range(num_phases):
                phase_state = logic.phases[i].state
                if 'G' not in phase_state and 'g' not in phase_state:
                    continue
                    
                priorities[i] = self.calculate_phase_priority(i)
            
            if not priorities:
                return self.current_phase
            
            best_phase = max(priorities.items(), key=lambda x: x[1])[0]
            
            current_priority = priorities.get(self.current_phase, 0)
            best_priority = priorities[best_phase]
            
            if best_phase != self.current_phase:
                if best_priority > current_priority + 0.15:
                    logger.info(f"🚦 Switching from phase {self.current_phase} to {best_phase}")
                    self.current_phase = best_phase
                    self.phase_start_time = current_time
            
            return self.current_phase
            
        except Exception as e:
            logger.error(f"Failed to select best phase: {e}")
            return self.current_phase
    
    def get_phase_explanation(self, phase_index: int) -> str:
        """Giải thích phase này cho phép xe đi theo hướng nào"""
        if not _TRACI_AVAILABLE:
            return "Unknown"
            
        try:
            logic = traci.trafficlight.getAllProgramLogics(self.tls_id)[0]
            phase = logic.phases[phase_index]
            state = phase.state
            
            controlled_lanes = traci.trafficlight.getControlledLanes(self.tls_id)
            
            green_directions = []
            for i, signal in enumerate(state):
                if signal in ['G', 'g'] and i < len(controlled_lanes):
                    lane = controlled_lanes[i]
                    green_directions.append(lane)
            
            if not green_directions:
                return "All red (clearance phase)"
            
            return f"Green for: {', '.join(green_directions[:3])}{'...' if len(green_directions) > 3 else ''}"
            
        except Exception as e:
            return f"Error: {e}"
