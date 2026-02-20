/**
 * 알람 빈도 차트 컴포넌트
 */

import React from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  Cell,
} from 'recharts';

interface AlarmFrequencyChartProps {
  data: Array<{
    kpi: string;
    count: number;
  }>;
}

const AlarmFrequencyChart: React.FC<AlarmFrequencyChartProps> = ({ data }) => {
  const colors: { [key: string]: string } = {
    OEE: '#60a5fa',
    THP: '#4ade80',
    TAT: '#fbbf24',
    WIP_EXCEED: '#f87171',
    WIP_SHORTAGE: '#a78bfa',
  };

  return (
    <div style={{ width: '100%', height: '300px' }}>
      <ResponsiveContainer>
        <BarChart
          data={data}
          margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
        >
          <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
          <XAxis
            dataKey="kpi"
            stroke="#94a3b8"
            style={{ fontSize: '12px' }}
          />
          <YAxis stroke="#94a3b8" style={{ fontSize: '12px' }} />
          <Tooltip
            contentStyle={{
              backgroundColor: '#1e293b',
              border: '1px solid #334155',
              borderRadius: '8px',
              color: '#e2e8f0',
            }}
          />
          <Legend wrapperStyle={{ color: '#94a3b8', fontSize: '13px' }} />
          <Bar dataKey="count" name="알람 발생 횟수" radius={[8, 8, 0, 0]}>
            {data.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={colors[entry.kpi] || '#64748b'} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default AlarmFrequencyChart;