import React from 'react';

const TelegramLogin = () => {
  return (
    <div style={{ textAlign: 'center', color: 'white', marginTop: '50px' }}>
      <h2>Please login via Telegram.</h2>
      <p>Make sure you have a valid user_id.</p>
      {/* Optionally add a button or a link to redirect users to the Telegram auth */}
    </div>
  );
};

export default TelegramLogin;
