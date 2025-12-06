import React, { useState } from "react";
import {
  Search,
  X,
  Sun,
  Moon,
  Info,
  Shield,
  Globe,
  Settings,
  LogIn,
} from "lucide-react";
import { useNavigate } from "react-router-dom";
import { useSelector } from "react-redux";
import type { RootState } from "../../../../data/redux/store";
import { UserRole } from "../../../../domain/models/AuthModels";
import { useTranslation } from "react-i18next";

interface UserMapHeaderProps {
  onThemeToggle: () => void;
  isDarkMode: boolean;
  onSearch: (query: string) => void;
  searchQuery: string;
}

export const UserMapHeader: React.FC<UserMapHeaderProps> = ({
  onThemeToggle,
  isDarkMode,
  onSearch,
  searchQuery,
}) => {
  const [localSearchQuery, setLocalSearchQuery] = useState(searchQuery);
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const navigate = useNavigate();
  const { user } = useSelector((state: RootState) => state.auth);
  const { t, i18n } = useTranslation(["maps", "aqi", "common"]);

  const changeLanguage = (lng: string) => {
    i18n.changeLanguage(lng);
  };

  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const query = e.target.value;
    setLocalSearchQuery(query);
    onSearch(query);
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") {
      onSearch(localSearchQuery);
    }
  };

  return (
    <header className="h-18 glass-effect shadow-lg px-2 md:px-4 py-3 z-50 relative">
      <div className="flex items-center justify-between h-full">
        {/* Logo and Title */}
        <div className="flex items-center space-x-2 md:space-x-4">
          <div className="flex items-center space-x-2">
            <img
              src="/logo.png"
              alt="GreenWave Logo"
              className="w-12 h-12 object-contain"
            />
            <div>
              <h1 className="text-sm md:text-xl font-bold text-gray-900 dark:text-white">
                GreenWave
              </h1>
            </div>
          </div>
        </div>

        {/* Search Bar */}
        <div className="flex-1 max-w-xl mx-2 md:mx-8">
          <div className="relative">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <Search className="h-5 w-5 text-gray-400" />
            </div>
            <input
              type="text"
              value={localSearchQuery}
              onChange={handleSearchChange}
              onKeyPress={handleKeyPress}
              placeholder={t("header.searchPlaceholder")}
              className="block w-full pl-10 pr-10 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent"
            />
            {localSearchQuery && (
              <button
                onClick={() => {
                  setLocalSearchQuery("");
                  onSearch("");
                }}
                className="absolute inset-y-0 right-0 pr-3 flex items-center"
              >
                <X className="h-5 w-5 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300" />
              </button>
            )}
          </div>
        </div>

        {/* Right Side Controls */}
        <div className="flex items-center space-x-4">
          {/* Legend */}
          <div className="hidden md:flex items-center space-x-3 px-3 py-2 bg-gray-100 dark:bg-gray-700 rounded-lg">
            <span className="text-xs font-medium text-gray-600 dark:text-gray-300">
              {t("header.legendTitle")}
            </span>
            <div className="flex items-center space-x-2">
              <div className="flex items-center">
                <div className="w-3 h-3 bg-green-500 rounded-full mr-1"></div>
                <span className="text-xs text-gray-600 dark:text-gray-300">
                  {t("good", { ns: "aqi" })}
                </span>
              </div>
              <div className="flex items-center">
                <div className="w-3 h-3 bg-yellow-500 rounded-full mr-1"></div>
                <span className="text-xs text-gray-600 dark:text-gray-300">
                  {t("moderate", { ns: "aqi" })}
                </span>
              </div>
              <div className="flex items-center">
                <div className="w-3 h-3 bg-orange-500 rounded-full mr-1"></div>
                <span className="text-xs text-gray-600 dark:text-gray-300">
                  {t("unhealthy", { ns: "aqi" })}
                </span>
              </div>
              <div className="flex items-center">
                <div className="w-3 h-3 bg-red-500 rounded-full mr-1"></div>
                <span className="text-xs text-gray-600 dark:text-gray-300">
                  {t("hazardous", { ns: "aqi" })}
                </span>
              </div>
            </div>
          </div>

          {/* About Us Link */}
          <button
            onClick={() => navigate("/introduce")}
            className="p-2 rounded-lg bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors"
            title={t("header.about")}
          >
            <Info className="w-5 h-5" />
          </button>

          {/* Login Button */}
          {!user && (
            <button
              onClick={() => navigate("/login")}
              className="p-2 rounded-lg bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors"
              title={t("common:login", "Login")}
            >
              <LogIn className="w-5 h-5" />
            </button>
          )}

          {/* Settings Dropdown */}
          <div className="relative">
            <button
              onClick={() => setIsMenuOpen(!isMenuOpen)}
              className="p-2 rounded-lg bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors"
              title={t("common:settings", "Settings")}
            >
              <Settings className="w-5 h-5" />
            </button>

            {isMenuOpen && (
              <div className="absolute right-0 mt-2 w-64 bg-white dark:bg-gray-800 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700 py-2 z-50">
                {/* Admin Link */}
                {user &&
                  (user.role === UserRole.ADMIN ||
                    user.role === UserRole.AREA_MANAGER) && (
                    <button
                      onClick={() => {
                        navigate("/admin");
                        setIsMenuOpen(false);
                      }}
                      className="w-full px-4 py-2 text-left text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 flex items-center gap-2"
                    >
                      <Shield className="w-4 h-4" />
                      {t("header.admin")}
                    </button>
                  )}

                {/* Theme Toggle */}
                <button
                  onClick={onThemeToggle}
                  className="w-full px-4 py-2 text-left text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 flex items-center justify-between"
                >
                  <div className="flex items-center gap-2">
                    {isDarkMode ? (
                      <Moon className="w-4 h-4" />
                    ) : (
                      <Sun className="w-4 h-4" />
                    )}
                    <span>{t("common:appearance", "Appearance")}</span>
                  </div>
                  <span className="text-xs text-gray-500">
                    {isDarkMode
                      ? t("common:dark", "Dark")
                      : t("common:light", "Light")}
                  </span>
                </button>

                <hr className="my-2 border-gray-200 dark:border-gray-700" />

                {/* Language Switcher */}
                <div className="px-4 py-2 flex items-center justify-between text-sm text-gray-700 dark:text-gray-300">
                  <div className="flex items-center gap-2">
                    <Globe className="w-4 h-4" />
                    <span>{t("common:language")}</span>
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
            )}
          </div>
        </div>
      </div>
    </header>
  );
};
