class DriverSerializer < ActiveModel::Serializer
  include Rails.application.routes.url_helpers
  attributes :id, :name, :email, :cnic, :driver_license
  belongs_to :region

  def driver_license
    rails_blob_path(object.driver_license, only_path: true) if object.driver_license.attached?
  end
end
