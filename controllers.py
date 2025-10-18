from flask import Blueprint, render_template, request, redirect, url_for, flash
from sqlalchemy.orm import selectinload
from sqlalchemy import func, and_, extract
from models import db, Customer, MenuItem, Order, OrderItem, Ingredient, Pizza, Drink, Dessert, DeliveryPerson, DiscountCode
from datetime import date, datetime, timezone
from zoneinfo import ZoneInfo

customers_bp = Blueprint("customers", __name__)
menu_items_bp = Blueprint("menu_items", __name__, url_prefix="/menu-items")
orders_bp = Blueprint("orders", __name__)
ingredients_bp = Blueprint("ingredients", __name__)
create_order_bp = Blueprint("create_order", __name__)
staff_reports_bp = Blueprint("staff_reports", __name__)


#customers
@customers_bp.route("/customers")
def list_customers():
    customers = Customer.query.order_by(Customer.customer_id).all()
    return render_template("customers.html", title="Customers", customers=customers)

@customers_bp.route("/customers/new")
def new_customer():
    return render_template("customer_form.html", title="New Customer", customer=None)

@customers_bp.route("/customers", methods=["POST"])
def create_customer():
    first_name = request.form.get("first_name", "").strip()
    last_name = request.form.get("last_name", "").strip()
    phone_number = request.form.get("phone_number", "").strip()
    address = request.form.get("address", "").strip()
    birthdate_str = request.form.get("birthdate", "").strip()
    gender = request.form.get("gender", "").strip()
    
    if not all([first_name, last_name, phone_number, birthdate_str]):
        flash("First name, last name, phone number, and birthdate are required.", "error")
        return redirect(url_for("customers.new_customer"))
    
    try:
        birthdate = datetime.strptime(birthdate_str, '%Y-%m-%d').date()
        gender_val = int(gender) if gender else None
        customer = Customer(
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            address=address,
            birthdate=birthdate,
            gender=gender_val
        )
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


# menu display
@menu_items_bp.route("/")
def list_menu_items():
    pizzas = Pizza.query.all()
    drinks = Drink.query.all()
    desserts = Dessert.query.all()
    print(pizzas[1].label)
    return render_template("menu_items.html", title="Menu Items", pizzas=pizzas, drinks=drinks, desserts=desserts)

@menu_items_bp.route("/new")
def new_menu_item():
    return render_template("menu_item_form.html", title="New Menu Item", menu_item=None)

@menu_items_bp.route("/", methods=["POST"])
def create_menu_item():
    item_name = request.form.get("item_name", "").strip()
    item_price = request.form.get("item_price", "").strip()
    item_type = request.form.get("item_type", "").strip()
    
    if not item_name or (item_type != "pizza" and not item_price):
        flash("Item name (and price for drinks/desserts) are required.", "error")
        return redirect(url_for("menu_items.new_menu_item"))
    
    try:
        menu_item = None
        if item_type == "pizza":
            pizza = Pizza(name=item_name)
            db.session.add(pizza)
            db.session.flush()
            menu_item = MenuItem(item_type="pizza", item_ref_id=pizza.pizza_id)
        elif item_type == "drink":
            price = float(item_price)
            drink = Drink(name=item_name, price=price)
            db.session.add(drink)
            db.session.flush()
            menu_item = MenuItem(item_type="drink", item_ref_id=drink.drink_id)
        elif item_type == "dessert":
            price = float(item_price)
            dessert = Dessert(name=item_name, price=price)
            db.session.add(dessert)
            db.session.flush()
            menu_item = MenuItem(item_type="dessert", item_ref_id=dessert.dessert_id)

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

@ingredients_bp.route("/ingredients")
def list_ingredients():
    ingredients = Ingredient.query.order_by(Ingredient.ingredient_id).all()
    return render_template("ingredients.html", title="Ingredients", ingredients=ingredients)

@ingredients_bp.route("/ingredients/new")
def new_ingredient():
    return render_template("ingredient_form.html", title="New Ingredient", ingredient=None)

@ingredients_bp.route("/ingredients", methods=["POST"])
def create_ingredient():
    ingredient_name = request.form.get("ingredient_name", "").strip()
    price = request.form.get("price", "").strip()
    vegetarian = request.form.get("vegetarian") == "on"
    vegan = request.form.get("vegan") == "on"
    
    if not ingredient_name or not price:
        flash("Ingredient name and price are required.", "error")
        return redirect(url_for("ingredients.new_ingredient"))
    
    try:
        price_val = float(price)
        if price_val <= 0:
            flash("Price must be greater than 0.", "error")
            return redirect(url_for("ingredients.new_ingredient"))
        
        ingredient = Ingredient(
            ingredient_name=ingredient_name,
            price=price_val,
            vegetarian=vegetarian,
            vegan=vegan
        )
        db.session.add(ingredient)
        db.session.commit()
        flash("Ingredient created successfully.", "success")
        return redirect(url_for("ingredients.list_ingredients"))
    except ValueError:
        flash("Price must be a valid number.", "error")
        return redirect(url_for("ingredients.new_ingredient"))
    except Exception as e:
        flash(f"Error creating ingredient: {str(e)}", "error")
        return redirect(url_for("ingredients.new_ingredient"))

