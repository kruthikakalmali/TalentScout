// src/components/Chatbot.tsx
import React, { useState } from "react";
import axios from "axios";
import { PROD_HOST_URL } from "../../constants";
import "./chatbot.css";

interface ChatEntry {
  user: string;
  bot: string;
}

const Chatbot: React.FC = () => {
  // 1) Default mode = "vector"
  const [mode, setMode] = useState<"vector" | "openai">("vector");
  const [userMessage, setUserMessage] = useState("");
  const [chatHistory, setChatHistory] = useState<ChatEntry[]>([]);
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    const msg = userMessage.trim();
    if (!msg) return;
    if (!mode) return;

    // 1) add placeholder entry
    setChatHistory(prev => [...prev, { user: msg, bot: "…" }]);
    setLoading(true);
    setUserMessage("");

    try {
      const { data } = await axios.post(`${PROD_HOST_URL}/chat`, {
        message: msg,
        mode,
      });

      setChatHistory(prev => {
        const updated = [...prev];
        const last = updated[updated.length - 1];
        updated[updated.length - 1] = { user: last.user, bot: data.reply };
        return updated;
      });
    } catch (err) {
      console.error(err);
      setChatHistory(prev => {
        const updated = [...prev];
        updated[updated.length - 1] = {
          user: updated[updated.length - 1].user,
          bot: "Oops! Something went wrong.",
        };
        return updated;
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="chatbot-container">
      <h2 style={{ textAlign: "center", marginBottom: 20 }}>
        Welcome to the HR Chatbot
      </h2>

      {/* mode-selection */}
      <div className="mode-selection">
        <button
          onClick={() => setMode("vector")}
          className={mode === "vector" ? "selected" : ""}
        >
          Search Candidate Database
        </button>
        <button
          onClick={() => setMode("openai")}
          className={mode === "openai" ? "selected" : ""}
        >
          Ask Any HR Question
        </button>
      </div>

      <p style={{ margin: "10px 0" }}>
        Selected Mode:{" "}
        {mode === "vector"
          ? "Search Candidate Database"
          : "Ask Any HR Question"}
      </p>

      {/* chat history */}
      <div className="chat-history">
        {chatHistory.map((c, i) => (
          <div key={i} className="chat-message">
            <p><strong>You:</strong> {c.user}</p>
            <p><strong>Bot:</strong> {c.bot}</p>
          </div>
        ))}
      </div>

      {/* input + send */}
      <div className="chat-input">
        <input
          type="text"
          value={userMessage}
          onChange={e => setUserMessage(e.target.value)}
          placeholder="Type your message..."
        />
        <button
          onClick={sendMessage}
          disabled={loading || !userMessage.trim()}
        >
          {loading ? "Processing..." : "Send"}
        </button>
      </div>
    </div>
  );
};

export default Chatbot;
