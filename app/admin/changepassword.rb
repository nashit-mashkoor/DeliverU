ActiveAdmin.register_page "Change Password" do
  menu priority: 2
  content do
    panel 'Please fill all fields' do
      form action: "form1", method: :post do |f|
        f.div style: 'display: flex; align-items: center; justify-content: space-between' do
          f.label "Current Password"
          f.input :current_password, type: :password, placeholder: 'Current Password'
        end
        f.div  style: 'display: flex; align-items: center; justify-content: space-between' do
          f.label "New Password"
          f.input :new_password, type: :password, label: 'New Password', placeholder: 'New Password'
        end
        f.div style: 'display: flex; align-items: center; justify-content: space-between' do
          f.label "Confirm Password"
          f.input :password_confirmation, type: :password, label: 'Confirm Password', placeholder: 'Confirm Password'
        end
        f.div do
          f.input :Submit, type: :submit
        end
      end
    end
  end
end
