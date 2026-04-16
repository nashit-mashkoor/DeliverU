import { useState, useEffect } from 'react'
import { useForm } from 'react-hook-form'
import { toast } from 'react-toastify'
import itemsService from '../services/items.service'
import './Items.css'

function Items() {
  const [items, setItems] = useState([])
  const [loading, setLoading] = useState(true)
  const [showModal, setShowModal] = useState(false)
  const [editingItem, setEditingItem] = useState(null)

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm()

  useEffect(() => {
    fetchItems()
  }, [])

  const fetchItems = async () => {
    try {
      const data = await itemsService.getItems()
      setItems(data.items)
    } catch (error) {
      toast.error('Failed to fetch items')
    } finally {
      setLoading(false)
    }
  }

  const openModal = (item = null) => {
    setEditingItem(item)
    if (item) {
      reset({ name: item.name, description: item.description || '' })
    } else {
      reset({ name: '', description: '' })
    }
    setShowModal(true)
  }

  const closeModal = () => {
    setShowModal(false)
    setEditingItem(null)
    reset()
  }

  const onSubmit = async (data) => {
    try {
      if (editingItem) {
        await itemsService.updateItem(editingItem.uuid, data)
        toast.success('Item updated')
      } else {
        await itemsService.createItem(data.name, data.description || null)
        toast.success('Item created')
      }
      closeModal()
      fetchItems()
    } catch (error) {
      toast.error(editingItem ? 'Failed to update item' : 'Failed to create item')
    }
  }

  const handleDelete = async (uuid) => {
    if (!confirm('Are you sure you want to delete this item?')) return
    
    try {
      await itemsService.deleteItem(uuid)
      toast.success('Item deleted')
      fetchItems()
    } catch (error) {
      toast.error('Failed to delete item')
    }
  }

  if (loading) {
    return (
      <div className="items-loading">
        <div className="loading-spinner"></div>
      </div>
    )
  }

  return (
    <div className="items-page">
      <header className="items-header">
        <div>
          <h1>Items</h1>
          <p>Manage your items</p>
        </div>
        <button onClick={() => openModal()} className="btn btn-primary">
          + New Item
        </button>
      </header>

      {items.length === 0 ? (
        <div className="items-empty">
          <div className="empty-icon">📦</div>
          <h3>No items yet</h3>
          <p>Create your first item to get started</p>
          <button onClick={() => openModal()} className="btn btn-primary">
            Create Item
          </button>
        </div>
      ) : (
        <div className="items-grid">
          {items.map((item) => (
            <div key={item.uuid} className="item-card">
              <div className="item-header">
                <h3>{item.name}</h3>
                <span className={`item-status ${item.is_active ? 'active' : 'inactive'}`}>
                  {item.is_active ? 'Active' : 'Inactive'}
                </span>
              </div>
              {item.description && (
                <p className="item-description">{item.description}</p>
              )}
              <div className="item-meta">
                <span>Created: {new Date(item.created_at).toLocaleDateString()}</span>
              </div>
              <div className="item-actions">
                <button
                  onClick={() => openModal(item)}
                  className="btn btn-secondary btn-sm"
                >
                  Edit
                </button>
                <button
                  onClick={() => handleDelete(item.uuid)}
                  className="btn btn-danger btn-sm"
                >
                  Delete
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      {showModal && (
        <div className="modal-overlay" onClick={closeModal}>
          <div className="modal" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2>{editingItem ? 'Edit Item' : 'New Item'}</h2>
              <button onClick={closeModal} className="modal-close">×</button>
            </div>
            <form onSubmit={handleSubmit(onSubmit)}>
              <div className="form-group">
                <label htmlFor="name">Name</label>
                <input
                  id="name"
                  type="text"
                  placeholder="Item name"
                  {...register('name', {
                    required: 'Name is required',
                    maxLength: {
                      value: 255,
                      message: 'Name must be less than 255 characters',
                    },
                  })}
                />
                {errors.name && <span className="form-error">{errors.name.message}</span>}
              </div>

              <div className="form-group">
                <label htmlFor="description">Description (optional)</label>
                <textarea
                  id="description"
                  placeholder="Item description"
                  rows={4}
                  {...register('description', {
                    maxLength: {
                      value: 1000,
                      message: 'Description must be less than 1000 characters',
                    },
                  })}
                />
                {errors.description && (
                  <span className="form-error">{errors.description.message}</span>
                )}
              </div>

              <div className="modal-actions">
                <button type="button" onClick={closeModal} className="btn btn-secondary">
                  Cancel
                </button>
                <button type="submit" className="btn btn-primary">
                  {editingItem ? 'Update' : 'Create'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  )
}

export default Items

