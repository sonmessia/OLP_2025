# SUMO API Client

API client cho hệ thống điều khiển giao thông thông minh SUMO (Simulation of Urban MObility).

## Cấu trúc

```
src/frontend/src/api/
├── sumoApi.ts       # SUMO API client functions
├── sumoTypes.ts     # TypeScript type definitions
├── axiosConfig.ts   # Axios configuration
└── index.ts         # Export tất cả APIs
```

## API Endpoints

### 1. Kiểm tra trạng thái SUMO

```typescript
import { getSumoStatus } from "@/api";

const status = await getSumoStatus();
// Returns: { connected: boolean, scenario?: string, tls_id?: string, ... }
```

### 2. Khởi động SUMO Simulation

```typescript
import { startSumoSimulation } from "@/api";

const response = await startSumoSimulation({
  scenario: "Nga4ThuDuc",
  gui: false,
  port: 8813,
});
// Returns: { status, message, description, tls_id, initial_state, ... }
```

### 3. Lấy trạng thái real-time

```typescript
import { getSumoState } from "@/api";

const state = await getSumoState();
// Returns: {
//   simulation_time,
//   vehicle_count,
//   avg_speed,
//   traffic_lights,
//   ...
// }
```

### 4. Thực hiện một bước simulation

```typescript
import { executeSumoStep } from "@/api";

const stepResult = await executeSumoStep();
// Returns: { time, state, step_count }
```

### 5. Dừng SUMO Simulation

```typescript
import { stopSumoSimulation } from "@/api";

const result = await stopSumoSimulation();
// Returns: { status: 'success', message: '...' }
```

### 6. Lấy danh sách scenarios

```typescript
import { getSumoScenarios } from "@/api";

const scenarios = await getSumoScenarios();
// Returns: ScenarioInfo[]
```

### 7. Bật AI Traffic Control

```typescript
import { enableAIControl } from "@/api";

const aiStatus = await enableAIControl();
// Returns: {
//   status,
//   message,
//   num_traffic_lights,
//   algorithm,
//   features
// }
```

### 8. Thực hiện AI Control Step

```typescript
import { executeAIStep } from "@/api";

const aiDecisions = await executeAIStep();
// Returns: {
//   simulation_time,
//   decisions: AIDecision[],
//   total_switches,
//   total_holds
// }
```

### 9. Tắt AI Control

```typescript
import { disableAIControl } from "@/api";

const result = await disableAIControl();
// Returns: { status: 'success', message: '...' }
```

## Sử dụng trong React Components

### Ví dụ 1: Hiển thị trạng thái SUMO

```typescript
import { useEffect, useState } from "react";
import { getSumoStatus, type SumoStatus } from "@/api";

function SumoStatusComponent() {
  const [status, setStatus] = useState<SumoStatus | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchStatus = async () => {
      try {
        const data = await getSumoStatus();
        setStatus(data);
      } catch (error) {
        console.error("Failed to fetch SUMO status:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchStatus();
    const interval = setInterval(fetchStatus, 5000); // Update every 5s

    return () => clearInterval(interval);
  }, []);

  if (loading) return <div>Loading...</div>;

  return (
    <div>
      <h2>SUMO Status</h2>
      <p>Connected: {status?.connected ? "✅" : "❌"}</p>
      <p>Scenario: {status?.scenario || "N/A"}</p>
      <p>Traffic Light ID: {status?.tls_id || "N/A"}</p>
    </div>
  );
}
```

### Ví dụ 2: Điều khiển SUMO Simulation

```typescript
import { useState } from "react";
import {
  startSumoSimulation,
  stopSumoSimulation,
  type SumoStartRequest,
} from "@/api";

function SumoControlPanel() {
  const [isRunning, setIsRunning] = useState(false);
  const [scenario, setScenario] = useState("Nga4ThuDuc");

  const handleStart = async () => {
    try {
      const request: SumoStartRequest = {
        scenario,
        gui: false,
        port: 8813,
      };

      const response = await startSumoSimulation(request);
      console.log("SUMO started:", response);
      setIsRunning(true);
    } catch (error) {
      console.error("Failed to start SUMO:", error);
      alert("Cannot start SUMO. Please check backend connection.");
    }
  };

  const handleStop = async () => {
    try {
      await stopSumoSimulation();
      setIsRunning(false);
    } catch (error) {
      console.error("Failed to stop SUMO:", error);
    }
  };

  return (
    <div>
      <select value={scenario} onChange={(e) => setScenario(e.target.value)}>
        <option value="Nga4ThuDuc">Ngã Tư Thủ Đức</option>
        <option value="NguyenThaiSon">Ngã 6 Nguyễn Thái Sơn</option>
        <option value="QuangTrung">Quang Trung</option>
      </select>

      <button onClick={handleStart} disabled={isRunning}>
        Start SUMO
      </button>
      <button onClick={handleStop} disabled={!isRunning}>
        Stop SUMO
      </button>
    </div>
  );
}
```

