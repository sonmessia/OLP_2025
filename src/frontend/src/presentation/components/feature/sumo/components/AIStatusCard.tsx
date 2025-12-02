import React from "react";
import { Circle, Info } from "lucide-react";

interface AIStatusCardProps {
  aiControlState: any;
  onShowDetails: () => void;
}

export const AIStatusCard: React.FC<AIStatusCardProps> = ({
  aiControlState,
  onShowDetails,
}) => {
  if (!aiControlState) return null;

  const getStatusColor = () => {
    switch (aiControlState.status) {
      case "ENABLED":
        return "text-emerald-500";
      case "INITIALIZING":
        return "text-yellow-500";
      case "ERROR":
        return "text-red-500";
      default:
        return "text-gray-500";
    }
  };

  const getStatusIcon = () => {
    switch (aiControlState.status) {
      case "ENABLED":
      case "INITIALIZING":
      case "ERROR":
        return <Circle className="w-4 h-4 fill-current" />;
      default:
        return <Circle className="w-4 h-4" />;
    }
  };

  return (
    <div className="space-y-4">
      {/* Status Card */}
      <div className="bg-gray-50 dark:bg-gray-800/50 rounded-lg p-4">
        <div className="flex items-center justify-between mb-3">
          <span className="text-xs text-gray-600 dark:text-gray-400">
            AI Status
          </span>
          <div className={`flex items-center gap-2 ${getStatusColor()}`}>
            {getStatusIcon()}
            <span className="text-sm font-bold">{aiControlState.status}</span>
          </div>
        </div>

        <div className="flex items-center justify-between">
          <span className="text-xs text-gray-600 dark:text-gray-400">
            Controlled Lights
          </span>
          <span className="text-sm font-bold text-gray-900 dark:text-white">
            {aiControlState.numTrafficLights} lights
          </span>
        </div>
      </div>

      {/* Model Info - Clickable */}
      <button
        onClick={onShowDetails}
        className="w-full bg-gradient-to-r from-emerald-50 to-blue-50 dark:from-emerald-900/20 dark:to-blue-900/20 
                   rounded-lg p-4 border border-emerald-200 dark:border-emerald-800
                   hover:shadow-lg transition-all duration-200 hover:scale-105 text-left"
      >
        <div className="flex items-center justify-between">
          <div>
            <p className="text-xs text-emerald-600 dark:text-emerald-400 mb-1">
              AI Model
            </p>
            <p className="text-sm font-bold text-emerald-900 dark:text-emerald-100">
              {aiControlState.algorithm || "GreenWave DQN"}
            </p>
          </div>
          <Info className="w-5 h-5 text-emerald-600 dark:text-emerald-400" />
        </div>
      </button>

      {/* Last Decision Time */}
      {aiControlState.lastDecisionTime && (
        <div className="bg-purple-50 dark:bg-purple-900/20 rounded-lg p-4 border-l-4 border-purple-500">
          <p className="text-xs text-purple-600 dark:text-purple-400 mb-1">
            Last Decision
          </p>
          <p className="text-sm font-bold text-purple-900 dark:text-purple-100">
            {new Date(aiControlState.lastDecisionTime).toLocaleTimeString(
              "vi-VN"
            )}
          </p>
        </div>
      )}
    </div>
  );
};
