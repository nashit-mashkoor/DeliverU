ActiveAdmin.register Region do
  menu false
  permit_params :name, :driver_id

  show do
    attributes_table do
      row :name
      row :driver_id
      #row :driver_license do |driver|
        #link_to(image_tag(url_for(driver.driver_license), style: 'width: 150px; height: 150px; object-fit: cover;'), url_for(driver.driver_license))
      #end
      column_chart Order.group(:timeslot_id).count()
    end
  end

end
