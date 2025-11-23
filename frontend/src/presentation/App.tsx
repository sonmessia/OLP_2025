// src/core/App.tsx
import React from "react";
import { Provider } from "react-redux";
import { store } from "../data/redux/store";
import { DigitalTwinPage } from "./pages/DigitalTwinPage";

const App: React.FC = () => {
  return (
    <Provider store={store}>
      <DigitalTwinPage />
    </Provider>
  );
};

export default App;
