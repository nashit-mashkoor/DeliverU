class CreateAdminModels < ActiveRecord::Migration[6.0]
  def change
    create_table :admin_models do |t|
      t.string :admin_id
      t.string :email
      t.string :password

      t.timestamps
    end
  end
end
