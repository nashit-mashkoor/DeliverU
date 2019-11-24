class RegionSerializer < ActiveModel::Serializer
  attributes :id, :TlLat, :TlLang, :BrLat, :BrLang

  has_one :driver
  has_many :customers
  has_many :resturants
  has_many :timeslots
end
