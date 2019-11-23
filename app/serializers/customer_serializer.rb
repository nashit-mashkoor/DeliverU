class CustomerSerializer < ActiveModel::Serializer
  attributes :id, :name, :email, :customer_lat, :customer_lang

  belongs_to :region
end
