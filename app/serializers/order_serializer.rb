class OrderSerializer < ActiveModel::Serializer
  attributes :id, :item_count, :order_message, :place_date, :category, :status, :created_by, :proof_of_payment

  belongs_to :timeslot
  belongs_to :customer
  has_many :grocerryitems
  has_many :resturantitems

  def proof_of_payment
    rails_blob_path(object.proof_of_Payment, only_path: true) if object.proof_of_payment.attached?
  end

end
