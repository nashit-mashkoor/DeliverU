class AddDriverToUser < ActiveRecord::Migration[6.0]
  def change
    add_reference :users, :driver, null: true
  end
end
