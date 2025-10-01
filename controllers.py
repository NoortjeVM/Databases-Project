from flask import Blueprint, render_template, request, redirect, url_for, flash
from sqlalchemy.orm import selectinload
from models import db, Customer, MenuItem, Order, OrderItem, Ingredient, Pizza, Drink, Dessert, DeliveryPerson, DiscountCode
from datetime import date, datetime

customers_bp = Blueprint("customers", __name__)
menu_items_bp = Blueprint("menu_items", __name__, url_prefix="/menu-items")
orders_bp = Blueprint("orders", __name__)
ingredients_bp = Blueprint("ingredients", __name__)
pizzas_bp = Blueprint("pizzas", __name__)

# ----------------------
# Customers
# ----------------------
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

# ----------------------
# Menu Items
# ----------------------
@menu_items_bp.route("/")
def list_menu_items():
    menu_items = MenuItem.query.order_by(MenuItem.item_id).all()
    return render_template("menu_items.html", title="Menu Items", menu_items=menu_items)

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

# ----------------------
# Ingredients
# ----------------------
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

# ----------------------
# Pizzas
# ----------------------
@pizzas_bp.route("/pizzas")
def list_pizzas():
    pizzas = (
        Pizza.query
        .options(selectinload(Pizza.ingredients))
        .order_by(Pizza.pizza_id)
        .all()
    )
    return render_template("pizzas.html", title="Pizzas", pizzas=pizzas)

# ----------------------
# Orders
# ----------------------
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

    delivery_person_id = assign_delivery_person(postal_code)
    if delivery_person_id is None:
        flash("Order placement failed, no delivery person available in your postal code.", "error")

    try:
        amount = int(amount)
        if amount < 1:
            amount = 1
    except:
        amount = 1
    
    customer = Customer.query.get(customer_id)
    delivery_person = DeliveryPerson.query.get(delivery_person_id)
    menu_item = MenuItem.query.get(menu_item_id)
    
    if not customer or not delivery_person or not menu_item:
        flash("Please select valid customer and menu item.", "error")
        return redirect(url_for("orders.new_order"))
    
    try:
        # Calculate total price (simplified - just item price * amount for now)
        total_price = float(menu_item.price) * amount   # use .price property
        
        # Apply discount if provided
        if discount_id:
            discount = DiscountCode.query.get(discount_id)
            if discount:
                total_price = total_price * (1 - discount.percentage / 100)
        
        order = Order(
            customer_id=customer.customer_id,
            delivery_person_id=delivery_person.delivery_person_id,
            discount_id=discount_id,
            total_price=total_price,
            delivery_address=delivery_address
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
        flash(f"Error creating order: {str(e)}", "error")
        return redirect(url_for("orders.new_order"))

# ----------------------
# Delivery person helper
# ----------------------
def assign_delivery_person(order_postal_code):
    for dps in DeliveryPerson.query.all():
        if dps.postal_code == order_postal_code:
            return dps.delivery_person_id
    return None