# Orders
@orders_bp.route("/list_orders")
def list_orders():
    orders = Order.query.order_by(Order.order_time.desc()).all()
    print(f"amount of orders: {len(orders)}")
    return render_template("orders.html", orders=orders)

@create_order_bp.route("/create_order", methods=["GET","POST"])
def create_order():
    #load data
    customers = Customer.query.order_by(Customer.first_name).all()
    menu_items = MenuItem.query.order_by(MenuItem.item_id).all()

    if request.method == "GET":
        return render_template("order_form.html",
                               title="New Order",
                               customers=customers,
                               menu_items=menu_items)
    
    elif request.method == "POST":
        customer_id = request.form.get("customer_id")
        discount_code = request.form.get("discount_code") or None
        delivery_address = request.form.get("delivery_address", "").strip()
        postal_code = request.form.get("postal_code", "").strip()
        action = request.form.get("action")  # "preview" or "create"
        request.form.get("use_customer_address")

        customer = Customer.query.get(customer_id)
        discount = DiscountCode.query.filter_by(discount_code=discount_code).first() if discount_code else None

        if request.form.get("use_customer_address"):
            postal_code = customer.postal_code
        else:
            # Normalize postal code from input
            postal_code = postal_code.replace(" ", "").upper()

        #collect selected order items
        order_items = []
        for item in menu_items:
            try:
                amount = int(request.form.get(f"item_{item.item_id}", 0))
            except ValueError:
                amount = 0
            if amount > 0:
                order_items.append((item, amount))

        #validation
        if not customer or not order_items:
            flash("Please select a valid customer and at least one menu item.", "error")
            return redirect(url_for("create_order.create_order"))
        
        # Assign delivery person based on postal code
        delivery_person_id, pickup_time, expected_delivery_time = assign_delivery_person(postal_code)
    
        # Check if a delivery person is found
        if delivery_person_id is None:
            postcodes = [dp.postal_code for dp in DeliveryPerson.query.all()]
            flash(f"No delivery person available for your postal code. Try one of these: {', '.join(postcodes)}", "error")
            return redirect(url_for("create_order.create_order"))
        
        price_list = list_prices_by_type(order_items)
        
        raw_price = sum(item.price * amount for item, amount in order_items)
        discounts = calculate_discounts(customer, raw_price, price_list["pizzas"], price_list["drinks"], discount)

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

        elif action == "create":
            
            try:
                if len(price_list["pizzas"]) < 1:
                    flash(f"Error creating order: choose at least 1 pizza for a valid order", "error")
                    return redirect(url_for("create_order.create_order")) 
                
                discount_id = discount.discount_id if discount else None

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
                db.session.flush()

                for item, amount in order_items:
                    db.session.add(OrderItem(order_id=order.order_id,
                                         item_id=item.item_id,
                                         amount=amount))
            
                # Update delivery person's availability
                # They will be busy until they finish this delivery
                delivery_person = DeliveryPerson.query.get(delivery_person_id)
                delivery_person.next_available_time = expected_delivery_time

                db.session.commit()

                set_discount_to_used(order) #puts any used idscount in the list of a customers used discounts

                # Show success message with timing information
                pickup_str = pickup_time.strftime('%H:%M')
                delivery_str = expected_delivery_time.strftime('%H:%M')
                flash(f"Order created! Pickup at {pickup_str}, delivery by {delivery_str}.", "success")
                return redirect(url_for("orders.list_orders"))

            except Exception as e:
                db.session.rollback()
                flash(f"Error creating order: {str(e)}", "error")
                return redirect(url_for("create_order.create_order"))

        # Fallback
        return redirect(url_for("create_order.create_order"))


#helper method for check constraint and discount calculations
def list_prices_by_type(order_items):
    pizza_prices = []
    drink_prices = []

     # count amount of pizza's and put pizza and drink prices in a list
    for menu_item, amount in order_items:
        if menu_item.item_type == "pizza":
            # repeats the price in the list as many times as the item is in the order
            pizza_prices.extend([menu_item.price] * amount)
        elif menu_item.item_type == "drink":
            drink_prices.extend([menu_item.price] * amount)
    return {"pizzas": pizza_prices, "drinks": drink_prices}


