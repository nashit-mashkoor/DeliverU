class Api::V1::ComplaintsController < Api::V1::ApiBaseController
    include ApplicationHelper
    before_action :set_complaint, only: [:show, :update]
    before_action :authenticate_customer!, only: [:index, :show, :update, :destory, :create]


    #You pass in param filter
    # If 0 gets pending 
    # If 1 gets resolved
    # No params gets all the results
    # GET /complaints
    def index
        if index_params.present?
            @complaints = Complaint.where(status: index_params[:filter], customer_id: current_user.customer_id)
        else
            @complaints = Complaint.all
        end
        render json: @complaints, status: 200
    end
    
    # GET /complaints/1
    def show
        render json: @complaint, status: 200
    end
    
    # POST /complaints
    # Dont send status
    # Dont send customer or region id
    def create
        @complaint = Complaint.new(complaint_params)
        @complaint.customer_id = current_user.customer_id
        @complaint.region_id = current_user.customer.region_id

        if @complaint.save
            render json: @complaint, status: :created, location: api_v1_complaint_url(@complaint)
        else
            render json: @complaint.errors, status: :unprocessable_entity
        end
    end
    
    # PATCH/PUT /complaints/1
    def update
        if @complaint.update(complaint_params)
            render json: @complaint, status: 200
        else
            render json: @complaint.errors, status: :unprocessable_entity
        end
    end
  
    # DELETE /complaints/1
    def destroy
       Complaint.where(id: params[:id], customer_id: current_user.customer_id).destroy_all
    end        

    private
    # Use callbacks to share common setup or constraints between actions.
    def set_complaint
        @complaint = Complaint.where(id: params[:id], customer_id: current_user.customer_id)#current_user.customer_id)
    end

    # Only allow a trusted parameter “white list” through.
    def index_params
        params.permit(:filter)
    end

    def complaint_params
        params.require(:complaint).permit(:message)
    end
end