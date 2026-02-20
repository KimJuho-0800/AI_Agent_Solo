/**
 * 대시보드 개요 페이지 (차트 포함)
 */

import React from 'react';
import KpiTrendChart from '../components/KpiTrendChart';
import AlarmFrequencyChart from '../components/AlarmFrequencyChart';

const DashboardOverview: React.FC = () => {
  // 샘플 데이터 (실제로는 API에서 가져와야 함)
  const kpiTrendData = [
    { date: '01-25', oee_v: 65.2, oee_t: 70, thp_v: 245, thp_t: 250 },
    { date: '01-26', oee_v: 68.5, oee_t: 70, thp_v: 240, thp_t: 250 },
    { date: '01-27', oee_v: 71.6, oee_t: 70, thp_v: 235, thp_t: 250 },
    { date: '01-28', oee_v: 69.0, oee_t: 70, thp_v: 240, thp_t: 250 },
    { date: '01-29', oee_v: 72.2, oee_t: 70, thp_v: 230, thp_t: 250 },
    { date: '01-30', oee_v: 65.2, oee_t: 70, thp_v: 245, thp_t: 250 },
    { date: '01-31', oee_v: 76.4, oee_t: 70, thp_v: 227, thp_t: 250 },
  ];

  const alarmFrequencyData = [
    { kpi: 'OEE', count: 3 },
    { kpi: 'THP', count: 4 },
    { kpi: 'TAT', count: 2 },
    { kpi: 'WIP_EXCEED', count: 2 },
    { kpi: 'WIP_SHORTAGE', count: 1 },
  ];

  return (
    <div>
      {/* KPI 요약 카드 */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '16px', marginBottom: '24px' }}>
        <div className="card" style={{ padding: '20px' }}>
          <div style={{ fontSize: '13px', color: '#94a3b8', marginBottom: '8px' }}>총 알람</div>
          <div style={{ fontSize: '32px', fontWeight: 700, color: '#60a5fa' }}>12</div>
          <div style={{ fontSize: '12px', color: '#64748b', marginTop: '4px' }}>최근 7일</div>
        </div>
        <div className="card" style={{ padding: '20px' }}>
          <div style={{ fontSize: '13px', color: '#94a3b8', marginBottom: '8px' }}>평균 OEE</div>
          <div style={{ fontSize: '32px', fontWeight: 700, color: '#4ade80' }}>69.7%</div>
          <div style={{ fontSize: '12px', color: '#64748b', marginTop: '4px' }}>목표: 70%</div>
        </div>
        <div className="card" style={{ padding: '20px' }}>
          <div style={{ fontSize: '13px', color: '#94a3b8', marginBottom: '8px' }}>평균 처리량</div>
          <div style={{ fontSize: '32px', fontWeight: 700, color: '#fbbf24' }}>237</div>
          <div style={{ fontSize: '12px', color: '#64748b', marginTop: '4px' }}>목표: 250개</div>
        </div>
        <div className="card" style={{ padding: '20px' }}>
          <div style={{ fontSize: '13px', color: '#94a3b8', marginBottom: '8px' }}>다운타임</div>
          <div style={{ fontSize: '32px', fontWeight: 700, color: '#f87171' }}>1.2h</div>
          <div style={{ fontSize: '12px', color: '#64748b', marginTop: '4px' }}>최근 7일</div>
        </div>
      </div>

      {/* KPI 트렌드 차트 */}
      <div className="card" style={{ marginBottom: '24px' }}>
        <div className="card-header">
          <h2 className="card-title">
            <span>📈</span>
            KPI 트렌드 (최근 7일)
          </h2>
        </div>
        <div className="card-body">
          <KpiTrendChart data={kpiTrendData} />
        </div>
      </div>

      {/* 알람 빈도 차트 */}
      <div className="card">
        <div className="card-header">
          <h2 className="card-title">
            <span>📊</span>
            KPI별 알람 발생 빈도
          </h2>
        </div>
        <div className="card-body">
          <AlarmFrequencyChart data={alarmFrequencyData} />
        </div>
      </div>
    </div>
  );
};

export default DashboardOverview;