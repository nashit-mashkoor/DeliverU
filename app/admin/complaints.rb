ActiveAdmin.register Complaint do
  menu false
  permit_params :message, :status, :region_id, :customer_id
  actions :index, :show, :update, :edit

  form do |f|
    f.inputs do
      f.input :status
    end
    f.actions
  end
end
