class AddEnumsToOrder < ActiveRecord::Migration[6.0]
  def change
    add_column :orders, :category, :integer, default: 0
    add_column :orders, :status, :integer, default: 0
    add_column :orders, :created_by, :integer, default: 0
  end
end
