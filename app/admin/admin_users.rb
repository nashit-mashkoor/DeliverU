ActiveAdmin.register AdminUser do
  permit_params :email, :password, :password_confirmation
  menu false
  actions :index, :show, :new, :create#, :update
  index do
    selectable_column
    id_column
    column :email
    column :current_sign_in_at
    column :sign_in_count
    column :created_at
    #actions
    #column "" do |resource|
      #links = ''.html_safe
      #links += link_to I18n.t('active_admin.view'), resource_path(resource), class: "member_link show_link"
      #links += link_to I18n.t('active_admin.edit'), edit_resource_path(resource), class: "member_link edit_link"
      #links += link_to I18n.t('active_admin.delete'), resource_path(resource), method: :delete, confirm: I18n.t('active_admin.delete_confirmation'), class: "member_link delete_link"
      #links
    #end
  end

  filter :email
  filter :current_sign_in_at
  filter :sign_in_count
  filter :created_at

  form do |f|
    f.inputs do
      f.input :email
      #f.input :password
      #f.input :password_confirmation
    end
    f.actions
  end

end
