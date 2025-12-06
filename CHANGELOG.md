# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-12-06

### Added

- **Core Platform**: Initial release of the GreenWave Smart Traffic Management System.
- **Backend**:
  - Python-based backend service located in `src/backend`.
  - Integration with SUMO (Simulation of Urban MObility) for real-time traffic simulation.
  - Deep Q-Network (DQN) model (`dqn_model.keras`) for intelligent traffic signal control.
  - REST API endpoints for traffic data and simulation control.
  - Synthetic data generators for air quality, carbon footprint, and traffic impact.
- **Frontend**:
  - React-based web dashboard located in `src/frontend`.
  - Vite build setup for fast development and optimized production builds.
  - Nginx configuration for serving the frontend application.
- **Documentation**:
  - Comprehensive documentation site built with Docusaurus in `docs/`.
  - Architecture diagrams and guides in `assets/`.
  - API documentation and "How to Test" guides.
- **Data Models**:
  - NGSI-LD context files in `ld-context-files/` for standardizing data models (AirQualityObserved, Building, Device, RoadSegment, TrafficEnvironmentImpact).
  - OpenAPI specification in `openAPI/smartmodels.yaml`.
- **Deployment & Scripts**:
  - `docker-compose.yaml` for orchestrating backend, frontend, and database services.
  - Utility scripts in `scripts/` for managing SUMO instances (`start_sumo.py`, `check_sumo.py`).
