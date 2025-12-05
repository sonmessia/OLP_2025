import React, { useState } from "react";
import { useAppDispatch, useAppSelector } from "../../../../data/redux/hooks";
import {
  performSimulationStep,
  stopSimulation,
} from "../../../../data/redux/sumoSlice";

interface SimulationControlPanelProps {
  onLog?: (message: string) => void;
}

export const SimulationControlPanel: React.FC<SimulationControlPanelProps> = ({
  onLog,
}) => {
  const dispatch = useAppDispatch();
  const { status, isSimulationRunning, simulationState } = useAppSelector(
    (state) => state.sumo
  );

  const [isRunning, setIsRunning] = useState(false);
  const [isPaused, setIsPaused] = useState(false);
  const [simulationSpeed, setSimulationSpeed] = useState(1);
  const [stepInterval, setStepInterval] = useState<number | null>(null);

  // Start simulation (auto-stepping)
  const handleStart = () => {
    if (!isSimulationRunning) {
      onLog?.(
        '❌ Please connect to SUMO first by clicking "Start SUMO" button'
      );
      return;
    }

    setIsRunning(true);
    setIsPaused(false);
    onLog?.("▶ Simulation started - Running SUMO steps");

    // Start auto-stepping based on speed
    const interval = setInterval(async () => {
      try {
        await dispatch(performSimulationStep()).unwrap();
      } catch (error) {
        console.error("Step error:", error);
      }
    }, 1000 / simulationSpeed);

    setStepInterval(interval);
  };

  // Pause simulation
  const handlePause = () => {
    if (stepInterval) {
      clearInterval(stepInterval);
      setStepInterval(null);
    }
    setIsRunning(false);
    setIsPaused(true);
    onLog?.("⏸ Simulation paused");
  };

  // Reset simulation
  const handleReset = async () => {
    if (stepInterval) {
      clearInterval(stepInterval);
      setStepInterval(null);
    }
    setIsRunning(false);
    setIsPaused(false);

    // Stop SUMO simulation
    try {
      await dispatch(stopSimulation()).unwrap();
      onLog?.("🔄 Simulation reset - SUMO stopped");
    } catch (error) {
      onLog?.(`❌ Failed to reset: ${error}`);
    }
  };

  // Update simulation speed
  const handleSpeedChange = (value: number) => {
    setSimulationSpeed(value);
    onLog?.(`Simulation speed changed to ${value}x`);

    // If currently running, restart with new speed
    if (isRunning && stepInterval) {
      clearInterval(stepInterval);

      const interval = setInterval(async () => {
        try {
          await dispatch(performSimulationStep()).unwrap();
        } catch (error) {
          console.error("Step error:", error);
        }
      }, 1000 / value);

      setStepInterval(interval);
    }
  };

  // Cleanup on unmount
  React.useEffect(() => {
    return () => {
      if (stepInterval) {
        clearInterval(stepInterval);
      }
    };
  }, [stepInterval]);

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
      <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-4">
        Control Panel
      </h2>

      {/* Control Buttons */}
      <div className="flex gap-3 mb-6">
        <button
          onClick={handleStart}
          disabled={isRunning || !isSimulationRunning}
          className="flex-1 px-4 py-3 bg-green-600 hover:bg-green-700 text-white font-bold rounded-lg
                     transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed
                     hover:shadow-lg disabled:hover:shadow-none"
        >
          ▶ Start
        </button>

        <button
          onClick={handlePause}
          disabled={!isRunning}
          className="flex-1 px-4 py-3 bg-gray-600 hover:bg-gray-700 text-white font-bold rounded-lg
                     transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed
                     hover:shadow-lg disabled:hover:shadow-none"
        >
          ⏸ Pause
        </button>

        <button
          onClick={handleReset}
          disabled={!isSimulationRunning}
          className="flex-1 px-4 py-3 bg-blue-600 hover:bg-blue-700 text-white font-bold rounded-lg
                     transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed
                     hover:shadow-lg disabled:hover:shadow-none"
        >
          🔄 Reset
        </button>
      </div>

      {/* Simulation Speed Control */}
      <div>
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Simulation Speed:{" "}
          <strong className="text-blue-600 dark:text-blue-400">
            {simulationSpeed}x
          </strong>
        </label>
        <input
          type="range"
          min="1"
          max="10"
          value={simulationSpeed}
          onChange={(e) => handleSpeedChange(Number(e.target.value))}
          className="w-full h-2 bg-gray-200 dark:bg-gray-700 rounded-lg appearance-none cursor-pointer
                     accent-blue-600"
        />
        <div className="flex justify-between text-xs text-gray-500 dark:text-gray-400 mt-1">
          <span>1x</span>
          <span>5x</span>
          <span>10x</span>
        </div>
      </div>

      {/* Status Info */}
      <div className="mt-6 p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
        <div className="grid grid-cols-2 gap-3 text-sm">
          <div>
            <span className="text-gray-600 dark:text-gray-400">Status:</span>
            <p className="font-bold text-gray-900 dark:text-white">
              {isRunning ? "🟢 Running" : isPaused ? "🟡 Paused" : "⚫ Stopped"}
            </p>
          </div>
          <div>
            <span className="text-gray-600 dark:text-gray-400">Sim Time:</span>
            <p className="font-bold text-gray-900 dark:text-white">
              {simulationState?.simulationTime.toFixed(1) || "0.0"}s
            </p>
          </div>
        </div>
      </div>

      {/* Instructions */}
      {!isSimulationRunning && (
        <div className="mt-4 p-3 bg-yellow-50 dark:bg-yellow-900/20 border-l-4 border-yellow-400 rounded">
          <p className="text-xs text-yellow-800 dark:text-yellow-200">
            <strong>⚠️ SUMO Status:</strong>{" "}
            {status.connected ? (
              <>
                🟢 Connected to {status.scenario || "SUMO"} but simulation not
                started.
                <br />
                Please click "Start SUMO" button to begin simulation.
              </>
            ) : (
              <>⚫ Not connected. Please start SUMO connection first.</>
            )}
          </p>
        </div>
      )}
    </div>
  );
};
