// Copyright (c) 2025 Green Wave Team
//
// This software is released under the MIT License.
// https://opensource.org/licenses/MIT

import type { ReactNode } from "react";
import clsx from "clsx";
import Link from "@docusaurus/Link";
import useDocusaurusContext from "@docusaurus/useDocusaurusContext";
import Layout from "@theme/Layout";
import HomepageFeatures from "@site/src/components/HomepageFeatures";
import Heading from "@theme/Heading";

import styles from "./index.module.css";
import WhatIsFeatures from "../components/WhatIsFeatures";
import OrganizationFeatures from "@site/src/components/OrganizationFeatures";
import TechFeatures from "@site/src/components/TechFeatures";

function HomepageHeader() {
  const { siteConfig } = useDocusaurusContext();
  return (
    <header className={clsx("hero hero--primary", styles.heroBanner)}>
      <div className="container">
        <div
          style={{
            height: "250px",
            maxWidth: "600px",
            aspectRatio: "16/9",
            margin: "0 auto 1rem",
            overflow: "hidden",
            borderRadius: "12px",
          }}
        >
          <video
            src="video/logo_video.mp4"
            autoPlay
            loop
            muted
            playsInline
            style={{
              width: "100%",
              height: "100%",
              objectFit: "cover",
              objectPosition: "center",
            }}
          />
        </div>
        <Heading as="h1" className="hero__title">
          {siteConfig.title}
        </Heading>
        <p className="hero__subtitle">{siteConfig.tagline}</p>
        <div className={styles.ctaButtons}>
          <Link
            className={clsx(
              "button button--primary button--lg",
              styles.primaryButton
            )}
            to="/docs/intro"
          >
            Read Documentation
          </Link>

          <Link
            className="button button--secondary button--lg"
            to="/docs/installation"
          >
            Installation Guide
          </Link>
        </div>
      </div>
    </header>
  );
}

export default function Home(): ReactNode {
  const { siteConfig } = useDocusaurusContext();
  return (
    <Layout
      title={`Hello from ${siteConfig.title}`}
      description="Description will go into a meta tag in <head />"
    >
      <HomepageHeader />
      <main>
        <HomepageFeatures />
        <WhatIsFeatures />
        <TechFeatures />
        <OrganizationFeatures />
      </main>
    </Layout>
  );
}
