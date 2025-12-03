import React, { useState, useEffect, useCallback } from "react";
import { useAppDispatch, useAppSelector } from "../../../../data/redux/hooks";
import {
  startSimulation,
  stopSimulation,
  fetchSumoStatus,
  performSimulationStep,
} from "../../../../data/redux/sumoSlice";
import { SumoModelFactory } from "../../../../domain/models/SumoModels";
import { Settings, MapPin } from "lucide-react";
import { SumoStatusDisplay } from "../sumo/components/SumoStatusDisplay";
import { SumoActionButtons } from "../sumo/components/SumoActionButtons";

interface AreaControlPanelProps {
  areaName: string;
  onLog?: (message: string) => void;
}

export const AreaControlPanel: React.FC<AreaControlPanelProps> = ({
  areaName,
  onLog,
}) => {
  const dispatch = useAppDispatch();
  const { status, isLoading, isSimulationRunning, simulationState, error } =
    useAppSelector((state) => state.sumo);

  // Hardcoded for now, but could be mapped from areaName
  const scenario = "Nga4ThuDuc";
  const [useGUI, setUseGUI] = useState(false);
  const [port] = useState(8813);
  const [isStepping, setIsStepping] = useState(false);
  const [autoStep, setAutoStep] = useState(false);

  const handleStartSumo = async () => {
    try {
      const config = SumoModelFactory.createConfiguration(
        scenario,
        useGUI,
        port
      );
      await dispatch(startSimulation(config)).unwrap();
      onLog?.(`✅ Đã kết nối tới hệ thống điều khiển tại: ${areaName}`);
    } catch (error) {
      onLog?.(`❌ Kết nối thất bại: ${error}`);
    }
  };

  const handleStopSumo = async () => {
    try {
      setAutoStep(false);
      await dispatch(stopSimulation()).unwrap();
      onLog?.("🛑 Đã ngắt kết nối hệ thống");
    } catch (error) {
      onLog?.(`❌ Ngắt kết nối thất bại: ${error}`);
    }
  };

  const handleStepForward = useCallback(async () => {
    if (!isSimulationRunning) return;
    setIsStepping(true);
    try {
      await dispatch(performSimulationStep()).unwrap();
      onLog?.(
        `⏭️ Simulation step executed at time: ${
          simulationState?.simulationTime || "N/A"
        }`
      );
    } catch (error) {
      onLog?.(`❌ Failed to execute step: ${error}`);
    } finally {
      setIsStepping(false);
    }
  }, [dispatch, isSimulationRunning, onLog, simulationState?.simulationTime]);

  const handleRefreshStatus = async () => {
    try {
      await dispatch(fetchSumoStatus()).unwrap();
      onLog?.("🔄 Đã cập nhật trạng thái");
    } catch (error) {
      onLog?.(`❌ Cập nhật thất bại: ${error}`);
    }
  };

  useEffect(() => {
    if (autoStep && isSimulationRunning && !isStepping) {
      const interval = setInterval(() => {
        handleStepForward();
      }, 1000);
      return () => clearInterval(interval);
    }
  }, [autoStep, isSimulationRunning, isStepping, handleStepForward]);

  return (
    <div className="glass-card rounded-xl p-6 shadow-xl">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-3">
          <Settings className="w-6 h-6 text-emerald-600 dark:text-emerald-400" />
          <h2 className="text-xl font-bold text-gray-900 dark:text-white">
            Điều khiển khu vực
          </h2>
        </div>
        <div className="flex items-center gap-2 px-3 py-1 bg-blue-50 dark:bg-blue-900/20 rounded-full">
          <MapPin className="w-4 h-4 text-blue-600 dark:text-blue-400" />
          <span className="text-sm font-medium text-blue-700 dark:text-blue-300">
            {areaName}
          </span>
        </div>
      </div>

      <SumoStatusDisplay
        status={status}
        simulationState={simulationState}
        error={error}
      />

      <div className="my-4">
        <label className="flex items-center space-x-2 cursor-pointer">
          <input
            type="checkbox"
            checked={useGUI}
            onChange={(e) => setUseGUI(e.target.checked)}
            disabled={isSimulationRunning}
            className="form-checkbox h-4 w-4 text-emerald-600 rounded border-gray-300 focus:ring-emerald-500"
          />
          <span className="text-sm text-gray-700 dark:text-gray-300">
            Hiển thị giao diện mô phỏng (SUMO GUI)
          </span>
        </label>
      </div>

      <SumoActionButtons
        isSimulationRunning={isSimulationRunning}
        isLoading={isLoading}
        isStepping={isStepping}
        autoStep={autoStep}
        setAutoStep={setAutoStep}
        onStart={handleStartSumo}
        onStop={handleStopSumo}
        onStep={handleStepForward}
        onRefresh={handleRefreshStatus}
      />
    </div>
  );
};
