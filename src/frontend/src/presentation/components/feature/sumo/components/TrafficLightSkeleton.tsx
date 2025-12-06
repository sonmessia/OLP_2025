// Copyright (c) 2025 Green Wave Team
// 
// This software is released under the MIT License.
// https://opensource.org/licenses/MIT

import React from "react";

export const TrafficLightSkeleton: React.FC = () => (
  <div
    className="relative p-4 rounded-lg border-l-4 border-gray-300 dark:border-gray-600 
               bg-gray-50 dark:bg-gray-800/50 animate-pulse"
  >
    {/* Header Skeleton */}
    <div className="flex items-center justify-between mb-3">
      <div className="h-4 w-24 bg-gray-300 dark:bg-gray-600 rounded" />
      <div className="h-6 w-16 bg-gray-300 dark:bg-gray-600 rounded-full" />
    </div>

    {/* Signal Lights Skeleton */}
    <div className="flex gap-1 mb-3">
      {[...Array(8)].map((_, i) => (
        <div
          key={i}
          className="w-5 h-5 rounded-full bg-gray-300 dark:bg-gray-600"
        />
      ))}
    </div>

    {/* Info Skeleton */}
    <div className="flex gap-2">
      <div className="h-5 w-16 bg-gray-300 dark:bg-gray-600 rounded" />
      <div className="h-5 w-16 bg-gray-300 dark:bg-gray-600 rounded" />
    </div>
  </div>
);
