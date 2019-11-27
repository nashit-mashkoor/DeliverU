class Driver < ApplicationRecord
  belongs_to :region, optional: true
  has_one :user,  dependent: :destroy
  has_many :payables, dependent: :destroy

  #validates :name, :dob, :email, :cnic, :region_id, :driver_license, presence: true
  has_one_attached :driver_license
end
