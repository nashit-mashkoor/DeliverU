ActiveAdmin.register_page "Change Password" do
  menu priority: 2
  content do
    panel 'Please fill all fields' do
      form action: admin_change_password_update_path, method: :post do |f|
        f.input :name => 'authenticity_token', :type => :hidden, :value => form_authenticity_token.to_s
        f.div style: 'display: flex; align-items: center; justify-content: space-between' do
          f.label "Current Password"
          f.input :current_password, type: :password, placeholder: 'Current Password', name: 'current_password'
        end
        f.div  style: 'display: flex; align-items: center; justify-content: space-between' do
          f.label "New Password"
          f.input :new_password, type: :password, label: 'New Password', placeholder: 'New Password', name: 'new_password'
        end
        f.div style: 'display: flex; align-items: center; justify-content: space-between' do
          f.label "Confirm Password"
          f.input :password_confirmation, type: :password, label: 'Confirm Password', placeholder: 'Confirm Password', name: 'password_confirmation'
        end
        f.div do
          f.input :Submit, type: :submit
        end
      end
    end
  end

  page_action :update, method: :post do
    if params[:current_password].empty?
      flash[:error] = 'Current password is required'
      redirect_to admin_change_password_path
      return
    end
    if params[:new_password].empty?
      flash[:error] = 'New password is required'
      redirect_to admin_change_password_path
      return
    end
    if params[:password_confirmation].empty?
      flash[:error] = 'Confirm password is required'
      redirect_to admin_change_password_path
      return
    end

    if not current_admin_user.valid_password?(params[:current_password])
      flash[:error] = 'Current password is incorrect'
      redirect_to admin_change_password_path
      return
    end

    if not params[:new_password] == params[:password_confirmation]
      flash[:error] = 'Passwords donot match'
      redirect_to admin_change_password_path
      return
    end

    current_admin_user.password = params[:new_password]
    current_admin_user.password_confirmation = params[:password_confirmation]
    current_admin_user.save!
    flash[:notice] = 'Password updated successfully'
    redirect_to admin_dashboard_path
  end
end
