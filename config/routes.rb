Rails.application.routes.draw do
  # For admin
  devise_for :admin_users, ActiveAdmin::Devise.config
  ActiveAdmin.routes(self)
  # For authentication
  mount_devise_token_auth_for 'User', at: 'auth'
  
  # API routes
  namespace :api do
    namespace :v1 do
      resources :drivers, only: [:show, :index] do
        collection do
          get 'driver_payables', to: 'drivers#driver_payables', as: 'driver_payables' 
          get 'payable_amount', to: 'drivers#payable_amount', as: 'payable_amount' 
        end
      end
      resources :customers do
        member do
          put 'update_location', to: 'customers#update_location', as: 'update_location'  
        end
        collection do
          get 'region_driver', to: 'customers#region_driver', as: 'region_driver'
        end
      end
      resources :timeslots do
        collection do
          get 'region_slots/:region_id', to: 'timeslots#region_slots', as: 'region_slots' 
        end
      end
      resources :orders, only: [:index, :show, :create, :update]  do
        member do
          put 'cancel', to: 'orders#cancel', as:  'cancel'
          put 'mark_order_complete', to: 'orders#mark_order_complete', as: 'mark_order_complete'
        end
        collection do
          get 'customer_recurring_orders', to: 'orders#customer_recurring_orders', as: 'customer_recurring_orders' 
          get 'customer_single_orders', to: 'orders#customer_single_orders', as: 'customer_single_orders' 
          get 'driver_recurring_orders', to: 'orders#driver_recurring_orders', as: 'driver_recurring_orders' 
          get 'driver_single_orders', to: 'orders#driver_single_orders', as: 'driver_single_orders' 
          get 'driver_history', to: 'orders#driver_history', as: 'driver_history' 
        end
      
      end
      resources :grocerrystores, only: [:index]
      resources :resturants, only: [:index]
      resources :complaints, only: [:show, :index, :create, :update, :destroy]
    end
  end

end
