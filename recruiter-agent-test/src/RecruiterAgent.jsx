import React, { useState } from 'react';
import axios from 'axios';

function RecruiterAgent() {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');

    const sendMessage = async () => {
        if (!input.trim()) return;

        // Create a message from the user
        const userMessage = { sender: 'user', text: input };
        setMessages(prevMessages => [...prevMessages, userMessage]);

        try {
            // Send the user input to the backend
            const response = await axios.post('http://localhost:8000/api/agent', { query: input });

            // Log the complete response from the backend
            console.log("Backend Response:", response.data);

            // Extract the response text based on the backend's format
            const text = response.data.response.text || (response.data.choices && response.data.choices[0]?.message?.content);

            if (text) {
                // Create an agent message with the response text
                const agentReply = { sender: 'agent', text: text };
                setMessages(prevMessages => [...prevMessages, agentReply]);
            } else {
                // Handle the case where no valid text is found
                const errorReply = { sender: 'agent', text: 'Response text is missing or malformed' };
                setMessages(prevMessages => [...prevMessages, errorReply]);
            }

        } catch (error) {
            console.error("Error sending message:", error);
            const errorReply = { sender: 'agent', text: 'Sorry, something went wrong.' };
            setMessages(prevMessages => [...prevMessages, errorReply]);
        }

        // Clear the input field after sending the message
        setInput('');
    };

    return (
        <div style={{ maxWidth: '600px', margin: 'auto' }}>
            <div style={{ height: '400px', overflowY: 'scroll', border: '1px solid #ccc', padding: '10px' }}>
                {/* Render the messages */}
                {messages.map((msg, index) => (
                    <div key={index} style={{ textAlign: msg.sender === 'user' ? 'right' : 'left' }}>
                        <p><strong>{msg.sender}:</strong> {msg.text}</p>
                    </div>
                ))}
            </div>
            <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
                style={{ width: '80%', padding: '10px' }}
            />
            <button onClick={sendMessage} style={{ padding: '10px' }}>Send</button>
        </div>
    );
}

export default RecruiterAgent;