@staff_reports_bp.route("/staff_reports", methods=["GET"])
def staff_reports():
    from datetime import timedelta
    from sqlalchemy import func, extract
    
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
    
    # Query undelivered orders (pending or out_for_delivery)
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
    
    # Apply filters
    if gender_filter is not None:
        query = query.filter(Customer.gender == gender_filter)
    
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
    
    if postal_code_filter:
        query = query.filter(Order.postal_code == postal_code_filter)
    
    # Group by customer and order by total spent
    results = (
        query
        .group_by(Customer.customer_id, Customer.first_name, Customer.last_name, 
                  Customer.gender, Customer.birthdate)
        .order_by(func.sum(Order.total_price).desc())
        .all()
    )
    
    # Calculate total earnings
    total_earnings = sum(r.total_spent for r in results) if results else 0
    
    # Calculate age for each customer
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

def calculate_age(birthdate):
    """Calculate age from birthdate"""
    today = date.today()
    age = today.year - birthdate.year
    if today.month < birthdate.month or (today.month == birthdate.month and today.day < birthdate.day):
        age -= 1
    return age

def assign_delivery_person(postal_code):
    """
    Find a delivery person for the given postal code.
    Returns (delivery_person_id, pickup_time, expected_delivery_time) tuple if found,
    (None, None, None) otherwise.
    """
    from datetime import timedelta
    
    # Normalize postal code (remove spaces, convert to uppercase)
    postal_code_normalized = postal_code.replace(" ", "").upper()
    
    # Query delivery person who serves this postal code
    delivery_person = (
        DeliveryPerson.query
        .filter(DeliveryPerson.postal_code == postal_code_normalized)
        .first()
    )
    
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
    if not customer.birthday:
        return False
        
    # if the customer has already placed an order today they have already received their free pizza (every order contains pizza so that is always true)
    # decide: do we want to check if they have also used their free drink in that order?
    # -> no, just let them use birthday discount on the first order of that day.

    # so check if they have already placed another order today
    # (on which the discount was then automatically used) -> if not, they get free pizza and drink
    for ord in customer.orders:
        if (
            ord.order_time.day == date.today().day
            and ord.order_time.month == date.today().month
            and ord.order_time.year == date.today().year
        ):
            return False
    return True
    


def valid_discount_code(customer, discount):
    # method that checks if a customer has already placed an order with this discount
    if (discount is None):
        return None

    discounts = DiscountCode.query.all()
    if (discount not in discounts):
        return False
    
    for ord in customer.orders:
        if ord.discount_id == discount.discount_id:
            return False
        
    return True

#discount is the actual discountcode object, not a string
def calculate_discounts(customer, raw_price, pizza_prices, drink_prices, discount):
    subtotal = raw_price
    discounts_applied = []

    # Check discounts
    free_pizza = 0
    free_drink = 0

    if valid_birthday_discount(customer):
        free_pizza += 1
        free_drink += 1
        discounts_applied.append("happy birthday! you get one pizza and drink for free")

    # apply 10 pizza discount with how many the remainder of division by 10 has increased 
    ten_discount = (customer.total_pizzas_ordered + len(pizza_prices)) // 10 - (customer.total_pizzas_ordered // 10)
    if ten_discount>0:
        free_pizza+=ten_discount
        discounts_applied.append(f"10-pizza discount applied ({ten_discount} free pizza('s))")

    # Apply free pizza discount on cheapest pizza's
    for i in range(free_pizza):
        if pizza_prices:
            cheapest = min(pizza_prices)
            subtotal -= cheapest
            pizza_prices.remove(cheapest)

    # Apply birthday drink discount
    for i in range(free_drink):
        if drink_prices:
            cheapest = min(drink_prices)
            subtotal -= cheapest
            drink_prices.remove(cheapest)

    # Apply discount code if one is chosen and if it's valid
    if discount:
        if valid_discount_code(customer, discount) == True:
            discount_multiplier = (100 - discount.percentage) / 100
            subtotal *= discount_multiplier
            discounts_applied.append(f"discount code applied, {discount.percentage}% off")
        else:
            discounts_applied.append(f"discount code is invalid")
    
    return {"total": round(subtotal, 2), "messages": discounts_applied}
    

def set_discount_to_used(order):
    # for birthday discounts we automatically check if it was already used so we dont do that here

    # set discount code in used discounts of the customer
    if order.discount_code and valid_discount_code(order.customer, order.discount_code) == True:
        order.customer.discounts.append(order.discount_code)
        db.session.commit()