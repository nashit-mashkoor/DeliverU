class AddLocationToRegion < ActiveRecord::Migration[6.0]
  def change
    add_column :regions, :TlLat, :decimal, {:precision=>10, :scale=>6}
    add_column :regions, :TlLong, :decimal, {:precision=>10, :scale=>6}
    add_column :regions, :BrLat, :decimal, {:precision=>10, :scale=>6}
    add_column :regions, :BrLong, :string, {:precision=>10, :scale=>6}
  end
end
