import { Outlet, Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { toast } from 'react-toastify'
import './Layout.css'

function Layout() {
  const { user, logout } = useAuth()
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

  return (
    <div className="layout">
        <nav className="navbar">
          <div className="navbar-brand">
            <Link to="/app" className="brand-link" aria-label="Go to home">
              <span className="logo-icon">◆</span>
              <span className="logo-text">DeliverU</span>
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
