class AddQuantityToGrocerryitem < ActiveRecord::Migration[6.0]
  def change
    add_column :grocerryitems, :quantity, :integer, null: true
  end
end
