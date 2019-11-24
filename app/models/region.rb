class Region < ApplicationRecord
  has_one :driver, dependent: :nullify
  has_many :customers, dependent: :nullify
  has_many :resturants, dependent: :nullify
  has_many :timeslots, dependent: :nullify

  def self.get_customer_region lat, lang
    region_id = nil
    Region.all.each do |r|
      sw_point = Geokit::LatLng.new(r.BrLat,r.BrLong)
      ne_point = Geokit::LatLng.new(r.TlLat,r.TlLong)
      point = Geokit::LatLng.new(lat, lang)
      bounds=Geokit::Bounds.new(sw_point,ne_point)
      region_id = r.id if bounds.contains?(point)   
    end
    return region_id
  end
  validates :name, presence: true

end
