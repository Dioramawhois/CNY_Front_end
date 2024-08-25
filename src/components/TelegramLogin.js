import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const TelegramLogin = () => {
  const navigate = useNavigate();

  useEffect(() => {
    const userId = new URLSearchParams(window.location.search).get('user_id');

    if (userId) {
      fetch(`/api/check-whitelist?user_id=${userId}`)
        .then(response => response.json())
        .then(data => {
          if (data.is_whitelisted) {
            navigate('/message-sender');
          } else {
            alert('You are not authorized to access this page.');
          }
        })
        .catch(error => console.error('Error checking whitelist:', error));
    } else {
      alert('No user_id provided.');
    }
  }, [navigate]);

  return <div>Checking authorization...</div>;
};

export default TelegramLogin;
