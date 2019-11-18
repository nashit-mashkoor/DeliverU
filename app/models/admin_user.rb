class AdminUser < ApplicationRecord
  # Include default devise modules. Others available are:
  validates :email, :password, :password_confirmation, presence: true
  # :confirmable, :lockable, :timeoutable, :trackable and :omniauthable
  devise :database_authenticatable, 
         :recoverable, :rememberable, :validatable
end
