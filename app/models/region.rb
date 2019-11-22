class Region < ApplicationRecord
  has_one :driver, required: false
  validates :name, presence: true

end
