ActiveAdmin.register_page "Analytics" do
  menu priority: 3
  content do
    #column_chart AdminUser.group(:created_at).count()
    column_chart Order.group(:timeslot_id).count()

  end
end
