ActiveAdmin.register_page "Analytics" do
  menu priority: 3
  content do
    column_chart Order.joins(:timeslot).group(:region_id).count
  end
end
