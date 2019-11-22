class Driver < ApplicationRecord
  belongs_to :region, optional: true
end
