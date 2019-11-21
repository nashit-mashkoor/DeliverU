class Resturantitem < ApplicationRecord
  belongs_to :resturant
  belongs_to :order
end
