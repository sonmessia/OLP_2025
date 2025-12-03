# Frontend Architecture

This document outlines the architecture of the frontend application, which is built using React, TypeScript, and Vite. The project follows a **Clean Architecture** inspired structure to ensure separation of concerns, scalability, and maintainability.

## Technology Stack

- **Core**: React 19, TypeScript
- **Build Tool**: Vite
- **State Management**: Redux Toolkit (React-Redux)
- **Routing**: React Router DOM v7
- **Styling**: Tailwind CSS v4
- **HTTP Client**: Axios
- **Maps**: Leaflet, React Leaflet, MapTiler SDK
- **Visualization**: Chart.js, React Chartjs 2
- **Icons**: Lucide React

## Project Structure

The source code is located in `src/frontend/src` and is organized into the following layers:

```
src/frontend/src/
├── api/            # API clients and HTTP configuration
├── app/            # Application-level configuration and context
├── assets/         # Static assets (images, fonts, etc.)
├── data/           # Data layer (Redux slices, DTOs, Mappers)
├── domain/         # Domain layer (Models, Entities)
├── presentation/   # UI layer (Components, Pages, Hooks)
└── main.tsx        # Application entry point
```

## Architecture Layers

### 1. Domain Layer (`src/domain`)

This layer contains the business logic and entities of the application. It is independent of the UI and external data sources.

- **Models**: TypeScript interfaces/types representing the core business entities.
- **Independence**: This layer has **zero dependencies** on external frameworks (React, Redux, Axios) or other layers.
- **Example**: `src/domain/models/SumoModels.ts` defines pure TypeScript interfaces like `SumoSimulationState` and `TrafficLight`.

### 2. Data Layer (`src/data` & `src/api`)

This layer is responsible for data management, fetching, and transformation.

- **API (`src/api`)**: Contains specific API clients (e.g., `sumoApi.ts`) and the base Axios configuration.
  - **Single Source of Truth**: API response types are imported directly from DTOs to ensure consistency.
- **DTOs (`src/data/dtos`)**: Data Transfer Objects defining the shape of data returned by the API (typically snake_case).
- **Mappers (`src/data/mappers`)**: Functions to transform DTOs into Domain Models (camelCase).
  - **Strict Typing**: Mappers enforce strict type boundaries and handle data validation (e.g., Enum conversion) to ensure only valid data reaches the Domain Layer.
- **Redux (`src/data/redux`)**: State management logic using Redux Toolkit slices.
  - **Dependency Injection**: API clients are injected into Redux thunks via `extraArgument`, improving testability.

### 3. Presentation Layer (`src/presentation`)

This layer handles the User Interface and user interactions.

- **Components**: Reusable UI components.
- **Pages**: Top-level route components.
  - `LandingPage`: The entry page of the application.
  - `UserMap`: Interactive map for users.
  - `ManagerDashboard`: Dashboard for system managers.
  - `ControlTrafficPage`: Interface for controlling traffic systems.
  - `DeviceManagementPage`: Page for managing IoT devices.
- **Hooks**: Custom React hooks.
- **Styles**: Global styles and Tailwind configuration.
- **App.tsx**: The main application component setting up routes and providers.

## Key Concepts

### State Management & Data Flow

We use **Redux Toolkit** for managing global application state. The data flow follows a strict unidirectional pattern:

1.  **UI** triggers an action (e.g., `dispatch(fetchSumoStatus())`).
2.  **Redux Thunk** calls the injected **API Client**.
3.  **API Client** returns a raw **DTO**.
4.  **Mapper** transforms the **DTO** into a **Domain Model**.
5.  **Redux Reducer** updates the **State** with the Domain Model.
6.  **UI** updates based on the new State selector.

### API Integration

API calls are encapsulated in dedicated service files within `src/api`. These services use a configured Axios instance (`axiosConfig.ts`).

- **Dependency Injection**: The `sumoApi` is injected into the Redux store configuration, allowing for easy mocking in tests.

### Styling

**Tailwind CSS** is used for utility-first styling. This allows for rapid UI development and consistent design tokens.

### Routing

**React Router DOM** manages client-side navigation. Routes are defined in `App.tsx`, mapping paths to Page components.

## Development

To start the development server:

```bash
npm run dev
```

To build for production:

```bash
npm run build
```
