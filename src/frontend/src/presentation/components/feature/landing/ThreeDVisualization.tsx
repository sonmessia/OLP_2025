// Copyright (c) 2025 Green Wave Team
// 
// This software is released under the MIT License.
// https://opensource.org/licenses/MIT

import React, { useEffect, useRef } from 'react';

const ThreeDVisualization: React.FC = () => {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;

    let rotation = 0;

    const animate = () => {
      rotation += 0.01;

      const particles = container.querySelectorAll('.particle-3d');
      particles.forEach((particle, index) => {
        const angle = (index / particles.length) * Math.PI * 2 + rotation;
        const radius = 120;
        const x = Math.cos(angle) * radius;
        const z = Math.sin(angle) * radius;
        const y = Math.sin(angle * 2) * 30;

        const element = particle as HTMLElement;
        element.style.transform = `translate3d(${x}px, ${y}px, ${z}px)`;
        element.style.opacity = `${0.6 + (z + radius) / (radius * 2) * 0.4}`;
        element.style.left = '50%';
        element.style.top = '50%';
        element.style.marginLeft = '-8px';
        element.style.marginTop = '-8px';
      });

      requestAnimationFrame(animate);
    };

    animate();
  }, []);

  return (
    <div ref={containerRef} className="relative w-64 h-64 mx-auto">
      <div className="absolute inset-0 rounded-full border-2 opacity-20"
           style={{ borderColor: 'var(--color-greenwave-primary-light)' }}
      />
      {[...Array(12)].map((_, i) => (
        <div
          key={i}
          className="particle-3d absolute w-4 h-4 rounded-full transition-opacity duration-300"
          style={{
            background: i % 2 === 0 ? 'var(--color-greenwave-primary-light)' : 'var(--color-traffic-info)',
            boxShadow: `0 0 ${10 + i * 2}px ${i % 2 === 0 ? 'var(--color-greenwave-primary-light)' : 'var(--color-traffic-info)'}`,
            transformStyle: 'preserve-3d',
            willChange: 'transform, opacity'
          }}
        />
      ))}

      {/* Central core */}
      <div
        className="absolute top-1/2 left-1/2 w-8 h-8 rounded-full -translate-x-1/2 -translate-y-1/2"
        style={{
          background: 'radial-gradient(circle, var(--color-greenwave-primary-light) 0%, transparent 70%)',
          boxShadow: '0 0 30px var(--color-greenwave-primary-light)',
          animation: 'pulse-core 2s ease-in-out infinite'
        }}
      />

    </div>
  );
};

export default ThreeDVisualization;