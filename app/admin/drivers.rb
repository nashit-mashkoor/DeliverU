ActiveAdmin.register Driver do
  menu false
  permit_params :name, :dob, :email, :cnic, :region_id, :driver_license, payables_attributes: [ :_destroy ]

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

    panel "Payables", only: [:show] do
      table_for driver.payables do
        column :amount
        column :category do |payable|
          span payable.typeString, class: payable.color
        end
        column :actions do |payable|
          (link_to I18n.t('active_admin.edit'), edit_admin_driver_payable_path(resource, payable), :method => :get, :confirm => I18n.t('active_admin.edit_confirmation')) + " " +
          (link_to I18n.t('active_admin.delete'), admin_driver_payable_path(resource, payable), :method => :delete, :confirm => I18n.t('active_admin.delete_confirmation'))
        end
      end
      hr
      span 'Total Due:', style: 'font-weight: bold'
      span resource.total_due
      span 'PKR'
      para do
      end
    end
  end

  action_item :createPayable, only: :show do
    link_to 'Create New Payable', new_admin_driver_payable_path(resource.id)
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
