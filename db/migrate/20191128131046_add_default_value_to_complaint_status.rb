class AddDefaultValueToComplaintStatus < ActiveRecord::Migration[6.0]
  def up
    change_column_default :complaints, :status, 0
  end

  def down
      change_column_default :complaints, :status, nil
  end
end
