// Copyright (c) 2025 Green Wave Team
// 
// This software is released under the MIT License.
// https://opensource.org/licenses/MIT

import React from "react";
import { useTranslation } from "react-i18next";

export const Footer: React.FC = () => {
  const { t } = useTranslation("landing");

  return (
    <footer
      className="py-12 px-4"
      style={{ background: "var(--color-greenwave-accent-dark)" }}
    >
      <div className="max-w-6xl mx-auto">
        <div className="flex flex-col md:flex-row justify-between items-center gap-8">
          <div className="text-center md:text-left">
            <h3 className="text-2xl font-bold text-greenwave-primary-light mb-2">
              GreenWave
            </h3>
            <p className="text-text-muted-dark">{t("footer.rights")}</p>
          </div>

          <div className="flex gap-6">
            <a
              href="https://github.com/sonmessia/GreenWave.git"
              className="text-text-muted-dark hover:text-greenwave-primary-light transition-colors"
            >
              {t("footer.sourceCode")}
            </a>
            <a
              href=""
              className="text-text-muted-dark hover:text-greenwave-primary-light transition-colors"
            >
              {t("footer.dataModels")}
            </a>
            <a
              href=""
              className="text-text-muted-dark hover:text-greenwave-primary-light transition-colors"
            >
              {t("footer.contact")}
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
};
