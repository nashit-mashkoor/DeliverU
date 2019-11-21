class Complaint < ApplicationRecord
  belongs_to :region
  belongs_to :customer
end
