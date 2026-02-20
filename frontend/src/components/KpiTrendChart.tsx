/**
 * KPI 트렌드 차트 컴포넌트
 */

import React from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';

interface KpiTrendChartProps {
  data: Array<{
    date: string;
    oee_v: number;
    thp_v: number;
    oee_t: number;
    thp_t: number;
  }>;
}

const KpiTrendChart: React.FC<KpiTrendChartProps> = ({ data }) => {
  return (
    <div style={{ width: '100%', height: '400px' }}>
      <ResponsiveContainer>
        <LineChart
          data={data}
          margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
        >
          <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
          <XAxis
            dataKey="date"
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
          <Legend
            wrapperStyle={{ color: '#94a3b8', fontSize: '13px' }}
          />
          <Line
            type="monotone"
            dataKey="oee_v"
            stroke="#60a5fa"
            name="OEE 실제"
            strokeWidth={2}
            dot={{ fill: '#60a5fa', r: 4 }}
          />
          <Line
            type="monotone"
            dataKey="oee_t"
            stroke="#3b82f6"
            name="OEE 목표"
            strokeWidth={2}
            strokeDasharray="5 5"
            dot={false}
          />
          <Line
            type="monotone"
            dataKey="thp_v"
            stroke="#4ade80"
            name="THP 실제"
            strokeWidth={2}
            dot={{ fill: '#4ade80', r: 4 }}
          />
          <Line
            type="monotone"
            dataKey="thp_t"
            stroke="#16a34a"
            name="THP 목표"
            strokeWidth={2}
            strokeDasharray="5 5"
            dot={false}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default KpiTrendChart;