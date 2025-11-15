// src/core/App.tsx
import React from "react";
import { Provider } from "react-redux";
import { store } from "../data/redux/store";
import { DashboardContainer } from "./container/DashboardContainer";

const App: React.FC = () => {
  return (
    <Provider store={store}>
      <DashboardContainer />
    </Provider>
  );
};

export default App;
