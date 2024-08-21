import React, { useState } from 'react';
import '../styles/UserManager.css';

const UserManager = () => {
  const [users, setUsers] = useState([]); // Состояние для хранения списка пользователей
  const [inputValue, setInputValue] = useState('');

  const handleAddUser = () => {
    if (inputValue.trim()) {
      const newUsers = inputValue
        .split('\n') // Разделяем ввод по строкам
        .map((line, index) => ({ id: users.length + index + 1, name: line.trim() }))
        .filter(user => user.name !== '');
      setUsers([...users, ...newUsers]);
      setInputValue('');
    }
  };

  const handleDeleteUser = (id) => {
    setUsers(users.filter(user => user.id !== id));
  };

  const handleDeleteAllUsers = () => {
    const confirmDelete = window.confirm('Are you sure you want to delete all users?');
    if (confirmDelete) {
      setUsers([]);
    }
  };

  return (
    <div className="user-manager">
      <h2>User Management</h2>
      <textarea
        placeholder="Enter usernames or chat IDs, one per line"
        value={inputValue}
        onChange={(e) => setInputValue(e.target.value)}
      />
      <div className="button-group">
        <button className="add-user-btn" onClick={handleAddUser}>
          Add User/Chat
        </button>
        <button className="delete-all-btn" onClick={handleDeleteAllUsers}>
          Delete All Users
        </button>
      </div>

      <ul className="user-list">
        {users.map((user) => (
          <li key={user.id}>
            {user.name}
            <button className="delete-btn" onClick={() => handleDeleteUser(user.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default UserManager;
