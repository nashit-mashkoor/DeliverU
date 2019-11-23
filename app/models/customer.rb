class Customer < ApplicationRecord
  belongs_to :region, optional: true
  has_many :orders, dependent: :destroy
  has_many :timeslots, through: :orders  
end
