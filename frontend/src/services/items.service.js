import api from './api'

export const itemsService = {
  async getItems(limit = 100, offset = 0) {
    const response = await api.get('/items', {
      params: { limit, offset },
    })
    return response.data
  },

  async getItem(uuid) {
    const response = await api.get(`/items/${uuid}`)
    return response.data
  },

  async createItem(name, description = null) {
    const response = await api.post('/items', {
      name,
      description,
    })
    return response.data
  },

  async updateItem(uuid, data) {
    const response = await api.patch(`/items/${uuid}`, data)
    return response.data
  },

  async deleteItem(uuid) {
    const response = await api.delete(`/items/${uuid}`)
    return response.data
  },
}

export default itemsService

