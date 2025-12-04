import React, { useState, useEffect } from "react";
import { useSelector, useDispatch } from "react-redux";
import { UserMapHeader } from "../../components/feature/usermap/UserMapHeader";
import { UserMapView } from "../../components/feature/usermap/UserMapView";
import { HealthInsightPanel } from "../../components/feature/usermap/HealthInsightPanel";
import { AQIGauge } from "../../components/feature/usermap/AQIGauge";
import { TrafficStatusCard } from "../../components/feature/usermap/TrafficStatusCard";
import type { AirQualityObservedModel } from "../../../domain/models/AirQualityObservedModel";
import type { LocationModel } from "../../../domain/models/CommonModels";
import { AirQualityRepositoryImpl } from "../../../data/repositories/AirQualityRepositoryImpl";
import { GetAirQualityDataUseCase } from "../../../domain/usecases/airquality/GetAirQualityDataUseCase";
import { fetchSumoState } from "../../../data/redux/sumoSlice";
import type { RootState, AppDispatch } from "../../../data/redux/store";

export const UserMap: React.FC = () => {
  const dispatch = useDispatch<AppDispatch>();
  const { simulationState } = useSelector((state: RootState) => state.sumo);

  const [isDarkMode, setIsDarkMode] = useState(false);
  const [selectedLocation, setSelectedLocation] =
    useState<LocationModel | null>(null);
  const [selectedAirQuality, setSelectedAirQuality] =
    useState<AirQualityObservedModel | null>(null);
  const [searchQuery, setSearchQuery] = useState("");
  const [airQualityData, setAirQualityData] = useState<
    AirQualityObservedModel[]
  >([]);

  // Initialize dark mode
  useEffect(() => {
    const getInitialDarkMode = () => {
      if (typeof window !== "undefined") {
        const stored = localStorage.getItem("darkMode");
        if (stored !== null) {
          return stored === "true";
        }
        return window.matchMedia("(prefers-color-scheme: dark)").matches;
      }
      return false;
    };

    setIsDarkMode(getInitialDarkMode());
  }, []);

  // Fetch Air Quality Data
  useEffect(() => {
    const fetchData = async () => {
      try {
        const repository = new AirQualityRepositoryImpl();
        const useCase = new GetAirQualityDataUseCase(repository);
        const data = await useCase.execute();
        setAirQualityData(data);
      } catch (error) {
        console.error("Failed to fetch air quality data:", error);
      }
    };

    fetchData();
  }, []);

  // Poll SUMO Traffic Data
  useEffect(() => {
    // Fetch immediately
    dispatch(fetchSumoState());

    // Poll every 5 seconds
    const intervalId = setInterval(() => {
      dispatch(fetchSumoState());
    }, 5000);

    return () => clearInterval(intervalId);
  }, [dispatch]);

  // Apply dark mode class
  useEffect(() => {
    if (isDarkMode) {
      document.documentElement.classList.add("dark");
    } else {
      document.documentElement.classList.remove("dark");
    }
  }, [isDarkMode]);

  const handleThemeToggle = () => {
    const newDarkMode = !isDarkMode;
    setIsDarkMode(newDarkMode);
    localStorage.setItem("darkMode", newDarkMode.toString());
  };

  const handleLocationSelect = (
    location: LocationModel,
    airQuality?: AirQualityObservedModel
  ) => {
    setSelectedLocation(location);
    setSelectedAirQuality(airQuality || null);
  };

  const handleSearch = (query: string) => {
    setSearchQuery(query);
    // Search functionality will be implemented in the search component
  };

  const handleTrafficSelect = (_scenarioId: string) => {
    // For now, we assume selecting a traffic location triggers a fetch of the state
    // In a real app, this might switch the active scenario on the backend
    // or fetch specific data for that scenario.
    // For this demo, we'll just ensure we are fetching the global state
    // and maybe set a local state to show we are focusing on this traffic node.

    // If you wanted to switch scenario:
    // dispatch(startSimulation({ scenario: scenarioId, gui: false, port: 8813 }));

    // Just fetch state for now
    dispatch(fetchSumoState());

    // We could also set a "selectedTrafficNode" state if we wanted to show specific info
    // distinct from the global simulation state, but the request implies showing the card.
  };

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 relative">
      {/* Header */}
      <UserMapHeader
        onThemeToggle={handleThemeToggle}
        isDarkMode={isDarkMode}
        onSearch={handleSearch}
        searchQuery={searchQuery}
      />

      {/* Main Content */}
      <div className="relative h-[calc(100vh-72px)]">
        {/* Map View */}
        <UserMapView
          isDarkMode={isDarkMode}
          airQualityData={airQualityData}
          selectedLocation={selectedLocation}
          onLocationSelect={handleLocationSelect}
          onTrafficSelect={handleTrafficSelect}
          searchQuery={searchQuery}
        />

        {/* AQI Gauge - Fixed Position (Bottom Left) */}
        <div className="absolute bottom-6 left-4 z-[1000]">
          <AQIGauge
            value={selectedAirQuality?.airQualityIndex || 50}
            isDarkMode={isDarkMode}
          />
        </div>

        {/* Traffic Status Card - Fixed Position (Bottom Right) */}
        {simulationState && (
          <div className="absolute bottom-6 right-4 z-[1000] w-80">
            <TrafficStatusCard
              avgSpeed={simulationState.avgSpeed}
              vehicleCount={simulationState.vehicleCount}
              waitingTime={simulationState.waitingTime}
              lastUpdated={new Date()} // In a real app, this would come from simulationState.timestamp or similar
              isDarkMode={isDarkMode}
            />
          </div>
        )}

        {/* Health Insight Panel - Fixed Position (Top Right) */}
        {selectedAirQuality && (
          <div className="absolute top-4 right-4 z-[1000] w-80">
            <HealthInsightPanel
              airQuality={selectedAirQuality}
              isDarkMode={isDarkMode}
            />
          </div>
        )}
      </div>
    </div>
  );
};
