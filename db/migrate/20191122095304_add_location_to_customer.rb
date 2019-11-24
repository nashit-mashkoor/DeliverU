class AddLocationToCustomer < ActiveRecord::Migration[6.0]
  def change
    add_column :customers, :customer_lat, :decimal, {:precision=>10, :scale=>6}
    add_column :customers, :customer_lang, :decimal, {:precision=>10, :scale=>6}
  end
end
