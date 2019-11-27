ActiveAdmin.register Timeslot do
  menu false
  permit_params :start, :region_id

  show do
    attributes_table do
      row :start
      row :region
      row :created_at
      row :updated_at
    end
  end

  form do |f|
    f.inputs "Please fill all fields" do
      f.input :region, required: true
      f.input :start, required: true
    end
    f.actions
  end
end
