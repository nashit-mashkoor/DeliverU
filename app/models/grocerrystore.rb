class Grocerrystore < ApplicationRecord
    has_many :grocerryitem, dependent: :destroy
end
