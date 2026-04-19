const ROLE_HOME_PATHS = {
  admin: '/app/admin',
  customer: '/app/customer',
  driver: '/app/driver',
}

export function getUserRole(user) {
  if (!user) {
    return null
  }

  const role = typeof user.role === 'string' ? user.role.toLowerCase() : null
  if (role && ROLE_HOME_PATHS[role]) {
    return role
  }

  return 'customer'
}

export function getRoleHomePath(user) {
  const role = getUserRole(user)

  if (!role) {
    return '/app'
  }

  return ROLE_HOME_PATHS[role]
}
