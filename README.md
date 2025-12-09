<!--
 Copyright (c) 2025 Green Wave Team

 This software is released under the MIT License.
 https://opensource.org/licenses/MIT
-->

<div align="center">
  <img src="./assets/docusaurus/logo.png" alt="GreenWave-Logo" width="200" height="200" style="border-radius: 50%; object-fit: cover; margin-bottom: 20px;">

# GreenWave - Smart Traffic Management System

### _AI-Powered Traffic Optimization for Cleaner Cities_

<a href="https://opensource.org/licenses/MIT" target="_blank"><img src="https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge" alt="License: MIT"/></a>
<a href="https://www.fiware.org/" target="_blank"><img src="https://img.shields.io/badge/FIWARE-Orion--LD-002E67?style=for-the-badge&logo=fiware" alt="FIWARE"/></a>
<a href="https://www.docker.com/" target="_blank"><img src="https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker"/></a>

  <br />

<a href="https://sonmessia.github.io/GreenWave/" target="_blank"><strong>Documentation</strong></a> • [**Quick Start**](#getting-started) • [**Architecture**](#architecture) • [**Features**](#features)

</div>

<br />

## Overview

> **⚠️ Warning**
>
> **Disclaimer:** This example is for demo use only. It's not production-ready and may omit important features.

**GreenWave** is an intelligent traffic management system that uses **Reinforcement Learning** to simultaneously optimize traffic flow and reduce environmental pollution. Unlike traditional systems that only focus on minimizing wait times, GreenWave considers real-time air quality data to prevent pollution hotspots near schools, hospitals, and residential areas.

<div align="center">

### Key Highlights

|                                  🚦 Intelligent Control                                  |                           🌱 Environmental Awareness                            |
| :--------------------------------------------------------------------------------------: | :-----------------------------------------------------------------------------: |
| **Multi-Objective Optimization**<br>Balances traffic flow and air quality simultaneously | **Pollution Prevention**<br>Protects sensitive areas like schools and hospitals |
| **AI-Driven Decision Making**<br>Uses Reinforcement Learning (DQN) for adaptive signals  |       **Real-Time Monitoring**<br>Live dashboards with sub-second updates       |
|   **Linked Data Integration**<br>Fully NGSI-LD compliant for semantic interoperability   |           **FIWARE-Based**<br>Built on industry-standard IoT platform           |

<br/>

<video src="./assets/Video%20Project%202.mp4" style="width: 300px; height: 300px; object-fit: cover; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.15);" autoplay loop muted playsinline></video>

</div>

## Features

### **Intelligent Control**

- [x] **AI-Driven Traffic Coordination** - DQN-based adaptive signal control
- [x] **Multi-Objective Optimization** - Balance traffic flow & air quality
- [x] **Real-Time Decision Making** - Sub-second response to traffic changes

### **Environmental Awareness**

- [x] **Air Quality Monitoring** - PM2.5, CO, NO2 sensors at intersections
- [x] **Emission Estimation** - Traffic-based pollution prediction
- [x] **Pollution Hotspot Prevention** - Protect sensitive areas

### **Monitoring & Visualization**

**Admin Dashboard** - Comprehensive control panel with AI/manual modes

- [x] **Public Air Quality Portal** - User-facing environmental metrics
- [x] **Historical Analytics** - Time-series data visualization
- [x] **Real-Time Monitoring** - Live dashboards and analytics for instant insights
- [x] **Control Panel By Hand/AI** - Manual and AI modes for traffic control
- [x] **Manage Sensors** - Add, remove, and configure sensors
- [x] **Manage Subscriptions** - Subscribe to real-time data streams

### **DevOps & Standards**

- [x] **CI/CD Pipeline** - Automated testing & deployment
- [x] **OpenAPI Documentation** - Comprehensive API specs
- [x] **Open Source Compliance** - MIT License, Contributing Guidelines

## Architecture

<div align="center">

![Architecture](./assets/gif/architecture.gif)

</div>

### Core Components

| Component          | Technology                                                                                             | Purpose                                     |
| :----------------- | :----------------------------------------------------------------------------------------------------- | :------------------------------------------ |
| **Context Broker** | ![Orion-LD](https://img.shields.io/badge/Orion--LD-002E67?style=flat-square)                           | Real-time context management (NGSI-LD)      |
| **AI Engine**      | ![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)    | Reinforcement Learning traffic optimization |
| **Simulation**     | ![SUMO](https://img.shields.io/badge/SUMO-E3A600?style=flat-square)                                    | Urban mobility simulation                   |
| **Time-Series DB** | ![CrateDB](https://img.shields.io/badge/CrateDB-009DC7?style=flat-square)                              | Historical data storage & analytics         |
| **Frontend**       | ![React](https://img.shields.io/badge/React-61DAFB?style=flat-square&logo=react&logoColor=black)       | Admin dashboard & public portal             |
| **Database**       | ![MongoDB](https://img.shields.io/badge/MongoDB-47A248?style=flat-square&logo=mongodb&logoColor=white) | Current state persistence                   |

## Getting Started

### Prerequisites

| Requirement | Version | Download                                                                      |
| :---------- | :------ | :---------------------------------------------------------------------------- |
| **Docker**  | 28.3.2+ | <a href="https://www.docker.com/get-started/" target="_blank">Get Docker</a>  |
| **Node.js** | 24.6.0+ | <a href="https://nodejs.org/en/download" target="_blank">Get Node.js</a>      |
| **SUMO**    | 1.25.0+ | <a href="https://sumo.dlr.de/docs/Downloads.php" target="_blank">Get SUMO</a> |

> **Note:** If you want to run SUMO on your local machine, you need to download and install it from the <a href="https://sumo.dlr.de/docs/Downloads.php" target="_blank">SUMO website</a>.

### 🏃‍♂️ Run the Application

Follow these steps to get GreenWave running locally:

```bash
# Clone the repository
git clone https://github.com/sonmessia/GreenWave.git

# Navigate to the project directory
cd GreenWave

# Copy the environment variables
cp .env.example .env

# Navigate to the project directory
cd src/backend

# Copy the environment variables
cp .env.example .env
```

#### Launch All Services

```bash
# Start all services with Docker Compose
docker compose up -d
```

#### Start Backend Only

```bash
# By Docker Compose
# Start backend service with Docker Compose
docker compose up -d backend

# Stop backend service with Docker Compose
docker compose down backend

# By Python
cd src/backend  # Change directory to backend

# Copy the environment variables
cp .env.example .env

pip install -r requirements.txt  # Install dependencies

uvicorn app.main:app --host 0.0.0.0 --port 8000  # Run backend
```

#### Start Frontend Only

```bash
# By Docker Compose
# Start frontend service with Docker Compose
docker compose up -d frontend

# Stop frontend service with Docker Compose
docker compose down frontend

# By Node.js
cd src/frontend  # Change directory to frontend

# Copy the environment variables
cp .env.example .env
npm install  # Install dependencies

npm run dev  # Run frontend
```

### Access Points

Once services are running, access them at:

| Service            | URL                                            | Description              |
| :----------------- | :--------------------------------------------- | :----------------------- |
| **Frontend**       | [http://localhost:5173](http://localhost:5173) | User & Admin interfaces  |
| **Backend API**    | [http://localhost:8000](http://localhost:8000) | REST API endpoints       |
| **Context Broker** | [http://localhost:1026](http://localhost:1026) | Orion-LD NGSI-LD API     |
| **Quantum Leap**   | [http://localhost:8668](http://localhost:8668) | Time-series data storage |

---

## Learn More

<div align="center">

### <a href="https://sonmessia.github.io/GreenWave" target="_blank"><strong>Read Full Documentation</strong></a>

Explore detailed tutorials, API references, architecture guides, and more!

</div>

# Contributing

## 📖 Contributing Guidelines

<p align="justify">

We are excited that you are interested in contributing to this project! Before submitting your contribution, please make sure to take a moment and read through the following guidelines:

Read through our [contributing guidelines](.github/CONTRIBUTING.md) to learn about our submission process, coding rules, and more.

</p>

## 💁 Want to Help?

<p align="justify">

Want to report a bug, contribute some code, or improve the documentation? Excellent! Read up on our guidelines for [contributing](.github/CONTRIBUTING.md) and then check out one of our issues labeled as <kbd>[help wanted](https://github.com/sonmessia/GreenWave/labels/help%20wanted)</kbd> or <kbd>[good first issue](https://github.com/sonmessia/GreenWave/labels/good%20first%20issue)</kbd>.

</p>

## 🫂 Code of Conduct

<p align="justify">

Help us keep GreenWave open and inclusive. Please read and follow our [Code of Conduct](.github/CODE_OF_CONDUCT.md).

</p>

# Support and Organization

<p align="center">
	<a href="https://hutech.edu.vn/" target="_blank">
		<img loading="lazy" src="./assets/images/hutech.png" height="60px" alt="Hutech">
	</a>
	<a href="https://vfossa.vn/" target="_blank">
		<img loading="lazy" src="./assets/images/vfossa.png" height="60px" alt="Hutech">
	</a>
	<a href="https://olp.husc.edu.vn/" target="_blank">
		<img loading="lazy" src="./assets/images/icpc.jpg" height="60px" alt="ICPC">
	</a>
</p>

# License

<p align="justify">

This project is licensed under the terms of the [MIT](LICENSE) license.

</p>
