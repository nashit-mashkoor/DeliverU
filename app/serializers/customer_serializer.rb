class CustomerSerializer < ActiveModel::Serializer
  attributes :id, :name, :customer_lat, :customer_lang

  belongs_to :region
  has_one :user
end
