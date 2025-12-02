import React, { useEffect, useRef } from "react";

interface LogEntry {
  timestamp: Date;
  message: string;
}

interface SystemLogsProps {
  logs: string[];
  maxLogs?: number;
}

export const SystemLogs: React.FC<SystemLogsProps> = ({
  logs,
  maxLogs = 20,
}) => {
  const logContainerRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when new logs are added
  useEffect(() => {
    if (logContainerRef.current) {
      logContainerRef.current.scrollTop = logContainerRef.current.scrollHeight;
    }
  }, [logs]);

  const formatTime = (timestamp: Date) => {
    return timestamp.toLocaleTimeString("vi-VN", {
      hour: "2-digit",
      minute: "2-digit",
      second: "2-digit",
    });
  };

  const getLogColor = (message: string) => {
    if (message.includes("✅") || message.includes("success")) {
      return "text-green-400";
    }
    if (
      message.includes("❌") ||
      message.includes("error") ||
      message.includes("Failed")
    ) {
      return "text-red-400";
    }
    if (message.includes("⚠️") || message.includes("warning")) {
      return "text-yellow-400";
    }
    if (message.includes("🧠") || message.includes("AI")) {
      return "text-purple-400";
    }
    if (message.includes("🚦") || message.includes("traffic")) {
      return "text-blue-400";
    }
    return "text-green-400";
  };

  // Keep only the last maxLogs entries
  const displayLogs = logs.slice(-maxLogs);

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
      <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-4">
        System Logs
      </h2>

      <div
        ref={logContainerRef}
        className="bg-gray-900 rounded-lg p-4 h-64 overflow-y-auto font-mono text-sm custom-scrollbar"
      >
        {displayLogs.length === 0 ? (
          <div className="text-gray-500 text-center py-8">
            No logs yet. System is ready.
          </div>
        ) : (
          <div className="space-y-1">
            {displayLogs.map((log, index) => {
              const timestamp = new Date();
              return (
                <div key={index} className="flex gap-2">
                  <span className="text-gray-500 flex-shrink-0">
                    [{formatTime(timestamp)}]
                  </span>
                  <span className={getLogColor(log)}>{log}</span>
                </div>
              );
            })}
          </div>
        )}
      </div>

      {/* Log Count */}
      <div className="mt-2 text-xs text-gray-500 dark:text-gray-400 text-right">
        {displayLogs.length} / {maxLogs} logs
      </div>

      <style jsx>{`
        .custom-scrollbar::-webkit-scrollbar {
          width: 6px;
        }
        .custom-scrollbar::-webkit-scrollbar-track {
          background: rgba(255, 255, 255, 0.1);
          border-radius: 10px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb {
          background: rgba(255, 255, 255, 0.3);
          border-radius: 10px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb:hover {
          background: rgba(255, 255, 255, 0.5);
        }
      `}</style>
    </div>
  );
};
