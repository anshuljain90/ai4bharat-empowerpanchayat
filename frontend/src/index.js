// File: frontend/src/index.js (Updated with ThemeProvider)
import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import { ThemeProvider } from "@mui/material/styles";
import { JMTemplateProvider } from "@jiomeet/core-template-web";
import CssBaseline from "@mui/material/CssBaseline";
import theme from "./theme";

// Import Roboto font
import "@fontsource/roboto/300.css";
import "@fontsource/roboto/400.css";
import "@fontsource/roboto/500.css";
import "@fontsource/roboto/700.css";

// Inject API Gateway x-api-key header into all fetch requests to the backend
const API_KEY = process.env.REACT_APP_API_GATEWAY_KEY;
if (API_KEY) {
  const originalFetch = window.fetch;
  window.fetch = function (url, options = {}) {
    const backendUrl = process.env.REACT_APP_BACKEND_URL || "";
    if (typeof url === "string" && backendUrl && url.startsWith(backendUrl)) {
      options.headers = {
        ...(options.headers || {}),
        "x-api-key": API_KEY,
      };
    }
    return originalFetch.call(this, url, options);
  };
}

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <React.StrictMode>
    <JMTemplateProvider>
      <ThemeProvider theme={theme}>
        {/* CssBaseline provides a consistent baseline across browsers */}
        <CssBaseline />
        <App />
      </ThemeProvider>
    </JMTemplateProvider>
  </React.StrictMode>
);
