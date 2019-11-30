class Customer < ApplicationRecord
  belongs_to :region, optional: true

  has_one :user, dependent: :destroy

  has_many :orders, dependent: :destroy
  has_many :timeslots, through: :orders
  
  has_many :complaints, dependent: :destroy

end
