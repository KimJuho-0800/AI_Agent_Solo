/**
 * AI 챗봇 페이지
 */

import React, { useState, useRef, useEffect } from 'react';
import { askQuestion } from '../services/api';
import { ChatMessage } from '../types';
import LoadingSpinner from '../components/LoadingSpinner';
import TypingIndicator from '../components/TypingIndicator';

const ChatBotPage: React.FC = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: '1',
      role: 'assistant',
      content: '안녕하세요! 과거 알람 이력에 대해 궁금하신 점을 질문해주세요. 🤖',
      timestamp: new Date(),
    },
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim() || loading) return;

    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      role: 'user',
      content: input.trim(),
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const response = await askQuestion(input.trim());

      const assistantMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: response.answer,
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error: any) {
      const errorMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: `죄송합니다. 오류가 발생했습니다: ${
          error.response?.data?.detail || error.message
        }`,
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const quickQuestions = [
    '최근 장비 다운타임이 발생한 적이 있나요?',
    'HOLD 상태가 자주 발생하는 이유는?',
    '레시피 복잡도가 높으면 어떤 문제가 생기나요?',
  ];

  return (
    <div className="chat-container">
      <div className="chat-header">
        <div className="chat-title">💬 AI 챗봇</div>
        <div className="chat-subtitle">과거 알람 이력 및 KPI 데이터에 대해 질문하세요</div>
      </div>

      <div className="chat-messages">
        {messages.map((message) => (
          <div key={message.id} className={`message ${message.role}`}>
            <div className="message-content">
              <div style={{ whiteSpace: 'pre-wrap' }}>{message.content}</div>
              <div className="message-time">
                {message.timestamp.toLocaleTimeString('ko-KR', {
                  hour: '2-digit',
                  minute: '2-digit',
                })}
              </div>
            </div>
          </div>
        ))}

        {loading && (
            <div className="message assistant">
                <TypingIndicator />
            </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      <div className="chat-input-area">
        <div className="chat-input-group">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="질문을 입력하세요..."
            disabled={loading}
            className="chat-input"
          />
          <button
            onClick={handleSend}
            disabled={!input.trim() || loading}
            className="btn btn-primary"
          >
            전송
          </button>
        </div>

        <div className="quick-questions">
          {quickQuestions.map((question, index) => (
            <button
              key={index}
              onClick={() => setInput(question)}
              disabled={loading}
              className="quick-question-btn"
            >
              💡 {question.substring(0, 20)}...
            </button>
          ))}
        </div>
      </div>
    </div>
  );
};

export default ChatBotPage;