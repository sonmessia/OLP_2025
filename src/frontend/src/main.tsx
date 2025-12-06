// Copyright (c) 2025 Green Wave Team
// 
// This software is released under the MIT License.
// https://opensource.org/licenses/MIT

import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./presentation/styles/index.css";
import "./presentation/i18n/config";
import App from "./presentation/App.tsx";

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <App />
  </StrictMode>
);
