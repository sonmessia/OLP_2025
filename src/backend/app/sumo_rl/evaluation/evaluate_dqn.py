#!/usr/bin/env python3
"""
Script đánh giá DQN Model với metrics chi tiết
So sánh: Baseline (Fixed-time) vs DQN vs Random
"""

import os
import sys

# Force CPU only to avoid GPU/CUDA issues
os.environ['CUDA_VISIBLE_DEVICES'] = ''

import numpy as np
import matplotlib.pyplot as plt
import json
from datetime import datetime
from collections import defaultdict

# SUMO imports
_SUMO_AVAILABLE = False
try:
    if 'SUMO_HOME' in os.environ:
        tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
        sys.path.append(tools)
    import traci
    _SUMO_AVAILABLE = True
except ImportError:
    print("Warning: SUMO/TraCI not available", file=sys.stderr)
    traci = None

# TensorFlow imports
import tensorflow as tf
from tensorflow import keras

# Configuration
SUMO_CONFIG_BASE = [
    'sumo',
    '-c', 'sumo_files/Nga4ThuDuc/Nga4ThuDuc.sumocfg',
    '--step-length', '0.1',
    '--lateral-resolution', '0',
    '--no-step-log', 'true',
    '--no-warnings', 'true'
]

EVALUATION_STEPS = 3600  # 360 giây = 6 phút
TLS_ID = "4066470692"
DETECTOR_IDS = ["e2_0", "e2_2"]
EDGE_IDS = ["720360980", "720360983#1", "1106838009#1"]
STATE_SIZE = 4
ACTION_SIZE = 2
MIN_GREEN_STEPS = 100


class TrafficMetrics:
    """Class để thu thập và tính toán metrics"""
    
    def __init__(self):
        self.reset()
    
    def reset(self):
        """Reset tất cả metrics"""
        self.total_waiting_time = 0
        self.total_queue_length = []
        self.total_throughput = 0
        self.total_pm25 = []
        self.total_co2 = []
        self.total_fuel = []
        self.phase_changes = 0
        self.avg_speed = []
        self.last_phase = -1
        self.step_count = 0
        
    def update(self, step):
        """Cập nhật metrics cho mỗi step"""
        self.step_count += 1
        
        # 1. Waiting Time (tổng thời gian chờ của tất cả xe)
        waiting_time = 0
        vehicle_ids = traci.vehicle.getIDList()
        for vid in vehicle_ids:
            waiting_time += traci.vehicle.getWaitingTime(vid)
        self.total_waiting_time += waiting_time
        
        # 2. Queue Length (số xe đang chờ tại detector)
        queue_length = sum([traci.lanearea.getLastStepHaltingNumber(det) 
                           for det in DETECTOR_IDS])
        self.total_queue_length.append(queue_length)
        
        # 3. Throughput (số xe đã hoàn thành hành trình)
        self.total_throughput = traci.simulation.getArrivedNumber()
        
        # 4. Emissions (PM2.5, CO2, Fuel)
        pm25 = sum([traci.edge.getPMxEmission(edge) * 0.1 for edge in EDGE_IDS])
        co2 = sum([traci.edge.getCO2Emission(edge) * 0.1 for edge in EDGE_IDS])
        fuel = sum([traci.edge.getFuelConsumption(edge) * 0.1 for edge in EDGE_IDS])
        
        self.total_pm25.append(pm25)
        self.total_co2.append(co2)
        self.total_fuel.append(fuel)
        
        # 5. Average Speed
        speeds = [traci.vehicle.getSpeed(vid) for vid in vehicle_ids]
        avg_speed = np.mean(speeds) if speeds else 0
        self.avg_speed.append(avg_speed)
        
        # 6. Phase Changes
        current_phase = traci.trafficlight.getPhase(TLS_ID)
        if self.last_phase != -1 and current_phase != self.last_phase:
            self.phase_changes += 1
        self.last_phase = current_phase
    
    def get_summary(self):
        """Tính toán summary metrics"""
        return {
            # Traffic Performance
            "avg_waiting_time": self.total_waiting_time / max(self.step_count, 1),
            "avg_queue_length": np.mean(self.total_queue_length),
            "max_queue_length": np.max(self.total_queue_length),
            "throughput": self.total_throughput,
            
            # Environmental Impact
            "total_pm25_mg": np.sum(self.total_pm25),
            "avg_pm25_mg_per_step": np.mean(self.total_pm25),
            "total_co2_mg": np.sum(self.total_co2),
            "avg_co2_mg_per_step": np.mean(self.total_co2),
            "total_fuel_ml": np.sum(self.total_fuel),
            "avg_fuel_ml_per_step": np.mean(self.total_fuel),
            
            # Control Performance
            "phase_changes": self.phase_changes,
            "avg_speed_m_s": np.mean(self.avg_speed),
            
            # Combined Score (lower is better)
            "combined_score": (
                np.mean(self.total_queue_length) * 0.4 +  # Traffic weight
                np.mean(self.total_pm25) * 0.3 +          # Emission weight
                (self.total_waiting_time / max(self.step_count, 1)) * 0.3  # Waiting time weight
            )
        }


