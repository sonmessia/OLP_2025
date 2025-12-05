import { useTranslation } from "react-i18next";
import { Eye } from "lucide-react";

interface SumoSettingsProps {
  selectedScenario: string;
  setSelectedScenario: (value: string) => void;
  useGUI: boolean;
  setUseGUI: (value: boolean) => void;
  port: number;
  setPort: (value: number) => void;
  isSimulationRunning: boolean;
}

export const SumoSettings: React.FC<SumoSettingsProps> = ({
  selectedScenario,
  setSelectedScenario,
  useGUI,
  setUseGUI,
  port,
  setPort,
  isSimulationRunning,
}) => {
  const { t } = useTranslation("sumo");

  return (
    <>
      {/* Scenario Selection */}
      <div className="mb-4">
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          {t("settings.scenario")}
        </label>
        <select
          value={selectedScenario}
          onChange={(e) => setSelectedScenario(e.target.value)}
          disabled={isSimulationRunning}
          className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg 
                     bg-white dark:bg-gray-700 text-gray-900 dark:text-white
                     focus:ring-2 focus:ring-emerald-500 focus:border-transparent
                     disabled:opacity-50 disabled:cursor-not-allowed transition-all"
        >
          <option value="Nga4ThuDuc">
            {t("settings.scenarios.nga4ThuDuc")}
          </option>
          <option value="NguyenThaiSon">
            {t("settings.scenarios.nguyenThaiSon")}
          </option>
          <option value="QuangTrung">
            {t("settings.scenarios.quangTrung")}
          </option>
        </select>
      </div>

      {/* Advanced Settings */}
      <div className="mb-4 space-y-3">
        <div className="flex items-center justify-between">
          <label className="text-sm font-medium text-gray-700 dark:text-gray-300">
            {t("settings.port")}
          </label>
          <input
            type="number"
            value={port}
            onChange={(e) => setPort(Number(e.target.value))}
            disabled={isSimulationRunning}
            className="w-24 px-3 py-1 border border-gray-300 dark:border-gray-600 rounded
                       bg-white dark:bg-gray-700 text-gray-900 dark:text-white
                       disabled:opacity-50 text-sm"
            min="1024"
            max="65535"
          />
        </div>

        <div className="flex items-center justify-between">
          <label className="text-sm font-medium text-gray-700 dark:text-gray-300 flex items-center gap-2">
            <Eye className="w-4 h-4" />
            {t("settings.useGui")}
          </label>
          <input
            type="checkbox"
            checked={useGUI}
            onChange={(e) => setUseGUI(e.target.checked)}
            disabled={isSimulationRunning}
            className="w-5 h-5 text-emerald-600 rounded focus:ring-2 focus:ring-emerald-500
                       disabled:opacity-50"
          />
        </div>
      </div>
    </>
  );
};
