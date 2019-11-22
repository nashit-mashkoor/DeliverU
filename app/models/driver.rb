class Driver < ApplicationRecord
  belongs_to :region
  validates :name, :dob, :email, :cnic, :region_id, presence: true
end