### Ví dụ 3: Real-time Traffic Data

```typescript
import { useEffect, useState } from "react";
import { getSumoState, type SumoState } from "@/api";

function TrafficMetrics() {
  const [state, setState] = useState<SumoState | null>(null);

  useEffect(() => {
    const fetchState = async () => {
      try {
        const data = await getSumoState();
        setState(data);
      } catch (error) {
        console.error("Failed to fetch SUMO state:", error);
      }
    };

    const interval = setInterval(fetchState, 1000); // Update every 1s
    return () => clearInterval(interval);
  }, []);

  if (!state) return <div>No data</div>;

  return (
    <div>
      <h2>Real-time Traffic Metrics</h2>
      <p>Vehicles: {state.vehicle_count}</p>
      <p>Avg Speed: {state.avg_speed.toFixed(1)} km/h</p>
      <p>Queue Length: {state.queue_length}</p>
      <p>Waiting Time: {state.waiting_time.toFixed(1)}s</p>

      <h3>Traffic Lights ({state.total_traffic_lights})</h3>
      {state.traffic_lights.map((tls) => (
        <div key={tls.id}>
          <strong>{tls.id}</strong>: Phase {tls.current_phase}({tls.time_until_switch.toFixed(
            1
          )}s)
        </div>
      ))}
    </div>
  );
}
```

### Ví dụ 4: AI Traffic Control

```typescript
import { useState } from "react";
import {
  enableAIControl,
  disableAIControl,
  executeAIStep,
  type AIStepResponse,
} from "@/api";

function AIControlPanel() {
  const [aiEnabled, setAiEnabled] = useState(false);
  const [lastDecision, setLastDecision] = useState<AIStepResponse | null>(null);

  const handleEnableAI = async () => {
    try {
      const response = await enableAIControl();
      console.log("AI enabled:", response);
      setAiEnabled(true);

      // Start AI control loop
      const interval = setInterval(async () => {
        const decision = await executeAIStep();
        setLastDecision(decision);
      }, 2000);

      // Store interval ID for cleanup
      (window as any).aiInterval = interval;
    } catch (error) {
      console.error("Failed to enable AI:", error);
    }
  };

  const handleDisableAI = async () => {
    try {
      await disableAIControl();
      setAiEnabled(false);

      // Clear interval
      if ((window as any).aiInterval) {
        clearInterval((window as any).aiInterval);
      }
    } catch (error) {
      console.error("Failed to disable AI:", error);
    }
  };

  return (
    <div>
      <h2>AI Traffic Control</h2>
      <button onClick={handleEnableAI} disabled={aiEnabled}>
        Enable AI
      </button>
      <button onClick={handleDisableAI} disabled={!aiEnabled}>
        Disable AI
      </button>

      {lastDecision && (
        <div>
          <h3>Last Decision (t={lastDecision.simulation_time.toFixed(0)}s)</h3>
          <p>Switches: {lastDecision.total_switches}</p>
          <p>Holds: {lastDecision.total_holds}</p>

          {lastDecision.decisions.map((d, i) => (
            <div key={i}>
              {d.tls_id}: {d.action}
              {d.action === "switch" && ` (${d.from_phase} → ${d.to_phase})`}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
```

## Type Definitions

Tất cả các types đều được export từ `sumoTypes.ts`:

- `SumoStatus` - Trạng thái kết nối SUMO
- `SumoState` - Trạng thái simulation real-time
- `SumoStartRequest` - Request để khởi động SUMO
- `SumoStartResponse` - Response khi khởi động thành công
- `SumoStepResponse` - Response của mỗi simulation step
- `AIControlResponse` - Response khi bật AI control
- `AIStepResponse` - Response của mỗi AI control step
- `AIDecision` - Quyết định của AI cho từng đèn giao thông
- `TrafficLight` - Thông tin đèn giao thông
- `TrafficLightSignal` - Trạng thái tín hiệu đèn
- `ScenarioInfo` - Thông tin scenario

## Configuration

Backend URL được cấu hình trong `axiosConfig.ts`:

```typescript
baseURL: import.meta.env.VITE_API_URL || "http://localhost:8000";
```

Để thay đổi backend URL, tạo file `.env` trong thư mục frontend:

```env
VITE_API_URL=http://your-backend-url:8000
```

## Error Handling

Tất cả các API functions đều throw error khi gặp lỗi. Nên wrap trong try-catch:

```typescript
try {
  const status = await getSumoStatus();
  // Handle success
} catch (error) {
  console.error("API Error:", error);
  // Handle error
}
```

## Notes

- Backend phải chạy trên `http://localhost:8000` (hoặc URL được cấu hình)
- SUMO simulation phải được khởi động trước khi sử dụng các API khác
- AI control chỉ hoạt động khi SUMO đã được kết nối
- Nên sử dụng polling (setInterval) để cập nhật real-time data
