class RenamePayableType < ActiveRecord::Migration[6.0]
  def change
    rename_column :payables, :type, :category
  end
end
