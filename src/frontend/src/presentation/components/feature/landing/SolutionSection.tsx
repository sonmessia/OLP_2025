import React, { useState } from "react";
import { useTranslation } from "react-i18next";

export const SolutionSection: React.FC = () => {
  const [sliderValue, setSliderValue] = useState(50);
  const { t } = useTranslation("landing");

  return (
    <section className="py-20 px-4 relative">
      <div className="max-w-6xl mx-auto">
        <div
          className="glass-card p-12 rounded-3xl"
          style={{
            background: "rgba(255, 255, 255, 0.03)",
            backdropFilter: "blur(15px)",
            border: "1px solid rgba(255, 255, 255, 0.1)",
          }}
        >
          <h3 className="text-3xl md:text-4xl font-bold text-center mb-4 text-text-main-dark">
            {t("solution.tradeOffTitle")}
          </h3>
          <p className="text-xl text-center text-text-muted-dark mb-12">
            {t("solution.tradeOffSubtitle")}
          </p>

          {/* Interactive Slider */}
          <div className="max-w-4xl mx-auto">
            <div className="mb-8">
              <div className="flex justify-between items-center mb-4">
                <span
                  className="text-lg font-semibold"
                  style={{ color: "var(--color-traffic-info)" }}
                >
                  {t("solution.trafficSpeed")}
                </span>
                <span
                  className="text-lg font-semibold"
                  style={{ color: "var(--color-greenwave-primary-light)" }}
                >
                  {t("solution.airQuality")}
                </span>
              </div>

              <div className="relative">
                <input
                  type="range"
                  min="0"
                  max="100"
                  value={sliderValue}
                  onChange={(e) => setSliderValue(Number(e.target.value))}
                  className="w-full h-3 rounded-lg appearance-none cursor-pointer slider"
                  style={{
                    background: `linear-gradient(to right,
                      var(--color-traffic-info) 0%,
                      var(--color-traffic-info) ${sliderValue}%,
                      var(--color-greenwave-primary-light) ${sliderValue}%,
                      var(--color-greenwave-primary-light) 100%)`,
                  }}
                />

                <div
                  className="absolute top-1/2 -translate-y-1/2 w-6 h-6 rounded-full border-2 border-white shadow-lg transition-all duration-300"
                  style={{
                    left: `${sliderValue}%`,
                    transform: "translate(-50%, -50%)",
                    background:
                      sliderValue > 50
                        ? "var(--color-greenwave-primary-light)"
                        : "var(--color-traffic-info)",
                    boxShadow: `0 0 20px ${
                      sliderValue > 50
                        ? "var(--color-greenwave-primary-light)"
                        : "var(--color-traffic-info)"
                    }`,
                  }}
                />
              </div>

              <div className="mt-6 grid grid-cols-2 gap-6">
                <div
                  className="text-center p-4 rounded-lg"
                  style={{ background: "rgba(59, 130, 246, 0.1)" }}
                >
                  <p className="text-sm text-text-muted-dark">
                    {t("solution.weightSpeed")}
                  </p>
                  <p
                    className="text-2xl font-bold"
                    style={{ color: "var(--color-traffic-info)" }}
                  >
                    {(100 - sliderValue) / 100}
                  </p>
                </div>
                <div
                  className="text-center p-4 rounded-lg"
                  style={{ background: "rgba(16, 124, 65, 0.1)" }}
                >
                  <p className="text-sm text-text-muted-dark">
                    {t("solution.weightAir")}
                  </p>
                  <p
                    className="text-2xl font-bold"
                    style={{ color: "var(--color-greenwave-primary-light)" }}
                  >
                    {sliderValue / 100}
                  </p>
                </div>
              </div>
            </div>

            <p className="text-center text-text-muted-dark">
              {t("solution.sliderInstruction")}
              <br />
              <span className="text-sm">{t("solution.morlExplanation")}</span>
            </p>
          </div>
        </div>
      </div>
    </section>
  );
};
