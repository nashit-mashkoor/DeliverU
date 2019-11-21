class Order < ApplicationRecord
  belongs_to :timeslot
  belongs_to :customer
end
