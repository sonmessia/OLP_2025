import React from "react";
import { AlertCircle, X } from "lucide-react";
import type { NotificationModel } from "../../../domain/models/NotificationModel";

interface NotificationPanelProps {
  notifications: NotificationModel[];
  onDismiss: (id: string) => void;
}

export const NotificationPanel: React.FC<NotificationPanelProps> = ({
  notifications,
  onDismiss,
}) => {
  if (notifications.length === 0) return null;

  const iconConfig = {
    error: {
      icon: AlertCircle,
      color: "bg-red-100 border-red-400 text-red-700",
    },
    warning: {
      icon: AlertCircle,
      color: "bg-yellow-100 border-yellow-400 text-yellow-700",
    },
    info: {
      icon: AlertCircle,
      color: "bg-blue-100 border-blue-400 text-blue-700",
    },
    success: {
      icon: AlertCircle,
      color: "bg-green-100 border-green-400 text-green-700",
    },
  };

  return (
    <div className="fixed top-4 left-4 z-50 space-y-2 max-w-md">
      {notifications.map((notif) => {
        const { icon: Icon, color } = iconConfig[notif.type];
        return (
          <div
            key={notif.id}
            className={`${color} border-l-4 p-4 rounded shadow-lg flex items-start gap-3`}
          >
            <Icon className="w-5 h-5 flex-shrink-0 mt-0.5" />
            <div className="flex-1">
              <p className="font-semibold text-sm">{notif.message}</p>
              <p className="text-xs mt-1 opacity-75">
                {notif.timestamp.toLocaleTimeString("vi-VN")}
              </p>
            </div>
            <button
              onClick={() => onDismiss(notif.id)}
              className="flex-shrink-0"
            >
              <X className="w-4 h-4" />
            </button>
          </div>
        );
      })}
    </div>
  );
};
