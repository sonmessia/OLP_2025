import React, { useState } from "react";
import {
  Moon,
  Sun,
  User,
  Monitor,
  Cpu,
  Route,
  Bell,
  Globe,
  Settings,
  LogOut,
} from "lucide-react";
import { useNavigate, useLocation } from "react-router-dom";
import { useTranslation } from "react-i18next";

import { useAppDispatch, useAppSelector } from "../../../../data/redux/hooks";
import { UserRole } from "../../../../domain/models/AuthModels";
import { logout } from "../../../../data/redux/authSlice";
import { NotificationPopover } from "./NotificationPopover";
import type { AlertLog } from "../../../../domain/models/DashboardModel";

interface DashboardHeaderProps {
  onThemeToggle?: () => void;
  isDarkMode?: boolean;
}

interface NavItem {
  label: string;
  path: string;
  icon: React.ElementType;
}

export const DashboardHeader: React.FC<DashboardHeaderProps> = ({
  onThemeToggle,
  isDarkMode = false,
}) => {
  const { t, i18n } = useTranslation([
    "navigation",
    "dashboard",
    "user",
    "common",
    "alerts",
  ]);
  const [isProfileOpen, setIsProfileOpen] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();
  const dispatch = useAppDispatch();
  const { user } = useAppSelector((state) => state.auth);

  const handleLogout = async () => {
    await dispatch(logout());
    navigate("/login");
  };

  const changeLanguage = (lng: string) => {
    i18n.changeLanguage(lng);
  };

  // Mock notifications state (In a real app, this would come from a store or context)
  const [notifications, setNotifications] = useState<AlertLog[]>([
    {
      id: "1",
      timestamp: new Date().toISOString(),
      type: "warning",
      message: t("alerts:pm25Warning", { location: "Quận 1", value: 160 }),
      resolved: false,
    },
    {
      id: "2",
      timestamp: new Date(Date.now() - 3600000).toISOString(),
      type: "info",
      message: t("alerts:systemAdjusted", { location: "Ngã tư Hàng Xanh" }),
      resolved: true,
    },
  ]);

  const handleMarkAsRead = (id: string) => {
    setNotifications((prev) =>
      prev.map((n) => (n.id === id ? { ...n, resolved: true } : n))
    );
  };

  const handleClearAll = () => {
    setNotifications([]);
  };

  const navItems: NavItem[] = [
    {
      label: t("navigation:dashboard"),
      path: "/admin",
      icon: Monitor,
    },
    {
      label:
        user?.role === UserRole.AREA_MANAGER
          ? t("navigation:areaControl")
          : t("navigation:trafficControl"),
      path: user?.role === UserRole.AREA_MANAGER ? "/area-manager" : "/control",
      icon: Route,
    },
    {
      label: t("navigation:deviceManagement"),
      path: "/devices",
      icon: Cpu,
    },
    {
      label: t("navigation:alerts"),
      path: "/subscriptions",
      icon: Bell,
    },
  ];

  return (
    <header className="bg-white dark:bg-gray-800 border-b-2 border-gray-200 dark:border-gray-700 px-6 py-2">
      <div className="flex items-center justify-between">
        {/* Logo and Title */}
        <div
          className="flex items-center gap-3 cursor-pointer"
          onClick={() => navigate("/")}
        >
          <img
            src="/logo.png"
            alt="GreenWave Logo"
            className="w-12 h-12 object-contain"
          />
          <div>
            <h1 className="text:xl md:text-2xl font-bold text-gray-900 dark:text-white">
              {t("dashboard:title")}
            </h1>
            <p className="text-xs md:text-sm text-gray-600 dark:text-gray-400">
              {t("dashboard:subtitle")}
            </p>
          </div>
        </div>

        {/* Navigation Menu */}
        <nav className="hidden lg:flex items-center gap-2">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = location.pathname === item.path;

            return (
              <button
                key={item.path}
                onClick={() => navigate(item.path)}
                className={`flex items-center gap-2 px-4 py-2 rounded-lg transition-colors ${
                  isActive
                    ? "bg-emerald-100 dark:bg-emerald-900/30 text-emerald-700 dark:text-emerald-300"
                    : "text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700"
                }`}
              >
                <Icon className="w-4 h-4" />
                <span className="text-sm font-medium">{item.label}</span>
              </button>
            );
          })}
        </nav>

        {/* Right Section */}
        <div className="flex items-center gap-4">
          {/* Notifications */}
          <NotificationPopover
            notifications={notifications}
            onMarkAsRead={handleMarkAsRead}
            onClearAll={handleClearAll}
          />

          {/* User Profile */}
          <div className="relative">
            <button
              onClick={() => setIsProfileOpen(!isProfileOpen)}
              className="flex items-center gap-3 p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
            >
              <div className="w-10 h-10 bg-emerald-600 dark:bg-emerald-500 rounded-full flex items-center justify-center">
                <span className="text-white font-bold text-lg">
                  {user?.name?.charAt(0).toUpperCase() || (
                    <User className="w-6 h-6" />
                  )}
                </span>
              </div>
              <div className="text-left hidden md:block">
                <p className="text-sm font-medium text-gray-900 dark:text-white">
                  {user?.name || t("user:guest")}
                </p>
                <p className="text-xs text-gray-500 dark:text-gray-400">
                  {user?.role === UserRole.ADMIN
                    ? t("user:admin")
                    : user?.role === UserRole.AREA_MANAGER
                    ? `${t("user:areaManager")}: ${user.areaName}`
                    : t("user:operator")}
                </p>
              </div>
            </button>

            {/* Dropdown Menu */}
            {isProfileOpen && (
              <div className="absolute right-0 mt-2 w-64 bg-white dark:bg-gray-800 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700 py-2 z-50">
                {/* Profile Links */}
                <button className="w-full px-4 py-2 text-left text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 flex items-center gap-2">
                  <User className="w-4 h-4" />
                  {t("navigation:profile")}
                </button>
                <button className="w-full px-4 py-2 text-left text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 flex items-center gap-2">
                  <Settings className="w-4 h-4" />
                  {t("navigation:settings")}
                </button>

                <hr className="my-2 border-gray-200 dark:border-gray-700" />

                {/* Appearance & Language */}
                <div className="px-4 py-2">
                  <p className="text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider mb-2">
                    {t("common:preferences", "Preferences")}
                  </p>

                  {/* Theme Toggle */}
                  <button
                    onClick={onThemeToggle}
                    className="w-full flex items-center justify-between py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-md px-2 -mx-2 mb-1"
                  >
                    <div className="flex items-center gap-2">
                      {isDarkMode ? (
                        <Moon className="w-4 h-4" />
                      ) : (
                        <Sun className="w-4 h-4" />
                      )}
                      <span>{t("dashboard:theme", "Theme")}</span>
                    </div>
                    <span className="text-xs text-gray-500">
                      {isDarkMode
                        ? t("common:dark", "Dark")
                        : t("common:light", "Light")}
                    </span>
                  </button>

                  {/* Language Selection */}
                  <div className="flex items-center justify-between py-2 text-sm text-gray-700 dark:text-gray-300">
                    <div className="flex items-center gap-2">
                      <Globe className="w-4 h-4" />
                      <span>{t("common:language", "Language")}</span>
                    </div>
                    <div className="flex gap-1">
                      <button
                        onClick={() => changeLanguage("vi")}
                        className={`px-2 py-1 text-xs rounded transition-colors ${
                          i18n.language === "vi"
                            ? "bg-emerald-100 text-emerald-700 dark:bg-emerald-900/50 dark:text-emerald-400 font-bold"
                            : "hover:bg-gray-100 dark:hover:bg-gray-700"
                        }`}
                      >
                        VI
                      </button>
                      <button
                        onClick={() => changeLanguage("en")}
                        className={`px-2 py-1 text-xs rounded transition-colors ${
                          i18n.language === "en"
                            ? "bg-emerald-100 text-emerald-700 dark:bg-emerald-900/50 dark:text-emerald-400 font-bold"
                            : "hover:bg-gray-100 dark:hover:bg-gray-700"
                        }`}
                      >
                        EN
                      </button>
                    </div>
                  </div>
                </div>

                <hr className="my-2 border-gray-200 dark:border-gray-700" />

                <button
                  onClick={handleLogout}
                  className="w-full px-4 py-2 text-left text-sm text-red-600 dark:text-red-400 hover:bg-gray-100 dark:hover:bg-gray-700 flex items-center gap-2"
                >
                  <LogOut className="w-4 h-4" />
                  {t("common:logout")}
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </header>
  );
};
