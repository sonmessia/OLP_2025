#!/usr/bin/env python3
# Copyright (c) 2025 Green Wave Team
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

"""
Production DQN Training Script - 10,000 steps
Optimized hyperparameters for best performance
"""

import os
import random
import sys
from collections import deque
from datetime import datetime

import numpy as np

# Force CPU only for stability
os.environ['CUDA_VISIBLE_DEVICES'] = ''

from tensorflow import keras
from tensorflow.keras import layers

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

# ===== PRODUCTION CONFIGURATION =====
SUMO_CONFIG = [
    'sumo',
    '-c', 'sumo_files/Nga4ThuDuc/Nga4ThuDuc.sumocfg',
    '--step-length', '0.1',
    '--lateral-resolution', '0',
    '--no-step-log', 'true',
    '--no-warnings', 'true'
]

# Training Configuration (Production)
TOTAL_STEPS = 10000  # Production training
ACTIONS = [0, 1]
STATE_SIZE = 4
ACTION_SIZE = len(ACTIONS)

# Reward weights (tuned for Vietnam traffic)
W_TRAFFIC = 0.6  # Priority: Traffic flow
W_ENV = 0.4      # Secondary: Air quality

# Optimized DQN Hyperparameters
GAMMA = 0.95
EPSILON_START = 1.0
EPSILON_END = 0.01
EPSILON_DECAY_STEPS = 7000  # Slower decay for better exploration
LEARNING_RATE = 0.0005      # Lower LR for stability
REPLAY_BUFFER_SIZE = 10000
BATCH_SIZE = 64
TARGET_UPDATE_FREQ = 200    # Less frequent updates

MIN_GREEN_STEPS = 100
last_switch_step = -MIN_GREEN_STEPS

# IDs
TLS_ID = "4066470692"
EDGE_IDS = ["720360980", "720360983#1", "1106838009#1"]
DETECTOR_IDS = ["e2_0", "e2_2"]
NUM_PHASES = 2


class ReplayBuffer:
    def __init__(self, capacity):
        self.buffer = deque(maxlen=capacity)
    
    def add(self, state, action, reward, next_state, done):
        self.buffer.append((state, action, reward, next_state, done))
    
    def sample(self, batch_size):
        return random.sample(self.buffer, batch_size)
    
    def __len__(self):
        return len(self.buffer)


def build_model(state_size, action_size):
    """Build DQN with improved architecture"""
    model = keras.Sequential([
        layers.Input(shape=(state_size,)),
        layers.Dense(128, activation='relu', kernel_initializer='he_normal'),
        layers.Dropout(0.2),
        layers.Dense(128, activation='relu', kernel_initializer='he_normal'),
        layers.Dropout(0.2),
        layers.Dense(64, activation='relu', kernel_initializer='he_normal'),
        layers.Dense(action_size, activation='linear')
    ])
    model.compile(
        loss='mse',
        optimizer=keras.optimizers.Adam(learning_rate=LEARNING_RATE)
    )
    return model


def to_array(state_tuple):
    return np.array(state_tuple, dtype=np.float32).reshape((1, -1))


def get_state():
    queues = [traci.lanearea.getLastStepVehicleNumber(det) for det in DETECTOR_IDS]
    phase = traci.trafficlight.getPhase(TLS_ID)
    total_pm25 = sum([traci.edge.getPMxEmission(edge) * 0.1 for edge in EDGE_IDS])
    return (*queues, phase, total_pm25)


def get_reward(state, last_state):
    """Improved reward with penalty for excessive switching"""
    total_queue = sum(state[:2])
    reward_traffic = -float(total_queue)
    
    total_pm25 = state[3]
    reward_env = -float(total_pm25)
    
    total_reward = (W_TRAFFIC * reward_traffic) + (W_ENV * reward_env)
    return total_reward


