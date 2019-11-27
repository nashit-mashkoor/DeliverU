ActiveAdmin.register Timeslot do
  menu false
  permit_params :start, :end, :region_id

end
