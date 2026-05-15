import React, { useState, useRef, useEffect } from 'react';
import { fetchChat } from '../data/api';
import { IoSend } from 'react-icons/io5';

export default function ChatInterface() {
  const [messages, setMessages] = useState([
    { id: 1, role: 'bot', content: '👋 Hello! I\'m your AI Traffic Assistant. Ask me about congestion, routes, or live conditions.' },
  ]);
  const [input, setInput] = useState('');
  const [typing, setTyping] = useState(false);
  const endRef = useRef(null);

  useEffect(() => { endRef.current?.scrollIntoView({ behavior: 'smooth' }); }, [messages, typing]);

  const send = async () => {
    if (!input.trim()) return;
    const q = input.trim();
    setMessages(p => [...p, { id: Date.now(), role: 'user', content: q }]);
    setInput('');
    setTyping(true);

    try {
      const data = await fetchChat(q);
      const showAction = q.toLowerCase().includes('route') || q.toLowerCase().includes('alternative');
      setMessages(p => [...p, {
        id: Date.now() + 1, role: 'bot', content: data.response,
        showAction, showMap: false,
      }]);
    } catch {
      setMessages(p => [...p, { id: Date.now() + 1, role: 'bot', content: 'Sorry, I couldn\'t reach the server. Please try again.' }]);
    }
    setTyping(false);
  };

  const revealMap = (msgId) => {
    setMessages(p => p.map(m => m.id === msgId ? { ...m, showAction: false, showMap: true } : m));
  };

  return (
    <div className="chat-wrap">
      <div className="chat-head">
        <div className="chat-avatar">🤖</div>
        <div>
          <div className="chat-title">AI Traffic Assistant</div>
          <div className="chat-online">● Online</div>
        </div>
      </div>

      <div className="chat-body">
        {messages.map(m => (
          <div key={m.id} className={`msg ${m.role}`}>
            {m.content}
            {m.showAction && (
              <div><button className="msg-action" onClick={() => revealMap(m.id)}>Show alternative routes</button></div>
            )}
            {m.showMap && (
              <div className="mini-map-card">
                <span style={{ fontSize:'1.8rem' }}>🗺️</span>
                <span className="route-label">Best Route — 12 min faster</span>
                <span className="route-sub">via Lake Drive → Central Avenue</span>
              </div>
            )}
          </div>
        ))}
        {typing && <div className="typing-dots"><span/><span/><span/></div>}
        <div ref={endRef} />
      </div>

      <div className="chat-input-row">
        <input className="chat-field" placeholder="Ask about traffic, routes, accidents..." value={input}
          onChange={e => setInput(e.target.value)} onKeyDown={e => e.key === 'Enter' && send()} />
        <button className="chat-send" onClick={send} aria-label="Send"><IoSend /></button>
      </div>
    </div>
  );
}
