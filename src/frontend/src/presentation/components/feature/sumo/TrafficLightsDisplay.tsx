import React from "react";
import { useAppSelector } from "../../../../data/redux/hooks";
import { TrafficCone, Star, Circle } from "lucide-react";
import { TrafficLightCard } from "./components/TrafficLightCard";
import { TrafficLightSkeleton } from "./components/TrafficLightSkeleton";

export const TrafficLightsDisplay: React.FC = () => {
  const { simulationState } = useAppSelector((state) => state.sumo);

  const totalLights = simulationState?.totalTrafficLights || 0;
  const hasData = simulationState && simulationState.trafficLights.length > 0;

  return (
    <div className="glass-card rounded-xl p-6 shadow-xl">
      <div className="flex items-center gap-3 mb-4">
        <TrafficCone className="w-6 h-6 text-emerald-600 dark:text-emerald-400" />
        <h2 className="text-xl font-bold text-gray-900 dark:text-white">
          Traffic Lights
          {totalLights > 0 && (
            <span className="ml-2 text-sm font-normal text-gray-600 dark:text-gray-400">
              ({totalLights} lights)
            </span>
          )}
        </h2>
      </div>

      <div className="h-[300px] overflow-y-auto pr-2">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          {hasData ? (
            simulationState.trafficLights.map((tls) => (
              <TrafficLightCard key={tls.id} tls={tls} />
            ))
          ) : (
            // Show skeleton loaders
            <>
              {[...Array(4)].map((_, index) => (
                <TrafficLightSkeleton key={`skeleton-${index}`} />
              ))}
            </>
          )}
        </div>

        {/* Waiting message */}
        {!hasData && (
          <div className="text-center py-4">
            <div
              className="inline-flex items-center gap-2 px-4 py-2 bg-blue-50 dark:bg-blue-900/20 
                            rounded-lg border border-blue-200 dark:border-blue-800"
            >
              <Circle className="w-4 h-4 text-blue-600 dark:text-blue-400 animate-pulse" />
              <span className="text-sm text-blue-800 dark:text-blue-200">
                Waiting for traffic light data...
              </span>
            </div>
          </div>
        )}
      </div>

      {/* Legend */}
      {hasData && (
        <div className="mt-4 pt-4 border-t border-gray-200 dark:border-gray-700">
          <div className="flex items-center gap-4 text-xs text-gray-600 dark:text-gray-400">
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full bg-emerald-500 shadow-lg shadow-emerald-500/50" />
              <span>Green</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full bg-yellow-500 shadow-lg shadow-yellow-500/50" />
              <span>Yellow</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full bg-red-500 shadow-lg shadow-red-500/50" />
              <span>Red</span>
            </div>
            <div className="flex items-center gap-2">
              <Star className="w-3 h-3 text-emerald-600 dark:text-emerald-400 fill-current" />
              <span>Main Control</span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
