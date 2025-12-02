import React from 'react';

export const Footer: React.FC = () => {
  return (
    <footer
      className="py-12 px-4"
      style={{ background: 'var(--color-greenwave-accent-dark)' }}
    >
      <div className="max-w-6xl mx-auto">
        <div className="flex flex-col md:flex-row justify-between items-center gap-8">
          <div className="text-center md:text-left">
            <h3 className="text-2xl font-bold text-greenwave-primary-light mb-2">
              GreenWave
            </h3>
            <p className="text-text-muted-dark">© 2025 GreenWave Project.</p>
          </div>

          <div className="flex gap-6">
            <button className="text-text-muted-dark hover:text-greenwave-primary-light transition-colors">
              Source Code
            </button>
            <button className="text-text-muted-dark hover:text-greenwave-primary-light transition-colors">
              Data Models Documentation
            </button>
            <button className="text-text-muted-dark hover:text-greenwave-primary-light transition-colors">
              Contact
            </button>
          </div>
        </div>
      </div>
    </footer>
  );
};