module ApplicationHelper

    def authenticate_customer!
       render json: {errors: ['Customer authentication required']}, status: 401 unless current_user.customer_id?
    end

    def authenticate_driver!
        render json: {errors: ['Driver authentication required']}, status: 401 unless current_user.driver_id?
    end
end
