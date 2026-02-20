/**
 * 메인 App 컴포넌트
 */

import React, { useState } from 'react';
import Sidebar from './components/Sidebar';
import AlarmPage from './pages/AlarmPage';
import ChatBotPage from './pages/ChatBotPage';
import DatabasePage from './pages/DatabasePage';

const App: React.FC = () => {
  const [currentPage, setCurrentPage] = useState<string>('alarm');

  const renderPage = () => {
    switch (currentPage) {
      case 'alarm':
        return <AlarmPage />;
      case 'chatbot':
        return <ChatBotPage />;
      case 'database':
        return <DatabasePage />;
      default:
        return <AlarmPage />;
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