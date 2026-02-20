import React, { useState } from 'react';
import Sidebar from './components/Sidebar';
import DashboardOverview from './pages/DashboardOverview';  // 추가
import AlarmPage from './pages/AlarmPage';
import ChatBotPage from './pages/ChatBotPage';
import DatabasePage from './pages/DatabasePage';

const App: React.FC = () => {
  const [currentPage, setCurrentPage] = useState<string>('dashboard');  // 기본값 변경

  const renderPage = () => {
    switch (currentPage) {
      case 'dashboard':  // 추가
        return <DashboardOverview />;
      case 'alarm':
        return <AlarmPage />;
      case 'chatbot':
        return <ChatBotPage />;
      case 'database':
        return <DatabasePage />;
      default:
        return <DashboardOverview />;
    }
  };

  return (
    <div className="app-container">
      <Sidebar currentPage={currentPage} onNavigate={setCurrentPage} />
      
      <div className="main-content">
        <header className="main-header">
          <div className="header-content">
            <h1 className="main-title">KPI Monitoring Agent</h1>
          </div>
        </header>

        <main className="content-area">
          {renderPage()}
        </main>
      </div>
    </div>
  );
};

export default App;