class Timeslot < ApplicationRecord
  belongs_to :region, optional: true
  has_many :orders
  has_many :customers, through: :orders
  validates :region, :start, presence: true

end
