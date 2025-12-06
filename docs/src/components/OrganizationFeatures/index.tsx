import type { ReactNode } from "react";
import clsx from "clsx";
import Heading from "@theme/Heading";
import Link from "@docusaurus/Link";
import styles from "./styles.module.css";

type FeatureItem = {
  title: string;
  Image: string;
  description: ReactNode;
  url: string;
};

const FeatureList: FeatureItem[] = [
  {
    title: "HUTECH",
    Image: require("@site/static/img/organization/hutech_logo.png").default,
    description: <>Ho Chi Minh City University of Technology</>,
    url: "https://www.hutech.edu.vn/",
  },
  {
    title: "FOSSA",
    Image: require("@site/static/img/organization/fossa_log.png").default,
    description: <>Free and Open Source Software Association</>,
    url: "https://vfossa.vn/",
  },
  {
    title: "OLP",
    Image: require("@site/static/img/organization/olp_logo.jpg").default,
    description: <>Vietnam Informatics Olympiad</>,
    url: "https://www.olp.vn/",
  },
];

function Feature({ title, Image, description, url }: FeatureItem) {
  return (
    <div className={clsx("col col--4")}>
      <Link
        href={url}
        className={styles.featureLink}
        target="_blank"
        rel="noopener noreferrer"
      >
        <div className={styles.featureCard}>
          <div className="text--center">
            <img
              src={Image}
              className={styles.featureSvg}
              alt={title}
              style={{ objectFit: "contain" }}
            />
          </div>
          <div className="text--center padding-horiz--md">
            <Heading as="h3">{title}</Heading>
            <p>{description}</p>
          </div>
        </div>
      </Link>
    </div>
  );
}

export default function OrganizationFeatures(): ReactNode {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="text--center">
          <Heading as="h1" style={{ marginBottom: "2rem" }}>
            Đơn Vị Tổ Chức
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
