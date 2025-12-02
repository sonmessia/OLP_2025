// src/infrastructure/store/store.ts
import { configureStore } from "@reduxjs/toolkit";

export const store = configureStore({
  reducer: {},
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: {
        // Ignore Date objects in state
        ignoredActions: [
          "sensors/fetchAll/fulfilled",
          "sensors/refresh/fulfilled",
        ],
        ignoredPaths: ["sensors.sensors", "sensors.selectedSensor"],
      },
    }),
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
