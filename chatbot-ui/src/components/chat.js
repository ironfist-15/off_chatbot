import React, { useEffect, useRef, useState } from 'react';

function Chat() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const bottomRef = useRef(null);

  useEffect(() => {
    if (bottomRef.current) {
        bottomRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages]);

  const sendMessage = async () => {
    const userMessage = input.trim();
    if (!userMessage) return;

    setMessages((prev) => [...prev, { from: 'user', text: userMessage }]);
    setInput('');

    try {
      const res = await fetch('http://localhost:5005/webhooks/rest/webhook', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          sender: 'user1',
          message: userMessage,
        }),
      });

      const data = await res.json();

      data.forEach((msg) => {
        if (msg.text) {
          setMessages((prev) => [...prev, { from: 'bot', text: msg.text }]);
        }
      });
    } catch (error) {
      console.error('Error communicating with Rasa:', error);
    }
  };

  return (
  <div style={{ maxWidth: '600px', margin: 'auto', fontFamily: 'Arial' }}>
    <h2>OpenFoodFacts ChatBot</h2>

    <div
      style={{
        border: '1px solid #ccc',
        padding: '1em',
        height: '300px',
        overflowY: 'auto',
        backgroundColor: '#f9f9f9',
      }}
    >
      {messages.map((msg, i) => (
        <p key={i}>
          <strong>{msg.from}:</strong> {msg.text}
        </p>
      ))}
      <div ref={bottomRef} />
    </div>

    <div style={{ marginTop: '1em' }}>
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
        placeholder="Type your message"
        style={{ width: '80%', padding: '0.5em' }}
      />
      <button onClick={sendMessage} style={{ padding: '0.5em 1em', marginLeft: '0.5em' }}>
        Send
      </button>
    </div>
  </div>
 );
}

export default Chat;
