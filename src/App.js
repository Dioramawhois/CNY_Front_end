import React, { useState, useEffect } from 'react';
import MessageSender from './components/MessageSender';
import UserManager from './components/UserManager';

function App() {
  const [isAuthorized, setIsAuthorized] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Получаем user_id из параметра URL
    const userId = new URLSearchParams(window.location.search).get('user_id');
    
    if (!userId) {
      setLoading(false);
      return;
    }

    // Проверка user_id через API
    fetch(`/api/check-whitelist?user_id=${userId}`)
      .then(response => response.json())
      .then(data => {
        if (data.status === 'success' && data.authorized) {
          setIsAuthorized(true);
        }
        setLoading(false);
      })
      .catch(error => {
        console.error('Error fetching whitelist status:', error);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      {isAuthorized ? (
        <div>
          {/* Здесь ваш основной контент */}
          <MessageSender />
          <UserManager />
        </div>
      ) : (
        <div>Вы не авторизованы для входа в эту страницу.</div>
      )}
    </div>
  );
}

export default App;
