class Resturant < ApplicationRecord
  belongs_to :region, optional: true
  validates :name, :region_id, :image, presence: true
  has_one_attached :image
end
