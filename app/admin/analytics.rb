ActiveAdmin.register_page "Analytics" do
  menu priority: 3
  content do
    column_chart Order.joins(:timeslot).group(:region_id).order('COUNT(*) DESC').limit(10).count.map{|k, v| [Region.find(k).name, v] }.to_h
  end
end
