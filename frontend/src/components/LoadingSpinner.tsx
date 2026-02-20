/**
 * 로딩 스피너 컴포넌트
 */

import React from 'react';

interface LoadingSpinnerProps {
  message?: string;
}

const LoadingSpinner: React.FC<LoadingSpinnerProps> = ({ 
  message = '처리 중...' 
}) => {
  return (
    <div className="loading-container">
      <div className="spinner"></div>
      {message && <p className="loading-text">{message}</p>}
    </div>
  );
};

export default LoadingSpinner;