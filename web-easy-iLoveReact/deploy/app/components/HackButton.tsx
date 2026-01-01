'use client';

import { useState } from 'react';

export default function HackButton() {
  const [buttonState, setButtonState] = useState<'idle' | 'hacking' | 'denied'>('idle');

  const handleClick = () => {
    setButtonState('hacking');
    
    setTimeout(() => {
      setButtonState('denied');
      
      setTimeout(() => {
        setButtonState('idle');
      }, 3000);
    }, 2000);
  };

  const getButtonText = () => {
    switch (buttonState) {
      case 'hacking':
        return 'HACKING IN PROGRESS...';
      case 'denied':
        return 'ACCESS DENIED (ЗАПЕНТЕЩЕН!!!)';
      default:
        return 'INITIATE HACK SEQUENCE';
    }
  };

  const getButtonStyle = () => {
    if (buttonState === 'denied') {
      return {
        borderColor: '#ff0000',
        color: '#ff0000',
        boxShadow: '0 0 20px rgba(255, 0, 0, 0.5)'
      };
    }
    return {};
  };

  return (
    <div style={{ textAlign: 'center' }}>
      <button
        className="hack-button"
        onClick={handleClick}
        disabled={buttonState !== 'idle'}
        style={getButtonStyle()}
      >
        {getButtonText()}
      </button>
    </div>
  );
}

