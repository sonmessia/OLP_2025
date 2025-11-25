import React, { useState, useEffect } from "react";
import { ArrowRight, Github } from "lucide-react";
import ParticleBackground from "./ParticleBackground";
import ThreeDVisualization from "./ThreeDVisualization";

export const HeroSection: React.FC = () => {
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
          className="glass-card p-12 rounded-3xl"
          style={{
            background: "rgba(255, 255, 255, 0.05)",
            backdropFilter: "blur(20px)",
            border: "1px solid rgba(255, 255, 255, 0.1)",
            boxShadow: "0 25px 50px -12px rgba(0, 0, 0, 0.5)",
          }}
        >
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            {/* Left Side - Text Content */}
            <div className="text-center lg:text-left">
              <h1 className="text-5xl md:text-7xl font-bold mb-6 bg-gradient-to-r from-greenwave-primary-light to-traffic-info bg-clip-text text-transparent">
                GreenWave
              </h1>
              <h2 className="text-2xl md:text-4xl font-semibold mb-4 text-text-main-dark">
                Hệ Thống Điều Phối Giao Thông Thích Ứng Đa Mục Tiêu
              </h2>
              <p className="text-lg md:text-xl text-text-muted-dark mb-8 max-w-2xl leading-relaxed">
                Không chỉ giải quyết kẹt xe. Chúng tôi giải cứu lá phổi thành phố
                bằng AI & Dữ liệu chuẩn hóa NGSI-LD.
              </p>

              <div className="flex flex-col sm:flex-row gap-4 justify-center lg:justify-start items-center">
                <button
                  onClick={handleGetStarted}
                  onMouseEnter={() => setIsHovered(true)}
                  onMouseLeave={() => setIsHovered(false)}
                  className="group relative px-8 py-4 rounded-full font-semibold text-lg transition-all duration-300 transform hover:scale-105"
                  style={{
                    background:
                      "linear-gradient(135deg, var(--color-greenwave-primary-light) 0%, var(--color-traffic-info) 100%)",
                    boxShadow: "0 10px 30px -10px rgba(16, 124, 65, 0.5)",
                  }}
                >
                  <span className="relative z-10 text-white flex items-center gap-2">
                    Get Started
                    <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
                  </span>
                  <div
                    className="absolute inset-0 rounded-full opacity-0 group-hover:opacity-100 transition-opacity duration-300"
                    style={{ boxShadow: "0 0 30px rgba(16, 124, 65, 0.6)" }}
                  />
                </button>

                <button
                  onClick={handleViewGithub}
                  className="px-8 py-4 rounded-full font-semibold text-lg border-2 transition-all duration-300 hover:bg-white hover:bg-opacity-10 flex items-center gap-2"
                  style={{
                    borderColor: "rgba(255, 255, 255, 0.2)",
                    color: "var(--color-text-main-dark)",
                  }}
                >
                  <Github className="w-5 h-5" />
                  View Github
                </button>
              </div>
            </div>

            {/* Right Side - Image with Animation */}
            <div className="relative">
              <div className="pollution-container relative w-full h-64 md:h-80 rounded-2xl overflow-hidden">
                {/* Pollution Smoke Effect */}
                <div
                  className={`pollution-smoke absolute inset-0 transition-all duration-1000 ${
                    isHovered ? 'opacity-10 scale-95' : 'opacity-60'
                  }`}
                />

                {/* Animated Cars */}
                <div className="absolute bottom-8 left-0 w-12 h-6 bg-red-600 rounded car-animation" />
                <div className="absolute bottom-12 right-0 w-12 h-6 bg-blue-600 rounded car-animation-reverse" />
                <div className="absolute bottom-4 left-1/4 w-10 h-5 bg-yellow-500 rounded car-animation-delay" />

                {/* Green Wave Effect */}
                <div
                  className={`green-wave absolute bottom-0 left-0 right-0 transition-all duration-1000 ${
                    isHovered ? 'h-full translate-y-0' : 'h-0 translate-y-full'
                  }`}
                >
                  {isHovered && (
                    <div
                      key="wave-sweep"
                      className="absolute top-0 left-0 w-full h-full wave-sweep"
                      style={{
                        background: 'linear-gradient(90deg, transparent 0%, rgba(16, 124, 65, 0.8) 45%, rgba(59, 130, 246, 0.6) 50%, rgba(16, 124, 65, 0.8) 55%, transparent 100%)'
                      }}
                    />
                  )}
                </div>

                {/* Background Image */}
                <img
                  src="https://maas-log-prod.cn-wlcb.ufileos.com/anthropic/da42b125-51d7-449a-a579-0b92c68dc4d6/3f5820511fd6f224b15dbbf501837c33.png?UCloudPublicKey=TOKEN_e15ba47a-d098-4fbd-9afc-a0dcf0e4e621&Expires=1764093147&Signature=CU5Tz6hRTjtkcEFffYnQbrgMBv8="
                  alt="GreenWave Traffic System"
                  className={`w-full h-full object-cover rounded-2xl transition-all duration-1000 ${
                    isHovered ? 'brightness-110 contrast-125 saturate-130 scale-102' : ''
                  }`}
                  style={{ filter: 'brightness(0.8) contrast(1.1)' }}
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
