# Clean Architecture Workflow for React/Redux/TypeScript

## 1. Workflow Overview (Data Flow)

```
         ┌───────────────────────┐
         │    Presentation/UI    │
         │  (Components, Pages)  │
         └───────────┬───────────┘
                     │ User Action
                     ▼
            ┌─────────────────────┐
            │    Use Case         │
            │   (Domain Layer)    │
            └──────────┬──────────┘
                       │ Calls
                       ▼
          ┌───────────────────────────┐
          │  Repository Interface     │
          │     (Domain Layer)        │
          └────────────┬──────────────┘
                       │ Implementation
                       ▼
     ┌────────────────────────────────────┐
     │   Repository Implementation        │
     │   (Infrastructure Layer)           │
     └──────────────────┬─────────────────┘
                         │ Calls API
                         ▼
            ┌────────────────────────┐
            │        API Layer       │
            │ (Axios/Fetch Rest API) │
            └────────────┬───────────┘
                         │ Returns DTO
                         ▼
               ┌──────────────────────┐
               │        Mappers       │
               │ (DTO → Model, Model → DTO)
               └───────────┬──────────┘
                           │ Clean data model
                           ▼
             ┌────────────────────────┐
             │     Redux/Data Layer   │
             │ (Slices, Store, State) │
             └─────────────┬──────────┘
                           │ Updates State
                           ▼
        ┌────────────────────────────────┐
        │   Presentation/UI Re-renders   │
        └────────────────────────────────┘
```

---

## 2. Folder Structure

```
src/
├── api/                     # Raw HTTP calls
├── core/                    # App bootstrap (App.tsx, router)
├── data/                    # Redux, DTOs, Mappers
│   ├── redux/
│   ├── dtos/
│   └── mappers/
├── domain/                  # Business logic, pure TS
│   ├── models/
│   └── use-cases/
├── services/          # Repositories + External Services
│   └── repositories/
├── presentation/            # UI Layer
│   ├── components/
│   ├── pages/
│   ├── containers/
│   └── hooks/
└── shared/                  # Utils, constants, config
```

---

## 3. Layer Responsibilities

### Domain Layer

- Contains business rules.
- Independent from React, Redux, API.
- Includes:

  - `models/` → Entities (User, Product…)
  - `use-cases/` → Pure business actions

### Data Layer

- Handles global state & data normalization.
- Includes:

  - Redux slices
  - DTO definitions
  - Mappers (DTO ↔ Model)

### Service Layer

- Implements Repository Interfaces.
- Connects business logic to external sources.

### API Layer

- Performs HTTP calls.
- Contains no business logic.

### Presentation Layer

- UI Components
- Pages & Views
- Hooks & interactions

---

## 4. Example Workflow Description

### Scenario: User clicks "Get Profile"

1. **UI Component** dispatches `getUserProfile()` action.
2. Action triggers a **Use Case**: `GetUserProfileUseCase`.
3. Use Case calls **UserRepository Interface**.
4. Infrastructure provides **UserRepositoryImpl**, which calls `user-api.ts`.
5. `user-api.ts` returns a **DTO**.
6. Mapper transforms DTO → Domain Model.
7. Redux slice updates state with Model.
8. UI re-renders automatically.

---

## 5. Benefits

- Framework independent
- Easy unit testing
- High scalability
- Separation of concerns
- Stable business logic regardless of API/UI changes

---

## 6. Notes

- Domain layer **never imports** from services, data, presentation.
- API response changes **never affect business logic**.
- Redux & UI are replaceable without touching domain.
