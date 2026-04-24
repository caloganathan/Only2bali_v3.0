import React, { useState, useRef, useEffect } from "react";
import "./ChatWidget.css";
import axios from "axios";

const FASTAPI_BASE = process.env.REACT_APP_FASTAPI_URL || "http://localhost:8000";

const INITIAL_MESSAGE = {
  role: "assistant",
  text: "Hi! I'm your Bali travel assistant 🌴 Ask me anything about planning your Bali trip!",
};

const FALLBACK_REPLY =
  "Great question! Our team will help you plan the perfect Bali experience. Please complete the trip form for a personalised itinerary, or reach out via WhatsApp for immediate assistance.";

const ChatWidget = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([INITIAL_MESSAGE]);
  const [input, setInput] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    if (isOpen) {
      messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages, isOpen]);

  const sendMessage = async () => {
    const text = input.trim();
    if (!text || isTyping) return;

    setMessages((prev) => [...prev, { role: "user", text }]);
    setInput("");
    setIsTyping(true);

    try {
      const res = await axios.post(
        `${FASTAPI_BASE}/api/v1/chat`,
        { message: text },
        { headers: { "Content-Type": "application/json" }, timeout: 10000 }
      );
      setMessages((prev) => [
        ...prev,
        { role: "assistant", text: res.data?.reply || FALLBACK_REPLY },
      ]);
    } catch {
      setMessages((prev) => [
        ...prev,
        { role: "assistant", text: FALLBACK_REPLY },
      ]);
    } finally {
      setIsTyping(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <>
      {isOpen && (
        <div className="cw-panel">
          <div className="cw-header">
            <span className="cw-header-title">🌴 Bali Travel Assistant</span>
            <button className="cw-close-btn" onClick={() => setIsOpen(false)}>
              ✕
            </button>
          </div>

          <div className="cw-messages">
            {messages.map((msg, i) => (
              <div
                key={i}
                className={`cw-message ${msg.role === "user" ? "cw-user" : "cw-assistant"}`}
              >
                {msg.text}
              </div>
            ))}
            {isTyping && (
              <div className="cw-message cw-assistant cw-typing">
                <span></span><span></span><span></span>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          <div className="cw-input-row">
            <input
              className="cw-input"
              type="text"
              placeholder="Ask about Bali..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              disabled={isTyping}
            />
            <button
              className="cw-send-btn"
              onClick={sendMessage}
              disabled={isTyping || !input.trim()}
            >
              ➤
            </button>
          </div>
        </div>
      )}

      <button
        className="cw-fab"
        onClick={() => setIsOpen((o) => !o)}
        aria-label="Open chat"
      >
        {isOpen ? "✕" : "💬"}
      </button>
    </>
  );
};

export default ChatWidget;
