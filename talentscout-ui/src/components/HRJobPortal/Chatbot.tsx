import React, { useState } from "react";
import axios from "axios";
import { PROD_HOST_URL } from "../../constants";
import './chatbot.css'

const Chatbot = () => {
  const [userMessage, setUserMessage] = useState("");
  const [chatHistory, setChatHistory] = useState<{ user: string; bot: string }[]>([]);
  const [loading, setLoading] = useState(false);
  const [mode, setMode] = useState<string>("");

  const sendMessage = async () => {
    if (userMessage.trim() === "") return;
    
    if (!mode) {
      alert("Please select a mode first.");
      return;
    }

    const newChatHistory = [...chatHistory, { user: userMessage, bot: "..." }];
    setChatHistory(newChatHistory);
    setLoading(true);
    setUserMessage("");

    try {
      const response = await axios.post(`${PROD_HOST_URL}/chat`, {
        message: userMessage,
        mode: mode,
      });

      setChatHistory([
        ...newChatHistory,
        { user: userMessage, bot: response.data.reply },
      ]);
    } catch (error) {
      console.error("Error sending message:", error);
      setChatHistory([
        ...newChatHistory,
        { user: userMessage, bot: "Oops! Something went wrong." },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="chatbot-container">
      <h2>Welcome to the HR Chatbot</h2>
      
      {/* Option to select search mode */}
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

      {/* Display selected mode */}
      {mode && <p>Selected Mode: {mode === "vector" ? "Search Candidate Database" : "Ask Any HR Question"}</p>}

      {/* Chat History */}
      <div className="chat-history">
        {chatHistory.map((chat, index) => (
          <div key={index} className="chat-message">
            <p><strong>You:</strong> {chat.user}</p>
            <p><strong>Bot:</strong> {chat.bot}</p>
          </div>
        ))}
      </div>

      {/* User input */}
      <div className="chat-input">
        <input
          type="text"
          value={userMessage}
          onChange={(e) => setUserMessage(e.target.value)}
          placeholder="Type your message..."
        />
        <button onClick={sendMessage} disabled={loading || !mode}>
          {loading ? "Processing..." : "Send"}
        </button>
      </div>
    </div>
  );
};

export default Chatbot;
