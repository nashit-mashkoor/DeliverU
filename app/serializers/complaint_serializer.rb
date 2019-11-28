class ComplaintSerializer < ActiveModel::Serializer
  attributes :id, :message, :status, :region_id, :customer_id
end
