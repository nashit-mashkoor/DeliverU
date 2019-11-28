class ResturantSerializer < ActiveModel::Serializer
  include Rails.application.routes.url_helpers

  attributes :id, :name, :region_id, :menu_image

  def menu_image
    rails_blob_path(object.menu_image, only_path: true) if object.menu_image.attached?
  end

end
