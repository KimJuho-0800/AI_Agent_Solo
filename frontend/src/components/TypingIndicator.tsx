/**
 * 챗봇 타이핑 인디케이터
 */

import React from 'react';

const TypingIndicator: React.FC = () => {
  return (
    <div style={{
      display: 'flex',
      gap: '4px',
      padding: '12px 16px',
      backgroundColor: '#1e293b',
      border: '1px solid #334155',
      borderRadius: '12px',
      borderBottomLeftRadius: '4px',
      maxWidth: 'fit-content',
    }}>
      <div className="typing-dot" style={{ animationDelay: '0s' }} />
      <div className="typing-dot" style={{ animationDelay: '0.2s' }} />
      <div className="typing-dot" style={{ animationDelay: '0.4s' }} />
    </div>
  );
};

export default TypingIndicator;