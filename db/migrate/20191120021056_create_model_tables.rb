class CreateModelTables < ActiveRecord::Migration[6.0]
  def change
    create_table :regions do |t|
      t.string :name, null: true
  
      t.timestamps
    end
  
    create_table :timeslots do |t|
      t.time :start
      t.time :end
      t.references :region, null: false, foreign_key: true
      
  
      t.timestamps
    end
  
    create_table :customers do |t|
      t.string :name, null: true
      t.string :email, null: true
      t.date :dob, null: true
      t.references :region, null: true, foreign_key: true
  
      t.timestamps
    end
  
    create_table :orders do |t|
      t.integer :item_count
      t.string :order_message, null: true
      t.references :timeslot, null: false, foreign_key: true
      t.references :customer, null: false, foreign_key: true
  
      t.timestamps
    end
  
    create_table :resturants do |t|
      t.string :name, null: true
      t.references :region, null: true , foreign_key: true
  
      t.timestamps
    end
  
    create_table :resturantitems do |t|
      t.string :description, null: true
      t.references :resturant, null: false, foreign_key: true
      t.references :order
  
      t.timestamps
    end
  
    create_table :grocerrystores do |t|
      t.string :name
      t.integer :cost, null: true
  
      t.timestamps
    end
  
    create_table :grocerryitems do |t|
      t.references :order, null: false, foreign_key: true
      t.references :grocerrystore, null: false, foreign_key: true
  
      t.timestamps
    end
  
    create_table :drivers do |t|
      t.string :name, null: true
      t.date :dob, null: true
      t.string :email, null: true
      t.string :cnic, null: true
      t.references :region, null: true, foreign_key: true
  
      t.timestamps
    end
  
    create_table :payables do |t|
      t.integer :amount
      t.references :driver, null: false, foreign_key: true
      t.integer :type
  
      t.timestamps
    end
  
    create_table :complaints do |t|
      t.string :message
      t.integer :status
      t.references :region, null: true, foreign_key: true
      t.references :customer, null: true, foreign_key: true
  
      t.timestamps
    end
  end
end
