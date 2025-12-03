// src/presentation/components/common/AuthHeader.tsx

import React from "react";
import { useDispatch, useSelector } from "react-redux";
import { Link, useNavigate } from "react-router-dom";
import type { AppDispatch } from "../../../data/redux/store";
import { logout } from "../../../data/redux/authSlice";
import type { RootState } from "../../../data/redux/store";
import { UserRole } from "../../../domain/models/AuthModels";

interface AuthHeaderProps {
  title?: string;
}

const AuthHeader: React.FC<AuthHeaderProps> = ({
  title = "Hệ thống điều khiển giao thông",
}) => {
  const dispatch = useDispatch<AppDispatch>();
  const navigate = useNavigate();
  const { user } = useSelector((state: RootState) => state.auth);

  const handleLogout = async () => {
    await dispatch(logout());
    navigate("/login");
  };

  const handleHome = () => {
    if (user?.role === UserRole.ADMIN) {
      navigate("/control");
    } else if (user?.role === UserRole.AREA_MANAGER) {
      navigate("/area-manager");
    } else {
      navigate("/");
    }
  };

  const handleDashboard = () => {
    if (user?.role === UserRole.ADMIN) {
      navigate("/admin");
    } else {
      navigate("/area-manager");
    }
  };

  return (
    <header className="bg-white shadow-sm border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Left side - Title and Navigation */}
          <div className="flex items-center space-x-4">
            <button
              onClick={handleHome}
              className="text-xl font-semibold text-gray-900 hover:text-indigo-600 transition-colors"
            >
              {title}
            </button>

            {/* Navigation for admin */}
            {user?.role === UserRole.ADMIN && (
              <nav className="hidden md:flex space-x-4">
                <Link
                  to="/control"
                  className="text-sm font-medium text-gray-700 hover:text-indigo-600 px-3 py-2 rounded-md text-sm hover:bg-gray-50"
                >
                  Điều khiển
                </Link>
                <Link
                  to="/admin"
                  className="text-sm font-medium text-gray-700 hover:text-indigo-600 px-3 py-2 rounded-md text-sm hover:bg-gray-50"
                >
                  Dashboard
                </Link>
                <Link
                  to="/devices"
                  className="text-sm font-medium text-gray-700 hover:text-indigo-600 px-3 py-2 rounded-md text-sm hover:bg-gray-50"
                >
                  Thiết bị
                </Link>
              </nav>
            )}

            {/* Navigation for area manager */}
            {user?.role === UserRole.AREA_MANAGER && (
              <nav className="hidden md:flex space-x-4">
                <button
                  onClick={handleDashboard}
                  className="text-sm font-medium text-gray-700 hover:text-indigo-600 px-3 py-2 rounded-md text-sm hover:bg-gray-50"
                >
                  Dashboard
                </button>
              </nav>
            )}
          </div>

          {/* Right side - User info and actions */}
          <div className="flex items-center space-x-4">
            {/* User info */}
            <div className="flex items-center space-x-3">
              <div className="text-right hidden sm:block">
                <p className="text-sm font-medium text-gray-900">
                  {user?.name}
                </p>
                <p className="text-xs text-gray-500">
                  {user?.role === UserRole.ADMIN
                    ? "Quản lý chính"
                    : "Quản lý khu vực"}
                  {user?.areaName && ` • ${user.areaName}`}
                </p>
              </div>
              <div className="w-8 h-8 bg-indigo-500 rounded-full flex items-center justify-center">
                <span className="text-white text-sm font-medium">
                  {user?.name?.charAt(0).toUpperCase()}
                </span>
              </div>
            </div>

            {/* Logout button */}
            <button
              onClick={handleLogout}
              className="inline-flex items-center px-3 py-1.5 border border-transparent text-xs font-medium rounded text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 transition-colors"
            >
              <svg
                className="w-4 h-4 mr-1"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"
                />
              </svg>
              Đăng xuất
            </button>
          </div>
        </div>
      </div>
    </header>
  );
};

export default AuthHeader;
