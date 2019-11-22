class UpdateRegionDriver < ActiveRecord::Migration[6.0]
  def change
    remove_reference :regions, :driver, null: true, foreign_key: true
    add_reference :regions, :driver, null: true, foreign_key: true
  end
end
