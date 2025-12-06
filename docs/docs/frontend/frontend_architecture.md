---
sidebar_position: 1
title: Frontend Architecture
---

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
├── data/           # Data layer (Redux, DTOs, Mappers, Repository Impls)
├── domain/         # Domain layer (Models, Repository Interfaces, Use Cases)
├── presentation/   # UI layer (Components, Pages, Hooks)
└── main.tsx        # Application entry point
```

## Architecture Layers

### 1. Domain Layer (`src/domain`)

This layer contains the business logic, entities, and rules of the application. It is the core of the Clean Architecture and is independent of the UI and external data sources.

- **Models**: TypeScript interfaces/types representing the core business entities (e.g., `SumoModels.ts`, `SubscriptionModels.ts`).
- **Repository Interfaces**: Abstract definitions of how data should be accessed (e.g., `ISubscriptionRepository.ts`). This allows for dependency inversion.
- **Use Cases**: Classes or functions that encapsulate specific business rules and application logic (e.g., `CreateSubscriptionUseCase.ts`). They orchestrate the flow of data to and from the entities.
- **Independence**: This layer has **zero dependencies** on external frameworks (React, Redux, Axios) or other layers.

### 2. Data Layer (`src/data` & `src/api`)

This layer is responsible for data management, fetching, and transformation. It implements the interfaces defined in the Domain Layer.

- **API (`src/api`)**: Contains specific API clients (e.g., `sumoApi.ts`, `SubscriptionApiClient.ts`) and the base Axios configuration.
  - **Single Source of Truth**: API response types are imported directly from DTOs to ensure consistency.
- **DTOs (`src/data/dtos`)**: Data Transfer Objects defining the shape of data returned by the API (typically snake_case).
- **Mappers (`src/data/mappers`)**: Functions to transform DTOs into Domain Models (camelCase).
  - **Strict Typing**: Mappers enforce strict type boundaries and handle data validation (e.g., Enum conversion) to ensure only valid data reaches the Domain Layer.
- **Repositories (`src/data/repositories`)**: Concrete implementations of the Domain Repository interfaces (e.g., `SubscriptionRepositoryImpl.ts`). They coordinate between API clients, local storage, or other data sources.
- **Redux (`src/data/redux`)**: State management logic using Redux Toolkit slices for global UI state.

### 3. Presentation Layer (`src/presentation`)

This layer handles the User Interface and user interactions.

- **Components**: Reusable UI components.
- **Pages**: Top-level route components.
  - `LandingPage`: The entry page of the application.
  - `UserMap`: Interactive map for users.
  - `ManagerDashboard`: Dashboard for system managers.
  - `ControlTrafficPage`: Interface for controlling traffic systems.
  - `DeviceManagementPage`: Page for managing IoT devices.
  - `SubscriptionPage`: Page for managing system alerts and subscriptions.
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
