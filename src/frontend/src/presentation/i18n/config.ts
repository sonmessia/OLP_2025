// Copyright (c) 2025 Green Wave Team
// 
// This software is released under the MIT License.
// https://opensource.org/licenses/MIT

import i18n from "i18next";
import { initReactI18next } from "react-i18next";
import LanguageDetector from "i18next-browser-languagedetector";
import en from "./locales/en.json";
import vi from "./locales/vi.json";

export const defaultNS = "common";
export const resources = {
  en: {
    common: en.common,
    locations: en.locations,
    navigation: en.navigation,
    dashboard: en.dashboard,
    landing: en.landing,
    traffic: en.traffic,
    devices: en.devices,
    subscription: en.subscription,
    aqi: en.aqi,
    alerts: en.alerts,
    user: en.user,
    auth: en.auth,
    forms: en.forms,
    maps: en.maps,
    errors: en.errors,
    manualControl: en.manualControl,
    monitoring: en.monitoring,
    charts: en.charts,
    areaControl: en.areaControl,
    sumo: en.sumo,
  },
  vi: {
    common: vi.common,
    locations: vi.locations,
    navigation: vi.navigation,
    dashboard: vi.dashboard,
    landing: vi.landing,
    traffic: vi.traffic,
    devices: vi.devices,
    subscription: vi.subscription,
    aqi: vi.aqi,
    alerts: vi.alerts,
    user: vi.user,
    auth: vi.auth,
    forms: vi.forms,
    maps: vi.maps,
    errors: vi.errors,
    manualControl: vi.manualControl,
    monitoring: vi.monitoring,
    charts: vi.charts,
    areaControl: vi.areaControl,
    sumo: vi.sumo,
  },
} as const;

i18n
  .use(LanguageDetector)
  .use(initReactI18next)
  .init({
    debug: import.meta.env.DEV,
    fallbackLng: "en",
    defaultNS,
    resources,
    interpolation: {
      escapeValue: false, // not needed for react as it escapes by default
    },
  });

export default i18n;
