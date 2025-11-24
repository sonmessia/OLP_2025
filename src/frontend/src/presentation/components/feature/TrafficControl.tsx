import React from "react";

interface TrafficControlProps {
  onSetPhase: (phase: number) => void;
  currentPhase: number;
  disabled?: boolean;
}

export const TrafficControl: React.FC<TrafficControlProps> = ({
  onSetPhase,
  currentPhase,
  disabled = false,
}) => {
  const phases = [
    {
      id: 0,
      name: "Đông-Tây",
      icon: "↔️",
      color: "bg-green-500 hover:bg-green-600",
    },
    {
      id: 1,
      name: "Bắc-Nam",
      icon: "↕️",
      color: "bg-blue-500 hover:bg-blue-600",
    },
    {
      id: 2,
      name: "Chuyển tiếp",
      icon: "⚠️",
      color: "bg-yellow-500 hover:bg-yellow-600",
    },
  ];

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
      <h2 className="text-lg font-semibold mb-4 text-gray-800 dark:text-gray-100">
        🎮 Điều Khiển Đèn Giao Thông
      </h2>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
        {phases.map((phase) => (
          <button
            key={phase.id}
            onClick={() => onSetPhase(phase.id)}
            disabled={disabled}
            className={`
              ${phase.color}
              text-white font-semibold py-4 px-6 rounded-lg
              transition-all duration-200 transform
              ${
                currentPhase === phase.id
                  ? "ring-4 ring-offset-2 ring-blue-400 scale-105"
                  : ""
              }
              ${
                disabled
                  ? "opacity-50 cursor-not-allowed"
                  : "hover:scale-105 active:scale-95"
              }
              disabled:hover:scale-100
            `}
          >
            <div className="text-3xl mb-2">{phase.icon}</div>
            <div className="text-sm">Pha {phase.id}</div>
            <div className="text-xs opacity-90">{phase.name}</div>
          </button>
        ))}
      </div>

      <div className="mt-4 p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
        <p className="text-sm text-blue-800 dark:text-blue-200">
          <strong>💡 Gợi ý:</strong> Pha hiện tại là{" "}
          <strong>Pha {currentPhase}</strong>. Bấm vào nút để thay đổi pha đèn
          giao thông.
        </p>
      </div>
    </div>
  );
};
