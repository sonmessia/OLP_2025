// Copyright (c) 2025 Green Wave Team
//
// This software is released under the MIT License.
// https://opensource.org/licenses/MIT

import type { ReactNode } from "react";
import clsx from "clsx";
import Heading from "@theme/Heading";
import styles from "./styles.module.css";

type FeatureItem = {
  title: string;
  Svg?: React.ComponentType<React.ComponentProps<"svg">>;
  Image?: string;
  description: ReactNode;
};

const FeatureList: FeatureItem[] = [
  {
    title: "Open Source",
    Svg: require("@site/static/img/Open_Source_Initiative.svg").default,
    description: (
      <>
        Built on open source standards, ensuring transparency, collaboration,
        and unlimited scalability for the community.
      </>
    ),
  },
  {
    title: "NGSI-LD Standard",
    Image: require("@site/static/img/ngsi-ld.png").default,
    description: (
      <>
        Utilizes the NGSI-LD data standard for open data, enabling
        standardization and semantic data linking between IoT and Smart City
        systems.
      </>
    ),
  },
  {
    title: "Intelligent Traffic System",
    Image: require("@site/static/img/its.jpg").default,
    description: (
      <>
        Intelligent traffic management system applying AI to analyze, forecast,
        and optimize vehicle flow in real-time.
      </>
    ),
  },
];

function Feature({ title, Svg, Image, description }: FeatureItem) {
  return (
    <div className={clsx("col col--4")}>
      <div className={styles.featureCard}>
        <div className="text--center">
          {Svg ? (
            <Svg className={styles.featureSvg} role="img" />
          ) : (
            <img
              src={Image}
              className={styles.featureSvg}
              alt={title}
              style={{ objectFit: "contain" }}
            />
          )}
        </div>
        <div className="text--center padding-horiz--md">
          <Heading as="h3">{title}</Heading>
          <p>{description}</p>
        </div>
      </div>
    </div>
  );
}

export default function HomepageFeatures(): ReactNode {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="text--center">
          <Heading as="h2" style={{ marginBottom: "3rem" }}>
            Tính Năng Nổi Bật
          </Heading>
        </div>
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}
