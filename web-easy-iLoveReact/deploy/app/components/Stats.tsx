'use client';

import { useState, useEffect } from 'react';

interface StatItemProps {
  id: string;
  endValue: number;
  label: string;
}

function StatItem({ id, endValue, label }: StatItemProps) {
  const [value, setValue] = useState(0);

  useEffect(() => {
    const duration = 2000;
    const startTime = Date.now();
    
    const animate = () => {
      const now = Date.now();
      const progress = Math.min((now - startTime) / duration, 1);
      const currentValue = Math.floor(progress * endValue);
      setValue(currentValue);
      
      if (progress < 1) {
        requestAnimationFrame(animate);
      }
    };
    
    const timeout = setTimeout(() => {
      requestAnimationFrame(animate);
    }, 500);
    
    return () => clearTimeout(timeout);
  }, [endValue]);

  return (
    <div className="stat-item">
      <span className="stat-number">{value.toLocaleString()}</span>
      <div className="stat-label">{label}</div>
    </div>
  );
}

export default function Stats() {
  return (
    <div className="stats">
      <StatItem id="hacks" endValue={1337} label="HACKS EXECUTED" />
      <StatItem id="systems" endValue={42} label="SYSTEMS COMPROMISED" />
      <StatItem id="data" endValue={999} label="TERABYTES STOLEN" />
    </div>
  );
}

