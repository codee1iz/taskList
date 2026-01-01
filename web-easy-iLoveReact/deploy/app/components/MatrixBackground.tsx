'use client';

import { useEffect, useRef } from 'react';

export default function MatrixBackground() {
  const containerRef = useRef<HTMLDivElement>(null);
  const chars = '01アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン';
  const numbers = '0123456789';

  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;

    const createMatrixChar = () => {
      const char = document.createElement('div');
      char.className = 'matrix-char';
      char.textContent = Math.random() > 0.5 
        ? chars[Math.floor(Math.random() * chars.length)]
        : numbers[Math.floor(Math.random() * numbers.length)];
      char.style.left = Math.random() * 100 + '%';
      char.style.animationDuration = (Math.random() * 3 + 2) + 's';
      char.style.animationDelay = Math.random() * 2 + 's';
      container.appendChild(char);

      setTimeout(() => {
        char.remove();
      }, 5000);
    };

    const interval = setInterval(createMatrixChar, 100);
    return () => clearInterval(interval);
  }, []);

  return <div className="matrix-bg" ref={containerRef} />;
}