def get_state():
    """Lấy state từ SUMO"""
    queues = [traci.lanearea.getLastStepVehicleNumber(det) for det in DETECTOR_IDS]
    phase = traci.trafficlight.getPhase(TLS_ID)
    total_pm25 = sum([traci.edge.getPMxEmission(edge) * 0.1 for edge in EDGE_IDS])
    return (*queues, phase, total_pm25)


def run_baseline_evaluation():
    """Đánh giá Baseline: Fixed-time control (30s green, 30s green)"""
    print("\n" + "="*60)
    print("ĐÁNH GIÁ BASELINE: Fixed-time Traffic Light")
    print("="*60)
    
    metrics = TrafficMetrics()
    traci.start(SUMO_CONFIG_BASE)
    
    # Fixed-time: 30 giây (300 steps) mỗi pha
    FIXED_TIME_STEPS = 300
    step_counter = 0
    
    for step in range(EVALUATION_STEPS):
        # Đổi pha mỗi 300 steps
        if step_counter >= FIXED_TIME_STEPS:
            current_phase = traci.trafficlight.getPhase(TLS_ID)
            next_phase = (current_phase + 1) % 2
            traci.trafficlight.setPhase(TLS_ID, next_phase)
            step_counter = 0
        
        traci.simulationStep()
        metrics.update(step)
        step_counter += 1
        
        if step % 500 == 0:
            print(f"  Step {step}/{EVALUATION_STEPS}")
    
    traci.close()
    
    summary = metrics.get_summary()
    print("\n📊 BASELINE RESULTS:")
    print_metrics(summary)
    
    return summary, metrics


def run_random_evaluation():
    """Đánh giá Random: Random action selection"""
    print("\n" + "="*60)
    print("ĐÁNH GIÁ RANDOM: Random Traffic Control")
    print("="*60)
    
    metrics = TrafficMetrics()
    traci.start(SUMO_CONFIG_BASE)
    
    last_switch_step = -MIN_GREEN_STEPS
    
    for step in range(EVALUATION_STEPS):
        # Random action every 50 steps (but respect MIN_GREEN_STEPS)
        if step % 50 == 0 and step - last_switch_step >= MIN_GREEN_STEPS:
            if np.random.random() > 0.5:  # 50% chance to switch
                current_phase = traci.trafficlight.getPhase(TLS_ID)
                next_phase = (current_phase + 1) % 2
                traci.trafficlight.setPhase(TLS_ID, next_phase)
                last_switch_step = step
        
        traci.simulationStep()
        metrics.update(step)
        
        if step % 500 == 0:
            print(f"  Step {step}/{EVALUATION_STEPS}")
    
    traci.close()
    
    summary = metrics.get_summary()
    print("\n📊 RANDOM RESULTS:")
    print_metrics(summary)
    
    return summary, metrics


