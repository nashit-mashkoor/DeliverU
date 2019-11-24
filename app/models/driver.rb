class Driver < ApplicationRecord
  belongs_to :region, optional: true
  validates :name, :dob, :email, :cnic, :region_id, :image, presence: true
  has_one_attached :image
end
