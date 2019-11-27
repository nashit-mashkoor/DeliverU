class Api::V1::CustomersController < Api::V1::ApiBaseController
    include ApplicationHelper
    before_action :set_customer, only: [:show, :update, :destroy, :update_location]
    #before_action :authenticate_customer!, only: [:show, :update, :destory, :update_location]


    # GET /customers
    def index
        @customers = Customer.all
        render json: @customers, status: 200
    end
    
    # GET /customers/1
    def show
        render json: @customer, status: 200
    end
    
    # POST /customers
    def create
        @customer = Customer.new(customer_params)
        @customer_user_id = current_user 
        current_user.customer_id = @customer
         
        if @customer.save! && current_user.save!
            render json: @customer, status: :created, location: api_v1_customer_url(@customer)
        else
            render json: @customer.errors, status: :unprocessable_entity
        end
    end
    
    # PATCH/PUT /customers/1
    def update
        if @customer.update(customer_params)
            render json: @customer, status: 200
        else
            render json: @customer.errors, status: :unprocessable_entity
        end
    end
  
    # DELETE /customers/1
    def destroy
        @customer.destroy
    end
    
    #PATCH/PUT update customer location
    def update_location
        @region_id = Region.get_customer_region(location_params[:customer_lat], location_params[:customer_lang])
        if @region_id.present?
            @customer.update!(region_id: @region_id, customer_lat: params[:customer_lat], customer_lang: params[:customer_lang])
            render json: {Data: {region_id: @region_id}}, status: 200
        else
            render json: {errors: ['Region not found']}, status: 401 
        end
    end
        

    private
    # Use callbacks to share common setup or constraints between actions.
    def set_customer
        if current_user.customer_id == params[:id].to_i
            @customer = Customer.find(params[:id])
        else
            render json: {errors: ['Customer authentication required']}, status: 401
        end
    end
  
    # Only allow a trusted parameter “white list” through.
    def customer_params
       params.require(:customer).permit(:name, :customer_lat, :customer_lang, :region_id)
    end
    def location_params
        params.require(:customer).permit(:customer_lat, :customer_lang)
    end
end