import { useAuth } from '../context/AuthContext'
import './Dashboard.css'

function Dashboard() {
  const { user } = useAuth()

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <h1>Dashboard</h1>
        <p>Welcome back, {user?.email}</p>
      </header>

      <div className="dashboard-grid">
        <div className="stat-card">
          <div className="stat-icon">👋</div>
          <div className="stat-content">
            <h3>Welcome</h3>
            <p>Your account is active and ready to use</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">📦</div>
          <div className="stat-content">
            <h3>Items</h3>
            <p>Manage your items in the Items section</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">🔒</div>
          <div className="stat-content">
            <h3>Secure</h3>
            <p>Your data is protected with JWT authentication</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">⚡</div>
          <div className="stat-content">
            <h3>Fast</h3>
            <p>Built with FastAPI and React for performance</p>
          </div>
        </div>
      </div>

      <section className="dashboard-section">
        <h2>Getting Started</h2>
        <div className="info-card">
          <p>
            This is a template application showcasing a full-stack architecture with:
          </p>
          <ul>
            <li><strong>FastAPI</strong> - High-performance Python backend</li>
            <li><strong>React</strong> - Modern frontend with Vite</li>
            <li><strong>PostgreSQL</strong> - Robust database</li>
            <li><strong>Redis</strong> - Caching and background jobs</li>
            <li><strong>JWT Auth</strong> - Secure authentication</li>
          </ul>
        </div>
      </section>
    </div>
  )
}

export default Dashboard

