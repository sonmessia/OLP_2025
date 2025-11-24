// src/presentation/hooks/useSensors.ts
import { useEffect } from "react";
import { useAppDispatch, useAppSelector } from "../../data/redux/hooks";
import {
  fetchAllSensors,
  refreshSensors,
  setSelectedSensor,
  clearError,
} from "../../data/redux/sensorSlice";
import type { SensorModel } from "../../domain/models/SenSorModel";

export const useSensors = () => {
  const dispatch = useAppDispatch();
  const { sensors, selectedSensor, loading, error } = useAppSelector(
    (state) => state.sensors
  );

  useEffect(() => {
    dispatch(fetchAllSensors());
  }, [dispatch]);

  const handleRefresh = async () => {
    try {
      await dispatch(refreshSensors()).unwrap();
      return { success: true };
    } catch (err) {
      return { success: false, error: err };
    }
  };

  const selectSensor = (sensor: SensorModel | null) => {
    dispatch(setSelectedSensor(sensor));
  };

  const dismissError = () => {
    dispatch(clearError());
  };

  return {
    sensors,
    selectedSensor,
    loading,
    error,
    handleRefresh,
    selectSensor,
    dismissError,
  };
};
