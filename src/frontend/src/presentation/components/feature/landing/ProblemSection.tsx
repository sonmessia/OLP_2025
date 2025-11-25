import React from "react";

export const ProblemSection: React.FC = () => {
  return (
    <section className="py-20 px-4 relative">
      <div className="max-w-6xl mx-auto">
        <div className="grid lg:grid-cols-2 gap-12 items-center">
          {/* Left Side - Text */}
          <div className="space-y-6">
            <div
              className="glass-card p-8 rounded-2xl fractured-glass"
              style={{
                background: "rgba(255, 255, 255, 0.03)",
                backdropFilter: "blur(10px)",
                border: "1px solid rgba(255, 255, 255, 0.1)",
                position: "relative",
                overflow: "hidden",
              }}
            >
              <div className="absolute inset-0 opacity-10">
                <div className="absolute top-0 left-0 w-full h-px bg-gradient-to-r from-transparent via-traffic-red to-transparent" />
                <div className="absolute top-1/4 left-0 w-full h-px bg-gradient-to-r from-transparent via-traffic-red to-transparent" />
                <div className="absolute top-1/2 left-0 w-full h-px bg-gradient-to-r from-transparent via-traffic-red to-transparent" />
              </div>

              <h3 className="text-3xl md:text-4xl font-bold mb-4 text-text-main-dark relative z-10">
                Sự Tối Ưu Mù Quáng
                <span className="block text-lg font-normal text-text-muted-dark mt-2">
                  (Optimization Blindness)
                </span>
              </h3>

              <p className="text-text-muted-dark leading-relaxed relative z-10">
                Hiện trạng đèn giao thông gây ra các "Điểm nóng ô nhiễm"
                (Pollution Hotspots) do bắt xe dừng/chạy liên tục. Hệ thống tối
                ưu tốc độ đơn thuần đang tạo ra những "ốc đảo ô nhiễm" âm thầm
                giết chết sức khỏe cộng đồng.
              </p>
            </div>
          </div>

          {/* Right Side - Visual Chart */}
          <div
            className="glass-card p-8 rounded-2xl"
            style={{
              background: "rgba(255, 255, 255, 0.03)",
              backdropFilter: "blur(10px)",
              border: "1px solid rgba(255, 255, 255, 0.1)",
            }}
          >
            <h4 className="text-xl font-semibold mb-6 text-center text-text-main-dark">
              Hiện trạng Tối ưu Hướng tốc độ
            </h4>

            <div className="space-y-6">
              <div className="space-y-2">
                <div className="flex justify-between items-center">
                  <span className="text-text-muted-dark">Tốc độ xe</span>
                  <span className="text-greenwave-primary-light font-semibold">
                    Cao
                  </span>
                </div>
                <div className="h-8 bg-greenwave-accent-dark rounded-full overflow-hidden">
                  <div
                    className="h-full rounded-full transition-all duration-1000"
                    style={{
                      width: "85%",
                      background: "var(--color-traffic-info)",
                      boxShadow: "0 0 20px rgba(59, 130, 246, 0.5)",
                    }}
                  />
                </div>
              </div>

              <div className="space-y-2">
                <div className="flex justify-between items-center">
                  <span className="text-text-muted-dark">Sức khỏe phổi</span>
                  <span className="text-traffic-red font-semibold">
                    Nguy cấp
                  </span>
                </div>
                <div className="h-8 bg-greenwave-accent-dark rounded-full overflow-hidden">
                  <div
                    className="h-full rounded-full transition-all duration-1000"
                    style={{
                      width: "15%",
                      background: "var(--color-traffic-red)",
                      boxShadow: "0 0 20px rgba(217, 35, 47, 0.5)",
                    }}
                  />
                </div>
              </div>

              <div
                className="mt-6 p-4 rounded-lg"
                style={{ background: "rgba(217, 35, 47, 0.1)" }}
              >
                <p className="text-sm text-traffic-red text-center">
                  ⚠️ PM2.5 vượt ngưỡng an toàn 300% tại khu vực trường học
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};
