ActiveAdmin.register_page "Settings" do
  menu priority: 1
  content do
    (link_to "Admin", '/admin/admin_users') + " " + (link_to "Customers", '/admin/customers') + " " + (link_to "Complaints", '/admin/complaints') + " " + (link_to "Drivers", '/admin/drivers') + " " + (link_to "Regions", '/admin/regions') + " " + (link_to "Orders", '/admin/orders') + " " + (link_to "Restaurants", '/admin/resturants') + " " + (link_to "Grocery", '/admin/grocerrystores') + " " +(link_to "Time Slots", '/admin/timeslots')
  end

end