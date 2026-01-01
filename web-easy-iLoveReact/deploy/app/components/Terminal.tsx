'use client';

import { useState, useEffect } from 'react';

export default function Terminal() {
  const [currentLine, setCurrentLine] = useState(0);
  const terminalLines = [
    'Scanning for vulnerabilities...',
    'Injecting payload...',
    'Bypassing firewall...',
    'Accessing database...',
    'Extracting credentials...',
    'Covering tracks...',
    'Mission accomplished!'
  ];

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentLine((prev) => (prev + 1) % terminalLines.length);
    }, 2000);
    return () => clearInterval(interval);
  }, [terminalLines.length]);

  return (
    <div className="terminal">
      <div className="terminal-header">
        <div className="terminal-dot"></div>
        <div className="terminal-dot"></div>
        <div className="terminal-dot"></div>
        <span style={{ marginLeft: '10px', color: '#00ff00' }}>e1iz4vr@terminal:~#</span>
      </div>
      <div className="terminal-line">Initializing hack sequence...</div>
      <div className="terminal-line">Bypassing security protocols...</div>
      <div className="terminal-line">Accessing mainframe... <span className="cursor"></span></div>
      <div className="terminal-line">{terminalLines[currentLine]}</div>
    </div>
  );
}

