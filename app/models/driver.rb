class Driver < ApplicationRecord
  belongs_to :region, optional: true
  has_many :payables, dependent: :destroy
end
