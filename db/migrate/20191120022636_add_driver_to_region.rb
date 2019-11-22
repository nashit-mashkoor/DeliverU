class AddDriverToRegion < ActiveRecord::Migration[6.0]
  def change
    add_reference :regions, :driver, null: true, foreign_key: true
  end
end
