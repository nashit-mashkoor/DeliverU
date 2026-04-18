import { Outlet, Link, useLocation, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { toast } from 'react-toastify'
import './Layout.css'

function Layout() {
  const { user, logout } = useAuth()
  const location = useLocation()
  const navigate = useNavigate()

  const handleLogout = async () => {
    try {
      await logout()
      toast.success('Logged out successfully')
      navigate('/login')
    } catch (error) {
      toast.error('Logout failed')
    }
  }

  const isActive = (path) => location.pathname.startsWith(path)

  return (
    <div className="layout">
        <nav className="navbar">
          <div className="navbar-brand">
            <Link to="/app/dashboard">
              <span className="logo-icon">◆</span>
              <span className="logo-text">DeliverU</span>
            </Link>
          </div>

          <div className="navbar-links">
            <Link
              to="/app/dashboard"
              className={`nav-link ${isActive('/app/dashboard') ? 'active' : ''}`}
            >
              Dashboard
            </Link>
            <Link
              to="/app/items"
              className={`nav-link ${isActive('/app/items') ? 'active' : ''}`}
            >
              Items
            </Link>
          </div>

          <div className="navbar-user">
            <span className="user-email">{user?.email}</span>
            <button onClick={handleLogout} className="btn btn-secondary btn-sm">
              Logout
            </button>
          </div>
        </nav>

      <main className="main-content">
        <Outlet />
      </main>
    </div>
  )
}

export default Layout
