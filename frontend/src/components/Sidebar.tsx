/**
 * 사이드바 네비게이션
 */

import React from 'react';

interface SidebarProps {
  currentPage: string;
  onNavigate: (page: string) => void;
}

const Sidebar: React.FC<SidebarProps> = ({ currentPage, onNavigate }) => {
  const navItems = [
    { id: 'alarm', icon: '🚨', label: '알람 모니터링' },
    { id: 'chatbot', icon: '💬', label: 'AI 챗봇' },
    { id: 'database', icon: '📊', label: '데이터베이스' },
  ];

  return (
    <div className="sidebar">
      <div className="sidebar-header">
        <h1 className="sidebar-title">KPI Monitoring Agent</h1>
      </div>

      <nav className="sidebar-nav">
        {navItems.map((item) => (
          <div
            key={item.id}
            className={`nav-item ${currentPage === item.id ? 'active' : ''}`}
            onClick={() => onNavigate(item.id)}
          >
            <span className="nav-icon">{item.icon}</span>
            <span>{item.label}</span>
          </div>
        ))}
      </nav>

      <div style={{ padding: '20px', borderTop: '1px solid #334155', fontSize: '12px', color: '#64748b' }}>
        <p>Powered by</p>
        <p style={{ fontWeight: 600, color: '#94a3b8' }}>AWS Bedrock & LangGraph</p>
      </div>
    </div>
  );
};

export default Sidebar;