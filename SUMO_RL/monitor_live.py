#!/usr/bin/env python3
"""
Real-time Training Progress Monitor
Updates every 10 seconds
"""

import time
import os
import re
from datetime import datetime

LOG_FILE = "training_prod.log"
CHECK_INTERVAL = 10  # seconds

def parse_latest_metrics(log_path):
    """Extract latest metrics from log"""
    if not os.path.exists(log_path):
        return None
    
    with open(log_path, 'r') as f:
        lines = f.readlines()
    
    # Find latest progress line
    for line in reversed(lines):
        if '[' in line and '/10000]' in line:
            # Example: [  200/10000] ε=0.9716 | Loss=0.0460 | Avg R=-0.05 | Avg Q=0.18 | Switches=2 | Buffer=201
            match = re.search(r'\[\s*(\d+)/10000\].*ε=([0-9.]+).*Loss=([0-9.]+).*Avg R=(-?[0-9.]+).*Avg Q=([0-9.]+).*Switches=(\d+).*Buffer=(\d+)', line)
            if match:
                return {
                    'step': int(match.group(1)),
                    'epsilon': float(match.group(2)),
                    'loss': float(match.group(3)),
                    'reward': float(match.group(4)),
                    'queue': float(match.group(5)),
                    'switches': int(match.group(6)),
                    'buffer': int(match.group(7))
                }
    
    # Check for milestones
    for line in reversed(lines):
        if 'MILESTONE:' in line:
            match = re.search(r'MILESTONE: ([\d,]+) steps', line)
            if match:
                steps = int(match.group(1).replace(',', ''))
                return {'step': steps, 'milestone': True}
    
    return None

def draw_progress_bar(current, total, width=50):
    """Draw ASCII progress bar"""
    progress = current / total
    filled = int(width * progress)
    bar = '█' * filled + '░' * (width - filled)
    return f"[{bar}] {progress*100:.1f}%"

def format_eta(steps, steps_done, elapsed):
    """Estimate time remaining"""
    if steps_done == 0:
        return "Calculating..."
    
    rate = steps_done / elapsed  # steps/second
    remaining_steps = steps - steps_done
    eta_seconds = remaining_steps / rate
    
    hours = int(eta_seconds // 3600)
    minutes = int((eta_seconds % 3600) // 60)
    
    if hours > 0:
        return f"{hours}h {minutes}m"
    else:
        return f"{minutes}m"

def main():
    print("\n" + "="*70)
    print("🚀 DQN PRODUCTION TRAINING MONITOR")
    print("="*70)
    print("Monitoring: training_prod.log")
    print("Press Ctrl+C to stop monitoring\n")
    
    start_time = time.time()
    last_step = 0
    
    try:
        while True:
            os.system('clear' if os.name == 'posix' else 'cls')
            
            print("\n" + "="*70)
            print("🚀 DQN PRODUCTION TRAINING MONITOR".center(70))
            print("="*70 + "\n")
            
            metrics = parse_latest_metrics(LOG_FILE)
            
            if metrics:
                step = metrics.get('step', 0)
                elapsed = time.time() - start_time
                
                # Progress bar
                print("📊 Training Progress:")
                print(draw_progress_bar(step, 10000, 60))
                print(f"   Step: {step:,} / 10,000\n")
                
                # Metrics
                if not metrics.get('milestone'):
                    print("📈 Current Metrics:")
                    print(f"   Epsilon (ε):     {metrics['epsilon']:.4f}")
                    print(f"   Loss:            {metrics['loss']:.4f}")
                    print(f"   Avg Reward:      {metrics['reward']:.4f}")
                    print(f"   Avg Queue:       {metrics['queue']:.2f}")
                    print(f"   Phase Switches:  {metrics['switches']}")
                    print(f"   Replay Buffer:   {metrics['buffer']:,}/10,000\n")
                
                # Time estimates
                print("⏱️  Time Info:")
                elapsed_min = int(elapsed // 60)
                print(f"   Elapsed:         {elapsed_min} min")
                
                if step > last_step:
                    eta = format_eta(10000, step, elapsed)
                    print(f"   ETA:             {eta}")
                    steps_per_min = (step / elapsed) * 60
                    print(f"   Speed:           ~{steps_per_min:.0f} steps/min")
                
                last_step = step
                
                # Milestones
                if step >= 1000 and step % 1000 == 0:
                    print(f"\n🎯 Milestone: {step:,} steps completed!")
                
            else:
                print("⏳ Waiting for training to start...")
                print("   Log file: training_prod.log")
                print(f"   Checking every {CHECK_INTERVAL}s...\n")
            
            print("="*70)
            print(f"Last update: {datetime.now().strftime('%H:%M:%S')}")
            print("Press Ctrl+C to stop monitoring")
            
            time.sleep(CHECK_INTERVAL)
            
    except KeyboardInterrupt:
        print("\n\n✅ Monitoring stopped.\n")
        if metrics:
            print(f"Last seen: Step {metrics.get('step', 0):,}/10,000")

if __name__ == "__main__":
    main()
