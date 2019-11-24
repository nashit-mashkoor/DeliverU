class Driver < ApplicationRecord
  belongs_to :region, optional: true
  has_one :user,  dependent: :destroy
  has_many :payables, dependent: :destroy

end
