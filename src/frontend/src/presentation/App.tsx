// src/core/App.tsx
import React from "react";
import { Provider } from "react-redux";
import { store } from "../data/redux/store";
import { ManagerDashboard } from "./pages/ManagerDashboard";

const App: React.FC = () => {
  return (
    <Provider store={store}>
      <ManagerDashboard />
    </Provider>
  );
};

export default App;
