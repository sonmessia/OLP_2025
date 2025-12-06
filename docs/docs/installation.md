---
sidebar_position: 2
---

# Installation

This guide will help you install and run the GreenWave system on your local machine.

## System Requirements

Before starting, ensure your computer has the following software installed:

| Software    | Version | Download                                           |
| :---------- | :------ | :------------------------------------------------- |
| **Docker**  | 28.3.2+ | [Get Docker](https://www.docker.com/get-started/)  |
| **Node.js** | 24.6.0+ | [Get Node.js](https://nodejs.org/en/download)      |
| **SUMO**    | 1.25.0+ | [Get SUMO](https://sumo.dlr.de/docs/Downloads.php) |

:::info
If you want to run SUMO simulation locally (not via Docker), you need to download and install it from their website.
:::

## Installation and Running

Follow these steps to run GreenWave:

### 1. Clone the repository

Open your terminal and run the following command to download the source code:

```bash
git clone https://github.com/sonmessia/GreenWave.git
cd GreenWave
```

### 2. Configure Environment Variables

Copy the example configuration file to the official `.env` file:

```bash
cp .env.example .env
```

### 3. Run the Application

#### Run the Entire System (Docker Compose)

This is the simplest way to start the whole system:

```bash
docker compose up -d
```

#### Run Backend Only

**Using Docker:**

```bash
# Start backend
docker compose up -d backend

# Stop backend
docker compose down backend
```

**Run directly with Python:**

```bash
cd src/backend
cp .env.example .env
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

#### Run Frontend Only

**Using Docker:**

```bash
# Start frontend
docker compose up -d frontend

# Stop frontend
docker compose down frontend
```

**Run directly with Node.js:**

```bash
cd src/frontend
cp .env.example .env
npm install
npm run dev
```

## Project Structure

Here is an overview of the project's file structure:

```text
GreenWave
├── .github             # GitHub Actions workflows and templates
├── assets              # Project assets (images, videos)
├── docs                # Docusaurus documentation source
├── ld-context-files    # JSON-LD context files for NGSI-LD
├── openAPI             # API Specifications (Swagger/OpenAPI)
├── scripts             # Utility scripts
├── src
│   ├── backend         # Python FastAPI Backend
│   │   ├── app         # Application core logic
│   │   ├── tests       # Backend tests
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   └── frontend        # React Vite Frontend
│       ├── public
│       ├── src
│       ├── Dockerfile
│       └── package.json
├── .env.example        # Environment variables template
├── docker-compose.yaml # Docker orchestration service definition
├── README.md
└── start_sumo.py       # SUMO simulation runner
```

## Access Points

Once services are running, you can access them via the following URLs:

| Service            | URL                                            | Description              |
| :----------------- | :--------------------------------------------- | :----------------------- |
| **Frontend**       | [http://localhost:5173](http://localhost:5173) | User & Admin UI          |
| **Backend API**    | [http://localhost:8000](http://localhost:8000) | REST API endpoints       |
| **Context Broker** | [http://localhost:1026](http://localhost:1026) | Orion-LD NGSI-LD API     |
| **Quantum Leap**   | [http://localhost:8668](http://localhost:8668) | Time-series data storage |
