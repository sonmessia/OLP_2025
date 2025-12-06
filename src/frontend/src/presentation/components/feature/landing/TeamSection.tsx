import React from "react";
import thaiAnhAI from "../../../../assets/team/thaianh.png";
import sonCloud from "../../../../assets/team/son.jpg";
import huynhMinhTri from "../../../../assets/team/tri.jpg";
import { useTranslation } from "react-i18next";

export const TeamSection: React.FC = () => {
  const { t } = useTranslation("landing");

  const teamMembers = [
    {
      name: "Thái Anh 36",
      role: t("team.roles.aiData"),
      imageUrl: thaiAnhAI,
    },
    {
      name: "Hoàng Sơn",
      role: t("team.roles.backend"),
      imageUrl: sonCloud,
    },
    {
      name: "Huỳnh Minh Trí",
      role: t("team.roles.frontend"),
      imageUrl: huynhMinhTri,
    },
  ];

  return (
    <section className="py-20 px-4 relative">
      <div className="max-w-6xl mx-auto">
        <h3 className="text-3xl md:text-4xl font-bold text-center mb-16 text-text-main-dark">
          {t("team.title")}
        </h3>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {teamMembers.map((member, index) => (
            <div
              key={index}
              className="glass-card p-8 rounded-2xl text-center group"
              style={{
                background: "rgba(255, 255, 255, 0.03)",
                backdropFilter: "blur(10px)",
                border: "1px solid rgba(255, 255, 255, 0.1)",
              }}
            >
              <div
                className="w-32 h-32 mx-auto mb-6 rounded-full overflow-hidden border-2 group-hover:scale-110 transition-transform"
                style={{ borderColor: "var(--color-greenwave-primary-light)" }}
              >
                <div className="w-full h-full bg-greenwave-accent-light flex items-center justify-center">
                  <img src={member.imageUrl} alt="Avatar Member" />
                </div>
              </div>
              <h4 className="text-xl font-semibold text-text-main-dark mb-2">
                {member.name}
              </h4>
              <p className="text-text-muted-dark">{member.role}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};
