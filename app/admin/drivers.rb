ActiveAdmin.register Driver do
  menu false
  permit_params :name, :dob, :email, :cnic, :region_id, :driver_license

  show do
    attributes_table do
      row :region
      row :name
      row :dob
      row :email
      row :cnic
      row :driver_license do |driver|
        link_to(image_tag(url_for(driver.driver_license), style: 'width: 150px; height: 150px; object-fit: cover;'), url_for(driver.driver_license))
      end
    end
  end

  form do |f|
    f.inputs "Please fill all fields" do
      f.input :region, required: true
      f.input :name, required: true
      f.input :dob, start_year: 1900, required: true
      f.input :email, required: true
      f.input :cnic, required: true
      f.input :driver_license, required: true, as: :file
    end
    f.actions
  end

end
