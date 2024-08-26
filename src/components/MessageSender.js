import React, { useState, useEffect } from 'react';
import '../styles/MessageSender.css';
import io from 'socket.io-client';

const socket = io('http://localhost:5000', { transports: ['websocket', 'polling'] }); // Укажите правильный URL и порт

const MessageSender = () => {
  const [message, setMessage] = useState('');
  const [log, setLog] = useState([]);
  const [isSending, setIsSending] = useState(false);

  useEffect(() => {
    // Обработчик события для получения логов от сервера
    socket.on('log', (data) => {
      console.log('Received log from server:', data);
      setLog((prevLog) => [...prevLog, data.message]);
    });

    return () => {
      socket.off('log'); // Отключаем socket при размонтировании компонента
    };
  }, []);

  const handleMessageChange = (e) => {
    setMessage(e.target.value);
  };

  const sendMessage = async () => {
    if (!message.trim()) {
      setLog((prevLog) => [...prevLog, 'Message cannot be empty.']);
      return;
    }

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
        setMessage(''); // Clear the input after sending
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
    <div className="message-sender">
      <h2>Message Sender</h2>
      <input
        type="text"
        value={message}
        onChange={handleMessageChange}
        placeholder="Enter your message here"
      />
      <div className="button-group">
        <button onClick={sendMessage} disabled={isSending}>
          {isSending ? 'Sending...' : 'Send Message'}
        </button>
        <button onClick={stopSending} disabled={!isSending}>
          Stop Sending
        </button>
      </div>
      <div className="log-container">
        <h3>Log</h3>
        <div className="log-messages">
          {log.map((entry, index) => (
            <p key={index} className="log-message">{entry}</p>
          ))}
        </div>
      </div>
    </div>
  );
};

export default MessageSender;
