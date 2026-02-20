/**
 * 알람 모니터링 페이지
 */

import React, { useState } from 'react';
import AlarmAnalysis from '../components/AlarmAnalysis';
import AlarmHistory from '../components/AlarmHistory';

const AlarmPage: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'analysis' | 'history'>('analysis');

  return (
    <div>
      <div className="tabs">
        <button
          className={`tab ${activeTab === 'analysis' ? 'active' : ''}`}
          onClick={() => setActiveTab('analysis')}
        >
          최신 알람 분석
        </button>
        <button
          className={`tab ${activeTab === 'history' ? 'active' : ''}`}
          onClick={() => setActiveTab('history')}
        >
          과거 알람 이력
        </button>
      </div>

      {activeTab === 'analysis' && <AlarmAnalysis />}
      {activeTab === 'history' && <AlarmHistory />}
    </div>
  );
};

export default AlarmPage;