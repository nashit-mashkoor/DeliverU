class RemoveDriverIdFromRegion < ActiveRecord::Migration[6.0]
  def change
    remove_column :regions, :driver_id
  end
end
