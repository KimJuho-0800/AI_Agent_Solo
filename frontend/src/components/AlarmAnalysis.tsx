/**
 * 최신 알람 분석 컴포넌트
 */

import React, { useState, useEffect } from 'react';
import { getLatestAlarm, analyzeAlarm } from '../services/api';
import { AlarmAnalyzeResponse } from '../types';
import LoadingSpinner from './LoadingSpinner';
import ReportViewer from './ReportViewer';

const AlarmAnalysis: React.FC = () => {
  const [latestAlarm, setLatestAlarm] = useState<any>(null);
  const [analysisResult, setAnalysisResult] = useState<AlarmAnalyzeResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showReport, setShowReport] = useState(false);

  useEffect(() => {
    loadLatestAlarm();
  }, []);

  const loadLatestAlarm = async () => {
    try {
      const data = await getLatestAlarm();
      setLatestAlarm(data);
    } catch (err: any) {
      console.error('최신 알람 조회 실패:', err);
      setError('최신 알람을 불러올 수 없습니다.');
    }
  };

  const handleAnalyze = async () => {
    if (!latestAlarm) return;

    setLoading(true);
    setError(null);

    try {
      const result = await analyzeAlarm();
      setAnalysisResult(result);
    } catch (err: any) {
      console.error('알람 분석 실패:', err);
      setError(err.response?.data?.detail || '알람 분석에 실패했습니다.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      {/* 최신 알람 정보 카드 */}
      <div className="card">
        <div className="card-header">
          <h2 className="card-title">
            <span>🚨</span>
            최신 알람
          </h2>
          <button
            onClick={loadLatestAlarm}
            className="btn-secondary"
            style={{ padding: '8px 16px', fontSize: '13px' }}
          >
            🔄 새로고침
          </button>
        </div>

        {latestAlarm && (
          <div className="card-body">
            <div className="alarm-info-grid">
              <div className="info-item">
                <span className="info-label">날짜</span>
                <span className="info-value">{latestAlarm.date}</span>
              </div>
              <div className="info-item">
                <span className="info-label">장비</span>
                <span className="info-value">{latestAlarm.eqp_id}</span>
              </div>
              <div className="info-item">
                <span className="info-label">KPI</span>
                <span className={`kpi-badge ${latestAlarm.kpi}`}>
                  {latestAlarm.kpi}
                </span>
              </div>
            </div>

            {!analysisResult && (
              <button
                onClick={handleAnalyze}
                disabled={loading}
                className="btn btn-primary btn-full"
                style={{ marginTop: '20px' }}
              >
                {loading ? '분석 중...' : '🔍 AI 근본 원인 분석 시작'}
              </button>
            )}
          </div>
        )}
      </div>

      {/* 로딩 */}
      {loading && (
        <div className="card">
          <LoadingSpinner message="AI가 데이터를 분석하고 있습니다..." />
        </div>
      )}

      {/* 에러 */}
      {error && (
        <div className="error-box">
          <strong>오류:</strong> {error}
        </div>
      )}

      {/* 분석 결과 */}
      {analysisResult && !loading && (
        <>
          {/* 근본 원인 */}
          <div className="card">
            <div className="card-header">
              <h2 className="card-title">
                <span>✅</span>
                AI 분석 결과
              </h2>
            </div>
            <div className="card-body">
              <div className="result-box">
                <div className="result-title">
                  <span>🎯</span>
                  근본 원인
                </div>
                <div className="result-content">
                  {analysisResult.selected_cause.cause}
                </div>
                <div className="result-meta">
                  확률: {analysisResult.selected_cause.probability}% | 
                  근거: {analysisResult.selected_cause.evidence.substring(0, 100)}...
                </div>
              </div>

              {/* 모든 원인 후보 */}
              <details style={{ marginTop: '16px', cursor: 'pointer' }}>
                <summary style={{ color: '#94a3b8', fontWeight: 600 }}>
                  모든 원인 후보 보기 ({analysisResult.root_causes.length}개)
                </summary>
                <div style={{ marginTop: '12px', display: 'flex', flexDirection: 'column', gap: '12px' }}>
                  {analysisResult.root_causes.map((cause, index) => (
                    <div
                      key={index}
                      style={{
                        padding: '12px',
                        backgroundColor: 'rgba(30, 41, 59, 0.5)',
                        border: '1px solid #334155',
                        borderRadius: '8px',
                      }}
                    >
                      <div style={{ fontWeight: 600, color: '#e2e8f0', marginBottom: '4px' }}>
                        {index + 1}. {cause.cause}
                      </div>
                      <div style={{ fontSize: '13px', color: '#94a3b8' }}>
                        확률: {cause.probability}%
                      </div>
                    </div>
                  ))}
                </div>
              </details>

              {/* 리포트 토글 */}
              <button
                onClick={() => setShowReport(!showReport)}
                className="btn btn-secondary btn-full"
                style={{ marginTop: '20px' }}
              >
                {showReport ? '📄 리포트 숨기기' : '📄 상세 리포트 보기'}
              </button>
            </div>
          </div>

          {/* 상세 리포트 */}
          {showReport && (
            <div className="card">
              <div className="card-header">
                <h2 className="card-title">
                  <span>📋</span>
                  상세 분석 리포트
                </h2>
              </div>
              <div className="card-body">
                <ReportViewer report={analysisResult.final_report} />
              </div>
            </div>
          )}

          {/* 메타 정보 */}
          <div className="card">
            <div className="card-body" style={{ fontSize: '13px', color: '#94a3b8' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <span>⏱️ 처리 시간: {analysisResult.processing_time?.toFixed(2)}초</span>
                <span>🤖 LLM 호출: {analysisResult.llm_calls}회</span>
                <span>💾 RAG 저장: {analysisResult.rag_saved ? '✅ 완료' : '❌ 실패'}</span>
                <span>🆔 리포트 ID: {analysisResult.report_id}</span>
              </div>
            </div>
          </div>
        </>
      )}
    </div>
  );
};

export default AlarmAnalysis;