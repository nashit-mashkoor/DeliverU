ActiveAdmin.register Resturant do
  menu false
  permit_params :name, :region_id, :image
  # See permitted parameters documentation:
  # https://github.com/activeadmin/activeadmin/blob/master/docs/2-resource-customization.md#setting-up-strong-parameters
  #
  # Uncomment all parameters which should be permitted for assignment
  #
  # permit_params :name, :region_id
  #
  # or
  #
  # permit_params do
  #   permitted = [:name, :region_id]
  #   permitted << :other if params[:action] == 'create' && current_user.admin?
  #   permitted
  # end

  form do |f|
    f.inputs "Please fill all fields" do
      f.input :region, required: true
      f.input :name, required: true
      f.input :image, required: true, as: :file
    end
    f.actions
  end

end
