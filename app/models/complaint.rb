class Complaint < ApplicationRecord
  belongs_to :region, optional: true
  belongs_to :customer
  enum status: { pending: 0, completed: 1 }
end
