/**
 * 리포트 뷰어 컴포넌트 (마크다운)
 */

import React from 'react';
import ReactMarkdown from 'react-markdown';

interface ReportViewerProps {
  report: string;
}

const ReportViewer: React.FC<ReportViewerProps> = ({ report }) => {
  return (
    <div style={{
      backgroundColor: '#1e293b',
      border: '1px solid #334155',
      borderRadius: '8px',
      padding: '24px',
      color: '#cbd5e1',
      lineHeight: '1.8',
    }}>
      <ReactMarkdown
        components={{
          h1: ({ children }) => (
            <h1 style={{ color: '#60a5fa', fontSize: '24px', fontWeight: 700, marginBottom: '16px', borderBottom: '2px solid #2563eb', paddingBottom: '8px' }}>
              {children}
            </h1>
          ),
          h2: ({ children }) => (
            <h2 style={{ color: '#60a5fa', fontSize: '20px', fontWeight: 600, marginTop: '24px', marginBottom: '12px' }}>
              {children}
            </h2>
          ),
          h3: ({ children }) => (
            <h3 style={{ color: '#94a3b8', fontSize: '16px', fontWeight: 600, marginTop: '16px', marginBottom: '8px' }}>
              {children}
            </h3>
          ),
          p: ({ children }) => (
            <p style={{ marginBottom: '12px', color: '#cbd5e1' }}>
              {children}
            </p>
          ),
          ul: ({ children }) => (
            <ul style={{ marginLeft: '20px', marginBottom: '12px', listStyleType: 'disc' }}>
              {children}
            </ul>
          ),
          ol: ({ children }) => (
            <ol style={{ marginLeft: '20px', marginBottom: '12px' }}>
              {children}
            </ol>
          ),
          li: ({ children }) => (
            <li style={{ marginBottom: '6px', color: '#cbd5e1' }}>
              {children}
            </li>
          ),
          strong: ({ children }) => (
            <strong style={{ color: '#e2e8f0', fontWeight: 700 }}>
              {children}
            </strong>
          ),
        }}
      >
        {report}
      </ReactMarkdown>
    </div>
  );
};

export default ReportViewer;