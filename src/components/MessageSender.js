import React, { useState } from 'react';

const MessageSender = () => {
  const [message, setMessage] = useState('');
  const [log, setLog] = useState([]);
  const [isSending, setIsSending] = useState(false);

  const handleMessageChange = (e) => {
    setMessage(e.target.value);
  };

  const sendMessage = async () => {
    try {
      const response = await fetch('/api/start', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message })
      });

      if (response.ok) {
        const data = await response.json();
        setLog((prevLog) => [...prevLog, `Message sent to users: ${data.echo}`]);
        setIsSending(true);
      } else {
        setLog((prevLog) => [...prevLog, 'Error sending message']);
      }
    } catch (error) {
      setLog((prevLog) => [...prevLog, `Error: ${error.message}`]);
    }
  };

  const stopSending = async () => {
    try {
      const response = await fetch('/api/stop', {
        method: 'POST',
      });

      if (response.ok) {
        setLog((prevLog) => [...prevLog, 'Message sending stopped.']);
        setIsSending(false);
      } else {
        setLog((prevLog) => [...prevLog, 'Error stopping message sending.']);
      }
    } catch (error) {
      setLog((prevLog) => [...prevLog, `Error: ${error.message}`]);
    }
  };

  return (
    <div>
      <h2>Message Sender</h2>
      <input
        type="text"
        value={message}
        onChange={handleMessageChange}
        placeholder="Enter your message here"
      />
      <button onClick={sendMessage} disabled={isSending}>
        Send Message
      </button>
      <button onClick={stopSending} disabled={!isSending}>
        Stop Sending
      </button>
      <div className="log">
        <h3>Log</h3>
        {log.map((entry, index) => (
          <p key={index}>{entry}</p>
        ))}
      </div>
    </div>
  );
};

export default MessageSender;
