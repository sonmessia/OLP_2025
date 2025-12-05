// src/presentation/pages/RegisterPage.tsx

import React, { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import { useTranslation } from "react-i18next";
import type { AppDispatch } from "../../../data/redux/store";
import { register, clearError } from "../../../data/redux/authSlice";
import type { RootState } from "../../../data/redux/store";
import { type RegisterData, UserRole } from "../../../domain/models/AuthModels";

const RegisterPage: React.FC = () => {
  const { t } = useTranslation("auth");

  const [formData, setFormData] = useState<RegisterData>({
    email: "",
    password: "",
    name: "",
    role: UserRole.ADMIN,
  });

  const [errors, setErrors] = useState<{
    email?: string;
    password?: string;
    name?: string;
    role?: string;
    areaName?: string;
  }>({});

  const dispatch = useDispatch<AppDispatch>();
  const navigate = useNavigate();

  const { isLoading, error, isAuthenticated } = useSelector(
    (state: RootState) => state.auth
  );

  useEffect(() => {
    // Nếu đã authenticated, redirect đến dashboard
    if (isAuthenticated) {
      navigate("/dashboard");
    }
  }, [isAuthenticated, navigate]);

  useEffect(() => {
    // Clear error khi component unmount
    return () => {
      dispatch(clearError());
    };
  }, [dispatch]);

  const validateForm = (): boolean => {
    const newErrors: typeof errors = {};

    if (!formData.email.trim()) {
      newErrors.email = t("validation.emailRequired");
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      newErrors.email = t("validation.emailInvalid");
    }

    if (!formData.password.trim()) {
      newErrors.password = t("validation.passwordRequired");
    } else if (formData.password.length < 6) {
      newErrors.password = t("validation.passwordMinLength");
    }

    if (!formData.name.trim()) {
      newErrors.name = t("validation.nameRequired");
    }

    if (!formData.role) {
      newErrors.role = t("validation.roleRequired");
    }

    if (formData.role === UserRole.AREA_MANAGER && !formData.areaName?.trim()) {
      newErrors.areaName = t("validation.areaNameRequired");
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!validateForm()) {
      return;
    }

    dispatch(register(formData));
  };

  const handleInputChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>
  ) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));

    // Clear error for this field when user starts typing
    if (errors[name as keyof typeof errors]) {
      setErrors((prev) => ({
        ...prev,
        [name]: undefined,
      }));
    }
  };

  if (isAuthenticated) {
    return null; // Will redirect in useEffect
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div>
          <div className="flex justify-center">
            <div className="w-16 h-16 bg-indigo-600 rounded-full flex items-center justify-center">
              <svg
                className="w-8 h-8 text-white"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z"
                />
              </svg>
            </div>
          </div>
          <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
            {t("register.title")}
          </h2>
          <p className="mt-2 text-center text-sm text-gray-600">
            {t("register.subtitle")}{" "}
            <Link
              to="/login"
              className="font-medium text-indigo-600 hover:text-indigo-500"
            >
              {t("register.loginLink")}
            </Link>
          </p>
        </div>

        <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
          {error && (
            <div className="rounded-md bg-red-50 p-4">
              <div className="flex">
                <div className="flex-shrink-0">
                  <svg
                    className="h-5 w-5 text-red-400"
                    viewBox="0 0 20 20"
                    fill="currentColor"
                  >
                    <path
                      fillRule="evenodd"
                      d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                      clipRule="evenodd"
                    />
                  </svg>
                </div>
                <div className="ml-3">
                  <p className="text-sm text-red-800">{error}</p>
                </div>
              </div>
            </div>
          )}

          <div className="space-y-4">
            <div>
              <label
                htmlFor="name"
                className="block text-sm font-medium text-gray-700"
              >
                {t("register.nameLabel")}
              </label>
              <input
                id="name"
                name="name"
                type="text"
                autoComplete="name"
                value={formData.name}
                onChange={handleInputChange}
                className={`mt-1 block w-full px-3 py-2 border rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm ${
                  errors.name ? "border-red-300" : "border-gray-300"
                }`}
                placeholder={t("register.namePlaceholder")}
              />
              {errors.name && (
                <p className="mt-1 text-sm text-red-600">{errors.name}</p>
              )}
            </div>

            <div>
              <label
                htmlFor="email"
                className="block text-sm font-medium text-gray-700"
              >
                {t("register.emailLabel")}
              </label>
              <input
                id="email"
                name="email"
                type="email"
                autoComplete="email"
                value={formData.email}
                onChange={handleInputChange}
                className={`mt-1 block w-full px-3 py-2 border rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm ${
                  errors.email ? "border-red-300" : "border-gray-300"
                }`}
                placeholder={t("register.emailPlaceholder")}
              />
              {errors.email && (
                <p className="mt-1 text-sm text-red-600">{errors.email}</p>
              )}
            </div>

            <div>
              <label
                htmlFor="password"
                className="block text-sm font-medium text-gray-700"
              >
                {t("register.passwordLabel")}
              </label>
              <input
                id="password"
                name="password"
                type="password"
                autoComplete="new-password"
                value={formData.password}
                onChange={handleInputChange}
                className={`mt-1 block w-full px-3 py-2 border rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm ${
                  errors.password ? "border-red-300" : "border-gray-300"
                }`}
                placeholder={t("register.passwordPlaceholder")}
              />
              {errors.password && (
                <p className="mt-1 text-sm text-red-600">{errors.password}</p>
              )}
            </div>

            <div>
              <label
                htmlFor="role"
                className="block text-sm font-medium text-gray-700"
              >
                {t("register.roleLabel")}
              </label>
              <select
                id="role"
                name="role"
                value={formData.role}
                onChange={handleInputChange}
                className={`mt-1 block w-full px-3 py-2 border rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm ${
                  errors.role ? "border-red-300" : "border-gray-300"
                }`}
              >
                <option value="">{t("register.rolePlaceholder")}</option>
                <option value={UserRole.ADMIN}>{t("user.admin")}</option>
                <option value={UserRole.AREA_MANAGER}>{t("user.areaManager")}</option>
              </select>
              {errors.role && (
                <p className="mt-1 text-sm text-red-600">{errors.role}</p>
              )}
            </div>

            {formData.role === UserRole.AREA_MANAGER && (
              <div>
                <label
                  htmlFor="areaName"
                  className="block text-sm font-medium text-gray-700"
                >
                  {t("register.areaNameLabel")}
                </label>
                <input
                  id="areaName"
                  name="areaName"
                  type="text"
                  value={formData.areaName || ""}
                  onChange={handleInputChange}
                  className={`mt-1 block w-full px-3 py-2 border rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm ${
                    errors.areaName ? "border-red-300" : "border-gray-300"
                  }`}
                  placeholder={t("register.areaNamePlaceholder")}
                />
                {errors.areaName && (
                  <p className="mt-1 text-sm text-red-600">{errors.areaName}</p>
                )}
              </div>
            )}
          </div>

          <div>
            <button
              type="submit"
              disabled={isLoading}
              className={`group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white ${
                isLoading
                  ? "bg-indigo-400 cursor-not-allowed"
                  : "bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
              } transition duration-150 ease-in-out`}
            >
              {isLoading ? (
                <>
                  <svg
                    className="animate-spin -ml-1 mr-3 h-5 w-5 text-white"
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                  >
                    <circle
                      className="opacity-25"
                      cx="12"
                      cy="12"
                      r="10"
                      stroke="currentColor"
                      strokeWidth="4"
                    ></circle>
                    <path
                      className="opacity-75"
                      fill="currentColor"
                      d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                    ></path>
                  </svg>
                  {t("register.registering")}
                </>
              ) : (
                t("register.registerButton")
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default RegisterPage;
