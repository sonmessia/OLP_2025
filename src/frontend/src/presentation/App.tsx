// src/presentation/App.tsx
import React, { useEffect } from "react";
import { Provider } from "react-redux";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { store } from "../data/redux/store";
import {
  verifyToken,
  setAuthState,
  clearAuthState,
} from "../data/redux/authSlice";
import { UserRole } from "../domain/models/AuthModels";
import { ManagerDashboard } from "./pages/ManagerDashboard";
import { UserMap } from "./pages/UserMap";
import LandingPage from "./pages/LandingPage";
import { DeviceManagementPage } from "./pages/DeviceManagementPage";
import { ControlTrafficPage } from "./pages/ControlTrafficPage";
import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";
import AreaManagerPage from "./pages/AreaManagerPage";
import UnauthorizedPage from "./pages/UnauthorizedPage";
import ProtectedRoute from "./components/common/ProtectedRoute";

const AppContent: React.FC = () => {
  useEffect(() => {
    // Check for existing auth state in localStorage on app load
    const token = localStorage.getItem("authToken");
    const userStr = localStorage.getItem("user");

    if (token && userStr) {
      try {
        const user = JSON.parse(userStr);
        // Set auth state from localStorage
        store.dispatch(setAuthState({ user, token }));

        // Verify token is still valid
        store.dispatch(verifyToken(token));
      } catch (error) {
        // If parsing fails, clear invalid data
        store.dispatch(clearAuthState());
        localStorage.removeItem("authToken");
        localStorage.removeItem("user");
      }
    }
  }, []);

  return (
    <Router>
      <Routes>
        {/* Public routes */}
        <Route path="/" element={<UserMap />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/introduce" element={<LandingPage />} />
        <Route path="/unauthorized" element={<UnauthorizedPage />} />

        {/* Protected routes */}
        <Route
          path="/admin"
          element={
            <ProtectedRoute requiredRole={UserRole.ADMIN}>
              <ManagerDashboard />
            </ProtectedRoute>
          }
        />

        <Route
          path="/control"
          element={
            <ProtectedRoute requiredRole={UserRole.ADMIN}>
              <ControlTrafficPage />
            </ProtectedRoute>
          }
        />

        <Route
          path="/area-manager"
          element={
            <ProtectedRoute requiredRole={UserRole.AREA_MANAGER}>
              <AreaManagerPage />
            </ProtectedRoute>
          }
        />

        <Route
          path="/devices"
          element={
            <ProtectedRoute>
              <DeviceManagementPage />
            </ProtectedRoute>
          }
        />
      </Routes>
    </Router>
  );
};

const App: React.FC = () => {
  return (
    <Provider store={store}>
      <AppContent />
    </Provider>
  );
};

export default App;
