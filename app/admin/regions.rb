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
        column_chart Order.where(timeslot_id: resource.timeslots).group(:timeslot_id).order('COUNT(*) DESC').limit(10).count.map{|k, v| [Timeslot.find(k).start, v] }.to_h
      end
    end
  end

end
