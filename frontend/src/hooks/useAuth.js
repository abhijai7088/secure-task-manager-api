import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

/**
 * Custom hook for authentication state management.
 */
export function useAuth() {
  const navigate = useNavigate();

  const getUser = () => {
    const raw = localStorage.getItem('user');
    return raw ? JSON.parse(raw) : null;
  };

  const [user, setUser] = useState(getUser);

  const login = (token, userData) => {
    localStorage.setItem('token', token);
    localStorage.setItem('user', JSON.stringify(userData));
    setUser(userData);
  };

  const logout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    setUser(null);
    navigate('/login');
  };

  const isAuthenticated = !!localStorage.getItem('token');

  return { user, login, logout, isAuthenticated };
}
