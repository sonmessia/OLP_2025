import React, { useState, useEffect, useCallback } from "react";
import { useTranslation } from "react-i18next";
import { useAppDispatch, useAppSelector } from "../../../../data/redux/hooks";
import {
  startSimulation,
  stopSimulation,
  fetchSumoStatus,
  performSimulationStep,
} from "../../../../data/redux/sumoSlice";
import { SumoModelFactory } from "../../../../domain/models/SumoModels";
import { Settings } from "lucide-react";
import { SumoStatusDisplay } from "./components/SumoStatusDisplay";
import { SumoSettings } from "./components/SumoSettings";
import { SumoActionButtons } from "./components/SumoActionButtons";

interface SumoControlPanelProps {
  onLog?: (message: string) => void;
}

export const SumoControlPanel: React.FC<SumoControlPanelProps> = ({
  onLog,
}) => {
  const { t } = useTranslation("sumo");
  const dispatch = useAppDispatch();
  const { status, isLoading, isSimulationRunning, simulationState, error } =
    useAppSelector((state) => state.sumo);

  const [selectedScenario, setSelectedScenario] = useState("Nga4ThuDuc");
  const [useGUI, setUseGUI] = useState(false);
  const [port, setPort] = useState(8813);
  const [isStepping, setIsStepping] = useState(false);
  const [autoStep, setAutoStep] = useState(false);

  const handleStartSumo = async () => {
    try {
      const config = SumoModelFactory.createConfiguration(
        selectedScenario,
        useGUI,
        port
      );
      await dispatch(startSimulation(config)).unwrap();
      onLog?.(t("controlPanel.log.started", { scenario: selectedScenario }));
    } catch (error) {
      onLog?.(t("controlPanel.log.startFailed", { error }));
    }
  };

  const handleStopSumo = async () => {
    try {
      setAutoStep(false);
      setAutoStep(false);
      await dispatch(stopSimulation()).unwrap();
      onLog?.(t("controlPanel.log.stopped"));
    } catch (error) {
      onLog?.(t("controlPanel.log.stopFailed", { error }));
    }
  };

  const handleStepForward = useCallback(async () => {
    if (!isSimulationRunning) return;
    setIsStepping(true);
    try {
      await dispatch(performSimulationStep()).unwrap();
      onLog?.(
        t("controlPanel.log.stepExecuted", {
          time: simulationState?.simulationTime || "N/A",
        })
      );
    } catch (error) {
      onLog?.(t("controlPanel.log.stepFailed", { error }));
    } finally {
      setIsStepping(false);
    }
  }, [
    dispatch,
    isSimulationRunning,
    onLog,
    simulationState?.simulationTime,
    t,
  ]);

  const handleRefreshStatus = async () => {
    try {
      await dispatch(fetchSumoStatus()).unwrap();
      onLog?.(t("controlPanel.log.refreshed"));
    } catch (error) {
      onLog?.(t("controlPanel.log.refreshFailed", { error }));
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
      <div className="flex items-center gap-3 mb-6">
        <Settings className="w-6 h-6 text-emerald-600 dark:text-emerald-400" />
        <h2 className="text-xl font-bold text-gray-900 dark:text-white">
          {t("controlPanel.title")}
        </h2>
      </div>

      <SumoStatusDisplay
        status={status}
        simulationState={simulationState}
        error={error}
      />

      <SumoSettings
        selectedScenario={selectedScenario}
        setSelectedScenario={setSelectedScenario}
        useGUI={useGUI}
        setUseGUI={setUseGUI}
        port={port}
        setPort={setPort}
        isSimulationRunning={isSimulationRunning}
      />

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
