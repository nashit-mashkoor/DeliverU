class Payable < ApplicationRecord
  enum type: [:to_pay, :to_recieve]
  belongs_to :driver
  self.inheritance_column = nil

  def color
    self.type == 'to_recieve' ? 'blue' : 'red'
  end
  
  def typeString
    self.type == 'to_recieve' ? 'Recieval' : 'Payable'
  end
end
