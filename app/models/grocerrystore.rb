class Grocerrystore < ApplicationRecord
    has_many :grocerryitems, dependent: :destroy
    has_many :orders, through: :grocerryitems
end
