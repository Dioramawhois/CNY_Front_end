import React, { useState } from 'react';
import '../styles/MessageSender.css';

function MessageSender() {
  const [message, setMessage] = useState('');

  const handleSendMessage = () => {
    // логика для отправки сообщения
    console.log('Message sent:', message);
  };

  const handleStopSending = () => {
    // логика для остановки отправки сообщений
    console.log('Sending stopped');
  };

  return (
    <div className="message-sender">
      <textarea
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder="Type your message here..."
      />
      <div className="button-group">
        <button className="button-64" onClick={handleSendMessage}>
          <span className="text">Send Message</span>
        </button>
        <button className="button-64" onClick={handleStopSending}>
          <span className="text">Stop Sending</span>
        </button>
      </div>
    </div>
  );
}

export default MessageSender;
