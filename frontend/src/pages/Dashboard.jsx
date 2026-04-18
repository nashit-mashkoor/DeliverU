import { useAuth } from '../context/AuthContext'
import './Dashboard.css'

function Dashboard() {
  const { user } = useAuth()

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <h1>DeliverU Operations</h1>
        <p>Welcome back, {user?.email}. Core modules are being enabled in sequence.</p>
      </header>

      <div className="dashboard-grid">
        <div className="stat-card">
          <div className="stat-icon">🚀</div>
          <div className="stat-content">
            <h3>Foundation Active</h3>
            <p>Authentication and app shell are live for DeliverU implementation</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">🧭</div>
          <div className="stat-content">
            <h3>Routing Enabled</h3>
            <p>API routing is active and ready for real DeliverU domain modules</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">🔒</div>
          <div className="stat-content">
            <h3>Secure Access</h3>
            <p>JWT authentication protects access to authenticated API flows</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">🛒</div>
          <div className="stat-content">
            <h3>Next Up</h3>
            <p>Regions, delivery slots, drivers, and grocery catalog modules</p>
          </div>
        </div>
      </div>

      <section className="dashboard-section">
        <h2>Current Scope</h2>
        <div className="info-card">
          <p>
            This workspace is now aligned for phased DeliverU development with:
          </p>
          <ul>
            <li><strong>Auth APIs</strong> - Register, login, refresh, and profile access</li>
            <li><strong>API Foundation</strong> - Active `/api/v1` routing without placeholder blockers</li>
            <li><strong>Frontend Shell</strong> - Authenticated app layout ready for role-aware pages</li>
            <li><strong>Next Slice Ready</strong> - Real domain modules can now be added incrementally</li>
          </ul>
        </div>
      </section>
    </div>
  )
}

export default Dashboard
