class ChangeStartEndToBeStringInTimeslot < ActiveRecord::Migration[6.0]
  def up
    change_column :timeslots, :start, :string
    change_column :timeslots, :end, :string
  end
  def down
    change_column :timeslots, :start, :time
    change_column :timeslots, :end, :time
  end
end
