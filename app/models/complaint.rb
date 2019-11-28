class Complaint < ApplicationRecord
  belongs_to :region, optional: true
  belongs_to :customer, optional: true
  enum status: { pending: 0, resolved: 1 }
end
