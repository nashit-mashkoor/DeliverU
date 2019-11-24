ActiveAdmin.register Resturant do
  menu false
  permit_params :name, :region_id, :menu_image
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

  show do
    attributes_table do
      row :region
      row :name
      row :menu_image do |resturant|
        link_to(image_tag(url_for(resturant.menu_image), style: 'width: 150px; height: 150px; object-fit: cover;'), url_for(resturant.menu_image))
      end
    end
  end

  form do |f|
    f.inputs "Please fill all fields" do
      f.input :region, required: true
      f.input :name, required: true
      f.input :menu_image, required: true, as: :file
    end
    f.actions
  end

end
