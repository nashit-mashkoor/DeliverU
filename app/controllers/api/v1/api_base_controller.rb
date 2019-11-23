class Api::V1::ApiBaseController < ApplicationController
    before_action   :set_default_format
    around_action   :handle_exceptions
    
    private 

    def handle_exceptions
        begin
            yield
        rescue ActiveRecord::RecordNotFound => e
            status = 404
        rescue ActiveRecord::RecordInvalid => e
            status = 403
        rescue Exception => e
            status = 500
        end
        handle_error "#{e.message}", status unless e.class == NilClass
    end

    def handle_error(message, status = 500)
        message = message.is_a?(Array) ? message.join(', ') : message
        @errors = {message: message, status: status}
        render json: @errors, :status => status
    end
    def set_default_format
        request.format = :json
    end
   
  end