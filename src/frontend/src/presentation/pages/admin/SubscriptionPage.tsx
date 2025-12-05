import React, { useState, useEffect } from "react";
import { DashboardHeader } from "../../components/feature/dashboard/DashboardHeader";
import type {
  Subscription,
  SubscriptionCreate,
} from "../../../domain/models/SubscriptionModels";
import { GetSubscriptionsUseCase } from "../../../domain/usecases/subscription/GetSubscriptionsUseCase";
import { CreateSubscriptionUseCase } from "../../../domain/usecases/subscription/CreateSubscriptionUseCase";
import { DeleteSubscriptionUseCase } from "../../../domain/usecases/subscription/DeleteSubscriptionUseCase";
import { SubscriptionRepositoryImpl } from "../../../data/repositories/SubscriptionRepositoryImpl";
import { subscriptionApiClient } from "../../../api/SubscriptionApiClient";
import { Plus, Bell } from "lucide-react";
import { SubscriptionList } from "../../components/feature/subscription/SubscriptionList";
import { SubscriptionForm } from "../../components/feature/subscription/SubscriptionForm";

// Initialize dependencies
const subscriptionRepository = new SubscriptionRepositoryImpl(
  subscriptionApiClient
);
const getSubscriptionsUseCase = new GetSubscriptionsUseCase(
  subscriptionRepository
);
const createSubscriptionUseCase = new CreateSubscriptionUseCase(
  subscriptionRepository
);
const deleteSubscriptionUseCase = new DeleteSubscriptionUseCase(
  subscriptionRepository
);

export const SubscriptionPage: React.FC = () => {
  // Theme state
  const getInitialDarkMode = () => {
    if (typeof window !== "undefined") {
      const stored = localStorage.getItem("darkMode");
      if (stored !== null) {
        return stored === "true";
      }
      return window.matchMedia("(prefers-color-scheme: dark)").matches;
    }
    return false;
  };

  const [isDarkMode, setIsDarkMode] = useState(getInitialDarkMode);
  const [subscriptions, setSubscriptions] = useState<Subscription[]>([]);
  const [loading, setLoading] = useState(false);
  const [isModalOpen, setIsModalOpen] = useState(false);

  useEffect(() => {
    if (isDarkMode) {
      document.documentElement.classList.add("dark");
    } else {
      document.documentElement.classList.remove("dark");
    }
  }, [isDarkMode]);

  const handleThemeToggle = () => {
    const newDarkMode = !isDarkMode;
    setIsDarkMode(newDarkMode);
    localStorage.setItem("darkMode", newDarkMode.toString());
  };

  const fetchSubscriptions = async () => {
    setLoading(true);
    try {
      const data = await getSubscriptionsUseCase.execute();
      setSubscriptions(data);
    } catch (error) {
      console.error("Failed to fetch subscriptions", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchSubscriptions();
  }, []);

  const handleDelete = async (id: string) => {
    if (window.confirm("Bạn có chắc chắn muốn xóa cảnh báo này không?")) {
      try {
        await deleteSubscriptionUseCase.execute(id);
        fetchSubscriptions();
      } catch (error) {
        console.error("Failed to delete subscription", error);
        alert("Không thể xóa cảnh báo");
      }
    }
  };

  const handleCreate = async (newSubscription: SubscriptionCreate) => {
    try {
      await createSubscriptionUseCase.execute(newSubscription);
      setIsModalOpen(false);
      fetchSubscriptions();
    } catch (error) {
      console.error("Failed to create subscription", error);
      alert("Không thể tạo cảnh báo. Vui lòng kiểm tra lại thông tin.");
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 transition-colors duration-200">
      <DashboardHeader
        onThemeToggle={handleThemeToggle}
        isDarkMode={isDarkMode}
      />

      <main className="container mx-auto px-4 py-8">
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-2xl font-bold text-gray-900 dark:text-white flex items-center gap-2">
              <Bell className="w-8 h-8 text-emerald-600" />
              Quản lý Cảnh báo (Subscriptions)
            </h1>
            <p className="text-gray-600 dark:text-gray-400 mt-1">
              Quản lý các đăng ký nhận thông báo về thay đổi chất lượng không
              khí và lưu lượng giao thông.
            </p>
          </div>
          <button
            onClick={() => setIsModalOpen(true)}
            className="flex items-center gap-2 bg-emerald-600 hover:bg-emerald-700 text-white px-4 py-2 rounded-lg transition-colors shadow-md"
          >
            <Plus className="w-5 h-5" />
            Tạo Cảnh báo Mới
          </button>
        </div>

        <SubscriptionList
          subscriptions={subscriptions}
          loading={loading}
          onDelete={handleDelete}
        />
      </main>

      <SubscriptionForm
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onSubmit={handleCreate}
      />
    </div>
  );
};
