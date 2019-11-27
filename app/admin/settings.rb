ActiveAdmin.register_page "Settings" do
  menu priority: 1
  content do
    columns do
      column do
        a href: '/admin/admin_users', style: 'text-decoration: none; width: 110px;display:block;' do 
          h3 "Admin", style: 'margin-bottom: 5px;'
          para "Register new Admins"
        end
      end
      column do
        a href: '/admin/customers', style: 'text-decoration: none; width: 110px;display:block;' do 
          h3 "Customers", style: 'margin-bottom: 5px;'
          para "View Customer Account"
        end
      end
      column do
        a href: '/admin/complaints', style: 'text-decoration: none; width: 110px;display:block;' do 
          h3 "Complaints", style: 'margin-bottom: 5px;'
          para "Manage User Complaints"
        end
      end
      column do
        a href: '/admin/orders', style: 'text-decoration: none; width: 110px;display:block;' do 
          h3 "Orders", style: 'margin-bottom: 5px;'
          para "View User Orders"
        end
      end
      column do
        a href: '/admin/regions', style: 'text-decoration: none; width: 110px;display:block;' do 
          h3 "Regions", style: 'margin-bottom: 5px;'
          para "Manage Regions Data"
        end
      end
      column do
        a href: '/admin/drivers', style: 'text-decoration: none; width: 110px;display:block;' do 
          h3 "Drivers", style: 'margin-bottom: 5px;'
          para "Manage Driver Data"
        end
      end
    end
    columns do
      column do
        a href: '/admin/resturants', style: 'text-decoration: none; width: 110px;display: block;' do 
          h3 "Restaurants", style: 'margin-bottom: 5px;'
          para "Manage Restaurant Data"
        end
      end
      column do
        a href: '/admin/grocerrystores', style: 'text-decoration: none; width: 110px;display:block;' do 
          h3 "Grocery", style: 'margin-bottom: 5px;'
          para "Manage Grocery Data"
        end
      end
      column do
        a href: '/admin/timeslots', style: 'text-decoration: none; width: 110px;display:block;' do 
          h3 "Timeslots", style: 'margin-bottom: 5px;'
          para "Manage Timeslots Records"
        end
      end
      column do
      end
      column do
      end
      column do
      end
    end
  end
end