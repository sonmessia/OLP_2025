// Copyright (c) 2025 Green Wave Team
// 
// This software is released under the MIT License.
// https://opensource.org/licenses/MIT

// src/infrastructure/store/store.ts
import { configureStore } from "@reduxjs/toolkit";
import sumoReducer from "./sumoSlice";
import authReducer from "./authSlice";

// Basic reducers
const rootReducer = {
  auth: authReducer,
  // Add your reducers here as you create them
  // sensors: sensorsReducer,
  // airQuality: airQualityReducer,
  sumo: sumoReducer,
};

import { sumoApi } from "../../api/sumoApi";
import { authApi } from "../../api/authApi";

export const store = configureStore({
  reducer: rootReducer,
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      thunk: {
        extraArgument: {
          sumoApi,
          authApi,
        },
      },
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
