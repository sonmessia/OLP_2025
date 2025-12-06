// Copyright (c) 2025 Green Wave Team
//
// This software is released under the MIT License.
// https://opensource.org/licenses/MIT

import type { ReactNode } from "react";
import Heading from "@theme/Heading";
import styles from "./styles.module.css";

type TechItem = {
  name: string;
  logo?: string;
  icon?: ReactNode;
};

const TechList: TechItem[] = [
  {
    name: "React",
    logo: require("@site/static/img/tech/react.png").default,
  },
  {
    name: "FastAPI",
    logo: require("@site/static/img/tech/fastapi.png").default,
  },
  {
    name: "MongoDB",
    logo: require("@site/static/img/tech/mongodb.png").default,
  },
  {
    name: "FIWARE",
    logo: require("@site/static/img/tech/fiware.png").default,
  },
  {
    name: "QuantumLeap",
    icon: (
      <svg
        xmlns="http://www.w3.org/2000/svg"
        width="64"
        height="64"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
      >
        <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z" />
        <polyline points="3.29 7 12 12 20.71 7" />
        <line x1="12" y1="22" x2="12" y2="12" />
      </svg>
    ),
  },
  {
    name: "CrateDB",
    logo: require("@site/static/img/tech/catedb.webp").default,
  },
  {
    name: "Context Broker",
    icon: (
      <svg
        xmlns="http://www.w3.org/2000/svg"
        width="64"
        height="64"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
      >
        <rect width="18" height="18" x="3" y="3" rx="2" />
        <path d="M7 7h10" />
        <path d="M7 12h10" />
        <path d="M7 17h10" />
      </svg>
    ),
  },
  {
    name: "AWS",
    logo: require("@site/static/img/tech/aws.png").default,
  },
];

function TechItem({ name, logo, icon }: TechItem) {
  return (
    <div className={styles.techItem}>
      <div className={styles.techLogo}>
        {logo ? (
          <img src={logo} alt={name} />
        ) : (
          <div className={styles.techIcon}>{icon}</div>
        )}
      </div>
      <span className={styles.techName}>{name}</span>
    </div>
  );
}

export default function TechFeatures(): ReactNode {
  return (
    <section className={styles.techSection}>
      <div className="container">
        <div className="text--center">
          <Heading as="h2" style={{ marginBottom: "3rem" }}>
            Công Nghệ Sử Dụng
          </Heading>
        </div>
      </div>

      <div className={styles.marqueeContainer}>
        <div className={styles.marquee}>
          <div className={styles.marqueeContent}>
            {TechList.map((tech, idx) => (
              <TechItem key={`tech-1-${idx}`} {...tech} />
            ))}
          </div>
          {/* Duplicate for seamless loop */}
          <div className={styles.marqueeContent} aria-hidden="true">
            {TechList.map((tech, idx) => (
              <TechItem key={`tech-2-${idx}`} {...tech} />
            ))}
          </div>
          {/* Third copy for extra smoothness */}
          <div className={styles.marqueeContent} aria-hidden="true">
            {TechList.map((tech, idx) => (
              <TechItem key={`tech-3-${idx}`} {...tech} />
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
