class Region < ApplicationRecord
  has_one :driver, dependent: :nullify
  has_many :customers, dependent: :nullify
  has_many :resturants, dependent: :nullify
  has_many :timeslots, dependent: :nullify
end
