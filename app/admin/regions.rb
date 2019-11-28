ActiveAdmin.register Region do
  menu false
  permit_params :name, :TlLat, :TlLong, :BrLat, :BrLong

  show do
    attributes_table do
      row :name
      row :driver
      # row :driver_license do |driver|
      #   link_to(image_tag(url_for(driver.driver_license), style: 'width: 150px; height: 150px; object-fit: cover;'), url_for(driver.driver_license))
      # end
      row :analytics do
        column_chart resource.get_all_orders.count()
      end
    end
  end

end
