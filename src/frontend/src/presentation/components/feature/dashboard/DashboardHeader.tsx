import React, { useState } from "react";
import { Moon, Sun, User, Leaf } from "lucide-react";

interface DashboardHeaderProps {
  onThemeToggle?: () => void;
  isDarkMode?: boolean;
}

export const DashboardHeader: React.FC<DashboardHeaderProps> = ({
  onThemeToggle,
  isDarkMode = false,
}) => {
  const [isProfileOpen, setIsProfileOpen] = useState(false);

  return (
    <header className="bg-white dark:bg-gray-800 border-b-2 border-gray-200 dark:border-gray-700 px-6 py-2">
      <div className="flex items-center justify-between">
        {/* Logo and Title */}
        <div className="flex items-center gap-3">
          <div className="p-2 bg-emerald-100 dark:bg-emerald-900/30 rounded-lg">
            <Leaf className="w-8 h-8 text-emerald-600 dark:text-emerald-400" />
          </div>
          <div>
            <h1 className="text:xl md:text-2xl font-bold text-gray-900 dark:text-white">
              GreenWave
            </h1>
            <p className="text-xs md:text-sm text-gray-600 dark:text-gray-400">
              Dashboard Quản lý Giao thông
            </p>
          </div>
        </div>

        {/* Right Section */}
        <div className="flex items-center gap-4">
          {/* Theme Toggle */}
          <button
            onClick={onThemeToggle}
            className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
            aria-label="Toggle theme"
          >
            {isDarkMode ? (
              <Sun className="w-5 h-5 text-gray-600 dark:text-gray-400" />
            ) : (
              <Moon className="w-5 h-5 text-gray-600 dark:text-gray-400" />
            )}
          </button>

          {/* User Profile */}
          <div className="relative">
            <button
              onClick={() => setIsProfileOpen(!isProfileOpen)}
              className="flex items-center gap-3 p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
            >
              <div className="w-10 h-10 bg-emerald-600 dark:bg-emerald-500 rounded-full flex items-center justify-center">
                <User className="w-6 h-6 text-white" />
              </div>
              <div className="text-left hidden md:block">
                <p className="text-sm font-medium text-gray-900 dark:text-white">
                  Quản lý viên
                </p>
                <p className="text-xs text-gray-500 dark:text-gray-400">
                  Admin
                </p>
              </div>
            </button>

            {/* Dropdown Menu */}
            {isProfileOpen && (
              <div className="absolute right-0 mt-2 w-48 bg-white dark:bg-gray-800 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700 py-2 z-50">
                <button className="w-full px-4 py-2 text-left text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700">
                  Hồ sơ
                </button>
                <button className="w-full px-4 py-2 text-left text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700">
                  Cài đặt
                </button>
                <hr className="my-2 border-gray-200 dark:border-gray-700" />
                <button className="w-full px-4 py-2 text-left text-sm text-red-600 dark:text-red-400 hover:bg-gray-100 dark:hover:bg-gray-700">
                  Đăng xuất
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </header>
  );
};
