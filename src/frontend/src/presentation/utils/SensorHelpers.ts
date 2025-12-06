// Copyright (c) 2025 Green Wave Team
// 
// This software is released under the MIT License.
// https://opensource.org/licenses/MIT

export const getAirQualityLevelFromAQI = (aqi: number): string => {
  if (aqi <= 50) return "Good";
  if (aqi <= 100) return "Moderate";
  if (aqi <= 150) return "Unhealthy for Sensitive Groups";
  if (aqi <= 200) return "Unhealthy";
  if (aqi <= 300) return "Very Unhealthy";
  return "Hazardous";
};

export const getAirQualityColor = (level: string): string => {
  const levelLower = level.toLowerCase();
  if (levelLower.includes("good")) return "#10b981";
  if (levelLower.includes("moderate")) return "#f59e0b";
  if (levelLower.includes("unhealthy")) return "#ef4444";
  if (levelLower.includes("very")) return "#9333ea";
  if (levelLower.includes("hazardous")) return "#7c2d12";
  return "#6b7280";
};

export const getWaterQualityColor = (level?: string): string => {
  if (!level) return "#6b7280";
  const levelLower = level.toLowerCase();
  if (levelLower === "excellent") return "#10b981";
  if (levelLower === "good") return "#22c55e";
  if (levelLower === "moderate") return "#f59e0b";
  if (levelLower === "poor") return "#ef4444";
  if (levelLower === "very_poor") return "#7c2d12";
  return "#6b7280";
};

export const getWaterQualityText = (level?: string): string => {
  if (!level) return "Không rõ";
  const texts: Record<string, string> = {
    excellent: "Xuất sắc",
    good: "Tốt",
    moderate: "Trung bình",
    poor: "Kém",
    very_poor: "Rất kém",
  };
  return texts[level] || "Không rõ";
};

export const getAirQualityText = (level?: string): string => {
  if (!level) return "Không rõ";
  const levelLower = level.toLowerCase();
  if (levelLower.includes("good")) return "Tốt";
  if (levelLower.includes("moderate")) return "Trung bình";
  if (levelLower.includes("sensitive")) return "Không tốt cho nhóm nhạy cảm";
  if (levelLower.includes("very")) return "Rất không lành mạnh";
  if (levelLower.includes("unhealthy")) return "Không lành mạnh";
  if (levelLower.includes("hazardous")) return "Nguy hại";
  return "Không rõ";
};
