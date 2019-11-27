class Resturant < ApplicationRecord
  belongs_to :region, optional: true
  has_many :resturantitems, dependent: :destroy
  #validates :name, :region_id, :menu_image, presence: true
  has_one_attached :menu_image

  has_many :orders, through: :resturantitems
end
