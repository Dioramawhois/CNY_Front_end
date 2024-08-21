import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import './styles/App.css';
import MessageSender from './components/MessageSender';
import UserManager from './components/UserManager';

function App() {
  return (
    <Router>
      <div className="App">
        <nav>
          <Link to="/">Message Sender</Link>
          <Link to="/user-manager">User Management</Link>
        </nav>
        <Routes>
          <Route path="/" element={<MessageSender />} />
          <Route path="/user-manager" element={<UserManager />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
