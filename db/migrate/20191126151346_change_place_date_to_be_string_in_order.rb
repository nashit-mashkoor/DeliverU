class ChangePlaceDateToBeStringInOrder < ActiveRecord::Migration[6.0]
  def up
    change_column :orders, :place_date, :string
  end
  def down
    change_column :orders, :place_date, :time
  end
end
