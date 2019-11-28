ActiveAdmin.register Region do
  menu false
  # actions :index, :show, :update, :edit, :new, :create
  actions :all

  show do
    attributes_table do
      row :name
      row :driver
      row :TlLat
      row :TlLong
      row :BrLat
      row :BrLong
      # row :driver_license do |driver|
      #   link_to(image_tag(url_for(driver.driver_license), style: 'width: 150px; height: 150px; object-fit: cover;'), url_for(driver.driver_license))
      # end
      row :analytics do
        column_chart Order.where(timeslot_id: resource.timeslots).group(:timeslot_id).order('COUNT(*) DESC').limit(10).count.map{|k, v| [Timeslot.find(k).start, v] }.to_h
      end
    end
  end

  

  form partial: 'region_map', locals: { resource: @resource }

  controller do
    def permitted_params
      params.permit [:authenticity_token, :commit, :name, :TlLat, :TlLong, :BrLat, :BrLong, :id]
    end

    def create
      region_params = [:name, :TlLat, :TlLong, :BrLat, :BrLong]

      region_data = {}
      region_params.each{|k| region_data[k] = permitted_params[k]}
      

      region = Region.new(region_data)
      region.save!

      redirect_to admin_regions_path()
    end

    def update
      region_params = [:name, :TlLat, :TlLong, :BrLat, :BrLong]

      region_data = {}
      region_params.each{|k| region_data[k] = permitted_params[k]}
      

      region = Region.find(permitted_params[:id]).update_attributes(region_data)
      # region.save!

      redirect_to admin_region_path(resource)
    end
  end


end
