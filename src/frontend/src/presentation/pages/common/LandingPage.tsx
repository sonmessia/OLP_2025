// Copyright (c) 2025 Green Wave Team
// 
// This software is released under the MIT License.
// https://opensource.org/licenses/MIT

import React from "react";
import { HeroSection } from "../../components/feature/landing/HeroSection";
import { ProblemSection } from "../../components/feature/landing/ProblemSection";
import { SolutionSection } from "../../components/feature/landing/SolutionSection";
import { ArchitectureSection } from "../../components/feature/landing/ArchitectureSection";
import { KeyFeaturesSection } from "../../components/feature/landing/KeyFeaturesSection";
import { TeamSection } from "../../components/feature/landing/TeamSection";
import { Footer } from "../../components/feature/landing/Footer";

const LandingPage: React.FC = () => {
  return (
    <div className="min-h-screen bg-greenwave-accent-dark text-text-main-dark overflow-x-hidden">
      <HeroSection />
      <ProblemSection />
      <SolutionSection />
      <ArchitectureSection />
      <KeyFeaturesSection />
      <TeamSection />
      <Footer />
    </div>
  );
};

export default LandingPage;
