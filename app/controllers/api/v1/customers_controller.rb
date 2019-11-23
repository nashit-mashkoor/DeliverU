class Api::V1::CustomersController < Api::V1::ApiBaseController
    before_action :set_customer, only: [:show, :update, :destroy]
    
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
        if @customer.save
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
  
    private
    # Use callbacks to share common setup or constraints between actions.
    def set_customer
        @customer = Customer.find(params[:id])
    end
  
    # Only allow a trusted parameter “white list” through.
    def customer_params
       params.require(:customer).permit(:id, :name, :email, :customer_lat, :customer_lang, :region_id)
    end
end