import React, { useState, useEffect } from "react";
import { ArrowRight, Github, BookOpen, Car, Zap } from "lucide-react";
import { useTranslation } from "react-i18next";
import ParticleBackground from "./ParticleBackground";
import ThreeDVisualization from "./ThreeDVisualization";
import LandingImage from "../../../../assets/landing.png";

export const HeroSection: React.FC = () => {
  const { t } = useTranslation("landing");
  const [scrollY, setScrollY] = useState(0);
  const [isHovered, setIsHovered] = useState(false);

  useEffect(() => {
    const handleScroll = () => setScrollY(window.scrollY);
    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  const handleGetStarted = () => {
    window.location.href = "/";
  };

  const handleViewGithub = () => {
    window.open("https://github.com/sonmessia/GreenWave.git", "_blank");
  };

  return (
    <section className="relative min-h-screen flex items-center justify-center px-4">
      {/* Particle Background */}
      <ParticleBackground />

      {/* Animated Background */}
      <div className="absolute inset-0 overflow-hidden">
        <div
          className="absolute inset-0 opacity-20"
          style={{
            background: `linear-gradient(45deg, var(--color-greenwave-primary-light) 0%, var(--color-traffic-info) 100%)`,
            transform: `translateY(${scrollY * 0.5}px) scale(1.1)`,
            filter: "blur(100px)",
          }}
        />
        <div
          className="absolute top-1/4 left-1/4 w-96 h-96 rounded-full float-animation"
          style={{
            background:
              "radial-gradient(circle, var(--color-greenwave-primary-light) 0%, transparent 70%)",
            opacity: 0.3,
          }}
        />
        <div
          className="absolute bottom-1/4 right-1/4 w-80 h-80 rounded-full float-animation-reverse"
          style={{
            background:
              "radial-gradient(circle, var(--color-traffic-info) 0%, transparent 70%)",
            opacity: 0.3,
          }}
        />
      </div>

      {/* Glass Card */}
      <div className="relative z-10 max-w-6xl mx-auto">
        <div
          className="glass-card p-8 rounded-3xl"
          style={{
            background: "rgba(255, 255, 255, 0.05)",
            backdropFilter: "blur(20px)",
            border: "1px solid rgba(255, 255, 255, 0.1)",
            boxShadow: "0 25px 50px -12px rgba(0, 0, 0, 0.5)",
          }}
        >
          <div className="grid lg:grid-cols-2 gap-8 items-center">
            {/* Left Side - Text Content */}
            <div className="text-center lg:text-left">
              <div className="flex items-center">
                <img
                  src="/logo.png"
                  alt="GreenWave Logo"
                  className="w-24 h-24 object-contain mr-2"
                />
                <h1 className="text-5xl md:text-7xl font-bold mb-6 bg-gradient-to-r from-greenwave-primary-light to-traffic-info bg-clip-text text-transparent">
                  {t("title")}
                </h1>
              </div>
              <h2 className="text-2xl md:text-4xl font-semibold mb-4 text-text-main-dark">
                {t("subtitle")}
              </h2>
              <p className="text-lg md:text-xl text-text-muted-dark mb-8 max-w-2xl leading-relaxed">
                {t("description")}
              </p>

              <div className="flex flex-wrap gap-4 justify-center lg:justify-start items-center w-full">
                <button
                  onClick={handleGetStarted}
                  onMouseEnter={() => setIsHovered(true)}
                  onMouseLeave={() => setIsHovered(false)}
                  className="group relative px-6 py-3 sm:px-8 sm:py-4 rounded-full font-semibold text-base sm:text-lg transition-all duration-300 transform hover:scale-105 whitespace-nowrap"
                  style={{
                    background:
                      "linear-gradient(135deg, var(--color-greenwave-primary-light) 0%, var(--color-traffic-info) 100%)",
                    boxShadow: "0 10px 30px -10px rgba(16, 124, 65, 0.5)",
                  }}
                >
                  <span className="relative z-10 text-white flex items-center gap-2">
                    {t("getStarted")}
                    <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
                  </span>
                  <div
                    className="absolute inset-0 rounded-full opacity-0 group-hover:opacity-100 transition-opacity duration-300"
                    style={{ boxShadow: "0 0 30px rgba(16, 124, 65, 0.6)" }}
                  />
                </button>

                <button
                  onClick={handleViewGithub}
                  className="px-6 py-3 sm:px-8 sm:py-4 rounded-full font-semibold text-base sm:text-lg border-2 transition-all duration-300 hover:bg-white hover:bg-opacity-10 flex items-center gap-2 whitespace-nowrap"
                  style={{
                    borderColor: "rgba(255, 255, 255, 0.2)",
                    color: "var(--color-text-main-dark)",
                  }}
                >
                  <Github className="w-5 h-5" />
                  {t("viewGithub")}
                </button>

                <button
                  onClick={() =>
                    window.open("http://localhost:3000/", "_blank")
                  }
                  className="px-6 py-3 sm:px-8 sm:py-4 rounded-full font-semibold text-base sm:text-lg border-2 transition-all duration-300 hover:bg-white hover:bg-opacity-10 flex items-center gap-2 whitespace-nowrap"
                  style={{
                    borderColor: "rgba(255, 255, 255, 0.2)",
                    color: "var(--color-text-main-dark)",
                  }}
                >
                  <BookOpen className="w-5 h-5" />
                  {t("documentation")}
                </button>
              </div>
            </div>

            {/* Right Side - Image with Animation */}
            <div className="relative">
              <div className="pollution-container relative w-full h-64 md:h-80 rounded-2xl overflow-hidden">
                {/* Pollution Smoke Effect */}
                <div
                  className={`pollution-smoke absolute inset-0 transition-all duration-1000 ${
                    isHovered ? "opacity-10 scale-95" : "opacity-60"
                  }`}
                />

                {/* Animated Cars Chase Scene */}
                {/* Polluting Car (The Villain) */}
                <div className="absolute bottom-2 left-0 car-animation z-20">
                  <div className="relative">
                    <Car className="w-16 h-16 text-red-500 fill-current drop-shadow-lg" />
                    {/* Heavy Smoke */}
                    <div className="absolute -top-4 -left-2 w-6 h-6 bg-gray-600 rounded-full opacity-70 animate-ping" />
                    <div className="absolute -top-6 -left-4 w-8 h-8 bg-gray-500 rounded-full opacity-50 animate-pulse" />
                    <div className="absolute -top-2 -left-6 w-4 h-4 bg-gray-700 rounded-full opacity-60 animate-bounce" />
                  </div>
                </div>

                {/* GreenWave Team Car (The Hero) */}
                <div
                  className="absolute bottom-2 left-0 car-animation z-20"
                  style={{ animationDelay: "1.5s" }}
                >
                  <div className="relative">
                    <Car className="w-16 h-16 text-green-500 fill-current drop-shadow-[0_0_15px_rgba(16,185,129,0.8)]" />
                    {/* Clean Energy Aura */}
                    <div className="absolute inset-0 bg-green-400 rounded-full opacity-20 blur-md animate-pulse" />
                    <Zap className="absolute -top-6 right-4 w-8 h-8 text-yellow-400 animate-bounce drop-shadow-lg" />
                    {/* Cleaning Beam */}
                    <div className="absolute top-1/2 left-16 w-24 h-1 bg-gradient-to-r from-green-400 to-transparent opacity-50" />
                  </div>
                </div>

                {/* Background Traffic (Atmosphere) */}
                <div
                  className="absolute bottom-16 right-0 car-animation-reverse opacity-50"
                  style={{ animationDuration: "12s" }}
                >
                  <Car className="w-10 h-10 text-blue-400 fill-current transform scale-x-[-1]" />
                </div>

                {/* Green Wave Effect */}
                <div
                  className={`green-wave absolute bottom-0 left-0 right-0 transition-all duration-1000 ${
                    isHovered ? "h-full translate-y-0" : "h-0 translate-y-full"
                  }`}
                >
                  {isHovered && (
                    <div
                      key="wave-sweep"
                      className="absolute top-0 left-0 w-full h-full wave-sweep"
                      style={{
                        background:
                          "linear-gradient(90deg, transparent 0%, rgba(16, 124, 65, 0.8) 45%, rgba(59, 130, 246, 0.6) 50%, rgba(16, 124, 65, 0.8) 55%, transparent 100%)",
                      }}
                    />
                  )}
                </div>

                {/* Background Image */}
                <img
                  src={LandingImage}
                  alt="GreenWave Traffic System"
                  className={`w-full h-full object-cover rounded-2xl transition-all duration-1000 ${
                    isHovered
                      ? "brightness-110 contrast-125 saturate-130 scale-102"
                      : ""
                  }`}
                  style={{ filter: "brightness(0.8) contrast(1.1)" }}
                />
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* 3D Particle Visualization */}
      <div className="absolute right-10 top-1/2 -translate-y-1/2 hidden lg:block">
        <ThreeDVisualization />
      </div>
    </section>
  );
};
