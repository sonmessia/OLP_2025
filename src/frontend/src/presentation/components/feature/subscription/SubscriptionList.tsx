import React from "react";
import { Bell } from "lucide-react";
import { SubscriptionCard } from "./SubscriptionCard";
import type { Subscription } from "../../../../domain/models/SubscriptionModels";

interface SubscriptionListProps {
  subscriptions: Subscription[];
  loading: boolean;
  onDelete: (id: string) => void;
}

export const SubscriptionList: React.FC<SubscriptionListProps> = ({
  subscriptions,
  loading,
  onDelete,
}) => {
  if (loading) {
    return (
      <div className="flex justify-center py-12">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-emerald-600"></div>
      </div>
    );
  }

  if (subscriptions.length === 0) {
    return (
      <div className="col-span-full text-center py-12 text-gray-500 dark:text-gray-400 bg-white dark:bg-gray-800 rounded-xl border border-dashed border-gray-300 dark:border-gray-700">
        <Bell className="w-12 h-12 mx-auto mb-3 opacity-20" />
        <p>Chưa có cảnh báo nào được tạo.</p>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {subscriptions.map((sub) => (
        <SubscriptionCard key={sub.id} subscription={sub} onDelete={onDelete} />
      ))}
    </div>
  );
};
