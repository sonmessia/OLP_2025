// Copyright (c) 2025 Green Wave Team
// 
// This software is released under the MIT License.
// https://opensource.org/licenses/MIT

import React from "react";
import { useTranslation } from "react-i18next";
import { Globe } from "lucide-react";

export const LanguageSwitcher: React.FC = () => {
  const { i18n } = useTranslation();

  const languages = [
    { code: "en", name: "English", flag: "🇺🇸" },
    { code: "vi", name: "Tiếng Việt", flag: "🇻🇳" },
  ];

  const currentLanguage = languages.find(lang => lang.code === i18n.language) || languages[0];

  const handleLanguageChange = (languageCode: string) => {
    i18n.changeLanguage(languageCode);
  };

  return (
    <div className="relative group">
      <button className="flex items-center gap-2 p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors">
        <Globe className="w-5 h-5 text-gray-600 dark:text-gray-400" />
        <span className="hidden md:block text-sm font-medium text-gray-700 dark:text-gray-300">
          {currentLanguage.flag} {currentLanguage.name}
        </span>
        <span className="md:hidden text-sm font-medium text-gray-700 dark:text-gray-300">
          {currentLanguage.flag}
        </span>
      </button>

      {/* Dropdown Menu */}
      <div className="absolute right-0 mt-2 w-48 bg-white dark:bg-gray-800 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700 py-2 z-50 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200">
        {languages.map((language) => (
          <button
            key={language.code}
            onClick={() => handleLanguageChange(language.code)}
            className={`w-full px-4 py-2 text-left text-sm flex items-center gap-3 transition-colors ${
              i18n.language === language.code
                ? "bg-emerald-50 dark:bg-emerald-900/20 text-emerald-600 dark:text-emerald-400 font-medium"
                : "text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700"
            }`}
          >
            <span className="text-lg">{language.flag}</span>
            <span>{language.name}</span>
            {i18n.language === language.code && (
              <span className="ml-auto">✓</span>
            )}
          </button>
        ))}
      </div>
    </div>
  );
};