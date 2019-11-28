class Payable < ApplicationRecord
  enum category: [:to_pay, :to_recieve]
  belongs_to :driver
  belongs_to :order, optional: true
end
