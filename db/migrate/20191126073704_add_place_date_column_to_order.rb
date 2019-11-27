class AddPlaceDateColumnToOrder < ActiveRecord::Migration[6.0]
  def change
    add_column :orders, :place_date, :date, null: true
  end
end
