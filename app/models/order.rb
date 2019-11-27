class Order < ApplicationRecord
  enum category: {single: 0, recurring: 1}
  enum status: {pending: 0, completed: 1, cancelled: 2}
  enum created_by: {manual: 0, auto: 1}

  belongs_to :timeslot
  belongs_to :customer

  has_many :grocerryitems, dependent: :destroy
  has_many :resturantitems, dependent: :destroy

  has_many :grocerrystores, through:  :grocerryitems
  has_many :resturants, through: :resturantitems


  public

  def single_can_be_added?
    byebug
    Time.now + 1.hour <= Time.parse(self[:place_date] +' '+ self[:timeslot].start) 
  end

  def single_can_be_edited?
    Time.now + 1.hour <= Time.parse(self.place_date +' '+ self.timeslot.start) && self.completed? 
  end

  def add_first_entry_manually?
    (Time.now + 1.hour).strftime("%H:%M:%S") <= self.timeslot.start
  end

end
