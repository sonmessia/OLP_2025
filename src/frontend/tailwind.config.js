/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  darkMode: "class", // Hỗ trợ toggle dark mode
  theme: {
    extend: {
      colors: {
        // Brand Colors - GreenWave
        greenwave: {
          primary: {
            light: "#107C41", // Primary Green (Light Mode)
            dark: "#4CAF50", // Primary Green (Dark Mode)
            DEFAULT: "#107C41",
          },
          secondary: {
            light: "#E8F5E9", // Secondary Mint (Light Mode)
            dark: "#1B5E20", // Secondary Mint (Dark Mode)
            DEFAULT: "#E8F5E9",
          },
          accent: {
            light: "#FFFFFF", // Accent White (Light Mode)
            dark: "#121212", // Accent White (Dark Mode)
            DEFAULT: "#FFFFFF",
          },
          // Static shades for convenience
          dark: "#1B5E20",
          light: "#E8F5E9",
        },

        // Text Colors
        text: {
          main: {
            light: "#1F2937", // Text Main (Light Mode)
            dark: "#E0E0E0", // Text Main (Dark Mode)
            DEFAULT: "#1F2937",
          },
          muted: {
            light: "#6B7280", // Text Muted (Light Mode)
            dark: "#9E9E9E", // Text Muted (Dark Mode)
            DEFAULT: "#6B7280",
          },
        },

        // Functional Colors - Traffic Signals
        traffic: {
          red: "#D9232F", // Dừng lại / Ô nhiễm nguy hại (AQI > 150)
          yellow: "#FBBF24", // Chờ / Ô nhiễm trung bình (AQI 50-100)
          green: "#10B981", // Đi / Không khí trong lành (AQI < 50)
          info: "#3B82F6", // Thông tin chung, lưu lượng xe bình thường
        },
      },

      // Background colors using the palette
      backgroundColor: {
        primary: "var(--color-greenwave-accent)",
      },

      // Text colors using the palette
      textColor: {
        primary: "var(--color-text-main)",
        secondary: "var(--color-text-muted)",
      },
    },
  },
  plugins: [],
};
