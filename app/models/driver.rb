class Driver < ApplicationRecord
  belongs_to :region, optional: true
  validates :name, :dob, :email, :cnic, :region_id, presence: true
end
