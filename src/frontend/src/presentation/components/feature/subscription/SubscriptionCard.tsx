import React from "react";
import { Trash2, Activity, Wind, Car } from "lucide-react";
import type { Subscription } from "../../../../domain/models/SubscriptionModels";

interface SubscriptionCardProps {
  subscription: Subscription;
  onDelete: (id: string) => void;
}

export const SubscriptionCard: React.FC<SubscriptionCardProps> = ({
  subscription,
  onDelete,
}) => {
  return (
    <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6 hover:shadow-md transition-shadow">
      <div className="flex justify-between items-start mb-4">
        <div className="p-2 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
          {subscription.entities[0]?.type === "TrafficFlowObserved" ? (
            <Car className="w-6 h-6 text-blue-600 dark:text-blue-400" />
          ) : (
            <Wind className="w-6 h-6 text-green-600 dark:text-green-400" />
          )}
        </div>
        <button
          onClick={() => onDelete(subscription.id)}
          className="text-gray-400 hover:text-red-500 transition-colors p-1"
          title="Xóa cảnh báo"
        >
          <Trash2 className="w-5 h-5" />
        </button>
      </div>

      <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2 line-clamp-1">
        {subscription.description}
      </h3>

      <div className="space-y-2 text-sm text-gray-600 dark:text-gray-400">
        <div className="flex items-center gap-2">
          <Activity className="w-4 h-4" />
          <span className="font-medium">Loại:</span>
          <span className="bg-gray-100 dark:bg-gray-700 px-2 py-0.5 rounded text-xs">
            {subscription.entities[0]?.type || "N/A"}
          </span>
        </div>

        {subscription.watchedAttributes &&
          subscription.watchedAttributes.length > 0 && (
            <div className="flex flex-wrap gap-1 mt-2">
              {subscription.watchedAttributes.map((attr) => (
                <span
                  key={attr}
                  className="bg-emerald-50 dark:bg-emerald-900/20 text-emerald-700 dark:text-emerald-300 px-2 py-0.5 rounded text-xs border border-emerald-100 dark:border-emerald-800"
                >
                  {attr}
                </span>
              ))}
            </div>
          )}

        {subscription.q && (
          <div className="mt-2">
            <span className="font-medium text-xs text-gray-500">
              Điều kiện:
            </span>
            <code className="block mt-1 bg-gray-100 dark:bg-gray-900 px-2 py-1 rounded text-xs font-mono text-pink-600 dark:text-pink-400 break-all">
              {subscription.q}
            </code>
          </div>
        )}

        <div className="pt-2 mt-2 border-t border-gray-100 dark:border-gray-700">
          <p
            className="text-xs text-gray-500 truncate"
            title={subscription.notificationUri}
          >
            URI: {subscription.notificationUri}
          </p>
          <div className="flex justify-between mt-2 text-xs">
            <span
              className={
                subscription.status === "failed"
                  ? "text-red-500"
                  : "text-green-500"
              }
            >
              {subscription.status || "active"}
            </span>
            <span>Gửi: {subscription.timesSent || 0}</span>
          </div>
        </div>
      </div>
    </div>
  );
};
