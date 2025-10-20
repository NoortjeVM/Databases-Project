"""
Controllers (Routes) for Pizza Ordering System

This module defines all Flask blueprints and route handlers for the application.
It handles HTTP requests and responses for:
- Home page
- Customer management (CRUD operations)
- Menu item management (pizzas, drinks, desserts)
- Order creation and viewing
- Ingredient listing
- Staff reports and analytics

Each section is organized into blueprints for better code organization.
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash
from sqlalchemy.orm import selectinload
from sqlalchemy import func, and_, extract
from models import db, Customer, MenuItem, Order, OrderItem, Ingredient, Pizza, Drink, Dessert, DeliveryPerson, DiscountCode
from datetime import date, datetime, timezone, timedelta
from zoneinfo import ZoneInfo

# ============================================================================
# BLUEPRINT DEFINITIONS
# ============================================================================

# Define blueprints for different sections of the application
home_bp = Blueprint("home", __name__)
customers_bp = Blueprint("customers", __name__)
menu_items_bp = Blueprint("menu_items", __name__, url_prefix="/menu-items")
orders_bp = Blueprint("orders", __name__)
ingredients_bp = Blueprint("ingredients", __name__)
create_order_bp = Blueprint("create_order", __name__)
staff_reports_bp = Blueprint("staff_reports", __name__)

# ============================================================================
# HOME ROUTES
# ============================================================================
@home_bp.route("/")
def index():
    """
    Display the home page with navigation to all sections.
    
    Returns:
        Rendered index.html template
    """
    return render_template("index.html", title="Home")

# ============================================================================
# CUSTOMER ROUTES
# ============================================================================
@customers_bp.route("/customers")
def list_customers():
    """
    Display a list of all customers with their basic information.
    
    Shows customer ID, name, phone, address, birthdate, and order count.
    Customers are ordered by customer_id.
    
    Returns:
        Rendered customers.html template with customer list
    """
    customers = Customer.query.order_by(Customer.customer_id).all()
    return render_template("customers.html", title="Customers", customers=customers)

@customers_bp.route("/customers/new")
def new_customer():
    """
    Display the form for creating a new customer.
    
    Returns:
        Rendered customer_form.html template
    """
    return render_template("customer_form.html", title="New Customer", customer=None)

@customers_bp.route("/customers", methods=["POST"])
def create_customer():
    """
    Handle POST request to create a new customer.
    
    Validates and processes form data:
    - Required fields: first_name, last_name, phone_number, birthdate
    - Optional fields: address, gender
    - Postal code must be exactly 6 characters (normalized to uppercase, no spaces)
    - Birthdate cannot be in the future
    
    Form Data:
        first_name (str): Customer's first name
        last_name (str): Customer's last name
        phone_number (str): Phone number (must be unique)
        address (str): Street address
        postal_code (str): 6-character postal code
        birthdate (str): Date in YYYY-MM-DD format
        gender (str): "0" (Female), "1" (Male), or "2" (Other)
    
    Returns:
        Redirect to customer list on success, or back to form on error
        Flash messages indicate success or validation errors
    """
    # Extract and clean form data
    first_name = request.form.get("first_name", "").strip()
    last_name = request.form.get("last_name", "").strip()
    phone_number = request.form.get("phone_number", "").strip()
    address = request.form.get("address", "").strip()
    postal_code = request.form.get("postal_code", "").strip().replace(" ", "").upper()
    birthdate_str = request.form.get("birthdate", "").strip()
    gender = request.form.get("gender", "").strip()
    
    # Validate required fields
    if not all([first_name, last_name, phone_number, birthdate_str]):
        flash("First name, last name, phone number, and birthdate are required.", "error")
        return redirect(url_for("customers.new_customer"))
    
    # Validate postal code length
    if len(postal_code) != 6:
        flash("Postal code must be exactly 6 characters (e.g. 6222RT).")
        return redirect(url_for("customers.new_customer"))
    
    try:
        # Parse birthdate
        birthdate = datetime.strptime(birthdate_str, '%Y-%m-%d').date()

        # Validate birthdate is not in the future
        today = date.today()
        if birthdate > today:
            flash("Birthdate cannot be in the future.", "error")
            return redirect(url_for("customers.new_customer"))
        
        # Convert gender to integer or None
        gender_val = int(gender) if gender else None

        # Create customer object
        customer = Customer(
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            address=address,
            postal_code=postal_code,
            birthdate=birthdate,
            gender=gender_val
        )

        # Save to database
        db.session.add(customer)
        db.session.commit()

        flash("Customer created successfully.", "success")
        return redirect(url_for("customers.list_customers"))
    except ValueError:
        flash("Invalid birthdate format. Please use YYYY-MM-DD.", "error")
        return redirect(url_for("customers.new_customer"))
    except Exception as e:
        flash(f"Error creating customer: {str(e)}", "error")
        return redirect(url_for("customers.new_customer"))


# ============================================================================
# MENU ROUTES
# ============================================================================
@menu_items_bp.route("/")
def list_menu_items():
    """
    Display all menu items organized by type (pizzas, drinks, desserts).
    
    For pizzas, shows ingredients and dietary labels (vegan/vegetarian).
    For drinks and desserts, shows name and price.
    
    Returns:
        Rendered menu_items.html template with categorized items
    """
    pizzas = Pizza.query.all()
    drinks = Drink.query.all()
    desserts = Dessert.query.all()
    print(pizzas[1].label)
    return render_template("menu_items.html", title="Menu Items", pizzas=pizzas, drinks=drinks, desserts=desserts)

@menu_items_bp.route("/new")
def new_menu_item():
    """
    Display the form for creating a new menu item.
    
    Returns:
        Rendered menu_item_form.html template
    """
    return render_template("menu_item_form.html", title="New Menu Item", menu_item=None)

@menu_items_bp.route("/", methods=["POST"])
def create_menu_item():
    """
    Handle POST request to create a new menu item.
    
    Creates the specific item type (Pizza/Drink/Dessert) first, then creates
    a MenuItem entry that references it. Pizza prices are calculated from
    ingredients, so no price input is needed for pizzas.
    
    Form Data:
        item_name (str): Name of the item
        item_type (str): "pizza", "drink", or "dessert"
        item_price (str): Price (only for drinks/desserts, not pizzas)
    
    Returns:
        Redirect to menu list on success, or back to form on error
        Flash messages indicate success or validation errors
    """
    item_name = request.form.get("item_name", "").strip()
    item_price = request.form.get("item_price", "").strip()
    item_type = request.form.get("item_type", "").strip()
    
    # Validate required fields
    if not item_name or (item_type != "pizza" and not item_price):
        flash("Item name (and price for drinks/desserts) are required.", "error")
        return redirect(url_for("menu_items.new_menu_item"))
    
    try:
        menu_item = None

        # Create pizza (no price needed - calculated from ingredients)
        if item_type == "pizza":
            pizza = Pizza(name=item_name)
            db.session.add(pizza)
            db.session.flush() # Get pizza_id before creating MenuItem
            menu_item = MenuItem(item_type="pizza", item_ref_id=pizza.pizza_id)
        elif item_type == "drink":
            # Create drink with price
            price = float(item_price)
            drink = Drink(name=item_name, price=price)
            db.session.add(drink)
            db.session.flush()
            menu_item = MenuItem(item_type="drink", item_ref_id=drink.drink_id)
        elif item_type == "dessert":
            # Create dessert with price
            price = float(item_price)
            dessert = Dessert(name=item_name, price=price)
            db.session.add(dessert)
            db.session.flush()
            menu_item = MenuItem(item_type="dessert", item_ref_id=dessert.dessert_id)

        # Save MenuItem to database
        if menu_item:
            db.session.add(menu_item)
            db.session.commit()
            flash("Menu item created successfully.", "success")
        return redirect(url_for("menu_items.list_menu_items"))

    except ValueError:
        flash("Price must be a valid number.", "error")
        return redirect(url_for("menu_items.new_menu_item"))
    except Exception as e:
        flash(f"Error creating menu item: {str(e)}", "error")
        return redirect(url_for("menu_items.new_menu_item"))

# ============================================================================
# INGREDIENT ROUTE
# ============================================================================
@ingredients_bp.route("/ingredients")
def list_ingredients():
    """
    Display all ingredients with their prices and dietary information.
    
    Shows ingredient ID, name, price, and whether it's vegan/vegetarian.
    
    Returns:
        Rendered ingredients.html template with ingredient list
    """
    ingredients = Ingredient.query.order_by(Ingredient.ingredient_id).all()
    return render_template("ingredients.html", title="Ingredients", ingredients=ingredients)

# ============================================================================
# ORDER VIEWING ROUTES
# ============================================================================
@orders_bp.route("/list_orders")
def list_orders():
    """
    Display all orders with full details.
    
    Shows order ID, customer, items, total, delivery person, address,
    timestamps, and current status. Orders are sorted by order_time descending
    (most recent first).
    
    Returns:
        Rendered orders.html template with order list
    """
    orders = Order.query.order_by(Order.order_time.desc()).all()
    print(f"amount of orders: {len(orders)}")
    return render_template("orders.html", orders=orders)

# ============================================================================
# ORDER CREATION ROUTES
# ============================================================================
@create_order_bp.route("/create_order", methods=["GET","POST"])
def create_order():
    """
    Handle order creation with two-step process: preview then confirm.
    
    GET Request:
        Displays order form with customer selection, menu items, and address fields.
    
    POST Request (action=preview):
        Calculates and displays price with discounts applied, without creating order.
        Shows breakdown of:
        - Raw price (before discounts)
        - Applied discounts (birthday, loyalty, discount codes)
        - Final total price
    
    POST Request (action=create):
        Creates the order in the database after validation.
        Validates:
        - Customer selected
        - At least one item selected
        - At least one pizza in order (required)
        - Valid delivery address and postal code
        - Delivery person available for postal code
        
        Applies automatic discounts:
        - Birthday discount (if today is customer's birthday, not used today)
        - 10-pizza loyalty discount (1 free pizza per 10 pizzas ordered)
        - Discount code (if provided and valid)
        
        Updates delivery person availability after order creation.
    
    Form Data:
        customer_id (str): Selected customer ID
        postal_code (str): Delivery postal code
        delivery_address (str): Delivery street address
        use_customer_address (checkbox): Use customer's saved address
        discount_code (str): Optional discount code
        item_{item_id} (str): Quantity for each menu item
        action (str): "preview" or "create"
    
    Returns:
        GET: Rendered order_form.html
        POST preview: Rendered order_form.html with price calculation
        POST create: Redirect to orders list on success, form on error
    """
    # Load data needed for the form
    customers = Customer.query.order_by(Customer.first_name).all()
    menu_items = MenuItem.query.order_by(MenuItem.item_id).all()

    if request.method == "GET":
        # Display empty order form
        return render_template("order_form.html",
                               title="New Order",
                               customers=customers,
                               menu_items=menu_items)
    
    elif request.method == "POST":
        # Extract form data
        customer_id = request.form.get("customer_id")
        discount_code = request.form.get("discount_code") or None
        postal_code = request.form.get("postal_code", "").strip()
        action = request.form.get("action")  # "preview" or "create"
        request.form.get("use_customer_address")

        # Fetch customer and discount code objects
        customer = Customer.query.get(customer_id)
        discount = DiscountCode.query.filter_by(discount_code=discount_code).first() if discount_code else None

        # Determine delivery address and postal code
        if request.form.get("use_customer_address"):
            # Get customers saved address and postal code
            postal_code = customer.postal_code
            delivery_address=customer.address
        else:
            # Use manually entered address and postal code
            # Normalize postal code and address from input fields
            postal_code = postal_code.replace(" ", "").upper()
            delivery_address = request.form.get("delivery_address", "").strip()

        # Collect selected order items from form
        order_items = []
        for item in menu_items:
            try:
                amount = int(request.form.get(f"item_{item.item_id}", 0))
            except ValueError:
                amount = 0
            if amount > 0:
                order_items.append((item, amount))

        # Validate required fields
        if not customer or not order_items:
            flash("Please select a valid customer and at least one menu item.", "error")
            return redirect(url_for("create_order.create_order"))
        
        # Assign delivery person based on postal code
        delivery_person_id, pickup_time, expected_delivery_time = assign_delivery_person(postal_code)
    
        # Check if a delivery person is available for this postal code
        if delivery_person_id is None:
            postcodes = [dp.postal_code for dp in DeliveryPerson.query.all()]
            flash(f"No delivery person available for your postal code. Try one of these: {', '.join(postcodes)}", "error")
            return redirect(url_for("create_order.create_order"))
        
        # Categorize items by type for discount calculations
        price_list = list_prices_by_type(order_items)
        
        # Calculate raw price (before discounts)
        raw_price = sum(item.price * amount for item, amount in order_items)

        # Calculate all applicable discounts
        discounts = calculate_discounts(customer, raw_price, price_list["pizzas"], price_list["drinks"], discount)

        # PREVIEW ACTION: Show price breakdown without creating order
        if action == "preview":
            if len(price_list["pizzas"]) < 1: 
                flash("choose at least 1 pizza for a valid order")
            # Just show preview inside the same form
            return render_template("order_form.html",
                               title="New Order",
                               customers=customers,
                               menu_items=menu_items,
                               raw_price=raw_price,
                               total=discounts["total"],
                               messages=discounts["messages"])

        # CREATE ACTION: Actually create the order
        elif action == "create":
            
            try:
                # Validate at least one pizza is in the order
                if len(price_list["pizzas"]) < 1:
                    flash(f"Error creating order: choose at least 1 pizza for a valid order", "error")
                    return redirect(url_for("create_order.create_order")) 
                
                discount_id = discount.discount_id if discount else None

                # Create order object/record
                order = Order(
                    customer_id=customer.customer_id,
                    delivery_person_id=delivery_person_id,  # Use the unpacked variable
                    discount_id=discount_id,
                    delivery_address=delivery_address,
                    postal_code=postal_code,
                    pickup_time=pickup_time,  # Use the unpacked variable
                    total_price = discounts["total"]
                )
                db.session.add(order)
                db.session.flush() # Get order_id for order items

                # Create order items records
                for item, amount in order_items:
                    db.session.add(OrderItem(order_id=order.order_id,
                                         item_id=item.item_id,
                                         amount=amount))
            
                # Update delivery person's availability
                # They will be busy until they finish this delivery
                delivery_person = DeliveryPerson.query.get(delivery_person_id)
                delivery_person.next_available_time = expected_delivery_time

                db.session.commit()

                # Show success message with timing information
                pickup_str = pickup_time.strftime('%H:%M')
                delivery_str = expected_delivery_time.strftime('%H:%M')
                flash(f"Order created! Pickup at {pickup_str}, delivery by {delivery_str}.", "success")
                return redirect(url_for("orders.list_orders"))

            except Exception as e:
                db.session.rollback()
                flash(f"Error creating order: {str(e)}", "error")
                return redirect(url_for("create_order.create_order"))

        # Fallback for unexpected action values
        return redirect(url_for("create_order.create_order"))

# ============================================================================
# STAFF REPORTS ROUTES
# ============================================================================
@staff_reports_bp.route("/staff_reports", methods=["GET"])
def staff_reports():
    """
    Display staff analytics and reports dashboard.
    
    Provides three main reports:
    1. Top 3 pizzas sold in the last 30 days
    2. Undelivered orders (pending or out for delivery)
    3. Monthly earnings report with filtering options
    
    Monthly earnings report can be filtered by:
    - Month and year
    - Customer gender
    - Age range (min and max age)
    - Postal code
    
    Query Parameters:
        month (int): Month number (1-12), defaults to current month
        year (int): Year, defaults to current year
        gender (int): Gender filter (0=Female, 1=Male, 2=Other), optional
        min_age (int): Minimum customer age, optional
        max_age (int): Maximum customer age, optional
        postal_code (str): Postal code filter, optional
    
    Returns:
        Rendered staff_reports.html with analytics data
    """
    # Calculate date one month ago for top pizzas
    one_month_ago = datetime.now(ZoneInfo("Europe/Amsterdam")) - timedelta(days=30)
    
    # Query top 3 pizzas sold in the last month
    top_pizzas = (
        db.session.query(
            Pizza.name,
            func.sum(OrderItem.amount).label('total_sold')
        )
        .join(MenuItem, MenuItem.item_ref_id == Pizza.pizza_id)
        .join(OrderItem, OrderItem.item_id == MenuItem.item_id)
        .join(Order, Order.order_id == OrderItem.order_id)
        .filter(MenuItem.item_type == 'pizza')
        .filter(Order.order_time >= one_month_ago)
        .group_by(Pizza.pizza_id, Pizza.name)
        .order_by(func.sum(OrderItem.amount).desc())
        .limit(3)
        .all()
    )
    
    # Query undelivered orders (pending or out_for_delivery status)
    now = datetime.now(ZoneInfo("Europe/Amsterdam"))
    all_orders = Order.query.order_by(Order.order_time.desc()).all()
    
    undelivered_orders = []
    for order in all_orders:
        if order.status in ['pending', 'out_for_delivery']:
            undelivered_orders.append(order)

    # Monthly earnings report logic
    # Get filter parameters from query string
    gender_filter = request.args.get('gender', type=int)
    min_age = request.args.get('min_age', type=int)
    max_age = request.args.get('max_age', type=int)
    postal_code_filter = request.args.get('postal_code', '').strip().replace(" ", "").upper()
    
    # Get selected month and year (default to current month)
    now = datetime.now(ZoneInfo("Europe/Amsterdam"))
    selected_month = request.args.get('month', default=now.month, type=int)
    selected_year = request.args.get('year', default=now.year, type=int)
    
    # Build the base query for monthly earnings
    query = (
        db.session.query(
            Customer.customer_id,
            Customer.first_name,
            Customer.last_name,
            Customer.gender,
            Customer.birthdate,
            func.sum(Order.total_price).label('total_spent')
        )
        .join(Order, Order.customer_id == Customer.customer_id)
        .filter(extract('month', Order.order_time) == selected_month)
        .filter(extract('year', Order.order_time) == selected_year)
    )
    
    # Apply gender filter if provided
    if gender_filter is not None:
        query = query.filter(Customer.gender == gender_filter)
    
    # Apply age filters if provided
    if min_age is not None or max_age is not None:
        today = date.today()
        if max_age is not None:
            # Customer must be born after this date to be younger than max_age
            min_birthdate = date(today.year - max_age - 1, today.month, today.day)
            query = query.filter(Customer.birthdate > min_birthdate)
        if min_age is not None:
            # Customer must be born before this date to be older than min_age
            max_birthdate = date(today.year - min_age, today.month, today.day)
            query = query.filter(Customer.birthdate <= max_birthdate)
    
    # Apply postal code filter if provided
    if postal_code_filter:
        query = query.filter(Order.postal_code == postal_code_filter)
    
    # Group by customer and order by total spent (descending)
    results = (
        query
        .group_by(Customer.customer_id, Customer.first_name, Customer.last_name, 
                  Customer.gender, Customer.birthdate)
        .order_by(func.sum(Order.total_price).desc())
        .all()
    )
    
    # Calculate total earnings for the filtered results
    total_earnings = sum(r.total_spent for r in results) if results else 0
    
    # Calculate age for each customer and format data
    customers_with_age = []
    for r in results:
        age = calculate_age(r.birthdate)
        customers_with_age.append({
            'customer_id': r.customer_id,
            'full_name': f"{r.first_name} {r.last_name}",
            'gender': r.gender,
            'age': age,
            'total_spent': float(r.total_spent)
        })
    
    # Get available years for dropdown (from first order to current year)
    first_order = db.session.query(func.min(Order.order_time)).scalar()
    available_years = range(first_order.year, now.year + 1) if first_order else [now.year]
    
    return render_template("staff_reports.html",
                         title="Staff Reports",
                         top_pizzas=top_pizzas,
                         undelivered_orders=undelivered_orders,
                         customers=customers_with_age,
                         total_earnings=total_earnings,
                         selected_month=selected_month,
                         selected_year=selected_year,
                         available_years=available_years,
                         filters={
                             'gender': gender_filter,
                             'min_age': min_age,
                             'max_age': max_age,
                             'postal_code': postal_code_filter
                         })

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================
def calculate_age(birthdate):
    """
    Calculate age from birthdate.
    
    Properly accounts for whether birthday has occurred this year.
    
    Args:
        birthdate (date): Person's date of birth
    
    Returns:
        int: Age in years
    """
    today = date.today()

    # Calculate initial age as year difference
    age = today.year - birthdate.year

    # Adjust if birthday hasn't occurred yet this year
    # Check if current month is before birth month, OR
    # if months match but current day is before birth day
    if today.month < birthdate.month or (today.month == birthdate.month and today.day < birthdate.day):
        age -= 1
    return age

def list_prices_by_type(order_items):
    """
    Extract and organize item prices from an order by item type.
    
    This helper function processes order items and creates separate lists of
    individual prices for pizzas and drinks. Each price appears in the list
    as many times as the item quantity in the order.
    
    Purpose:
        - Prepares price data for discount calculations
        - Enables discount logic to target cheapest items (by using min())
        - Supports check constraints (e.g., "order must contain at least 1 pizza")
    
    Args:
        order_items (list of tuple): List of (MenuItem, quantity) tuples
            - MenuItem: Menu item object with item_type and price properties
            - quantity (int): Number of this item in the order
    
    Returns:
        dict: Dictionary containing two keys:
            - 'pizzas' (list of float): Individual prices for each pizza ordered
            - 'drinks' (list of float): Individual prices for each drink ordered
    
    Implementation Details:
        - Uses list.extend() to add multiple prices at once
        - Multiplies price into a list: [price] * amount
          Example: [10.99] * 2 becomes [10.99, 10.99]
        - Only processes 'pizza' and 'drink' item types
        - Desserts are intentionally excluded (not used in discount logic)
    
    Why Individual Prices?
        Storing each item's price separately (rather than totals) allows the
        discount calculation function to:
        - Remove the cheapest items when applying free item discounts
        - Count exact quantities for validation rules
        - Process multiple free items without complex calculations
    
    Note:
        This function does not modify the original order_items list.
        It creates new lists containing price values only.
    """
    # Initialize empty lists for each item type
    pizza_prices = []
    drink_prices = []

    # Process each order item
    for menu_item, amount in order_items:
        if menu_item.item_type == "pizza":
            # Add pizza price to list 'amount' times
            pizza_prices.extend([menu_item.price] * amount)
        elif menu_item.item_type == "drink":
            # Add drink price to list 'amount' times
            drink_prices.extend([menu_item.price] * amount)
        # Note: Desserts are not tracked in this function as they're not used in discount calculations
    # Return organized price data
    return {"pizzas": pizza_prices, "drinks": drink_prices}

def assign_delivery_person(postal_code):
    """
    Find and assign an available delivery person for a given postal code.
    
    This function handles the delivery logistics by:
    1. Finding a delivery person who serves the specified postal code
    2. Determining when they'll be available for pickup
    3. Calculating expected delivery time (pickup + 30 minutes)
    
    Delivery Logic:
        - Each postal code is served by a specific delivery person
        - Pickup occurs at max(now, delivery_person.next_available_time)
        - Delivery takes 30 minutes from pickup
        - All times are timezone-aware (Europe/Amsterdam)
    
    Args:
        postal_code (str): The delivery postal code (e.g., "6222RT" or "6222 RT")
                          Can contain spaces and mixed case
    
    Returns:
        tuple: A 3-element tuple containing:
            - delivery_person_id (int or None): ID of the assigned delivery person
            - pickup_time (datetime or None): When the order will be picked up
            - expected_delivery_time (datetime or None): When delivery is expected
            
            Returns (None, None, None) if no delivery person serves this postal code
    
    Note:
        - Postal codes are normalized (uppercase, no spaces) for matching
        - Times are timezone-aware using Europe/Amsterdam timezone
        - The function does NOT update the delivery person's availability
          (that must be done separately when the order is created)
    """
    # Normalize postal code (remove spaces, convert to uppercase)
    postal_code_normalized = postal_code.replace(" ", "").upper()
    
    # Query delivery person who serves this postal code
    delivery_person = (
        DeliveryPerson.query
        .filter(DeliveryPerson.postal_code == postal_code_normalized)
        .first()
    )
    
    # If no delivery person serves this postal code, return None
    if not delivery_person:
        return None, None, None
    
    # Calculate pickup and delivery times
    now = datetime.now(ZoneInfo("Europe/Amsterdam"))
    
    # Make next_available_time timezone-aware if it's naive
    next_available = delivery_person.next_available_time_aware
    
    # Now you can compare them
    pickup_time = max(now, next_available)
    
    # Expected delivery time = pickup time + 30 minutes for delivery
    expected_delivery_time = pickup_time + timedelta(minutes=30)
    
    return delivery_person.delivery_person_id, pickup_time, expected_delivery_time

def valid_birthday_discount(customer):
    """
    Check if a customer is eligible for their birthday discount today.
    
    Birthday Discount Rules:
        - Customer gets 1 free pizza and 1 free drink on their birthday
        - Discount can only be used once per birthday
        - If customer already placed an order today, discount was used
        - Customer must have a birthdate on file
    
    Business Logic:
        The system assumes every order contains at least one pizza, so if
        a customer has already ordered today, they've already received their
        free pizza. We don't track whether they used the free drink, as the
        discount is considered "used" after the first order of the day.
    
    Args:
        customer (Customer): Customer object to check for birthday eligibility
    
    Returns:
        bool: True if customer is eligible for birthday discount, False otherwise
            - False if customer has no birthdate on file
            - False if customer already placed an order today
            - True if it's their birthday and no orders placed yet today
    
    Note:
        This function checks the order_time against today's date, not the
        customer's birthdate directly. The birthday check happens elsewhere
        in the discount calculation flow.
    """
    # Check if customer has a birthdate
    if not customer.birthday:
        return False

    # Ceck if customer has already placed an order today
    for ord in customer.orders:
        # Compare order date to today's date
        if (
            ord.order_time.day == date.today().day
            and ord.order_time.month == date.today().month
            and ord.order_time.year == date.today().year
        ):  
            # Customer has already ordered today - discount used
            return False
    
    # No orders today - customer can use birthday discount
    return True
    
def valid_discount_code(customer, discount):
    """
    Validate whether a customer can use a specific discount code.
    
    Discount Code Rules:
        - Each discount code can only be used once per customer
        - Discount code must exist in the database
        - Customer cannot reuse a code from a previous order
    
    Args:
        customer (Customer): Customer attempting to use the discount code
        discount (DiscountCode or None): Discount code object to validate
                                         Can be None if no code provided
    
    Returns:
        bool or None: Validation result:
            - None: No discount code provided (discount is None)
            - False: Invalid discount code (doesn't exist or already used)
            - True: Valid discount code that customer can use
    
    Implementation Notes:
        - Checks discount against ALL discount codes in database
        - Iterates through customer's order history to check for prior usage
        - One-time use is enforced at the customer level, not globally
    """
    # Return None if no discount code provided
    if (discount is None):
        return None

    # Verify discount code exists in database
    discounts = DiscountCode.query.all()
    if (discount not in discounts):
        return False
    
    # Check if customer has already used this discount code in a previous order
    for ord in customer.orders:
        if ord.discount_id == discount.discount_id:
            return False
    
    # Discount code is valid and unused by this customer
    return True

def calculate_discounts(customer, raw_price, pizza_prices, drink_prices, discount):
    """
    Calculate all applicable discounts for an order and return the final price.
    
    This is the main discount calculation engine that applies multiple discount
    types in a specific order. It processes birthday discounts, loyalty rewards,
    and promotional discount codes.
    
    Discount Types Applied (in order):
        1. Birthday Discount: 1 free pizza + 1 free drink (if today is birthday)
        2. Loyalty Discount: 1 free pizza per 10 pizzas ordered historically
        3. Discount Code: Percentage off total (e.g., 10% off with WELCOME10)
    
    Discount Application Logic:
        - Free items are applied by removing the cheapest qualifying items
        - Pizza discounts remove the cheapest pizza(s) from the order
        - Drink discounts remove the cheapest drink(s) from the order
        - Percentage discount is applied AFTER free items are removed
        - Discount codes must be valid and unused by the customer
    
    Args:
        customer (Customer): Customer placing the order (for discount eligibility)
        raw_price (float): Total order price before any discounts
        pizza_prices (list of float): List of individual pizza prices in the order
                                      Modified in-place as free items are removed
        drink_prices (list of float): List of individual drink prices in the order
                                      Modified in-place as free items are removed
        discount (DiscountCode or None): Optional discount code object to apply
    
    Returns:
        dict: Dictionary containing:
            - 'total' (float): Final price after all discounts, rounded to 2 decimals
            - 'messages' (list of str): Human-readable list of applied discounts
    
    Calculation Details:
        Birthday Discount:
            - Checks if today is customer's birthday
            - Checks if discount hasn't been used today
            - Removes price of cheapest pizza and drink from order
        
        Loyalty Discount:
            - Formula: (total_pizzas + new_pizzas) // 10 - (total_pizzas // 10)
            - Example: Customer has ordered 12 pizzas, ordering 3 more
              - New total: 15 pizzas → 15 // 10 = 1 free pizza
              - Previous: 12 // 10 = 1 free pizza already earned
              - Difference: 1 - 1 = 0 new free pizzas this order
            - Example 2: Customer has 8 pizzas, ordering 5 more
              - New total: 13 pizzas → 13 // 10 = 1 free pizza
              - Previous: 8 // 10 = 0 free pizzas
              - Difference: 1 - 0 = 1 free pizza this order
        
        Discount Code:
            - Validates code hasn't been used by customer before
            - Applies percentage reduction to remaining total
            - Formula: subtotal * (100 - percentage) / 100
    
    Side Effects:
        - Modifies pizza_prices and drink_prices lists by removing discounted items
        - Does NOT create database records (that happens in the order creation)
    
    Note:
        - All free item discounts target the CHEAPEST items first
        - This benefits the business while still providing value to customers
        - Final price is rounded to 2 decimal places for currency precision
    """
    # Start with the raw price before discounts
    subtotal = raw_price

    # List to store human-readable discount messages
    discounts_applied = []

    # Check how many free pizza's and drinks to apply
    free_pizza = 0
    free_drink = 0

    # ========== BIRTHDAY DISCOUNT ==========
    # Check if customer is eligible for birthday discount
    if valid_birthday_discount(customer):
        free_pizza += 1 # One free pizza
        free_drink += 1 # One free drink
        discounts_applied.append("happy birthday! you get one pizza and drink for free")

    # ========== LOYALTY DISCOUNT (10-PIZZA REWARD) ==========
    # Calculate how many free pizzas customer earns from this order
    # Formula explanation:
    #   - (total + new) // 10: Total free pizzas after this order
    #   - (total) // 10: Free pizzas already earned before this order
    #   - Difference: New free pizzas earned with this order
    ten_discount = (
        customer.total_pizzas_ordered + len(pizza_prices)) // 10 - (customer.total_pizzas_ordered // 10
    )

    if ten_discount>0:
        free_pizza+=ten_discount
        discounts_applied.append(f"10-pizza discount applied ({ten_discount} free pizza('s))")

    # ========== APPLY FREE PIZZA DISCOUNTS ==========
    # Remove the cheapest pizzas from the order prices (free pizzas)
    for i in range(free_pizza):
        if pizza_prices:                    # Check if there are pizzas to discount
            cheapest = min(pizza_prices)    # Find cheapest pizza
            subtotal -= cheapest            # Subtract from total price
            pizza_prices.remove(cheapest)   # Remove from list 

    # ========== APPLY FREE DRINK DISCOUNTS ==========
    # Remove the cheapest drinks from the order  price (free drinks)
    for i in range(free_drink):
        if drink_prices:                    # Check if there are drinks to discount
            cheapest = min(drink_prices)    # Find cheapest drink
            subtotal -= cheapest            # Subtract from total price
            drink_prices.remove(cheapest)   # Remove from list

    # ========== DISCOUNT CODE ==========
    # Apply percentage-based discount code if provided and valid
    if discount:
        # Validate that customer hasn't used this code before
        if valid_discount_code(customer, discount) == True:
            # Calculate multiplier: 10% off means multiply by 0.90
            discount_multiplier = (100 - discount.percentage) / 100
            subtotal *= discount_multiplier
            discounts_applied.append(f"discount code applied, {discount.percentage}% off")
        else:
            # Discount code is invalid or already used
            discounts_applied.append(f"discount code is invalid")
            
    # Return final price rounded to 2 decimals and list of applied discounts
    return {"total": round(subtotal, 2), "messages": discounts_applied}
    