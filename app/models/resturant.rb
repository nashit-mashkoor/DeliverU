class Resturant < ApplicationRecord
  belongs_to :region, optional: true
  has_many :resturantitems, dependent: :destroy
end
