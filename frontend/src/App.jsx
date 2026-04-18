import { Routes, Route, Navigate } from 'react-router-dom'
import { useAuth } from './context/AuthContext'
import Layout from './components/Layout'
import Landing from './pages/Landing'
import Login from './pages/Login'
import Register from './pages/Register'
import Dashboard from './pages/Dashboard'
import { getRoleHomePath, getUserRole } from './utils/roleHome'

function ProtectedRoute({ children }) {
  const { isAuthenticated, loading } = useAuth()
  
  if (loading) {
    return (
      <div className="loading-screen">
        <div className="loading-spinner"></div>
      </div>
    )
  }
  
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />
  }
  
  return children
}

function PublicRoute({ children }) {
  const { isAuthenticated, loading, user } = useAuth()
  
  if (loading) {
    return (
      <div className="loading-screen">
        <div className="loading-spinner"></div>
      </div>
    )
  }
  
  if (isAuthenticated) {
    return <Navigate to={getRoleHomePath(user)} replace />
  }
  
  return children
}

function RoleHomeRedirect() {
  const { user } = useAuth()
  return <Navigate to={getRoleHomePath(user)} replace />
}

function RequireAdminRoute({ children }) {
  const { user } = useAuth()
  const role = getUserRole(user)

  if (role !== 'admin') {
    return <Navigate to={getRoleHomePath(user)} replace />
  }

  return children
}

function RequireCustomerRoute({ children }) {
  const { user } = useAuth()
  const role = getUserRole(user)

  if (role === 'customer') {
    return children
  }

  return <Navigate to={getRoleHomePath(user)} replace />
}

function RequireDriverRoute({ children }) {
  const { user } = useAuth()
  const role = getUserRole(user)

  if (role === 'driver') {
    return children
  }

  return <Navigate to={getRoleHomePath(user)} replace />
}

function App() {
  return (
    <>
      <div className="bg-pattern" />
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/login" element={
          <PublicRoute>
            <Login />
          </PublicRoute>
        } />
        <Route path="/register" element={
          <PublicRoute>
            <Register />
          </PublicRoute>
        } />
        <Route path="/app" element={
          <ProtectedRoute>
            <Layout />
          </ProtectedRoute>
        }>
          <Route index element={<RoleHomeRedirect />} />
          <Route path="dashboard" element={<RoleHomeRedirect />} />
          <Route path="customer" element={<RequireCustomerRoute><Dashboard /></RequireCustomerRoute>} />
          <Route path="driver" element={<RequireDriverRoute><Dashboard /></RequireDriverRoute>} />
          <Route path="admin" element={<RequireAdminRoute><Dashboard /></RequireAdminRoute>} />
        </Route>
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </>
  )
}

export default App
