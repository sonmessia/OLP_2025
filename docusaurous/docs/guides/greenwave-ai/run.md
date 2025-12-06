---
sidebar_position: 2
title: System Running Guide
---

<!--
 Copyright (c) 2025 Green Wave Team

 This software is released under the MIT License.
 https://opensource.org/licenses/MIT
-->

# System Running Guide

This document guides you on how to start and use GreenWave AI through two methods: using the Dashboard interface (recommended) and using the command line (CLI).

## Prerequisites

Ensure you have installed the following tools:

| Requirement | Version | Download                                           |
| ----------- | ------- | -------------------------------------------------- |
| **Docker**  | 28.3.2+ | [Get Docker](https://www.docker.com/get-started/)  |
| **Node.js** | 24.6.0+ | [Get Node.js](https://nodejs.org/en/download)      |
| **SUMO**    | 1.25.0+ | [Get SUMO](https://sumo.dlr.de/docs/Downloads.php) |

## Method 1: Running with Interface (Dashboard UI)

This is the most intuitive way to monitor and demo the system.

### Step 1: Start Backend

Open the terminal and run the Docker containers:

```bash
# At the project root directory
docker-compose up
```

### Step 2: Access Dashboard

1. Open your browser and visit: [http://localhost:5137/](http://localhost:5137/control)
2. Log in with the account:

   - email: "admin@olp.vn",
   - password: "admin123",

3. In the **SUMO Control** section, select Scenario.
4. Click the green **"Start"** button.
   - The status will change to `Connected`.

### Step 4: Activate AI

1. Scroll down to the **Control Panel** section.
2. On the Dashboard, press the **▶ Play** button to start the simulation.
3. Click the **"🤖 Enable AI Control"** button.
4. Observe the logs on the Dashboard to see AI controlling the light phases in real-time.

---

## Troubleshooting

### 1. Dashboard reports "Not Running"

- **Cause**: The `auto_start_sumo.py` script is not running or not on port 8813.
- **Fix**: Check the terminal running the python script, ensure there are no errors. Run `lsof -i :8813` to see if the port is open.

### 2. "Connection refused" Error

- **Cause**: Backend has not finished starting or incorrect network configuration.
- **Fix**: Run `docker logs backend` to view error logs. Ensure the `SUMO_HOST` environment variable points correctly to the host machine (usually `host.docker.internal` on Windows/Mac or `172.17.0.1` on Linux).

### 3. No vehicles moving

- **Cause**: Simulation is in Pause state or Play has not been pressed.
- **Fix**: Press the Play button on the Dashboard or send API `/sumo/step` continuously.
