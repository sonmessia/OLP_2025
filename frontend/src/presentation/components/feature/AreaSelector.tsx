import React from "react";
import type { Area } from "../../../domain/models/simulation.types";

interface AreaSelectorProps {
  areas: Area[];
  selectedArea: string | null;
  onSelectArea: (areaId: string) => void;
}

export const AreaSelector: React.FC<AreaSelectorProps> = ({
  areas,
  selectedArea,
  onSelectArea,
}) => {
  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-4">
      <h2 className="text-lg font-semibold mb-4 text-gray-800 dark:text-gray-100">
        🗺️ Chọn Khu Vực
      </h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
        {areas.map((area) => (
          <button
            key={area.id}
            onClick={() => onSelectArea(area.id)}
            className={`
              px-4 py-3 rounded-lg font-medium transition-all duration-200
              ${
                selectedArea === area.id
                  ? "bg-blue-600 text-white shadow-lg scale-105"
                  : "bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600"
              }
            `}
          >
            <div className="text-sm font-semibold">{area.name}</div>
            <div className="text-xs opacity-75 mt-1">
              {area.center[0].toFixed(4)}, {area.center[1].toFixed(4)}
            </div>
          </button>
        ))}
      </div>
    </div>
  );
};
