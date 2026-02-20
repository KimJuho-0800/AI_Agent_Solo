/**
 * 과거 알람 이력 컴포넌트
 */

import React, { useState } from 'react';
import { analyzeAlarm } from '../services/api';
import { AlarmAnalyzeResponse } from '../types';
import LoadingSpinner from './LoadingSpinner';
import ReportViewer from './ReportViewer';
import AnalysisProgress from './AnalysisProgress';

const AlarmHistory: React.FC = () => {
  // 하드코딩된 과거 알람 목록 (실제로는 API에서 가져와야 함)
  const historicalAlarms = [
    { date: '2026-01-31', eqp_id: 'EQP12', kpi: 'THP' },
    { date: '2026-01-30', eqp_id: 'EQP11', kpi: 'OEE' },
    { date: '2026-01-29', eqp_id: 'EQP10', kpi: 'WIP_SHORTAGE' },
    { date: '2026-01-28', eqp_id: 'EQP09', kpi: 'WIP_EXCEED' },
    { date: '2026-01-27', eqp_id: 'EQP08', kpi: 'TAT' },
    { date: '2026-01-26', eqp_id: 'EQP07', kpi: 'THP' },
    { date: '2026-01-25', eqp_id: 'EQP06', kpi: 'OEE' },
    { date: '2026-01-24', eqp_id: 'EQP05', kpi: 'WIP_SHORTAGE' },
    { date: '2026-01-23', eqp_id: 'EQP04', kpi: 'WIP_EXCEED' },
    { date: '2026-01-22', eqp_id: 'EQP03', kpi: 'TAT' },
    { date: '2026-01-21', eqp_id: 'EQP02', kpi: 'THP' },
    { date: '2026-01-20', eqp_id: 'EQP01', kpi: 'OEE' },
  ];

  const [selectedAlarm, setSelectedAlarm] = useState<any>(null);
  const [analysisResult, setAnalysisResult] = useState<AlarmAnalyzeResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [showReport, setShowReport] = useState(false);

  const handleAnalyzeHistory = async (alarm: any) => {
    setSelectedAlarm(alarm);
    setLoading(true);
    setShowReport(false);

    try {
      const result = await analyzeAlarm(alarm.date, alarm.eqp_id, alarm.kpi);
      setAnalysisResult(result);
    } catch (err: any) {
      console.error('과거 알람 분석 실패:', err);
      alert('과거 알람 분석에 실패했습니다.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      {/* 알람 이력 테이블 */}
      <div className="card">
        <div className="card-header">
          <h2 className="card-title">
            <span>📜</span>
            과거 알람 이력
          </h2>
        </div>
        <div className="card-body">
          <table className="data-table">
            <thead>
              <tr>
                <th>날짜</th>
                <th>장비 ID</th>
                <th>KPI</th>
                <th>작업</th>
              </tr>
            </thead>
            <tbody>
              {historicalAlarms.map((alarm, index) => (
                <tr key={index}>
                  <td>{alarm.date}</td>
                  <td>{alarm.eqp_id}</td>
                  <td>
                    <span className={`kpi-badge ${alarm.kpi}`}>
                      {alarm.kpi}
                    </span>
                  </td>
                  <td>
                    <button
                      onClick={() => handleAnalyzeHistory(alarm)}
                      className="btn btn-primary"
                      style={{ padding: '6px 16px', fontSize: '13px' }}
                      disabled={loading}
                    >
                      분석 보기
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* 로딩 */}
      <AnalysisProgress isAnalyzing={loading} />

      {/* 선택된 알람 분석 결과 */}
      {analysisResult && !loading && (
        <>
          <div className="card">
            <div className="card-header">
              <h2 className="card-title">
                <span>✅</span>
                {selectedAlarm.date} {selectedAlarm.eqp_id} 분석 결과
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
                  확률: {analysisResult.selected_cause.probability}%
                </div>
              </div>

              <button
                onClick={() => setShowReport(!showReport)}
                className="btn btn-secondary btn-full"
                style={{ marginTop: '16px' }}
              >
                {showReport ? '📄 리포트 숨기기' : '📄 상세 리포트 보기'}
              </button>
            </div>
          </div>

          {showReport && (
            <div className="card">
              <div className="card-body">
                <ReportViewer report={analysisResult.final_report} />
              </div>
            </div>
          )}
        </>
      )}
    </div>
  );
};

export default AlarmHistory;