// src/presentation/App.tsx
import React from "react";
import { Provider } from "react-redux";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { store } from "../data/redux/store";
import { ManagerDashboard } from "./pages/ManagerDashboard";
import { UserMap } from "./pages/UserMap";
import LandingPage from "./pages/LandingPage";
import { DeviceManagementPage } from "./pages/DeviceManagementPage";

const App: React.FC = () => {
  return (
    <Provider store={store}>
      <Router>
        <Routes>
          <Route path="/" element={<UserMap />} />
          <Route path="/admin" element={<ManagerDashboard />} />
          <Route path="/introduce" element={<LandingPage />} />
          <Route path="/devices" element={<DeviceManagementPage />} />
        </Routes>
      </Router>
    </Provider>
  );
};

export default App;
