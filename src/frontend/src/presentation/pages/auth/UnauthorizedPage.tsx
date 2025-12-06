// Copyright (c) 2025 Green Wave Team
// 
// This software is released under the MIT License.
// https://opensource.org/licenses/MIT

import React from "react";
import { Link, useNavigate } from "react-router-dom";
import { useSelector } from "react-redux";
import { useTranslation } from "react-i18next";
import type { RootState } from "../../../data/redux/store";

const UnauthorizedPage: React.FC = () => {
  const { t } = useTranslation(["auth", "common"]);
  const { user } = useSelector((state: RootState) => state.auth);
  const navigate = useNavigate();

  const handleGoBack = () => {
    navigate(-1);
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full text-center">
        <div className="flex justify-center mb-6">
          <div className="w-20 h-20 bg-red-100 rounded-full flex items-center justify-center">
            <svg
              className="w-10 h-10 text-red-600"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
              />
            </svg>
          </div>
        </div>

        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          {t("unauthorized.title")}
        </h1>

        <p className="text-gray-600 mb-6">
          {user
            ? t("unauthorized.loggedInDenied", { name: user.name })
            : t("unauthorized.notLoggedIn")}
        </p>

        {user && (
          <div className="mb-6 p-4 bg-gray-100 rounded-lg">
            <p className="text-sm text-gray-700">
              <strong>{t("unauthorized.accountInfo")}</strong>
            </p>
            <p className="text-sm text-gray-600">
              {t("unauthorized.email", { email: user.email })}
            </p>
            <p className="text-sm text-gray-600">
              {t("unauthorized.role", {
                role:
                  user.role === "admin"
                    ? t("common:user.admin" as any)
                    : t("common:user.areaManager" as any),
              })}
              {user.areaName && ` (${user.areaName})`}
            </p>
          </div>
        )}

        <div className="space-y-3">
          {user ? (
            <>
              <Link
                to="/"
                className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
              >
                {t("unauthorized.goHome")}
              </Link>

              {user.role === "admin" && (
                <Link
                  to="/control"
                  className="w-full flex justify-center py-2 px-4 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                >
                  {t("unauthorized.goToControl")}
                </Link>
              )}

              {user.role === "area_manager" && (
                <Link
                  to="/area-manager"
                  className="w-full flex justify-center py-2 px-4 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                >
                  {t("unauthorized.goToAreaManager")}
                </Link>
              )}
            </>
          ) : (
            <Link
              to="/login"
              className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              {t("unauthorized.login")}
            </Link>
          )}

          <button
            onClick={handleGoBack}
            className="w-full flex justify-center py-2 px-4 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
          >
            {t("unauthorized.goBack")}
          </button>
        </div>
      </div>
    </div>
  );
};

export default UnauthorizedPage;
