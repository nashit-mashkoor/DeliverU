class Customer < ApplicationRecord
  belongs_to :region
  has_many :orders
  has_many :timeslots, through: :orders  
end
