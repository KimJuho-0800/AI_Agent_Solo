/**
 * 분석 진행 상태 표시 컴포넌트
 */

import React, { useState, useEffect } from 'react';

interface AnalysisProgressProps {
  isAnalyzing: boolean;
}

const AnalysisProgress: React.FC<AnalysisProgressProps> = ({ isAnalyzing }) => {
  const [currentStep, setCurrentStep] = useState(0);
  const [progress, setProgress] = useState(0);

  const steps = [
    { icon: '📊', label: 'KPI 데이터 조회', duration: 2000 },
    { icon: '🔍', label: '컨텍스트 수집', duration: 3000 },
    { icon: '🤖', label: 'AI 근본 원인 분석', duration: 25000 },
    { icon: '📝', label: '리포트 생성', duration: 15000 },
    { icon: '💾', label: 'RAG 저장', duration: 2000 },
  ];

  useEffect(() => {
    if (!isAnalyzing) {
      setCurrentStep(0);
      setProgress(0);
      return;
    }

    let stepIndex = 0;
    let accumulatedTime = 0;
    const totalDuration = steps.reduce((sum, step) => sum + step.duration, 0);

    const timer = setInterval(() => {
      accumulatedTime += 100;
      const newProgress = Math.min((accumulatedTime / totalDuration) * 100, 100);
      setProgress(newProgress);

      // 다음 단계로 이동
      let stepDuration = 0;
      for (let i = 0; i <= stepIndex; i++) {
        stepDuration += steps[i].duration;
      }

      if (accumulatedTime > stepDuration && stepIndex < steps.length - 1) {
        stepIndex++;
        setCurrentStep(stepIndex);
      }

      if (accumulatedTime >= totalDuration) {
        clearInterval(timer);
      }
    }, 100);

    return () => clearInterval(timer);
  }, [isAnalyzing]);

  if (!isAnalyzing) return null;

  return (
    <div className="card">
      <div className="card-body">
        {/* 진행률 바 */}
        <div style={{ marginBottom: '24px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
            <span style={{ fontSize: '14px', fontWeight: 600, color: '#e2e8f0' }}>
              분석 진행 중...
            </span>
            <span style={{ fontSize: '14px', fontWeight: 600, color: '#60a5fa' }}>
              {Math.round(progress)}%
            </span>
          </div>
          <div style={{
            width: '100%',
            height: '8px',
            backgroundColor: '#1e293b',
            borderRadius: '4px',
            overflow: 'hidden',
            border: '1px solid #334155',
          }}>
            <div style={{
              width: `${progress}%`,
              height: '100%',
              background: 'linear-gradient(90deg, #2563eb 0%, #60a5fa 100%)',
              transition: 'width 0.3s ease',
              boxShadow: '0 0 10px rgba(96, 165, 250, 0.5)',
            }} />
          </div>
        </div>

        {/* 단계별 진행 상황 */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
          {steps.map((step, index) => {
            const isCompleted = index < currentStep;
            const isCurrent = index === currentStep;
            const isPending = index > currentStep;

            return (
              <div
                key={index}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '12px',
                  padding: '12px',
                  backgroundColor: isCurrent ? 'rgba(37, 99, 235, 0.1)' : 'transparent',
                  border: `1px solid ${isCurrent ? '#2563eb' : '#334155'}`,
                  borderRadius: '8px',
                  transition: 'all 0.3s',
                }}
              >
                {/* 아이콘 */}
                <div style={{
                  width: '40px',
                  height: '40px',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontSize: '20px',
                  backgroundColor: isCompleted ? '#1e3a8a' : isCurrent ? '#1e293b' : '#0f172a',
                  border: `2px solid ${isCompleted ? '#2563eb' : isCurrent ? '#60a5fa' : '#334155'}`,
                  borderRadius: '50%',
                  flexShrink: 0,
                }}>
                  {isCompleted ? '✓' : step.icon}
                </div>

                {/* 라벨 */}
                <div style={{ flex: 1 }}>
                  <div style={{
                    fontSize: '14px',
                    fontWeight: 600,
                    color: isCompleted ? '#4ade80' : isCurrent ? '#60a5fa' : '#64748b',
                  }}>
                    {step.label}
                  </div>
                  {isCurrent && (
                    <div style={{ fontSize: '12px', color: '#94a3b8', marginTop: '2px' }}>
                      처리 중...
                    </div>
                  )}
                </div>

                {/* 상태 표시 */}
                {isCompleted && (
                  <div style={{
                    fontSize: '12px',
                    color: '#4ade80',
                    fontWeight: 600,
                  }}>
                    완료
                  </div>
                )}
                {isCurrent && (
                  <div className="spinner" style={{ width: '20px', height: '20px', borderWidth: '2px' }} />
                )}
              </div>
            );
          })}
        </div>

        {/* 예상 소요 시간 */}
        <div style={{
          marginTop: '20px',
          padding: '12px',
          backgroundColor: 'rgba(30, 41, 59, 0.5)',
          borderRadius: '8px',
          fontSize: '13px',
          color: '#94a3b8',
          textAlign: 'center',
        }}>
          ⏱️ 예상 소요 시간: 약 40-60초
        </div>
      </div>
    </div>
  );
};

export default AnalysisProgress;