import React, { useState, useEffect } from 'react';
import MessageSender from './components/MessageSender';
import UserManager from './components/UserManager';
import TelegramLogin from './components/TelegramLogin';
import './styles/App.css';

function App() {
  const [view, setView] = useState('message-sender');
  const [isAuthorized, setIsAuthorized] = useState(false);
  const [isCheckingAuth, setIsCheckingAuth] = useState(true); // New state for checking auth

  useEffect(() => {
    const urlParams = new URLSearchParams(window.location.search);
    const userId = urlParams.get('user_id');

    if (userId) {
      fetch(`/api/check-whitelist?user_id=${userId}`)
        .then(response => response.json())
        .then(data => {
          if (data.authorized) {
            setIsAuthorized(true);
          } else {
            setIsAuthorized(false);
          }
          setIsCheckingAuth(false); // Finish checking
        })
        .catch(error => {
          console.error('Error checking whitelist:', error);
          setIsCheckingAuth(false);
        });
    } else {
      setIsAuthorized(false);
      setIsCheckingAuth(false);
    }
  }, []);

  if (isCheckingAuth) {
    return <div>Checking authorization...</div>; // New loading state
  }

  if (!isAuthorized) {
    return <TelegramLogin />; // Redirect to a login component
  }

  return (
    <div className="App">
      <header className="App-header">
        <h1>Umbrella CNY bot</h1>
        <nav>
          <button className={view === 'message-sender' ? 'active' : ''} onClick={() => setView('message-sender')}>Message Sender</button>
          <button className={view === 'user-management' ? 'active' : ''} onClick={() => setView('user-management')}>User Management</button>
        </nav>
      </header>
      <main>
        {view === 'message-sender' && <MessageSender />}
        {view === 'user-management' && <UserManager />}
      </main>
    </div>
  );
}

export default App;