def run_dqn_evaluation(model_path="dqn_model.keras"):
    """Đánh giá DQN Model"""
    print("\n" + "="*60)
    print(f"ĐÁNH GIÁ DQN: Trained Model ({model_path})")
    print("="*60)
    
    # Load model
    try:
        model = keras.models.load_model(model_path, compile=False)
        # Re-compile after loading
        model.compile(loss='mse', optimizer=keras.optimizers.Adam(learning_rate=0.001))
        print(f"✅ Model loaded from {model_path}")
    except Exception as e:
        print(f"❌ Cannot load model: {e}")
        # Try fallback to h5 format
        try:
            print("  Trying h5 format...")
            model = keras.models.load_model("dqn_model.h5", compile=False)
            model.compile(loss='mse', optimizer=keras.optimizers.Adam(learning_rate=0.001))
            print(f"✅ Model loaded from dqn_model.h5")
        except:
            return None, None
    
    metrics = TrafficMetrics()
    traci.start(SUMO_CONFIG_BASE)
    
    last_switch_step = -MIN_GREEN_STEPS
    
    for step in range(EVALUATION_STEPS):
        # Get state
        state = get_state()
        state_array = np.array(state, dtype=np.float32).reshape((1, -1))
        
        # Get action from DQN
        q_values = model.predict(state_array, verbose=0)[0]
        action = int(np.argmax(q_values))
        
        # Apply action (1 = switch phase)
        if action == 1 and step - last_switch_step >= MIN_GREEN_STEPS:
            current_phase = traci.trafficlight.getPhase(TLS_ID)
            next_phase = (current_phase + 1) % 2
            traci.trafficlight.setPhase(TLS_ID, next_phase)
            last_switch_step = step
        
        traci.simulationStep()
        metrics.update(step)
        
        if step % 500 == 0:
            print(f"  Step {step}/{EVALUATION_STEPS}")
    
    traci.close()
    
    summary = metrics.get_summary()
    print("\n📊 DQN RESULTS:")
    print_metrics(summary)
    
    return summary, metrics


def print_metrics(summary):
    """In metrics ra console"""
    print(f"""
  🚦 Traffic Performance:
    - Avg Waiting Time: {summary['avg_waiting_time']:.2f} s
    - Avg Queue Length: {summary['avg_queue_length']:.2f} vehicles
    - Max Queue Length: {summary['max_queue_length']:.0f} vehicles
    - Throughput: {summary['throughput']} vehicles
    - Avg Speed: {summary['avg_speed_m_s']:.2f} m/s
  
  🌍 Environmental Impact:
    - Total PM2.5: {summary['total_pm25_mg']:.2f} mg
    - Total CO2: {summary['total_co2_mg']:.2f} mg
    - Total Fuel: {summary['total_fuel_ml']:.2f} ml
  
  ⚙️ Control Performance:
    - Phase Changes: {summary['phase_changes']}
  
  📈 Combined Score: {summary['combined_score']:.4f} (lower is better)
    """)


