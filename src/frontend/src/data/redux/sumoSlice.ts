// Redux Slice - SUMO State Management
// Tuân thủ Clean Architecture: quản lý state và async actions

import {
  createSlice,
  createAsyncThunk,
  type PayloadAction,
} from "@reduxjs/toolkit";
import type {
  SumoDashboardState,
  SumoStatus,
  SumoSimulationState,
  AIControlState,
  AIStepResult,
  ScenarioInfo,
  SumoConfiguration,
} from "../../domain/models/SumoModels";
import { SumoModelFactory } from "../../domain/models/SumoModels";
import { SumoMapper, SumoReverseMapper } from "../mappers/SumoMapper";
import {
  getSumoStatus,
  startSumoSimulation,
  getSumoState,
  executeSumoStep,
  stopSumoSimulation,
  enableAIControl,
  executeAIStep,
  disableAIControl,
} from "../../api/sumoApi";

/**
 * SUMO Slice State
 */
interface SumoSliceState extends SumoDashboardState {
  isLoading: boolean;
  error: string | null;
  isSimulationRunning: boolean;
  isAIControlActive: boolean;
}

/**
 * Initial State with hardcoded scenarios
 */
const initialState: SumoSliceState = {
  ...SumoModelFactory.createDefaultDashboardState(),
  scenarios: [
    {
      id: "Nga4ThuDuc",
      name: "Ngã Tư Thủ Đức",
      description: "Ngã Tư Thủ Đức (4-way)",
      configFile: "Nga4ThuDuc.sumocfg",
    },
    {
      id: "NguyenThaiSon",
      name: "Ngã 6 Nguyễn Thái Sơn",
      description: "Ngã 6 Nguyễn Thái Sơn (6-way)",
      configFile: "NguyenThaiSon.sumocfg",
    },
    {
      id: "QuangTrung",
      name: "Quang Trung",
      description: "Quang Trung (Complex)",
      configFile: "QuangTrung.sumocfg",
    },
  ],
  isLoading: false,
  error: null,
  isSimulationRunning: false,
  isAIControlActive: false,
};

/**
 * Async Thunks
 */

// Fetch SUMO Status
export const fetchSumoStatus = createAsyncThunk(
  "sumo/fetchStatus",
  async (_, { rejectWithValue }) => {
    try {
      const response = await getSumoStatus();
      return SumoMapper.mapSumoStatus(response);
    } catch (error: unknown) {
      return rejectWithValue(
        error instanceof Error ? error.message : "Failed to fetch SUMO status"
      );
    }
  }
);

// Start SUMO Simulation
export const startSimulation = createAsyncThunk(
  "sumo/startSimulation",
  async (config: SumoConfiguration, { rejectWithValue }) => {
    try {
      const requestDTO = SumoReverseMapper.mapStartRequest(
        config.scenario,
        config.gui,
        config.port
      );
      const response = await startSumoSimulation(requestDTO);

      return {
        status: SumoMapper.mapSumoStatus({
          connected: true,
          scenario: response.scenario,
          description: response.description,
          tls_id: response.tls_id,
        }),
        initialState: response.initial_state
          ? SumoMapper.mapSumoState(response.initial_state)
          : null,
      };
    } catch (error: unknown) {
      return rejectWithValue(
        error instanceof Error
          ? error.message
          : "Failed to start SUMO simulation"
      );
    }
  }
);

// Fetch SUMO State
export const fetchSumoState = createAsyncThunk(
  "sumo/fetchState",
  async (_, { rejectWithValue }) => {
    try {
      const response = await getSumoState();
      return SumoMapper.mapSumoState(response);
    } catch (error: unknown) {
      return rejectWithValue(
        error instanceof Error ? error.message : "Failed to fetch SUMO state"
      );
    }
  }
);

// Execute Simulation Step
export const performSimulationStep = createAsyncThunk(
  "sumo/performStep",
  async (_, { rejectWithValue }) => {
    try {
      const response = await executeSumoStep();
      return SumoMapper.mapSumoState(response.state);
    } catch (error: unknown) {
      return rejectWithValue(
        error instanceof Error
          ? error.message
          : "Failed to execute simulation step"
      );
    }
  }
);

// Stop SUMO Simulation
export const stopSimulation = createAsyncThunk(
  "sumo/stopSimulation",
  async (_, { rejectWithValue }) => {
    try {
      await stopSumoSimulation();
      return true;
    } catch (error: unknown) {
      return rejectWithValue(
        error instanceof Error
          ? error.message
          : "Failed to stop SUMO simulation"
      );
    }
  }
);

// Scenarios are hardcoded in initial state (backend doesn't have /sumo/scenarios endpoint)

