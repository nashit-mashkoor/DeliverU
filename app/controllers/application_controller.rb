class ApplicationController < ActionController::Base
    protect_from_forgery with: :null_session, if: :json_request?

    def json_request?
        request.format.json?
    end
end
