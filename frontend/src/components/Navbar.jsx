import { Link } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';

/**
 * Top navigation bar.
 */
export default function Navbar() {
  const { user, logout, isAuthenticated } = useAuth();

  return (
    <header className="navbar">
      <Link to="/" className="logo">TaskManager</Link>
      <nav>
        {isAuthenticated ? (
          <>
            <Link to="/dashboard">Dashboard</Link>
            <Link to="/tasks">Tasks</Link>
            <span className="text-muted" style={{ fontSize: '0.8rem' }}>
              {user?.name || 'User'}
            </span>
            <button onClick={logout}>Logout</button>
          </>
        ) : (
          <>
            <Link to="/login">Login</Link>
            <Link to="/register">Register</Link>
          </>
        )}
      </nav>
    </header>
  );
}
