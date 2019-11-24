class Api::V1::TimeslotsController < ApplicationController
    before_action :set_timeslot, only: [:show, :update, :destroy]
    
    # GET /timeslots
    def index
        @timeslots = Timeslot.all
        render json: @timeslots, status: 200
    end
    
    # GET /timeslots/1
    def show
        render json: @timeslot, status: 200
    end
    
    # POST /timeslots
    def create
        @timeslot = Timeslot.new(timeslot_params)
        if @timeslot.save
            render json: @timeslot, status: :created, location: api_v1_timeslot_url(@timeslot)
        else
            render json: @timeslot.errors, status: :unprocessable_entity
        end
    end
    
    # PATCH/PUT /timeslots/1
    def update
        if @timeslot.update(timeslot_params)
            render json: @timeslot, status: 200
        else
            render json: @timeslot.errors, status: :unprocessable_entity
        end
    end
  
    # DELETE /timeslots/1
    def destroy
        @timeslot.destroy
    end

    # Non Resourcefull actions

    def region_slots
        @timeslots = Timeslot.where("region_id = ?", params[:region_id])
        render json: @timeslot, status: 200
    end
  
    private
    # Use callbacks to share common setup or constraints between actions.
    def set_timeslot
        @timeslot = Timeslot.find(params[:id])
    end
  
    # Only allow a trusted parameter “white list” through.
    def timeslot_params
       params.require(:timeslot).permit(:start, :end, :region_id)
    end
end
