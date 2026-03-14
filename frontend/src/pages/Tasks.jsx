import { useEffect, useState } from 'react';
import client from '../api/client';

export default function Tasks() {
  const [tasks, setTasks] = useState([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [statusFilter, setStatusFilter] = useState('');
  const [search, setSearch] = useState('');
  const [showModal, setShowModal] = useState(false);
  const [editing, setEditing] = useState(null);
  const [form, setForm] = useState({ title: '', description: '', status: 'pending' });
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const perPage = 20;

  const fetchTasks = async () => {
    try {
      const params = { page, per_page: perPage };
      if (statusFilter) params.status = statusFilter;
      if (search) params.search = search;
      const res = await client.get('/tasks', { params });
      setTasks(res.data.data);
      setTotal(res.data.total);
    } catch {
      setError('Failed to load tasks');
    }
  };

  useEffect(() => {
    fetchTasks();
  }, [page, statusFilter, search]);

  const openCreate = () => {
    setEditing(null);
    setForm({ title: '', description: '', status: 'pending' });
    setShowModal(true);
    setError('');
  };

  const openEdit = (task) => {
    setEditing(task);
    setForm({ title: task.title, description: task.description || '', status: task.status });
    setShowModal(true);
    setError('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    try {
      if (editing) {
        await client.put(`/tasks/${editing.id}`, form);
        setSuccess('Task updated');
      } else {
        await client.post('/tasks', form);
        setSuccess('Task created');
      }
      setShowModal(false);
      fetchTasks();
      setTimeout(() => setSuccess(''), 3000);
    } catch (err) {
      setError(err.response?.data?.detail || 'Operation failed');
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Delete this task?')) return;
    try {
      await client.delete(`/tasks/${id}`);
      setSuccess('Task deleted');
      fetchTasks();
      setTimeout(() => setSuccess(''), 3000);
    } catch {
      setError('Failed to delete task');
    }
  };

  const totalPages = Math.ceil(total / perPage);

  return (
    <div className="container">
      <div className="page-header">
        <h1>Tasks</h1>
        <button className="btn btn-primary" onClick={openCreate}>+ New Task</button>
      </div>

      {error && <div className="alert alert-error">{error}</div>}
      {success && <div className="alert alert-success">{success}</div>}

      {/* Filters */}
      <div className="filters">
        <input
          type="text"
          placeholder="Search tasks…"
          value={search}
          onChange={(e) => { setSearch(e.target.value); setPage(1); }}
        />
        <select value={statusFilter} onChange={(e) => { setStatusFilter(e.target.value); setPage(1); }}>
          <option value="">All Statuses</option>
          <option value="pending">Pending</option>
          <option value="in_progress">In Progress</option>
          <option value="completed">Completed</option>
        </select>
      </div>

      {/* Task list */}
      {tasks.length === 0 ? (
        <div className="empty-state">
          <p>No tasks found.</p>
          <button className="btn btn-outline" onClick={openCreate}>Create your first task</button>
        </div>
      ) : (
        <div className="task-list">
          {tasks.map((task) => (
            <div key={task.id} className="task-item">
              <div className="task-info">
                <h3>{task.title}</h3>
                <p>{task.description || 'No description'}</p>
              </div>
              <div className="task-actions">
                <span className={`badge badge-${task.status}`}>
                  {task.status.replace('_', ' ')}
                </span>
                <button className="btn btn-outline btn-sm" onClick={() => openEdit(task)}>Edit</button>
                <button className="btn btn-danger btn-sm" onClick={() => handleDelete(task.id)}>Delete</button>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Pagination */}
      {totalPages > 1 && (
        <div style={{ display: 'flex', justifyContent: 'center', gap: '0.5rem', marginTop: '1.5rem' }}>
          <button className="btn btn-outline btn-sm" disabled={page <= 1} onClick={() => setPage(page - 1)}>
            ← Prev
          </button>
          <span className="text-muted" style={{ alignSelf: 'center' }}>
            Page {page} of {totalPages}
          </span>
          <button className="btn btn-outline btn-sm" disabled={page >= totalPages} onClick={() => setPage(page + 1)}>
            Next →
          </button>
        </div>
      )}

      {/* Create / Edit Modal */}
      {showModal && (
        <div className="modal-overlay" onClick={() => setShowModal(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <h2>{editing ? 'Edit Task' : 'New Task'}</h2>
            {error && <div className="alert alert-error">{error}</div>}
            <form onSubmit={handleSubmit}>
              <div className="form-group">
                <label htmlFor="task-title">Title</label>
                <input
                  id="task-title"
                  value={form.title}
                  onChange={(e) => setForm({ ...form, title: e.target.value })}
                  required
                />
              </div>
              <div className="form-group">
                <label htmlFor="task-desc">Description</label>
                <textarea
                  id="task-desc"
                  value={form.description}
                  onChange={(e) => setForm({ ...form, description: e.target.value })}
                />
              </div>
              <div className="form-group">
                <label htmlFor="task-status">Status</label>
                <select
                  id="task-status"
                  value={form.status}
                  onChange={(e) => setForm({ ...form, status: e.target.value })}
                >
                  <option value="pending">Pending</option>
                  <option value="in_progress">In Progress</option>
                  <option value="completed">Completed</option>
                </select>
              </div>
              <div style={{ display: 'flex', gap: '0.75rem' }}>
                <button className="btn btn-primary" type="submit">
                  {editing ? 'Update' : 'Create'}
                </button>
                <button className="btn btn-outline" type="button" onClick={() => setShowModal(false)}>
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
