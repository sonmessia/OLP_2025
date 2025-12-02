// src/infrastructure/store/store.ts
import { configureStore } from "@reduxjs/toolkit";
import sumoReducer from "./sumoSlice";

// Initial state
const initialState = {};

// Basic reducers
const rootReducer = {
  // Add your reducers here as you create them
  // Example:
  // auth: authReducer,
  // sensors: sensorsReducer,
  // airQuality: airQualityReducer,
  sumo: sumoReducer,
};

export const store = configureStore({
  reducer: rootReducer,
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: {
        // Ignore Date objects in state
        ignoredActions: [
          "sensors/fetchAll/fulfilled",
          "sensors/refresh/fulfilled",
          "sumo/fetchStatus/fulfilled",
          "sumo/startSimulation/fulfilled",
          "sumo/fetchState/fulfilled",
          "sumo/performAIStep/fulfilled",
        ],
        ignoredPaths: [
          "sensors.sensors",
          "sensors.selectedSensor",
          "sumo.lastUpdated",
          "sumo.aiControlState.lastDecisionTime",
        ],
      },
    }),
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
