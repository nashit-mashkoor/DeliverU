class TimeslotSerializer < ActiveModel::Serializer
  attributes :id, :start

  belongs_to :region
end