def apply_action(action, current_sim_step):
    global last_switch_step
    
    if action == 1:
        if current_sim_step - last_switch_step >= MIN_GREEN_STEPS:
            current_phase = traci.trafficlight.getPhase(TLS_ID)
            next_phase = (current_phase + 1) % NUM_PHASES
            traci.trafficlight.setPhase(TLS_ID, next_phase)
            last_switch_step = current_sim_step
            return True
    return False


def get_action_from_policy(model, state_tuple, epsilon):
    if random.random() < epsilon:
        return random.choice(ACTIONS)
    else:
        state_array = to_array(state_tuple)
        q_values = model.predict(state_array, verbose=0)[0]
        return int(np.argmax(q_values))


def train_model(main_model, target_model, replay_buffer):
    if len(replay_buffer) < BATCH_SIZE:
        return 0.0
        
    minibatch = replay_buffer.sample(BATCH_SIZE)
    
    states = np.array([to_array(s[0])[0] for s in minibatch])
    actions = np.array([s[1] for s in minibatch])
    rewards = np.array([s[2] for s in minibatch])
    next_states = np.array([to_array(s[3])[0] for s in minibatch])
    
    # Double DQN: Use main model to select action, target to evaluate
    q_next_main = main_model.predict(next_states, verbose=0)
    q_next_target = target_model.predict(next_states, verbose=0)
    
    best_actions = np.argmax(q_next_main, axis=1)
    target_q = rewards + GAMMA * q_next_target[np.arange(BATCH_SIZE), best_actions]
    
    current_q = main_model.predict(states, verbose=0)
    
    for i in range(BATCH_SIZE):
        current_q[i][actions[i]] = target_q[i]
    
    history = main_model.fit(states, current_q, verbose=0)
    return history.history['loss'][0]


