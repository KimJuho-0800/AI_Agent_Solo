/**
 * 데이터베이스 조회 페이지
 */

import React, { useState } from 'react';

const DatabasePage: React.FC = () => {
  const [selectedTable, setSelectedTable] = useState<string>('KPI_DAILY');

  // 샘플 데이터 (실제로는 API에서 가져와야 함)
  const tables = {
    KPI_DAILY: [
      { date: '2026-01-31', eqp_id: 'EQP12', line_id: 'LINE2', oee_t: 70, oee_v: 76.44, thp_t: 250, thp_v: 227 },
      { date: '2026-01-30', eqp_id: 'EQP11', line_id: 'LINE2', oee_t: 70, oee_v: 65.23, thp_t: 250, thp_v: 245 },
      { date: '2026-01-29', eqp_id: 'EQP10', line_id: 'LINE2', oee_t: 70, oee_v: 72.18, thp_t: 250, thp_v: 230 },
      { date: '2026-01-28', eqp_id: 'EQP09', line_id: 'LINE2', oee_t: 70, oee_v: 68.94, thp_t: 250, thp_v: 240 },
      { date: '2026-01-27', eqp_id: 'EQP08', line_id: 'LINE1', oee_t: 70, oee_v: 71.56, thp_t: 250, thp_v: 235 },
    ],
    LOT_STATE: [
      { event_time: '2026-01-31 10:00', lot_id: 'LOT001', eqp_id: 'EQP12', lot_state: 'RUN', in_cnt: 50 },
      { event_time: '2026-01-31 11:00', lot_id: 'LOT002', eqp_id: 'EQP12', lot_state: 'WAIT', in_cnt: 50 },
      { event_time: '2026-01-31 12:00', lot_id: 'LOT003', eqp_id: 'EQP12', lot_state: 'HOLD', in_cnt: 50 },
      { event_time: '2026-01-31 13:00', lot_id: 'LOT004', eqp_id: 'EQP12', lot_state: 'END', in_cnt: 48 },
      { event_time: '2026-01-31 14:00', lot_id: 'LOT005', eqp_id: 'EQP11', lot_state: 'RUN', in_cnt: 50 },
    ],
    EQP_STATE: [
      { event_time: '2026-01-31 09:00', eqp_id: 'EQP12', line_id: 'LINE2', eqp_state: 'RUN', lot_id: 'LOT001' },
      { event_time: '2026-01-31 10:30', eqp_id: 'EQP12', line_id: 'LINE2', eqp_state: 'DOWN', lot_id: 'LOT001' },
      { event_time: '2026-01-31 11:00', eqp_id: 'EQP12', line_id: 'LINE2', eqp_state: 'RUN', lot_id: 'LOT002' },
      { event_time: '2026-01-31 15:00', eqp_id: 'EQP11', line_id: 'LINE2', eqp_state: 'RUN', lot_id: 'LOT005' },
      { event_time: '2026-01-31 16:00', eqp_id: 'EQP11', line_id: 'LINE2', eqp_state: 'IDLE', lot_id: null },
    ],
    RCP_STATE: [
      { rcp_id: 'RCP01', eqp_id: 'EQP01', complex_level: 9 },
      { rcp_id: 'RCP02', eqp_id: 'EQP01', complex_level: 4 },
      { rcp_id: 'RCP23', eqp_id: 'EQP12', complex_level: 8 },
      { rcp_id: 'RCP24', eqp_id: 'EQP12', complex_level: 10 },
      { rcp_id: 'RCP15', eqp_id: 'EQP08', complex_level: 6 },
    ],
    SCENARIO_MAP: [
      { date: '2026-01-31', alarm_eqp_id: 'EQP12', alarm_kpi: 'THP' },
      { date: '2026-01-30', alarm_eqp_id: 'EQP11', alarm_kpi: 'OEE' },
      { date: '2026-01-29', alarm_eqp_id: 'EQP10', alarm_kpi: 'WIP_SHORTAGE' },
      { date: '2026-01-28', alarm_eqp_id: 'EQP09', alarm_kpi: 'WIP_EXCEED' },
      { date: '2026-01-27', alarm_eqp_id: 'EQP08', alarm_kpi: 'TAT' },
    ],
  };

  const tableNames = Object.keys(tables);

  const renderTable = (tableName: string) => {
    const data = tables[tableName as keyof typeof tables];
    if (!data || data.length === 0) return <p>데이터 없음</p>;

    const columns = Object.keys(data[0]);

    return (
      <table className="data-table">
        <thead>
          <tr>
            {columns.map((col) => (
              <th key={col}>{col}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.map((row, index) => (
            <tr key={index}>
              {columns.map((col) => (
                <td key={col}>{(row as any)[col] ?? '-'}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    );
  };

  return (
    <div>
      <div className="card">
        <div className="card-header">
          <h2 className="card-title">
            <span>📊</span>
            데이터베이스 조회
          </h2>
        </div>
        <div className="card-body">
          <div style={{ marginBottom: '20px' }}>
            <label style={{ display: 'block', marginBottom: '8px', color: '#94a3b8', fontWeight: 600 }}>
              테이블 선택
            </label>
            <select
              value={selectedTable}
              onChange={(e) => setSelectedTable(e.target.value)}
              style={{
                padding: '10px',
                backgroundColor: '#1e293b',
                border: '1px solid #334155',
                borderRadius: '8px',
                color: '#e2e8f0',
                fontSize: '14px',
                width: '300px',
                cursor: 'pointer',
              }}
            >
              {tableNames.map((name) => (
                <option key={name} value={name}>
                  {name}
                </option>
              ))}
            </select>
          </div>

          <div style={{ overflowX: 'auto' }}>
            {renderTable(selectedTable)}
          </div>

          <div style={{ marginTop: '20px', padding: '16px', backgroundColor: 'rgba(30, 41, 59, 0.5)', borderRadius: '8px', fontSize: '13px', color: '#94a3b8' }}>
            <p><strong>참고:</strong> 이 데이터는 샘플 데이터입니다.</p>
            <p>실제 운영 시에는 Supabase PostgreSQL에서 실시간으로 조회됩니다.</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DatabasePage;