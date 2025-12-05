import React from 'react';
import { Activity, Globe, Shield } from 'lucide-react';

const features = [
  {
    icon: Activity,
    title: 'Digital Twin',
    description: 'Tích hợp hiển thị thông tin giao thông chính xác từng giây thực tế, tạo ra bản sao số của đô thị.',
    color: 'var(--color-traffic-info)',
    bgColor: 'rgba(59, 130, 246, 0.2)'
  },
  {
    icon: Globe,
    title: 'Global Standard',
    description: 'Tuân thủ tuyệt đối NGSI-LD, FIWARE Data Models & SOSA/SSN, đảm bảo tương thích toàn cầu.',
    color: 'var(--color-greenwave-primary-light)',
    bgColor: 'rgba(16, 124, 65, 0.2)'
  },
  {
    icon: Shield,
    title: 'Dynamic Response',
    description: 'Tự động phát hiện và xử lý khi PM2.5 vượt ngưỡng an toàn, chuyển màu cảnh báo tức thì.',
    color: 'var(--color-traffic-red)',
    bgColor: 'rgba(217, 35, 47, 0.2)'
  }
];

export const KeyFeaturesSection: React.FC = () => {
  return (
    <section className="py-20 px-4 relative">
      <div className="max-w-6xl mx-auto">
        <h3 className="text-3xl md:text-4xl font-bold text-center mb-16 text-text-main-dark">
          Tính năng Nổi bật
        </h3>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {features.map((feature, index) => (
            <div
              key={index}
              className="glass-card p-8 rounded-2xl group hover:scale-105 transition-all duration-300"
              style={{
                background: 'rgba(255, 255, 255, 0.03)',
                backdropFilter: 'blur(10px)',
                border: '1px solid rgba(255, 255, 255, 0.1)',
              }}
            >
              <div
                className="w-16 h-16 mx-auto mb-6 rounded-full flex items-center justify-center group-hover:scale-110 transition-transform"
                style={{ background: feature.bgColor }}
              >
                <feature.icon
                  className="w-8 h-8"
                  style={{ color: feature.color }}
                />
              </div>
              <h4 className="text-xl font-semibold text-center mb-4 text-text-main-dark">
                {feature.title}
              </h4>
              <p className="text-text-muted-dark text-center leading-relaxed">
                {feature.description}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};