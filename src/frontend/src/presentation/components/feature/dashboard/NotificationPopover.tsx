// Copyright (c) 2025 Green Wave Team
// 
// This software is released under the MIT License.
// https://opensource.org/licenses/MIT

import React, { useState } from "react";
import { Bell, CheckCircle, AlertTriangle, Info } from "lucide-react";
import type { AlertLog } from "../../../../domain/models/DashboardModel";

interface NotificationPopoverProps {
  notifications: AlertLog[];
  onMarkAsRead: (id: string) => void;
  onClearAll: () => void;
}

export const NotificationPopover: React.FC<NotificationPopoverProps> = ({
  notifications,
  onMarkAsRead,
  onClearAll,
}) => {
  const [isOpen, setIsOpen] = useState(false);


  const getIcon = (type: string) => {
    switch (type) {
      case "critical":
        return <AlertTriangle className="w-4 h-4 text-red-500" />;
      case "warning":
        return <AlertTriangle className="w-4 h-4 text-yellow-500" />;
      default:
        return <Info className="w-4 h-4 text-blue-500" />;
    }
  };

  // Mock data for demo purposes if no notifications provided
  const MOCK_NOTIFICATIONS: AlertLog[] = [
    {
      id: "notif_mock_1",
      timestamp: new Date().toISOString(),
      type: "critical",
      message: "Cảnh báo: Nồng độ PM2.5 vượt ngưỡng tại Ngã 4 Thủ Đức",
      resolved: false,
    },
    {
      id: "notif_mock_2",
      timestamp: new Date(Date.now() - 1800000).toISOString(),
      type: "warning",
      message: "Lưu lượng giao thông tăng cao tại Hàng Xanh",
      resolved: false,
    },
    {
      id: "notif_mock_3",
      timestamp: new Date(Date.now() - 3600000).toISOString(),
      type: "info",
      message: "Hệ thống đã tự động tối ưu hóa đèn tín hiệu",
      resolved: true,
    },
  ];

  const displayNotifications =
    notifications.length > 0 ? notifications : MOCK_NOTIFICATIONS;
  const unreadCount = displayNotifications.filter((n) => !n.resolved).length;

  return (
    <div className="relative">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="relative p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
      >
        <Bell className="w-5 h-5 text-gray-600 dark:text-gray-400" />
        {unreadCount > 0 && (
          <span className="absolute top-1 right-1 w-2.5 h-2.5 bg-red-500 rounded-full border-2 border-white dark:border-gray-800"></span>
        )}
      </button>

      {isOpen && (
        <>
          <div
            className="fixed inset-0 z-40"
            onClick={() => setIsOpen(false)}
          ></div>
          <div className="absolute right-0 mt-2 w-80 bg-white dark:bg-gray-800 rounded-lg shadow-xl border border-gray-200 dark:border-gray-700 z-50 overflow-hidden">
            <div className="px-4 py-3 border-b border-gray-200 dark:border-gray-700 flex justify-between items-center">
       
              {displayNotifications.length > 0 && (
                <button
                  onClick={onClearAll}
                  className="text-xs text-gray-500 hover:text-gray-700 dark:hover:text-gray-300"
                >
                  Xóa tất cả
                </button>
              )}
            </div>

            <div className="max-h-96 overflow-y-auto">
              {displayNotifications.length === 0 ? (
                <div className="p-4 text-center text-gray-500 dark:text-gray-400 text-sm">
                  Không có thông báo mới
                </div>
              ) : (
                <div className="divide-y divide-gray-100 dark:divide-gray-700">
                  {displayNotifications.map((notification) => (
                    <div
                      key={notification.id}
                      className={`p-3 hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors ${
                        !notification.resolved
                          ? "bg-blue-50/50 dark:bg-blue-900/10"
                          : ""
                      }`}
                    >
                      <div className="flex gap-3">
                        <div className="mt-1">{getIcon(notification.type)}</div>
                        <div className="flex-1">
                          <p className="text-sm text-gray-800 dark:text-gray-200 mb-1">
                            {notification.message}
                          </p>
                          <div className="flex justify-between items-center">
                            <span className="text-xs text-gray-500">
                              {new Date(
                                notification.timestamp
                              ).toLocaleTimeString()}
                            </span>
                            {!notification.resolved && (
                              <button
                                onClick={() => onMarkAsRead(notification.id)}
                                className="text-xs text-emerald-600 hover:text-emerald-700 font-medium flex items-center gap-1"
                              >
                                <CheckCircle className="w-3 h-3" /> Đã đọc
                              </button>
                            )}
                          </div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </>
      )}
    </div>
  );
};
