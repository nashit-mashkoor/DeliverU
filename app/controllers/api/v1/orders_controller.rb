class Api::V1::OrdersController < Api::V1::ApiBaseController
  include ApplicationHelper
  before_action :set_order, only: [:show, :update, :cancel, :mark_order_complete]
  before_action :authenticate_customer!, only: [:create, :update, :customer_recurring_orders, :customer_single_orders, :cancel]
  #Uncommenting breaks the code I dont know why
  #before_Action :authenticate_driver!, only:  [:driver_recurring_orders, :driver_single_orders, :mark_order_complete]

  #For testing
  # GET /orders
  def index
    @orders = Order.all
    render json: @orders, status: 200
  end

  # GET /orders/1
  def show
      render json: @order, status: 200
  end

  # Place Order
  # POST /orders
  # Recurring order start from the day you place them
  # Assuming Resturant sent belongs to the user region only
  def create      
      order_params = (place_order_params)
      order_params[:customer_id] = current_user.customer_id
      @order = Order.new(order_params)
      if @order.recurring?
        if((Time.now + 1.hour).strftime('%H:%M:%S') <= (Time.parse(@order.place_date + ' ' + @order.timeslot.start)).strftime('%H:%M:%S') && !@order.completed? )
          # Add the auto generated entry
          @order.category = 'single'
          @order.created_by = 'auto'
          @order.save!
        end
        # Improve this
        if Order.create!(order_params)
          render json: @order, status: 201
        else
          render json: {'errors': ['Order can no be placed']}, status: :unprocessable_entity
        end
      else
        if (Time.now + 1.hour <= Time.parse(@order.place_date + ' ' + @order.timeslot.start)) && @order.save!
            render json: @order, status: 201
        else
          render json: {'errorrs': ['Order can not be placed']}, status: :unprocessable_entity
        end
      end 
  end

  # Update order || Category can not be changed || Placed date || Time slot can not be changed |All ids are replaced|
  # PATCH/PUT /orders/1
  # Assuming Resturant sent belongs to the user region only
  def update
      if @order.single?
        if( (Time.now + 1.hour <= Time.parse(@order.place_date + ' ' + @order.timeslot.start)) && (!@order.completed? ) && @order.update(update_order_params) )
          render json: @order, status: 200
        else
          render json: {'errorrs': ['Order can not be updated']}, status: :unprocessable_entity
        end
      else
        if(@order.update(update_order_params))
          render json: @order, status: 200
        else
          render json: {'errorrs': ['Order can not be updated']}, status: :unprocessable_entity
        end
      end
  end

    # Cancel order 
    # PUT/order/id/cancel
  def cancel
      if @order.single?
        if( (Time.now + 1.hour <= Time.parse(@order.place_date + ' ' + @order.timeslot.start)) && (!@order.completed? ) && @order.update(update_order_params) )
          render json: @order, status: 200
        else
          render json: {'errorrs': ['Order can not be cancelled now']}, status: :unprocessable_entity
        end
      else
        if(@order.update(update_order_params))
          render json: @order, status: 200
        else
          render json: {'errorrs': ['Order can not be cancelled']}, status: :unprocessable_entity
        end
      end
    
  end

  # get/order/customer_recurring_orders
  # Gets  All recurring order that are used to generate auto orders for a customer || Check status
  def customer_recurring_orders
    # 1 represents 
    @orders = Order.where(customer_id: current_user.customer_id, category: :recurring)
    render json: @orders, status: 200
  
    
  end

  # get/order/customer_single_orders
  # Get all single order regardless they are manual or auto for a customer
  def customer_single_orders
    @orders = Order.where(customer_id: current_user.customer_id, category: :single)
    render json: @orders, status: 200

  end

  # get/order/driver_recurring_orders
  # Gets recurring order that are used to generate auto orders for a driver
  def driver_recurring_orders
    @orders = Timeslot.joins(:orders).where(orders: { category: :recurring}, timeslots: {region_id: current_user.driver.region_id})
    render json: @orders, status: 200
  end

  # get/order/driver_single_orders
  # Get all single order regardless they are manual or auto for a driver
  def driver_single_orders
    @orders = Timeslot.joins(:orders).where(orders: { category: :single}, timeslots: {region_id: current_user.driver.region_id})
    render json: @orders, status: 200
  end


  # put/order/1
  # Mark a order as complete by driver
  def mark_order_complete
    order_params = (driver_order_params)
    order_params[:payable_attributes][:driver_id] = current_user.customer_id
    if @order.single?
      if( (Time.now  >= Time.parse(@order.place_date + ' ' + @order.timeslot.start) || true) && (@order.pending? ) && @order.update(order_params) )
        render json: @order, status: 200
      else
        render json: {'errorrs': ['Order can not be completed']}, status: :unprocessable_entity
      end
    else
      if(@order.update(order_params))
        render json: @order, status: 200
      else
        render json: {'errorrs': ['Order can not be completed']}, status: :unprocessable_entity
      end
    end
  end

  private
  
  def set_order
    @order = Order.find(params[:id])
    if current_user.customer.present?
      @order = nil unless current_user.customer_id == @order.customer_id
    elsif current_user.driver.present?
      @order = nil unless current_user.driver_id == @order.timeslot.region.driver_id
    end 
  end
  
  def place_order_params
    # Do not allow status update
    params.require(:order).permit(:item_count, :order_message, :category, :created_by, :place_date, :timeslot_id, grocerryitems_attributes: [:grocerrystore_id, :quantity], resturantitems: [:resturant_id, :description])
  end

  def update_order_params
    params.require(:order).permit(:item_count, :order_message, :created_by, :status, grocerryitems_attributes: [:grocerrystore_id, :quantity], resturantitems: [:resturant_id, :description]  )
  end

  def driver_order_params
    # Could not test proof of payment
    params.require(:order).permit(:status,:proof_of_payment, :payable_attributes =>  :amount  )
  end
    
end