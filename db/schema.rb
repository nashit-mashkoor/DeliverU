# This file is auto-generated from the current state of the database. Instead
# of editing this file, please use the migrations feature of Active Record to
# incrementally modify your database, and then regenerate this schema definition.
#
# This file is the source Rails uses to define your schema when running `rails
# db:schema:load`. When creating a new database, `rails db:schema:load` tends to
# be faster and is potentially less error prone than running all of your
# migrations from scratch. Old migrations may fail to apply correctly if those
# migrations use external dependencies or application code.
#
# It's strongly recommended that you check this file into your version control system.

ActiveRecord::Schema.define(version: 2019_11_20_022636) do

  # These are extensions that must be enabled in order to support this database
  enable_extension "plpgsql"

  create_table "complaints", force: :cascade do |t|
    t.string "message"
    t.integer "status"
    t.bigint "region_id", null: false
    t.bigint "customer_id", null: false
    t.datetime "created_at", precision: 6, null: false
    t.datetime "updated_at", precision: 6, null: false
    t.index ["customer_id"], name: "index_complaints_on_customer_id"
    t.index ["region_id"], name: "index_complaints_on_region_id"
  end

  create_table "customers", force: :cascade do |t|
    t.string "name"
    t.string "email"
    t.date "dob"
    t.bigint "region_id", null: false
    t.datetime "created_at", precision: 6, null: false
    t.datetime "updated_at", precision: 6, null: false
    t.index ["region_id"], name: "index_customers_on_region_id"
  end

  create_table "drivers", force: :cascade do |t|
    t.string "name"
    t.date "dob"
    t.string "email"
    t.string "cnic"
    t.bigint "region_id", null: false
    t.datetime "created_at", precision: 6, null: false
    t.datetime "updated_at", precision: 6, null: false
    t.index ["region_id"], name: "index_drivers_on_region_id"
  end

  create_table "grocerryitems", force: :cascade do |t|
    t.bigint "order_id", null: false
    t.bigint "grocerrystore_id", null: false
    t.datetime "created_at", precision: 6, null: false
    t.datetime "updated_at", precision: 6, null: false
    t.index ["grocerrystore_id"], name: "index_grocerryitems_on_grocerrystore_id"
    t.index ["order_id"], name: "index_grocerryitems_on_order_id"
  end

  create_table "grocerrystores", force: :cascade do |t|
    t.string "name"
    t.integer "cost"
    t.datetime "created_at", precision: 6, null: false
    t.datetime "updated_at", precision: 6, null: false
  end

  create_table "orders", force: :cascade do |t|
    t.integer "item_count"
    t.string "order_message"
    t.bigint "timeslot_id", null: false
    t.bigint "customer_id", null: false
    t.datetime "created_at", precision: 6, null: false
    t.datetime "updated_at", precision: 6, null: false
    t.index ["customer_id"], name: "index_orders_on_customer_id"
    t.index ["timeslot_id"], name: "index_orders_on_timeslot_id"
  end

  create_table "payables", force: :cascade do |t|
    t.integer "amount"
    t.bigint "driver_id", null: false
    t.integer "type"
    t.datetime "created_at", precision: 6, null: false
    t.datetime "updated_at", precision: 6, null: false
    t.index ["driver_id"], name: "index_payables_on_driver_id"
  end

  create_table "regions", force: :cascade do |t|
    t.string "name"
    t.datetime "created_at", precision: 6, null: false
    t.datetime "updated_at", precision: 6, null: false
    t.bigint "driver_id", null: false
    t.index ["driver_id"], name: "index_regions_on_driver_id"
  end

  create_table "resturantitems", force: :cascade do |t|
    t.string "description"
    t.bigint "resturant_id", null: false
    t.bigint "order_id"
    t.datetime "created_at", precision: 6, null: false
    t.datetime "updated_at", precision: 6, null: false
    t.index ["order_id"], name: "index_resturantitems_on_order_id"
    t.index ["resturant_id"], name: "index_resturantitems_on_resturant_id"
  end

  create_table "resturants", force: :cascade do |t|
    t.string "name"
    t.bigint "region_id", null: false
    t.datetime "created_at", precision: 6, null: false
    t.datetime "updated_at", precision: 6, null: false
    t.index ["region_id"], name: "index_resturants_on_region_id"
  end

  create_table "timeslots", force: :cascade do |t|
    t.time "start"
    t.time "end"
    t.bigint "region_id", null: false
    t.datetime "created_at", precision: 6, null: false
    t.datetime "updated_at", precision: 6, null: false
    t.index ["region_id"], name: "index_timeslots_on_region_id"
  end

  create_table "users", force: :cascade do |t|
    t.string "email", default: "", null: false
    t.string "encrypted_password", default: "", null: false
    t.string "reset_password_token"
    t.datetime "reset_password_sent_at"
    t.datetime "remember_created_at"
    t.datetime "created_at", precision: 6, null: false
    t.datetime "updated_at", precision: 6, null: false
    t.integer "role"
    t.index ["email"], name: "index_users_on_email", unique: true
    t.index ["reset_password_token"], name: "index_users_on_reset_password_token", unique: true
  end

  add_foreign_key "complaints", "customers"
  add_foreign_key "complaints", "regions"
  add_foreign_key "customers", "regions"
  add_foreign_key "drivers", "regions"
  add_foreign_key "grocerryitems", "grocerrystores"
  add_foreign_key "grocerryitems", "orders"
  add_foreign_key "orders", "customers"
  add_foreign_key "orders", "timeslots"
  add_foreign_key "payables", "drivers"
  add_foreign_key "regions", "drivers"
  add_foreign_key "resturantitems", "resturants"
  add_foreign_key "resturants", "regions"
  add_foreign_key "timeslots", "regions"
end