// Enable AI Control
export const activateAIControl = createAsyncThunk(
  "sumo/activateAI",
  async (_, { rejectWithValue }) => {
    try {
      const response = await enableAIControl();
      return SumoMapper.mapAIControlState(response);
    } catch (error: unknown) {
      return rejectWithValue(
        error instanceof Error ? error.message : "Failed to enable AI control"
      );
    }
  }
);

// Execute AI Step
export const performAIStep = createAsyncThunk(
  "sumo/performAIStep",
  async (_, { rejectWithValue }) => {
    try {
      const response = await executeAIStep();
      return SumoMapper.mapAIStepResult(response);
    } catch (error: unknown) {
      return rejectWithValue(
        error instanceof Error ? error.message : "Failed to execute AI step"
      );
    }
  }
);

// Disable AI Control
export const deactivateAIControl = createAsyncThunk(
  "sumo/deactivateAI",
  async (_, { rejectWithValue }) => {
    try {
      await disableAIControl();
      return true;
    } catch (error: unknown) {
      return rejectWithValue(
        error instanceof Error ? error.message : "Failed to disable AI control"
      );
    }
  }
);

/**
 * SUMO Slice
 */
const sumoSlice = createSlice({
  name: "sumo",
  initialState,
  reducers: {
    clearError: (state) => {
      state.error = null;
    },
    updateLastUpdated: (state) => {
      state.lastUpdated = new Date();
    },
    incrementAIActionCount: (state) => {
      if (state.aiControlState) {
        state.aiControlState.actionCount += 1;
      }
    },
  },
  extraReducers: (builder) => {
    // Fetch Status
    builder
      .addCase(fetchSumoStatus.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(
        fetchSumoStatus.fulfilled,
        (state, action: PayloadAction<SumoStatus>) => {
          state.isLoading = false;
          state.status = action.payload;
          // Update isSimulationRunning based on connection status
          if (action.payload.connected) {
            state.isSimulationRunning = true;
          }
          state.lastUpdated = new Date();
        }
      )
      .addCase(fetchSumoStatus.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      });

    // Start Simulation
    builder
      .addCase(startSimulation.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(startSimulation.fulfilled, (state, action) => {
        state.isLoading = false;
        state.status = action.payload.status;
        state.simulationState = action.payload.initialState;
        state.isSimulationRunning = true;
        state.lastUpdated = new Date();
      })
      .addCase(startSimulation.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      });

    // Fetch State
    builder
      .addCase(fetchSumoState.pending, (state) => {
        state.error = null;
      })
      .addCase(
        fetchSumoState.fulfilled,
        (state, action: PayloadAction<SumoSimulationState>) => {
          state.simulationState = action.payload;
          state.lastUpdated = new Date();
        }
      )
      .addCase(fetchSumoState.rejected, (state, action) => {
        state.error = action.payload as string;
      });

    // Perform Step
    builder.addCase(
      performSimulationStep.fulfilled,
      (state, action: PayloadAction<SumoSimulationState>) => {
        state.simulationState = action.payload;
        state.lastUpdated = new Date();
      }
    );

    // Stop Simulation
    builder.addCase(stopSimulation.fulfilled, (state) => {
      state.isSimulationRunning = false;
      state.isAIControlActive = false;
      state.status = SumoModelFactory.createDefaultStatus();
      state.simulationState = null;
      state.aiControlState = null;
      state.lastUpdated = new Date();
    });

    // Scenarios are hardcoded in initial state

    // Activate AI
    builder
      .addCase(activateAIControl.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(
        activateAIControl.fulfilled,
        (state, action: PayloadAction<AIControlState>) => {
          state.isLoading = false;
          state.aiControlState = action.payload;
          state.isAIControlActive = true;
          state.lastUpdated = new Date();
        }
      )
      .addCase(activateAIControl.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      });

    // Perform AI Step
    builder.addCase(
      performAIStep.fulfilled,
      (state, action: PayloadAction<AIStepResult>) => {
        if (state.aiControlState) {
          state.aiControlState.actionCount += action.payload.totalSwitches;
          state.aiControlState.lastDecisionTime = new Date();
        }
        state.lastUpdated = new Date();
      }
    );

    // Deactivate AI
    builder.addCase(deactivateAIControl.fulfilled, (state) => {
      state.isAIControlActive = false;
      state.aiControlState = SumoModelFactory.createDefaultAIControlState();
      state.lastUpdated = new Date();
    });
  },
});

export const { clearError, updateLastUpdated, incrementAIActionCount } =
  sumoSlice.actions;
export default sumoSlice.reducer;
