class Driver < ApplicationRecord
  belongs_to :region, optional: true
  validates :name, :dob, :email, :cnic, :region_id, :driver_license, presence: true
  has_one_attached :driver_license
end
