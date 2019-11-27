class Api::V1::DriversController < Api::V1::ApiBaseController
    include ApplicationHelper
    before_action :set_driver, only: [:show]
    before_action :authenticate_driver!, only: [:show]


    # GET /Drivers
    def index
        @drivers = Driver.all
        render json: @drivers, status: 200
    end
    
    # GET /drivers/1
    def show
        render json: @driver, status: 200
    end
    
   
        

    private
    # Use callbacks to share common setup or constraints between actions.
    def set_driver
        if current_user.driver_id == params[:id].to_i
            @driver = Driver.find(params[:id])
        else
            render json: {errors: ['Driver authentication required']}, status: 401
        end
    end
  

end