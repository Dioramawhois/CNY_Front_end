import React, { useState, useEffect } from 'react';
import '../styles/UserManager.css';

const UserManager = () => {
  const [users, setUsers] = useState([]);
  const [newUsers, setNewUsers] = useState('');

  useEffect(() => {
    fetchUsers();
  }, []);

  const fetchUsers = async () => {
    try {
      const response = await fetch('/api/users/list');
      const data = await response.json();
      setUsers(data);
    } catch (error) {
      console.error('Error fetching users:', error);
    }
  };

  const handleAddUsers = async () => {
    if (!newUsers.trim()) return;
    
    try {
      const response = await fetch('/api/users/add', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ users: newUsers })
      });

      if (response.ok) {
        setNewUsers('');
        fetchUsers();
      } else {
        console.error('Failed to add users');
      }
    } catch (error) {
      console.error('Error adding users:', error);
    }
  };

  const handleDeleteUser = async (userId) => {
    try {
      const response = await fetch('/api/users/delete', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ user_id: userId })
      });

      if (response.ok) {
        fetchUsers();
      } else {
        console.error('Failed to delete user');
      }
    } catch (error) {
      console.error('Error deleting user:', error);
    }
  };

  const handleDeleteAllUsers = async () => {
    try {
      // Добавьте запрос к серверу для удаления всех пользователей
      await fetch('/api/users/delete-all', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        }
      });
      fetchUsers();
    } catch (error) {
      console.error('Error deleting all users:', error);
    }
  };

  return (
    <div className="user-manager">
      <h2>User Management</h2>
      <textarea
        value={newUsers}
        onChange={(e) => setNewUsers(e.target.value)}
        placeholder="Add users (by ID, link, or @username, each on a new line)"
      />
      <div className="button-group">
        <button className="add-user-btn" onClick={handleAddUsers}>Add User(s)</button>
        <button className="delete-all-btn" onClick={handleDeleteAllUsers}>Delete All Users</button>
      </div>
      <h3>Current Users</h3>
      <ul className="user-list">
        {users.map((user) => (
          <li key={user.userid}>
            {user.username || user.userid}
            <button className="delete-btn" onClick={() => handleDeleteUser(user.userid)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default UserManager;
