---
sidebar_position: 1
title: Introduction to GreenWave AI
---

# Introduction to GreenWave AI

GreenWave AI is a smart traffic light control system utilizing Artificial Intelligence (AI) and Reinforcement Learning, completely integrated with the FIWARE platform and SUMO traffic simulation.

## Overview

Unlike traditional traffic light systems that use fixed-time counters, GreenWave AI analyzes traffic flow in real-time to make the most optimal control decisions.

The system operates based on the principle: **"Green lights are only for directions that truly need them"**.

### Key Features

- **Independent Control**: Each traffic light pillar is analyzed and controlled independently by AI, not rigidly dependent on other lights.
- **Real-time**: Decisions are made every 2 seconds based on current data from sensors.
- **Conflict-Free**: The algorithm ensures safety, ensuring that signal conflicts never occur.
- **Multi-Objective**: Simultaneously optimizes multiple metrics: queue length, waiting time, and vehicle density.

## System Architecture

GreenWave AI operates according to the following closed-loop pipeline:

![Ai-Architecture.png](../assets/Event-Driven.png)

1. **Data Collection**: Sensors (Induction loops) in SUMO collect information about speed and vehicle count.
2. **Context Broker**: Data is normalized into TrafficFlowObserved and sent to Orion-LD.
3. **AI Processing**: The AI Agent receives notifications from Orion, analyzes the state, and makes a phase decision.
4. **Execution**: Control commands are sent back via the IoT Agent to change the light status in the simulation.

## AI Algorithm

The system uses the **Smart Priority-Based Phase Selection** algorithm.

### Switching Logic

- **Threshold**: To avoid the light changing states continuously (causing disorder), a new phase is only activated if its priority score is at least **15%** higher than the current phase.
- **Minimum Duration**: Each green phase must be maintained for at least 10 seconds before it can be switched.

## Performance

Compared to the fixed-time control method, GreenWave AI delivers significant improvements:

- **Average waiting time reduction**: ~13-20%
- **Emission reduction (CO2, PM2.5)**: Because vehicles stop and restart less often.
- **Throughput increase**: Better utilization of green time and road space.

The system has been successfully tested on real-world scenarios in HCMC such as Thu Duc Intersection, Nguyen Thai Son Roundabout, and Quang Trung Intersection.
