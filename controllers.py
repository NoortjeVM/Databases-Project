from flask import Blueprint, render_template, request, redirect, url_for, flash
from sqlalchemy.orm import selectinload
from models import db, Customer, MenuItem, Order, OrderItem, Ingredient, Pizza, Drink, Dessert, DeliveryPerson, DiscountCode
from datetime import date, datetime

customers_bp = Blueprint("customers", __name__)
menu_items_bp = Blueprint("menu_items", __name__, url_prefix="/menu-items")
orders_bp = Blueprint("orders", __name__)
ingredients_bp = Blueprint("ingredients", __name__)
pizzas_bp = Blueprint("pizzas", __name__)


# customers
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


# Menu display
@menu_items_bp.route("/")
def list_menu_items():
    pizzas = Pizza.query.all()
    drinks = Drink.query.all()
    desserts = Dessert.query.all()
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


# Ingredient display
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
@orders_bp.route("/orders")
def list_orders():
    orders = (Order.query
              .options(selectinload(Order.customer),
                       selectinload(Order.delivery_person),
                       selectinload(Order.discount_code),
                       selectinload(Order.order_items).selectinload(OrderItem.menu_item))
              .order_by(Order.order_id)
              .all())
    return render_template("orders.html", title="Orders", orders=orders)

@orders_bp.route("/orders/new")
def new_order():
    customers = Customer.query.order_by(Customer.first_name).all()
    menu_items = MenuItem.query.order_by(MenuItem.item_id).all()  # can't order by .name (Python property)
    delivery_persons = DeliveryPerson.query.order_by(DeliveryPerson.delivery_person_first_name).all()
    discount_codes = DiscountCode.query.order_by(DiscountCode.discount_code).all()
    return render_template("order_form.html", title="New Order", 
                         customers=customers, menu_items=menu_items,
                         delivery_persons=delivery_persons, discount_codes=discount_codes)

@orders_bp.route("/orders", methods=["POST"])
def create_order():
    customer_id = request.form.get("customer_id")
    discount_id = request.form.get("discount_id") or None
    delivery_address = request.form.get("delivery_address", "").strip()
    postal_code = request.form.get("postal_code", "").strip()
    menu_item_id = request.form.get("menu_item_id")
    amount = request.form.get("amount", "1")

    
    if delivery_person_id is None:
        flash("Order placement failed, no delivery person available in your postal code.", "error")

    # Validate the amount
    try:
        amount = int(amount)
        if amount < 1:
            amount = 1
    except:
        amount = 1
    
    customer = Customer.query.get(customer_id)
    delivery_person_id = assign_delivery_person(postal_code)
    menu_item = MenuItem.query.get(menu_item_id)

    # Check if objects exist
    if not customer or not menu_item:
        flash("Please select valid customer and menu item.", "error")
        return redirect(url_for("orders.new_order"))
    
    # Check if a delivery persion is found
    if delivery_person_id is None:
        flash("No delivery person available for your postal code.", "error")
        return redirect(url_for("orders.new_order"))
    
    try:
        # Calculate total price without discount
        total_price = float(menu_item.price) * amount   # use .price property
        
        # Apply discount if provided
        if discount_id:
            discount = DiscountCode.query.get(discount_id)
            if discount:
                total_price = total_price * (1 - discount.percentage / 100)
        
        order = Order(
            customer_id=customer.customer_id,
            delivery_person_id=delivery_person_id,
            discount_id=discount_id,
            total_price=total_price,
            delivery_address=delivery_address,
            postal_code=postal_code
        )
        db.session.add(order)
        db.session.flush()  # Get order ID
        
        # Add order item
        order_item = OrderItem(
            order_id=order.order_id,
            item_id=menu_item.item_id,
            amount=amount
        )
        db.session.add(order_item)
        db.session.commit()
        
        flash("Order created successfully.", "success")
        return redirect(url_for("orders.list_orders"))
    except Exception as e:
        # Something went wrong - undo everything
        db.session.rollback()
        flash(f"Error creating order: {str(e)}", "error")
        return redirect(url_for("orders.new_order"))

def assign_delivery_person(order):
    for dps in DeliveryPerson:
        # TODO: look at how the post code string is parsed, put both in all caps no spaces
        if DeliveryPerson.postal_code == order.postal_code:
            # TODO put the order in the queue of the delivery person.
            # where is that queue stored? do we need an extra column in the db?
            return dps.delivery_person_id
    return None

def valid_birthday_discount(order):
    if order.customer.birthday:
        # if the customer has already placed an order today they have already received their free pizza (every order contains pizza so that is always true)
        # decide: do we want to check if they have also used their free drink in that order?
        # -> I say no, just let them use birthday discount on the first order of that day.

        # so check if they have already placed another order today
        # (on which the discount was then automatically used) -> if not, they get free pizza and drink
        for ord in order.customer.orders:
            if (
                ord.order_time.day == date.today().day
                and ord.order_time.month == date.today().month
                and ord != order
            ):
                return False
        return True
    return False


def calculate_discounts(order):
    subtotal = order.raw_price

    # Check discounts
    free_pizza = order.customer.available_ten_pizza_discount
    free_drink = 0

    if valid_birthday_discount(order):
        free_pizza += 1
        free_drink += 1

    if free_pizza > 0 or free_drink > 0:
        pizza_prices = []
        drink_prices = []

        # Collect pizza and drink prices in the order
        for item in order.order_items:
            item_type = item.menu_item.__class__.__name__.lower()
            if item_type == "pizza":
                # repeats the price in the list as many times as the item is in the order
                pizza_prices.extend([item.menu_item.get_price()] * item.amount)
            elif item_type == "drink":
                drink_prices.extend([item.menu_item.get_price()] * item.amount)

        # Apply free pizza discount
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

    # Apply discount code if one is chosen
    if order.discount_code:
        discount_multiplier = (100 - order.discount_code.percentage) / 100
        subtotal *= discount_multiplier

    return round(subtotal, 2)


def set_discounts_to_used(order):
    # for birthday discounts we automatically check if it was already used so we dont do that here
    # set discount code to used
    # if order.discount_code:
    # TODO: sql update such that customer_discount.used = True

    # mark used free pizza discounts as used by changing field
    # ten_pizza_discount_used in the db
    pizza_count = 0
    for item in order.order_items:
        item_type = item.menu_item.__class__.__name__.lower()
        if item_type == "pizza":
            pizza_count += item.amount

    if valid_birthday_discount(order):
        # since they first use free birthday pizza, only then look at other free pizza discounts
        pizza_count -= 1

    # add the free pizza discounts they use for the rest of the order to the used discounts column
    order.customer.ten_pizza_discount_used += min(
        order.customer.available_ten_pizza_discount, pizza_count
    )
