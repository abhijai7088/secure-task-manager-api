import { Navigate } from 'react-router-dom';

/**
 * Wraps a route so only authenticated users can access it.
 */
export default function ProtectedRoute({ children }) {
  const token = localStorage.getItem('token');
  if (!token) {
    return <Navigate to="/login" replace />;
  }
  return children;
}
