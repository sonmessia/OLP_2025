// Copyright (c) 2025 Green Wave Team
// 
// This software is released under the MIT License.
// https://opensource.org/licenses/MIT

import React, { useState } from "react";
import { useTranslation } from "react-i18next";

const PipelineAnimation: React.FC = () => {
  const [activeStep, setActiveStep] = useState(0);
  const { t } = useTranslation("landing");

  const steps = [
    {
      title: t("pipeline.steps.sumo.title"),
      desc: t("pipeline.steps.sumo.desc"),
      color: "var(--color-traffic-info)",
    },
    {
      title: t("pipeline.steps.iotAgent.title"),
      desc: t("pipeline.steps.iotAgent.desc"),
      color: "var(--color-traffic-yellow)",
    },
    {
      title: t("pipeline.steps.orion.title"),
      desc: t("pipeline.steps.orion.desc"),
      color: "var(--color-greenwave-primary-light)",
    },
    {
      title: t("pipeline.steps.aiAgent.title"),
      desc: t("pipeline.steps.aiAgent.desc"),
      color: "var(--color-greenwave-primary-light)",
    },
    {
      title: t("pipeline.steps.dashboard.title"),
      desc: t("pipeline.steps.dashboard.desc"),
      color: "var(--color-traffic-info)",
    },
  ];

  React.useEffect(() => {
    const interval = setInterval(() => {
      setActiveStep((prev) => (prev + 1) % steps.length);
    }, 2000);

    return () => clearInterval(interval);
  }, [steps.length]);

  return (
    <div className="relative w-full max-w-6xl mx-auto">
      {/* Main pipeline line */}
      <div className="absolute top-1/2 left-0 right-0 h-1 transform -translate-y-1/2 z-0">
        <div
          className="h-full pipeline-flow rounded-full"
          style={{
            background:
              "linear-gradient(90deg, transparent 0%, var(--color-greenwave-primary-light) 50%, transparent 100%)",
            backgroundSize: "200% 100%",
            animation: "flow-pulse 3s ease-in-out infinite",
          }}
        />
      </div>

      {/* Pipeline nodes */}
      <div className="relative flex justify-between items-center z-10">
        {steps.map((step, index) => (
          <div key={index} className="relative group">
            {/* Connection indicator */}
            {activeStep === index && (
              <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2">
                <div
                  className="w-20 h-20 rounded-full animate-ping"
                  style={{ backgroundColor: step.color }}
                />
              </div>
            )}

            {/* Main node */}
            <div
              className={`relative w-32 h-32 rounded-full flex flex-col items-center justify-center text-center p-4 transition-all duration-300 cursor-pointer ${
                activeStep === index ? "scale-110 z-20" : "scale-100"
              }`}
              style={{
                background: `rgba(255, 255, 255, ${
                  activeStep === index ? 0.15 : 0.05
                })`,
                backdropFilter: "blur(10px)",
                border: `2px solid ${
                  activeStep === index ? step.color : "rgba(255, 255, 255, 0.1)"
                }`,
                boxShadow:
                  activeStep === index ? `0 0 30px ${step.color}` : "none",
              }}
              onMouseEnter={() => setActiveStep(index)}
            >
              <div
                className="w-12 h-12 rounded-full mb-2 flex items-center justify-center"
                style={{ backgroundColor: `${step.color}20` }}
              >
                <div
                  className="w-6 h-6 rounded-full"
                  style={{ backgroundColor: step.color }}
                />
              </div>

              <h4 className="font-semibold text-sm text-text-main-dark mb-1">
                {step.title}
              </h4>
              <p className="text-xs text-text-muted-dark leading-tight">
                {step.desc}
              </p>
            </div>

            {/* Data flow particles */}
            {activeStep === index && (
              <div className="absolute -top-2 -right-2">
                <div className="relative">
                  {[...Array(3)].map((_, i) => (
                    <div
                      key={i}
                      className="absolute w-2 h-2 rounded-full"
                      style={{
                        backgroundColor: step.color,
                        animation: `orbit-particle ${
                          1.5 + i * 0.3
                        }s linear infinite`,
                        transform: `rotate(${i * 120}deg) translateX(20px)`,
                      }}
                    />
                  ))}
                </div>
              </div>
            )}

            {/* Flow direction arrow */}
            {index < steps.length - 1 && (
              <div className="absolute top-1/2 left-full w-8 h-1 transform -translate-y-1/2 ml-8">
                <div
                  className="w-full h-full"
                  style={{ backgroundColor: step.color }}
                />
                <div
                  className="absolute right-0 top-1/2 transform -translate-y-1/2 w-0 h-0 border-t-4 border-b-4 border-l-4 border-transparent"
                  style={{ borderLeftColor: step.color }}
                />
              </div>
            )}
          </div>
        ))}
      </div>

      {/* Data flow indicators */}
      <div className="mt-16 text-center">
        <div
          className="inline-flex items-center gap-2 px-4 py-2 rounded-full"
          style={{
            background: "rgba(255, 255, 255, 0.05)",
            backdropFilter: "blur(10px)",
          }}
        >
          <div className="w-2 h-2 rounded-full bg-greenwave-primary-light animate-pulse" />
          <span className="text-sm text-text-muted-dark">
            {t("pipeline.flowActive")}
          </span>
        </div>
      </div>
    </div>
  );
};

export default PipelineAnimation;
