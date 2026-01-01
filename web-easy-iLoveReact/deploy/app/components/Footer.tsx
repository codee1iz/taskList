'use client';

import { useState, useEffect } from 'react';

export default function Footer() {
  const [timestamp, setTimestamp] = useState('');

  useEffect(() => {
    const updateTimestamp = () => {
      const now = new Date();
      const dateStr = now.toLocaleString('ru-RU', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
      });
      setTimestamp(dateStr);
    };

    updateTimestamp();
    const interval = setInterval(updateTimestamp, 1000);
    return () => clearInterval(interval);
  }, []);

  return (
    <footer>
      <p>[ SYSTEM STATUS: ONLINE ]</p>
      <p>[ LAST UPDATE: <span>{timestamp}</span> ]</p>
      <p style={{ marginTop: '10px', fontSize: '0.8rem', opacity: 0.7 }}>
        Сайт для жесткого пенетста 
      </p>
    </footer>
  );
}

