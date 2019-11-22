class Customer < ApplicationRecord
  belongs_to :region, optional: true
  has_many :orders
  has_many :timeslots, through: :orders  
end
