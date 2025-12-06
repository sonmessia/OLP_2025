import React from "react";
import { Activity, Globe, Shield } from "lucide-react";
import { useTranslation } from "react-i18next";

export const KeyFeaturesSection: React.FC = () => {
  const { t } = useTranslation("landing");

  const features = [
    {
      icon: Activity,
      title: t("keyFeaturesSection.digitalTwin.title"),
      description: t("keyFeaturesSection.digitalTwin.description"),
      color: "var(--color-traffic-info)",
      bgColor: "rgba(59, 130, 246, 0.2)",
    },
    {
      icon: Globe,
      title: t("keyFeaturesSection.globalStandard.title"),
      description: t("keyFeaturesSection.globalStandard.description"),
      color: "var(--color-greenwave-primary-light)",
      bgColor: "rgba(16, 124, 65, 0.2)",
    },
    {
      icon: Shield,
      title: t("keyFeaturesSection.dynamicResponse.title"),
      description: t("keyFeaturesSection.dynamicResponse.description"),
      color: "var(--color-traffic-red)",
      bgColor: "rgba(217, 35, 47, 0.2)",
    },
  ];

  return (
    <section className="py-20 px-4 relative">
      <div className="max-w-6xl mx-auto">
        <h3 className="text-3xl md:text-4xl font-bold text-center mb-16 text-text-main-dark">
          {t("keyFeaturesSection.title")}
        </h3>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {features.map((feature, index) => (
            <div
              key={index}
              className="glass-card p-8 rounded-2xl group hover:scale-105 transition-all duration-300"
              style={{
                background: "rgba(255, 255, 255, 0.03)",
                backdropFilter: "blur(10px)",
                border: "1px solid rgba(255, 255, 255, 0.1)",
              }}
            >
              <div
                className="w-16 h-16 mx-auto mb-6 rounded-full flex items-center justify-center group-hover:scale-110 transition-transform"
                style={{ background: feature.bgColor }}
              >
                <feature.icon
                  className="w-8 h-8"
                  style={{ color: feature.color }}
                />
              </div>
              <h4 className="text-xl font-semibold text-center mb-4 text-text-main-dark">
                {feature.title}
              </h4>
              <p className="text-text-muted-dark text-center leading-relaxed">
                {feature.description}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};
