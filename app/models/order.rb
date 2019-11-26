class Order < ApplicationRecord
  enum category: {single: 0, recurring: 1}
  enum status: {pending: 0, completed: 1, cancelled: 2}
  enum created_by: {manual: 0, auto: 1}

  belongs_to :timeslot
  belongs_to :customer
  has_many :grocerryitems
  has_many :resturantitems
end
