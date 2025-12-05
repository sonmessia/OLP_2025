import React from "react";
import { useTranslation } from "react-i18next";
import {
  Brain,
  X,
  Target,
  Activity,
  Zap,
  Award,
  TrendingUp,
  Clock,
  BarChart3,
} from "lucide-react";

import type { AIControlState } from "../../../../../domain/models/SumoModels";

interface AIModelDetailsDialogProps {
  isOpen: boolean;
  onClose: () => void;
  aiControlState: AIControlState;
}

export const AIModelDetailsDialog: React.FC<AIModelDetailsDialogProps> = ({
  isOpen,
  onClose,
  aiControlState,
}) => {
  const { t } = useTranslation(["sumo", "common"]);

  if (!isOpen || !aiControlState) return null;

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

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm">
      <div className="glass-card rounded-xl w-3/4 max-h-[85vh] shadow-2xl animate-in fade-in slide-in-from-bottom-4 duration-300 flex flex-col">
        {/* Header - Fixed */}
        <div className="flex items-center justify-between p-6 border-b border-gray-200 dark:border-gray-700">
          <div className="flex items-center gap-3">
            <Brain className="w-7 h-7 text-emerald-600 dark:text-emerald-400" />
            <h3 className="text-2xl font-bold text-gray-900 dark:text-white">
              {t("ai.title")}
            </h3>
          </div>
          <button
            onClick={onClose}
            className="p-2 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg transition-colors"
          >
            <X className="w-6 h-6 text-gray-500 dark:text-gray-400" />
          </button>
        </div>

        {/* Content - Scrollable */}
        <div className="flex-1 overflow-y-auto p-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Left Column */}
            <div className="space-y-6">
              {/* Algorithm */}
              <div className="bg-emerald-50 dark:bg-emerald-900/20 rounded-lg p-5">
                <div className="flex items-center gap-2 mb-3">
                  <Target className="w-5 h-5 text-emerald-600 dark:text-emerald-400" />
                  <p className="text-sm text-emerald-600 dark:text-emerald-400 font-semibold">
                    {t("ai.algorithm")}
                  </p>
                </div>
                <p className="text-lg font-bold text-emerald-900 dark:text-emerald-100">
                  {aiControlState.algorithm}
                </p>
              </div>

              {/* Features */}
              <div className="bg-purple-50 dark:bg-purple-900/20 rounded-lg p-5">
                <div className="flex items-center gap-2 mb-3">
                  <Activity className="w-5 h-5 text-purple-600 dark:text-purple-400" />
                  <p className="text-sm text-purple-600 dark:text-purple-400 font-semibold">
                    {t("ai.features")}
                  </p>
                </div>
                <div className="flex flex-wrap gap-2">
                  {aiControlState.features.map(
                    (feature: string, index: number) => (
                      <span
                        key={index}
                        className="px-3 py-1.5 bg-purple-200 dark:bg-purple-700 text-purple-900 
                               dark:text-purple-100 text-sm rounded-full font-medium"
                      >
                        {feature}
                      </span>
                    )
                  )}
                </div>
              </div>

              {/* Actions Counter */}
              <div className="bg-blue-50 dark:bg-blue-900/20 rounded-lg p-5">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-blue-600 dark:text-blue-400 mb-2">
                      {t("ai.totalActions")}
                    </p>
                    <p className="text-3xl font-bold text-blue-900 dark:text-blue-100">
                      {aiControlState.actionCount}
                    </p>
                  </div>
                  <Zap className="w-10 h-10 text-blue-600 dark:text-blue-400" />
                </div>
                <p className="text-xs text-blue-700 dark:text-blue-300 mt-3">
                  {t("ai.actionDesc")}
                </p>
              </div>

              {/* Stats Grid */}
              <div className="grid grid-cols-2 gap-4">
                <div className="bg-gray-50 dark:bg-gray-800/50 rounded-lg p-4 text-center">
                  <p className="text-xs text-gray-600 dark:text-gray-400 mb-2">
                    {t("ai.controlled")}
                  </p>
                  <p className="text-2xl font-bold text-gray-900 dark:text-white">
                    {aiControlState.numTrafficLights}
                  </p>
                  <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                    {t("ai.lights")}
                  </p>
                </div>
                <div className="bg-gray-50 dark:bg-gray-800/50 rounded-lg p-4 text-center">
                  <p className="text-xs text-gray-600 dark:text-gray-400 mb-2">
                    {t("ai.status")}
                  </p>
                  <p className={`text-2xl font-bold ${getStatusColor()}`}>
                    {aiControlState.status}
                  </p>
                </div>
              </div>
            </div>

            {/* Right Column */}
            <div className="space-y-6">
              {/* Model Performance */}
              <div className="bg-gradient-to-br from-yellow-50 to-orange-50 dark:from-yellow-900/20 dark:to-orange-900/20 rounded-lg p-5 border border-yellow-200 dark:border-yellow-800">
                <div className="flex items-center gap-2 mb-4">
                  <Award className="w-5 h-5 text-yellow-600 dark:text-yellow-400" />
                  <h4 className="text-lg font-bold text-gray-900 dark:text-white">
                    {t("ai.modelPerformance")}
                  </h4>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div className="bg-white/50 dark:bg-gray-800/50 rounded-lg p-4">
                    <p className="text-xs text-gray-600 dark:text-gray-400 mb-1">
                      {t("ai.dqnScore")}
                    </p>
                    <p className="text-2xl font-bold text-yellow-900 dark:text-yellow-100">
                      1383
                    </p>
                    <p className="text-xs text-gray-500 dark:text-gray-400">
                      {t("ai.points")}
                    </p>
                  </div>
                  <div className="bg-white/50 dark:bg-gray-800/50 rounded-lg p-4">
                    <p className="text-xs text-gray-600 dark:text-gray-400 mb-1">
                      {t("ai.vsBaseline")}
                    </p>
                    <div className="flex items-center gap-1">
                      <TrendingUp className="w-4 h-4 text-emerald-600" />
                      <p className="text-2xl font-bold text-emerald-600">
                        +13%
                      </p>
                    </div>
                  </div>
                  <div className="bg-white/50 dark:bg-gray-800/50 rounded-lg p-4">
                    <p className="text-xs text-gray-600 dark:text-gray-400 mb-1">
                      {t("ai.modelSize")}
                    </p>
                    <p className="text-xl font-bold text-gray-900 dark:text-white">
                      334 KB
                    </p>
                  </div>
                  <div className="bg-white/50 dark:bg-gray-800/50 rounded-lg p-4">
                    <p className="text-xs text-gray-600 dark:text-gray-400 mb-1">
                      {t("ai.inferenceTime")}
                    </p>
                    <div className="flex items-center gap-1">
                      <Clock className="w-4 h-4 text-blue-600" />
                      <p className="text-xl font-bold text-blue-900 dark:text-blue-100">
                        12 ms
                      </p>
                    </div>
                  </div>
                </div>
              </div>

              {/* Performance Comparison Chart */}
              <div className="bg-gray-50 dark:bg-gray-800/50 rounded-lg p-5">
                <div className="flex items-center gap-2 mb-4">
                  <BarChart3 className="w-5 h-5 text-gray-700 dark:text-gray-300" />
                  <h4 className="text-sm font-bold text-gray-900 dark:text-white">
                    {t("ai.performanceComparison")}
                  </h4>
                </div>

                <div className="space-y-3">
                  {/* DQN */}
                  <div>
                    <div className="flex items-center justify-between mb-1">
                      <span className="text-xs font-semibold text-emerald-700 dark:text-emerald-300">
                        {t("algorithms.dqn")}
                      </span>
                      <span className="text-xs font-bold text-emerald-900 dark:text-emerald-100">
                        1383
                      </span>
                    </div>
                    <div className="w-full h-6 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
                      <div
                        className="h-full bg-gradient-to-r from-emerald-500 to-emerald-600 flex items-center justify-end pr-2"
                        style={{ width: "100%" }}
                      >
                        <span className="text-xs font-bold text-white">
                          100%
                        </span>
                      </div>
                    </div>
                  </div>

                  {/* Baseline */}
                  <div>
                    <div className="flex items-center justify-between mb-1">
                      <span className="text-xs font-semibold text-gray-700 dark:text-gray-300">
                        {t("algorithms.baseline")}
                      </span>
                      <span className="text-xs font-bold text-gray-900 dark:text-white">
                        1227
                      </span>
                    </div>
                    <div className="w-full h-6 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
                      <div
                        className="h-full bg-gradient-to-r from-blue-500 to-blue-600 flex items-center justify-end pr-2"
                        style={{ width: "88.7%" }}
                      >
                        <span className="text-xs font-bold text-white">
                          88.7%
                        </span>
                      </div>
                    </div>
                  </div>

                  {/* Random */}
                  <div>
                    <div className="flex items-center justify-between mb-1">
                      <span className="text-xs font-semibold text-gray-600 dark:text-gray-400">
                        {t("algorithms.random")}
                      </span>
                      <span className="text-xs font-bold text-gray-700 dark:text-gray-300">
                        835
                      </span>
                    </div>
                    <div className="w-full h-6 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
                      <div
                        className="h-full bg-gradient-to-r from-gray-500 to-gray-600 flex items-center justify-end pr-2"
                        style={{ width: "60.4%" }}
                      >
                        <span className="text-xs font-bold text-white">
                          60.4%
                        </span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Algorithm Comparison Table */}
              <div className="bg-gray-50 dark:bg-gray-800/50 rounded-lg p-5">
                <div className="flex items-center gap-2 mb-4">
                  <BarChart3 className="w-5 h-5 text-gray-700 dark:text-gray-300" />
                  <h4 className="text-lg font-bold text-gray-900 dark:text-white">
                    {t("ai.algorithmComparison")}
                  </h4>
                </div>

                <div className="overflow-x-auto">
                  <table className="w-full text-sm">
                    <thead>
                      <tr className="border-b-2 border-gray-300 dark:border-gray-600">
                        <th className="text-left py-3 px-2 font-semibold text-gray-700 dark:text-gray-300">
                          {t("ai.algorithm")}
                        </th>
                        <th className="text-right py-3 px-2 font-semibold text-gray-700 dark:text-gray-300">
                          {t("ai.avgReward")}
                        </th>
                        <th className="text-right py-3 px-2 font-semibold text-gray-700 dark:text-gray-300">
                          {t("ai.speed")}
                        </th>
                        <th className="text-right py-3 px-2 font-semibold text-gray-700 dark:text-gray-300">
                          {t("ai.waitTime")}
                        </th>
                        <th className="text-right py-3 px-2 font-semibold text-gray-700 dark:text-gray-300">
                          {t("ai.throughput")}
                        </th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr className="border-b border-gray-200 dark:border-gray-700 bg-emerald-50 dark:bg-emerald-900/20">
                        <td className="py-3 px-2 font-bold text-emerald-900 dark:text-emerald-100">
                          {t("algorithms.dqn")}
                        </td>
                        <td className="text-right py-3 px-2 font-bold text-emerald-700 dark:text-emerald-300">
                          1383.03
                        </td>
                        <td className="text-right py-3 px-2 text-gray-900 dark:text-white">
                          48.5 km/h
                        </td>
                        <td className="text-right py-3 px-2 text-gray-900 dark:text-white">
                          32.1s
                        </td>
                        <td className="text-right py-3 px-2 text-gray-900 dark:text-white">
                          892
                        </td>
                      </tr>
                      <tr className="border-b border-gray-200 dark:border-gray-700">
                        <td className="py-3 px-2 font-semibold text-gray-700 dark:text-gray-300">
                          {t("algorithms.baselineFixed")}
                        </td>
                        <td className="text-right py-3 px-2 text-gray-700 dark:text-gray-300">
                          1227.20
                        </td>
                        <td className="text-right py-3 px-2 text-gray-700 dark:text-gray-300">
                          42.3 km/h
                        </td>
                        <td className="text-right py-3 px-2 text-gray-700 dark:text-gray-300">
                          45.7s
                        </td>
                        <td className="text-right py-3 px-2 text-gray-700 dark:text-gray-300">
                          756
                        </td>
                      </tr>
                      <tr className="border-b border-gray-200 dark:border-gray-700">
                        <td className="py-3 px-2 font-semibold text-gray-600 dark:text-gray-400">
                          {t("algorithms.random")}
                        </td>
                        <td className="text-right py-3 px-2 text-gray-600 dark:text-gray-400">
                          834.50
                        </td>
                        <td className="text-right py-3 px-2 text-gray-600 dark:text-gray-400">
                          35.8 km/h
                        </td>
                        <td className="text-right py-3 px-2 text-gray-600 dark:text-gray-400">
                          68.2s
                        </td>
                        <td className="text-right py-3 px-2 text-gray-600 dark:text-gray-400">
                          612
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Footer - Fixed */}
        <div className="p-6 border-t border-gray-200 dark:border-gray-700">
          <button
            onClick={onClose}
            className="w-full px-4 py-3 bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600
                       text-gray-900 dark:text-white font-semibold rounded-lg transition-colors"
          >
            {t("common:close")}
          </button>
        </div>
      </div>
    </div>
  );
};
