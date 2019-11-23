Rails.application.routes.draw do
  # For admin
  devise_for :admin_users, ActiveAdmin::Devise.config
  ActiveAdmin.routes(self)
  # For authentication
  mount_devise_token_auth_for 'User', at: 'api/v1/auth'
  
  # API routes
  namespace :api do
    namespace :v1 do
      resources :customers
    end
   end

end
