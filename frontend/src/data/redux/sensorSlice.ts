// src/infrastructure/store/sensorSlice.ts
import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import type { PayloadAction } from "@reduxjs/toolkit";
import type { SensorModel } from "../../domain/models/SenSorModel";
import { ServiceContainer } from "../../services/di/ServiceContainer";

interface SensorState {
  sensors: SensorModel[];
  selectedSensor: SensorModel | null;
  loading: boolean;
  error: string | null;
}

const initialState: SensorState = {
  sensors: [],
  selectedSensor: null,
  loading: false,
  error: null,
};

// Async Thunks
export const fetchAllSensors = createAsyncThunk(
  "sensors/fetchAll",
  async (_, { rejectWithValue }) => {
    try {
      const useCase =
        ServiceContainer.getInstance().createGetAllSensorsUseCase();
      return await useCase.execute();
    } catch (error) {
      return rejectWithValue((error as Error).message);
    }
  }
);

export const fetchSensorById = createAsyncThunk(
  "sensors/fetchById",
  async (id: string, { rejectWithValue }) => {
    try {
      const useCase =
        ServiceContainer.getInstance().createGetSensorByIdUseCase();
      return await useCase.execute(id);
    } catch (error) {
      return rejectWithValue((error as Error).message);
    }
  }
);

export const refreshSensors = createAsyncThunk(
  "sensors/refresh",
  async (_, { rejectWithValue }) => {
    try {
      const useCase =
        ServiceContainer.getInstance().createRefreshSensorsUseCase();
      return await useCase.execute();
    } catch (error) {
      return rejectWithValue((error as Error).message);
    }
  }
);

const sensorSlice = createSlice({
  name: "sensors",
  initialState,
  reducers: {
    setSelectedSensor: (state, action: PayloadAction<SensorModel | null>) => {
      state.selectedSensor = action.payload;
    },
    clearError: (state) => {
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
      // Fetch All Sensors
      .addCase(fetchAllSensors.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchAllSensors.fulfilled, (state, action) => {
        state.loading = false;
        state.sensors = action.payload;
      })
      .addCase(fetchAllSensors.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      })
      // Fetch Sensor By Id
      .addCase(fetchSensorById.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchSensorById.fulfilled, (state, action) => {
        state.loading = false;
        state.selectedSensor = action.payload;
      })
      .addCase(fetchSensorById.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      })
      // Refresh Sensors
      .addCase(refreshSensors.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(refreshSensors.fulfilled, (state, action) => {
        state.loading = false;
        state.sensors = action.payload;
      })
      .addCase(refreshSensors.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      });
  },
});

export const { setSelectedSensor, clearError } = sensorSlice.actions;
export default sensorSlice.reducer;
