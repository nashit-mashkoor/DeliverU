class Api::V1::GrocerrystoresController < Api::V1::ApiBaseController
    # GET /grocerrystores
    # For both customer and controller
    def index
        @grocerrystores = Grocerrystore.all
        render json: @grocerrystores, status: 200

    end
end