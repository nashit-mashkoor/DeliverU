class OrderSerializer < ActiveModel::Serializer
  attributes :id, :item_count, :order_message, :place_date, :category, :status, :created_by

  belongs_to :timeslot
  belongs_to :customer
  has_many :grocerryitems
  has_many :resturantitems
end
