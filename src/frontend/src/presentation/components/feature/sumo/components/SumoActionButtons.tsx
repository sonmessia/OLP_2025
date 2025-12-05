import React from "react";
import { useTranslation } from "react-i18next";
import {
  Play,
  Square,
  SkipForward,
  PlayCircle,
  PauseCircle,
  RefreshCw,
} from "lucide-react";

interface SumoActionButtonsProps {
  isSimulationRunning: boolean;
  isLoading: boolean;
  isStepping: boolean;
  autoStep: boolean;
  setAutoStep: (value: boolean) => void;
  onStart: () => void;
  onStop: () => void;
  onStep: () => void;
  onRefresh: () => void;
  disabled?: boolean;
}

export const SumoActionButtons: React.FC<SumoActionButtonsProps> = ({
  isSimulationRunning,
  isLoading,
  isStepping,
  autoStep,
  setAutoStep,
  onStart,
  onStop,
  onStep,
  onRefresh,
  disabled = false,
}) => {
  const { t } = useTranslation(["traffic", "common"]);
  return (
    <div className="space-y-3">
      <div className="grid grid-cols-2 gap-3">
        <button
          onClick={onStart}
          disabled={isSimulationRunning || isLoading || disabled}
          className="flex items-center justify-center gap-2 px-4 py-3 eco-gradient-primary text-white font-semibold rounded-lg
                     transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed
                     hover:shadow-lg hover:scale-105 disabled:hover:scale-100"
        >
          <Play className="w-4 h-4" />
          <Play className="w-4 h-4" />
          {isLoading ? t("traffic:connecting") : t("common:start")}
        </button>

        <button
          onClick={onStop}
          disabled={!isSimulationRunning || isLoading || disabled}
          className="flex items-center justify-center gap-2 px-4 py-3 bg-gray-600 hover:bg-gray-700 text-white font-semibold rounded-lg
                     transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed
                     hover:shadow-lg hover:scale-105 disabled:hover:scale-100"
        >
          <Square className="w-4 h-4" />
          {t("common:stop")}
        </button>
      </div>

      {/* Step Controls */}
      <div className="grid grid-cols-3 gap-2">
        <button
          onClick={onStep}
          disabled={!isSimulationRunning || isStepping || disabled}
          className="flex items-center justify-center gap-1 px-3 py-2 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg
                     transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed text-sm"
        >
          <SkipForward className="w-4 h-4" />
          <SkipForward className="w-4 h-4" />
          {t("traffic:stepForward")}
        </button>

        <button
          onClick={() => setAutoStep(!autoStep)}
          disabled={!isSimulationRunning || disabled}
          className={`flex items-center justify-center gap-1 px-3 py-2 font-medium rounded-lg transition-all duration-200
                     disabled:opacity-50 disabled:cursor-not-allowed text-sm
                     ${
                       autoStep
                         ? "bg-red-600 hover:bg-red-700 text-white"
                         : "bg-indigo-600 hover:bg-indigo-700 text-white"
                     }`}
        >
          {autoStep ? (
            <PauseCircle className="w-4 h-4" />
          ) : (
            <PlayCircle className="w-4 h-4" />
          )}
          {t("traffic:autoStep")}
        </button>

        <button
          onClick={onRefresh}
          disabled={isLoading || disabled}
          className="flex items-center justify-center gap-1 px-3 py-2 bg-purple-600 hover:bg-purple-700 text-white font-medium rounded-lg
                     transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed text-sm"
        >
          <RefreshCw className="w-4 h-4" />
        </button>
      </div>
    </div>
  );
};