def compare_and_visualize(baseline_summary, random_summary, dqn_summary, 
                          baseline_metrics, random_metrics, dqn_metrics):
    """So sánh và visualization"""
    
    print("\n" + "="*60)
    print("📊 COMPARATIVE ANALYSIS")
    print("="*60)
    
    # Create comparison table
    metrics_names = [
        "avg_waiting_time", "avg_queue_length", "throughput",
        "total_pm25_mg", "total_co2_mg", "phase_changes", "combined_score"
    ]
    
    print(f"\n{'Metric':<25} {'Baseline':<15} {'Random':<15} {'DQN':<15} {'DQN vs Base':<15}")
    print("-" * 85)
    
    for metric in metrics_names:
        base_val = baseline_summary[metric]
        rand_val = random_summary[metric]
        dqn_val = dqn_summary[metric]
        
        # Calculate improvement (negative is better for most metrics except throughput)
        if metric == "throughput":
            improvement = ((dqn_val - base_val) / base_val * 100) if base_val != 0 else 0
        else:
            improvement = ((base_val - dqn_val) / base_val * 100) if base_val != 0 else 0
        
        print(f"{metric:<25} {base_val:<15.2f} {rand_val:<15.2f} {dqn_val:<15.2f} {improvement:>+.2f}%")
    
    # Create visualization
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    fig.suptitle('DQN Traffic Control Evaluation', fontsize=16, fontweight='bold')
    
    # 1. Queue Length over time
    ax = axes[0, 0]
    steps = range(len(baseline_metrics.total_queue_length))
    ax.plot(steps, baseline_metrics.total_queue_length, label='Baseline', alpha=0.7)
    ax.plot(steps, random_metrics.total_queue_length, label='Random', alpha=0.7)
    ax.plot(steps, dqn_metrics.total_queue_length, label='DQN', alpha=0.7)
    ax.set_xlabel('Simulation Step')
    ax.set_ylabel('Queue Length (vehicles)')
    ax.set_title('Queue Length Over Time')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # 2. PM2.5 Emissions
    ax = axes[0, 1]
    ax.plot(steps, baseline_metrics.total_pm25, label='Baseline', alpha=0.7)
    ax.plot(steps, random_metrics.total_pm25, label='Random', alpha=0.7)
    ax.plot(steps, dqn_metrics.total_pm25, label='DQN', alpha=0.7)
    ax.set_xlabel('Simulation Step')
    ax.set_ylabel('PM2.5 Emission (mg)')
    ax.set_title('PM2.5 Emissions Over Time')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # 3. Average Speed
    ax = axes[0, 2]
    ax.plot(steps, baseline_metrics.avg_speed, label='Baseline', alpha=0.7)
    ax.plot(steps, random_metrics.avg_speed, label='Random', alpha=0.7)
    ax.plot(steps, dqn_metrics.avg_speed, label='DQN', alpha=0.7)
    ax.set_xlabel('Simulation Step')
    ax.set_ylabel('Average Speed (m/s)')
    ax.set_title('Average Speed Over Time')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # 4. Bar chart comparison - Traffic metrics
    ax = axes[1, 0]
    metrics_traffic = ['avg_waiting_time', 'avg_queue_length']
    x = np.arange(len(metrics_traffic))
    width = 0.25
    
    base_vals = [baseline_summary[m] for m in metrics_traffic]
    rand_vals = [random_summary[m] for m in metrics_traffic]
    dqn_vals = [dqn_summary[m] for m in metrics_traffic]
    
    ax.bar(x - width, base_vals, width, label='Baseline', alpha=0.8)
    ax.bar(x, rand_vals, width, label='Random', alpha=0.8)
    ax.bar(x + width, dqn_vals, width, label='DQN', alpha=0.8)
    ax.set_ylabel('Value')
    ax.set_title('Traffic Performance Comparison')
    ax.set_xticks(x)
    ax.set_xticklabels(['Avg Wait Time', 'Avg Queue'])
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    
    # 5. Bar chart comparison - Environmental metrics
    ax = axes[1, 1]
    metrics_env = ['total_pm25_mg', 'total_co2_mg']
    x = np.arange(len(metrics_env))
    
    base_vals = [baseline_summary[m] for m in metrics_env]
    rand_vals = [random_summary[m] for m in metrics_env]
    dqn_vals = [dqn_summary[m] for m in metrics_env]
    
    ax.bar(x - width, base_vals, width, label='Baseline', alpha=0.8)
    ax.bar(x, rand_vals, width, label='Random', alpha=0.8)
    ax.bar(x + width, dqn_vals, width, label='DQN', alpha=0.8)
    ax.set_ylabel('Total Emission (mg)')
    ax.set_title('Environmental Impact Comparison')
    ax.set_xticks(x)
    ax.set_xticklabels(['PM2.5', 'CO2'])
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    
    # 6. Combined Score comparison
    ax = axes[1, 2]
    controllers = ['Baseline', 'Random', 'DQN']
    scores = [
        baseline_summary['combined_score'],
        random_summary['combined_score'],
        dqn_summary['combined_score']
    ]
    colors = ['#ff7f0e', '#d62728', '#2ca02c']
    bars = ax.bar(controllers, scores, color=colors, alpha=0.8)
    ax.set_ylabel('Combined Score (lower is better)')
    ax.set_title('Overall Performance Score')
    ax.grid(True, alpha=0.3, axis='y')
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.2f}',
                ha='center', va='bottom')
    
    plt.tight_layout()
    
    # Save figure
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"evaluation_results_{timestamp}.png"
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"\n💾 Visualization saved to: {filename}")
    
    # Save results to JSON
    results = {
        "timestamp": timestamp,
        "evaluation_steps": EVALUATION_STEPS,
        "baseline": baseline_summary,
        "random": random_summary,
        "dqn": dqn_summary,
        "improvements": {
            metric: ((baseline_summary[metric] - dqn_summary[metric]) / baseline_summary[metric] * 100)
            if baseline_summary[metric] != 0 else 0
            for metric in metrics_names if metric != "throughput"
        }
    }
    
    json_filename = f"evaluation_results_{timestamp}.json"
    with open(json_filename, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"💾 Results saved to: {json_filename}")
    
    return results


