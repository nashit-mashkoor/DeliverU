class PayableSerializer < ActiveModel::Serializer
  attributes :id, :category, :amount, :created_at

  has_one :driver
end
