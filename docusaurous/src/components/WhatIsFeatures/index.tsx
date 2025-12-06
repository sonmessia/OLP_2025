// Copyright (c) 2025 Green Wave Team
//
// This software is released under the MIT License.
// https://opensource.org/licenses/MIT

import type { ReactNode } from "react";
import Heading from "@theme/Heading";
import styles from "./styles.module.css";

export default function WhatIsFeatures(): ReactNode {
  return (
    <section className={styles.features}>
      <div className="container">
        {/* Hero Section */}
        <div className={styles.heroSection}>
          <Heading as="h2" className={styles.sectionTitle}>
            What is GreenWave?
          </Heading>
          <p className={styles.sectionSubtitle}>
            An intelligent traffic signal control system that uses AI to
            simultaneously optimize traffic flow and minimize environmental
            impact.
          </p>
        </div>

        {/* Problem & Solution Section */}
        <div className={styles.problemSolution}>
          <div className="row">
            <div className="col col--6">
              <div className={styles.card}>
                <Heading as="h3" className={styles.cardTitle}>
                  ⚠️ The Problem
                </Heading>
                <p>
                  Current traffic control systems optimize for{" "}
                  <strong>traffic flow only</strong>, creating{" "}
                  <strong>pollution hotspots</strong> at intersections near
                  sensitive areas like schools and hospitals.
                </p>
                <p className={styles.highlight}>
                  They are completely "blind" to localized environmental impact.
                </p>
              </div>
            </div>
            <div className="col col--6">
              <div className={styles.card}>
                <Heading as="h3" className={styles.cardTitle}>
                  ✅ The Solution
                </Heading>
                <p>
                  <strong>GreenWave</strong> uses AI (Reinforcement Learning) to
                  make real-time trade-offs between:
                </p>
                <ul>
                  <li>
                    <strong>Traffic Goal:</strong> Minimize wait time & queue
                    length
                  </li>
                  <li>
                    <strong>Environment Goal:</strong> Minimize emissions & air
                    pollution
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
