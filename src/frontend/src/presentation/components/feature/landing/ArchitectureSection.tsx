import React from "react";
import { useTranslation } from "react-i18next";
import PipelineAnimation from "./PipelineAnimation";

export const ArchitectureSection: React.FC = () => {
  const { t } = useTranslation("landing");

  return (
    <section className="py-20 px-4 relative">
      <div className="max-w-6xl mx-auto">
        <h3 className="text-3xl md:text-4xl font-bold text-center mb-16 text-text-main-dark">
          {t("architecture.title")}
        </h3>

        <div className="relative">
          <PipelineAnimation />
        </div>
      </div>
    </section>
  );
};
