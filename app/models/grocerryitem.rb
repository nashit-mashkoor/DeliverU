class Grocerryitem < ApplicationRecord
  belongs_to :order
  belongs_to :grocerrystore
end
