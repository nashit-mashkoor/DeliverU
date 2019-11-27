ActiveAdmin.register_page "Analytics" do
  menu priority: 3
  content do
    column_chart resource.get_all_orders.count().order(:count).limit(10)
  end
end
