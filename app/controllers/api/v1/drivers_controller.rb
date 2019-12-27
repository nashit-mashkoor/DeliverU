class Api::V1::DriversController < Api::V1::ApiBaseController
    include ApplicationHelper

    before_action :authenticate_user!, :authenticate_driver!, only: [:show, :index, :driver_payables, :payable_amount]
    before_action :set_driver, only: [:show]
    


    # GET /Drivers
    def index
        @drivers = Driver.all
        render json: @drivers, status: 200
    end
    
    # GET /drivers/1
    def show
        render json: @driver, status: 200
    end

    # Get /payables  | Pass params[:filter] outside driver hash | 0 to_pay the amount driver owes 1 to_recieve the amount the driver needs to be payed | Ordered in ascending order
    def driver_payables
        if payables_params.present?
            @payables = Payable.where(category: payables_params[:filter], driver_id: current_user.driver_id).order(:created_at)
        else
            @payables = Payable.all
        end
        render json: @payables, status: 200
    end

    # Get /payable_amount  | Pass params[:filter] outside driver hash | 0 to_pay the amount driver owes 1 to_recieve the amount the driver needs to be payed 
    def payable_amount
        @amount = Payable.where(category: payables_params[:filter], driver_id: current_user.driver_id).sum(:amount)
        render json: {amount: @amount}, status: 200
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


    def payables_params
        params[:filter].permit
    end
  

end