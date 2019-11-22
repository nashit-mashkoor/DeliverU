class Region < ApplicationRecord
  has_one :driver
  validates :name, presence: true

end
