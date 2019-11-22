class Resturant < ApplicationRecord
  belongs_to :region, optional: true
end
