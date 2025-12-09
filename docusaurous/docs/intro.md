---
sidebar_position: 1
title: Introduction
---

<!--
 Copyright (c) 2025 Green Wave Team

 This software is released under the MIT License.
 https://opensource.org/licenses/MIT
-->

# Introduction

## The Problem

Current traffic control systems (fixed-timer or semi-smart) are designed with a single goal: **optimize traffic flow** (reduce wait times, reduce congestion).
However, they are completely "blind" to a critical factor: **localized environmental impact**. Continuous stop-and-go traffic or prolonged idling at an intersection creates **"pollution hotspots"**.

> **Example:** A system might optimize for fast vehicle flow but inadvertently push a large amount of PM2.5 and CO emissions into an intersection near a school or hospital. This is a failure in terms of public health optimization.

## The Core Solution

**GreenWave** builds a real-time adaptive traffic signal control system using **AI (Reinforcement Learning)** to simultaneously optimize two objectives (**multi-objective**):

1.  **Traffic Goal**: Minimize average wait time and queue length.
2.  **Environment Goal**: Minimize estimated emissions and/or observed air pollution indices at the site.

The system is no longer "blind"; it makes trade-offs between these two goals.

## Architecture & Data Flow

![Architecture](./assets/architecture.gif)

The system revolves around **Smart Data Models**:

1.  **Input Layer**:
    - **Traffic**: AI Cameras (counting, classification), Induction Loops.
    - **Environment**: Air Quality Sensors (PM2.5, CO, NO2) at intersections feeding `AirQualityObserved`.
2.  **Processing Layer**:
    - Camera data -> `TrafficEnvironmentImpact` (Estimated impact).
    - Sensor data -> `AirQualityObserved` (Real-time impact).
3.  **Decision Layer (AI Agent)**:
    - **State**: Traffic queues, current light phase, `AirQualityObserved`, `TrafficEnvironmentImpact`.
    - **Action**: Extend Green, Red Now, Priority Phase.

## Goals

**Intelligent Control**

- [x] **AI-Driven Traffic Coordination** - DQN-based adaptive signal control
- [x] **Multi-Objective Optimization** - Balance traffic flow & air quality
- [x] **Real-Time Decision Making** - Sub-second response to traffic changes

**Environmental Awareness**

- [x] **Air Quality Monitoring** - PM2.5, CO, NO2 sensors at intersections
- [x] **Emission Estimation** - Traffic-based pollution prediction
- [x] **Pollution Hotspot Prevention** - Protect sensitive areas

**Monitoring & Visualization**

**Admin Dashboard** - Comprehensive control panel with AI/manual modes

- [x] **Public Air Quality Portal** - User-facing environmental metrics
- [x] **Historical Analytics** - Time-series data visualization
- [x] **Real-Time Monitoring** - Live dashboards and analytics for instant insights
- [x] **Control Panel By Hand/AI** - Manual and AI modes for traffic control
- [x] **Manage Sensors** - Add, remove, and configure sensors
- [x] **Manage Subscriptions** - Subscribe to real-time data streams

**DevOps & Standards**

- [x] **CI/CD Pipeline** - Automated testing & deployment
- [x] **OpenAPI Documentation** - Comprehensive API specs
- [x] **Open Source Compliance** - MIT License, Contributing Guidelines

## Quick Started

### Prerequisites

- **Docker 28.3.2**: To run the Orion-LD Context Broker. Download at [Docker](https://www.docker.com/get-started/)
- **Node 24.6.0**: To run the frontend. Download at [NodeJS](https://nodejs.org/en/download)
- **SUMO 1.25.0**: To run the SUMO Traffic Simulation. Download at [SUMO](https://sumo.dlr.de/docs/Downloads.php)

### Start your site

Run the following command to start all services (Context Broker, Backend, Frontend, and Documentation):

```bash
cp .env.example .env
cd src/backend
cp .env.example .env
docker compose up -d
```

Once the services are up and running, you can access them at the following addresses:

- **Frontend**: [http://localhost:5173](http://localhost:5173)
- **Quantum Leap**: [http://localhost:8668](http://localhost:8668)
- **Backend API**: [http://localhost:8000](http://localhost:8000)
- **Context Broker**: [http://localhost:1026](http://localhost:1026)
