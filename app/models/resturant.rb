class Resturant < ApplicationRecord
  belongs_to :region, optional: true
  validates :name, :region_id, :menu_image, presence: true
  has_one_attached :menu_image
end
