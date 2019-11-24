class TimeslotSerializer < ActiveModel::Serializer
  attributes :id, :start, :end

  belongs_to :region
end