def main():
    """Main evaluation function"""
    print("\n" + "="*60)
    print("🚀 DQN TRAFFIC CONTROL EVALUATION FRAMEWORK")
    print("="*60)
    print(f"Evaluation duration: {EVALUATION_STEPS} steps ({EVALUATION_STEPS * 0.1:.1f} seconds)")
    
    # Check if model exists (prefer .keras format)
    model_path = "dqn_model.keras" if os.path.exists("dqn_model.keras") else "dqn_model.h5"
    
    if not os.path.exists(model_path):
        print(f"\n⚠️  Warning: No model file found!")
        print("Please train the model first using train_dqn_fast.py or train_dqn.py")
        
        # Run only baseline and random
        baseline_summary, baseline_metrics = run_baseline_evaluation()
        random_summary, random_metrics = run_random_evaluation()
        
        print("\n" + "="*60)
        print("❌ DQN evaluation skipped (model not found)")
        print("="*60)
        return
    
    # Run all evaluations
    baseline_summary, baseline_metrics = run_baseline_evaluation()
    random_summary, random_metrics = run_random_evaluation()
    dqn_summary, dqn_metrics = run_dqn_evaluation(model_path)
    
    if dqn_summary is None:
        print("\n❌ DQN evaluation failed")
        return
    
    # Compare and visualize
    results = compare_and_visualize(
        baseline_summary, random_summary, dqn_summary,
        baseline_metrics, random_metrics, dqn_metrics
    )
    
    # Final verdict
    print("\n" + "="*60)
    print("🏆 FINAL VERDICT")
    print("="*60)
    
    best_score = min(
        baseline_summary['combined_score'],
        random_summary['combined_score'],
        dqn_summary['combined_score']
    )
    
    if dqn_summary['combined_score'] == best_score:
        improvement = ((baseline_summary['combined_score'] - dqn_summary['combined_score']) 
                      / baseline_summary['combined_score'] * 100)
        print(f"✅ DQN Model is the BEST performer!")
        print(f"   Combined score improvement: {improvement:.2f}% vs Baseline")
        print(f"   Overall Performance: {'EXCELLENT' if improvement > 20 else 'GOOD' if improvement > 10 else 'MODERATE'}")
    else:
        print(f"⚠️  DQN Model needs improvement")
        if baseline_summary['combined_score'] < dqn_summary['combined_score']:
            print(f"   Baseline performs better by {((dqn_summary['combined_score'] - baseline_summary['combined_score']) / baseline_summary['combined_score'] * 100):.2f}%")
        print(f"   Suggestions: Increase training steps, tune hyperparameters, or adjust reward function")
    
    print("\n" + "="*60)
    print("Evaluation complete! 🎉")
    print("="*60)


if __name__ == "__main__":
    if not _SUMO_AVAILABLE:
        print("ERROR: SUMO is not available. Please set SUMO_HOME environment variable.", file=sys.stderr)
        sys.exit(1)
    main()
