class Complaint < ApplicationRecord
  belongs_to :region, optional: true
  belongs_to :customer
end
