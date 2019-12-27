ActiveAdmin.register Payable do
    permit_params :amount, :category
    belongs_to :driver

    form do |f|
        f.inputs "Please fill all fields" do
          f.input :amount
          f.input :category
        end
        f.actions
    end
    
    def index
        redirect_to collection_path
    end
end
