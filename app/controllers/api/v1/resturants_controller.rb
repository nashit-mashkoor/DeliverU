class Api::V1::ResturantsController < Api::V1::ApiBaseController
    before_action :authenticate_user!
    # GET /resturants
    # For both customer and driver
    def index
        if(current_user.customer_id?)
           @resturants = Resturant.where("region_id = ?", current_user.customer.region_id)
        else
            @resturants = Resturant.where("region_id = ?", current_user.driver.region_id)
        end
       
        render json: @resturants, status: 200
    end
end