def main_loop():
    global last_switch_step
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    print("\n" + "="*70)
    print("🚀 PRODUCTION DQN TRAINING - SMART TRAFFIC CONTROL")
    print("="*70)
    print(f"Training ID: {timestamp}")
    print(f"Total steps: {TOTAL_STEPS:,}")
    print(f"Replay buffer: {REPLAY_BUFFER_SIZE:,}")
    print(f"Batch size: {BATCH_SIZE}")
    print(f"Learning rate: {LEARNING_RATE}")
    print(f"Epsilon decay: {EPSILON_START} → {EPSILON_END} over {EPSILON_DECAY_STEPS:,} steps")
    print("="*70 + "\n")
    
    # Initialize models
    print("Building neural networks...")
    main_dqn_model = build_model(STATE_SIZE, ACTION_SIZE)
    target_dqn_model = build_model(STATE_SIZE, ACTION_SIZE)
    target_dqn_model.set_weights(main_dqn_model.get_weights())
    
    print("Model architecture:")
    main_dqn_model.summary()
    
    replay_buffer = ReplayBuffer(REPLAY_BUFFER_SIZE)
    
    epsilon = EPSILON_START
    
    # Tracking metrics
    episode_rewards = []
    losses = []
    avg_queues = []
    phase_switches = 0
    
    # Start SUMO
    print("\nStarting SUMO simulation...")
    traci.start(SUMO_CONFIG)
    
    state = get_state()
    episode_reward = 0
    
    print("Training started...\n")
    
    for step in range(TOTAL_STEPS):
        current_simulation_step = step
        
        # Choose action
        action = get_action_from_policy(main_dqn_model, state, epsilon)
        
        # Apply action
        switched = apply_action(action, current_simulation_step)
        if switched:
            phase_switches += 1
        
        # Step simulation
        traci.simulationStep()
        
        # Get new state and reward
        new_state = get_state()
        reward = get_reward(new_state, state)
        episode_reward += reward
        
        # Store in replay buffer
        replay_buffer.add(state, action, reward, new_state, False)
        
        # Train model
        loss = train_model(main_dqn_model, target_dqn_model, replay_buffer)
        if loss > 0:
            losses.append(loss)
        
        state = new_state
        
        # Track metrics
        avg_queues.append(sum(new_state[:2]))
        
        # Update epsilon
        if epsilon > EPSILON_END:
            epsilon -= (EPSILON_START - EPSILON_END) / EPSILON_DECAY_STEPS
            epsilon = max(epsilon, EPSILON_END)
            
        # Update target model
        if step % TARGET_UPDATE_FREQ == 0 and step > 0:
            target_dqn_model.set_weights(main_dqn_model.get_weights())
            avg_loss = np.mean(losses[-100:]) if losses else 0
            avg_reward = episode_reward / (step + 1)
            avg_queue = np.mean(avg_queues[-100:])
            
            print(f"[{step:5d}/{TOTAL_STEPS}] "
                  f"ε={epsilon:.4f} | "
                  f"Loss={avg_loss:.4f} | "
                  f"Avg R={avg_reward:.2f} | "
                  f"Avg Q={avg_queue:.2f} | "
                  f"Switches={phase_switches} | "
                  f"Buffer={len(replay_buffer):,}")
            
        # Milestone reporting
        if step > 0 and step % 1000 == 0:
            episode_rewards.append(episode_reward / step)
            print(f"\n{'='*70}")
            print(f"📊 MILESTONE: {step:,} steps completed")
            print(f"   Cumulative Reward: {episode_reward:.2f}")
            print(f"   Average Reward: {episode_reward/step:.4f}")
            print(f"   Phase Switches: {phase_switches}")
            print(f"   Epsilon: {epsilon:.4f}")
            print(f"   Buffer Utilization: {len(replay_buffer)/REPLAY_BUFFER_SIZE*100:.1f}%")
            print(f"{'='*70}\n")

    # Close SUMO
    traci.close()
    
    # Save models
    print("\n" + "="*70)
    print("💾 Saving models...")
    
    main_dqn_model.save(f"dqn_model_prod_{timestamp}.keras")
    main_dqn_model.save("dqn_model.keras")  # Latest
    main_dqn_model.save_weights(f"dqn_weights_prod_{timestamp}.weights.h5")
    
    print(f"   ✅ Model saved: dqn_model_prod_{timestamp}.keras")
    print("   ✅ Latest link: dqn_model.keras")
    print(f"   ✅ Weights: dqn_weights_prod_{timestamp}.weights.h5")
    
    # Save training stats
    stats = {
        'timestamp': timestamp,
        'total_steps': TOTAL_STEPS,
        'final_epsilon': float(epsilon),
        'final_reward': float(episode_reward),
        'avg_reward': float(episode_reward / TOTAL_STEPS),
        'phase_switches': phase_switches,
        'buffer_size': len(replay_buffer),
        'hyperparameters': {
            'gamma': GAMMA,
            'learning_rate': LEARNING_RATE,
            'batch_size': BATCH_SIZE,
            'buffer_size': REPLAY_BUFFER_SIZE,
            'epsilon_decay': EPSILON_DECAY_STEPS
        }
    }
    
    import json
    with open(f"training_stats_{timestamp}.json", 'w') as f:
        json.dump(stats, f, indent=2)
    
    print(f"   ✅ Stats saved: training_stats_{timestamp}.json")
    
    # Final summary
    print("\n" + "="*70)
    print("🎉 TRAINING COMPLETE!")
    print("="*70)
    print(f"Total Steps: {TOTAL_STEPS:,}")
    print(f"Final Epsilon: {epsilon:.4f}")
    print(f"Total Reward: {episode_reward:.2f}")
    print(f"Average Reward: {episode_reward/TOTAL_STEPS:.4f}")
    print(f"Phase Switches: {phase_switches}")
    print(f"Final Buffer Size: {len(replay_buffer):,}/{REPLAY_BUFFER_SIZE:,}")
    print(f"Training Duration: ~{TOTAL_STEPS*0.1/60:.1f} minutes simulated")
    print("="*70 + "\n")
    
    print("✅ Model ready for evaluation!")
    print("   Run: python3 evaluate_dqn.py")


if __name__ == "__main__":
    if not _SUMO_AVAILABLE:
        print("ERROR: SUMO is not available. Please set SUMO_HOME environment variable.", file=sys.stderr)
        sys.exit(1)
    main_loop()
