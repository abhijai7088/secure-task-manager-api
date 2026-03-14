import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import client from '../api/client';
import { useAuth } from '../hooks/useAuth';

export default function Dashboard() {
  const { user } = useAuth();
  const [stats, setStats] = useState({ total: 0, pending: 0, in_progress: 0, completed: 0 });

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const res = await client.get('/tasks', { params: { per_page: 100 } });
        const tasks = res.data.data;
        setStats({
          total: res.data.total,
          pending: tasks.filter((t) => t.status === 'pending').length,
          in_progress: tasks.filter((t) => t.status === 'in_progress').length,
          completed: tasks.filter((t) => t.status === 'completed').length,
        });
      } catch {
        // ignore
      }
    };
    fetchStats();
  }, []);

  return (
    <div className="container">
      <div className="page-header">
        <h1>Dashboard</h1>
      </div>

      <p style={{ marginBottom: '2rem', color: 'var(--color-text-secondary)' }}>
        Welcome back, <strong>{user?.name || 'User'}</strong>!
        {user?.role === 'admin' && (
          <span className="badge badge-in_progress" style={{ marginLeft: '0.5rem' }}>
            Admin
          </span>
        )}
      </p>

      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-value">{stats.total}</div>
          <div className="stat-label">Total Tasks</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">{stats.pending}</div>
          <div className="stat-label">Pending</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">{stats.in_progress}</div>
          <div className="stat-label">In Progress</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">{stats.completed}</div>
          <div className="stat-label">Completed</div>
        </div>
      </div>

      <Link to="/tasks" className="btn btn-primary">View All Tasks →</Link>
    </div>
  );
}
