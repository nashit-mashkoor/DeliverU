class Payable < ApplicationRecord
  enum category: {to_pay: 0, to_recieve: 1}
  belongs_to :driver
  belongs_to :order, optional: true
  self.inheritance_column = nil

  def color
    self.category == 'to_recieve' ? 'blue' : 'red'
  end
  
  def typeString
    self.category == 'to_recieve' ? 'Recieval' : 'Payable'
  end
end
