import React, { useState } from 'react';
import '../styles/MessageSender.css';

const MessageSender = () => {
    const [message, setMessage] = useState('');
    const [isSending, setIsSending] = useState(false);
    const [logMessages, setLogMessages] = useState([]); // State для логов

    const handleSendMessage = () => {
        setIsSending(true);
        // Имитация отправки сообщения
        setTimeout(() => {
            const log = `Message sent to users: ${message}`;
            addLogMessage(log);
            setIsSending(false);
        }, 1000); // Задержка для имитации отправки
    };

    const handleStopSending = () => {
        setIsSending(false);
        addLogMessage("Message sending stopped.");
    };

    const addLogMessage = (logMessage) => {
        setLogMessages((prevLogs) => [...prevLogs, logMessage]);
    };

    return (
        <div className="message-sender">
            <h2>Message Sender</h2>
            <textarea
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                placeholder="Type your message here..."
                disabled={isSending}
            />
            <div className="button-container">
                <button
                    className="button-64"
                    onClick={handleSendMessage}
                    disabled={isSending}
                >
                    <span className="text">Send Message</span>
                </button>
                <button
                    className="button-64 stop-button"
                    onClick={handleStopSending}
                    disabled={!isSending}
                >
                    <span className="text">Stop Sending</span>
                </button>
            </div>
            <div className="log-container">
                <h3>Log</h3>
                <div className="log-messages">
                    {logMessages.map((log, index) => (
                        <div key={index} className="log-message">
                            {log}
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
};

export default MessageSender;
