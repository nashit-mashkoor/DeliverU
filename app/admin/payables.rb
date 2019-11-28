ActiveAdmin.register Payable do
    permit_params :amount, :type
    belongs_to :driver

    def index
        redirect_to collection_path
    end
end
