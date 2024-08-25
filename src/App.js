import React, { useEffect, useState } from 'react';
import './App.css';
import MessageSender from './components/MessageSender';
import UserManager from './components/UserManager';
import TelegramLogin from './components/TelegramLogin';

function App() {
  const [isAuthorized, setIsAuthorized] = useState(false);
  const [currentView, setCurrentView] = useState('message-sender');

  useEffect(() => {
    // Проверка авторизации при загрузке приложения
    const checkAuthorization = async () => {
      const userId = new URLSearchParams(window.location.search).get('user_id');
      if (!userId) {
        setIsAuthorized(false);
        return;
      }
      try {
        const response = await fetch(`/api/check-whitelist?user_id=${userId}`);
        const data = await response.json();
        setIsAuthorized(data.authorized);
      } catch (error) {
        console.error('Error checking authorization:', error);
        setIsAuthorized(false);
      }
    };

    checkAuthorization();
  }, []);

  const handleNavigation = (view) => {
    setCurrentView(view);
  };

  if (!isAuthorized) {
    return <TelegramLogin />;
  }

  return (
    <div className="App">
      <header className="App-header">
        <h1>Message Sender</h1>
        <div className="menu">
          <button onClick={() => handleNavigation('message-sender')}>Message Sender</button>
          <button onClick={() => handleNavigation('user-management')}>User Management</button>
        </div>
      </header>
      {currentView === 'message-sender' && <MessageSender />}
      {currentView === 'user-management' && <UserManager />}
    </div>
  );
}

export default App;
