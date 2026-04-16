import api from './api'

export const authService = {
  async register(email, password, passwordConfirm) {
    const response = await api.post('/auth/register', {
      email,
      password,
      password_confirm: passwordConfirm,
    })
    return response.data
  },

  async login(email, password) {
    const response = await api.post('/auth/login', {
      email,
      password,
    })
    
    const { access_token, refresh_token } = response.data
    localStorage.setItem('access_token', access_token)
    localStorage.setItem('refresh_token', refresh_token)
    
    return response.data
  },

  async logout() {
    try {
      await api.post('/auth/logout')
    } finally {
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
    }
  },

  async getCurrentUser() {
    const response = await api.get('/auth/me')
    return response.data
  },

  async changePassword(currentPassword, newPassword, newPasswordConfirm) {
    const response = await api.post('/auth/change-password', {
      current_password: currentPassword,
      new_password: newPassword,
      new_password_confirm: newPasswordConfirm,
    })
    return response.data
  },

  isAuthenticated() {
    return !!localStorage.getItem('access_token')
  },
}

export default authService

