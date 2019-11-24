# This file should contain all the record creation needed to seed the database with its default values.
# The data can then be loaded with the rails db:seed command (or created alongside the database with db:setup).
#
# Examples:
#
#   movies = Movie.create([{ name: 'Star Wars' }, { name: 'Lord of the Rings' }])
#   Character.create(name: 'Luke', movie: movies.first)
AdminUser.create!(email: 'admin@example.com', password: 'password', password_confirmation: 'password') if Rails.env.development?
u =User.create email: 'ignitorkhan@gmail.com', password: 123456 
u2 =User.create email: 'example@example.com', password: 123456 
c = Customer.create! name: 'nashit', customer_lat: 4.921118 , customer_lang: -0.798065 
c2 =Customer.create! name: 'Ali', customer_lat: 4.948995 , customer_lang: -0.755855 
Customer.create!
r = Region.create! name: 'Sabzazar', TlLat: 4.925308, TlLong: -0.815567, BrLat: 4.913678 , BrLong:-0.789314  
u.customer = c
u.save!
c.save!
u2.customer = c2
u2.save!
c2.save!
