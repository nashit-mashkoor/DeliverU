class Payable < ApplicationRecord
  enum type: [:to_pay, :to_recieve]
  belongs_to :driver
end
