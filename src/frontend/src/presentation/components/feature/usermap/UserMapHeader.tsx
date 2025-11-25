import React, { useState } from "react";
import { Wind, Search, X, Sun, Moon } from "lucide-react";

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
    <header className="h-18 bg-white dark:bg-gray-800 shadow-lg border-b border-gray-200 dark:border-gray-700 px-4 py-3">
      <div className="flex items-center justify-between h-full">
        {/* Logo and Title */}
        <div className="flex items-center space-x-4">
          <div className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-green-600 rounded-lg flex items-center justify-center">
              <Wind className="w-5 h-5 text-white" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-gray-900 dark:text-white">
                GreenWave
              </h1>
              <p className="text-xs text-gray-500 dark:text-gray-400">
                Bản đồ chất lượng không khí
              </p>
            </div>
          </div>
        </div>

        {/* Search Bar */}
        <div className="flex-1 max-w-xl mx-8">
          <div className="relative">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <Search className="h-5 w-5 text-gray-400" />
            </div>
            <input
              type="text"
              value={localSearchQuery}
              onChange={handleSearchChange}
              onKeyPress={handleKeyPress}
              placeholder="Tìm địa điểm (ví dụ: Quận 1, Nhà thờ Đức Bà...)"
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
              AQI:
            </span>
            <div className="flex items-center space-x-2">
              <div className="flex items-center">
                <div className="w-3 h-3 bg-green-500 rounded-full mr-1"></div>
                <span className="text-xs text-gray-600 dark:text-gray-300">
                  Tốt
                </span>
              </div>
              <div className="flex items-center">
                <div className="w-3 h-3 bg-yellow-500 rounded-full mr-1"></div>
                <span className="text-xs text-gray-600 dark:text-gray-300">
                  Trung bình
                </span>
              </div>
              <div className="flex items-center">
                <div className="w-3 h-3 bg-orange-500 rounded-full mr-1"></div>
                <span className="text-xs text-gray-600 dark:text-gray-300">
                  Kém
                </span>
              </div>
              <div className="flex items-center">
                <div className="w-3 h-3 bg-red-500 rounded-full mr-1"></div>
                <span className="text-xs text-gray-600 dark:text-gray-300">
                  Nguy hại
                </span>
              </div>
            </div>
          </div>

          {/* Theme Toggle */}
          <button
            onClick={onThemeToggle}
            className="p-2 rounded-lg bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors"
            title={
              isDarkMode ? "Chuyển sang chế độ sáng" : "Chuyển sang chế độ tối"
            }
          >
            {isDarkMode ? (
              <Sun className="w-5 h-5" />
            ) : (
              <Moon className="w-5 h-5" />
            )}
          </button>
        </div>
      </div>
    </header>
  );
};
