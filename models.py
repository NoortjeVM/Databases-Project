from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Numeric
from datetime import date, timedelta
from zoneinfo import ZoneInfo
from faker import Faker
import random

db = SQLAlchemy()

class MenuItem(db.Model):
    __tablename__ = "menu_item"
    item_id = db.Column(db.Integer, primary_key=True)
    item_type = db.Column(db.String(20), nullable=False)  # "pizza", "drink" of "dessert"
    item_ref_id = db.Column(db.Integer, nullable=False)   # points to pizza_id / drink_id / dessert_id

    order_items = db.relationship("OrderItem", back_populates="menu_item")

    @property
    def name(self):
        if self.item_type == "pizza":
            return Pizza.query.get(self.item_ref_id).name
        elif self.item_type == "drink":
            return Drink.query.get(self.item_ref_id).name
        elif self.item_type == "dessert":
            return Dessert.query.get(self.item_ref_id).name
        else:
            return "[unknown]"

    @property
    def price(self):
        if self.item_type == "pizza":
            return float(Pizza.query.get(self.item_ref_id).price)
        elif self.item_type == "drink":
            return float(Drink.query.get(self.item_ref_id).price)
        elif self.item_type == "dessert":
            return float(Dessert.query.get(self.item_ref_id).price)
        else: 
            return 0

class Pizza(db.Model):
    __tablename__ = "pizza"
    pizza_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    ingredients = db.relationship(
        "Ingredient",
        secondary="pizza_ingredient",
        back_populates="pizzas"
    )

    @property
    def price(self):
        return float(sum(ing.price for ing in self.ingredients))

    @property
    def label(self):
        if all (ing.vegan for ing in self.ingredients):
            return "vegan"
        elif all (ing.vegetarian for ing in self.ingredients):
            return "vegetarian"
        return "non-vegetarian"
    
    def __repr__(self):
        return f"<Pizza {self.name} {self.price}>"


class Drink(db.Model):
    __tablename__ = "drink"
    drink_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Numeric(8, 2), nullable=False)
    
    def __repr__(self):
        return f"<Drink {self.name} price {self.price}>"

class Dessert(db.Model):
    __tablename__ = "dessert"
    dessert_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Numeric(8, 2), nullable=False)

    def __repr__(self):
        return f"<Dessert {self.name} price {self.price}>"

class Ingredient(db.Model):
    __tablename__ = "ingredient"
    ingredient_id = db.Column(db.Integer, primary_key=True)
    ingredient_name = db.Column(db.String(32), nullable=False, unique=True)
    price = db.Column(db.Numeric(8, 2), nullable=False)
    vegetarian = db.Column(db.Boolean, nullable=False, default=False)
    vegan = db.Column(db.Boolean, nullable=False, default=False)
    
    # Relationships
    pizzas = db.relationship("Pizza", secondary="pizza_ingredient", back_populates="ingredients")

    def __repr__(self):
        return f"<Ingredient {self.ingredient_id} {self.ingredient_name} ${self.price}>"

# Association table for Pizza-Ingredient many-to-many relationship
pizza_ingredient = db.Table('pizza_ingredient',
    db.Column('pizza_id', db.Integer, db.ForeignKey('pizza.pizza_id'), primary_key=True),
    db.Column('ingredient_id', db.Integer, db.ForeignKey('ingredient.ingredient_id'), primary_key=True)
)

class Customer(db.Model):
    __tablename__ = "customer"
    customer_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(32), nullable=False)
    last_name = db.Column(db.String(32), nullable=False)
    birthdate = db.Column(db.Date, nullable=False)
    address = db.Column(db.String(255))
    phone_number = db.Column(db.String(32), nullable=False, unique=True)
    gender = db.Column(db.Integer)  # 0, 1, 2 for different gender options
    
    # Relationships
    orders = db.relationship("Order", back_populates="customer", cascade="all, delete-orphan")

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def birthday(self):
        if self.birthdate.month == date.today().month and self.birthdate.day == date.today().day:
            return True
        return False
    
    @property
    def total_pizzas_ordered(self):
        pizza_count = 0
        for order in self.orders:
            for item in order.order_items:
                # Ensure the item is a pizza
                if isinstance(item.menu_item, Pizza):
                    pizza_count += item.amount
        return pizza_count
    
    def __repr__(self):
        return f"<Customer {self.customer_id} {self.full_name}>"

class DiscountCode(db.Model):
    __tablename__ = "discount_code"
    discount_id = db.Column(db.Integer, primary_key=True)
    percentage = db.Column(db.Integer, nullable=False)
    discount_code = db.Column(db.String(32), nullable=False, unique=True)
    
    # Relationships
    orders = db.relationship("Order", back_populates="discount_code")
    
    def __repr__(self):
        return f"<DiscountCode {self.discount_id} {self.discount_code} {self.percentage}%>"


class DeliveryPerson(db.Model):
    __tablename__ = "delivery_person"
    delivery_person_id = db.Column(db.Integer, primary_key=True)
    delivery_person_first_name = db.Column(db.String(32), nullable=False)
    delivery_person_last_name = db.Column(db.String(32), nullable=False)
    postal_code = db.Column(db.String(6), nullable=False)
    next_available_time = db.Column(db.DateTime, default=lambda: datetime.now(ZoneInfo("Europe/Amsterdam")), nullable=False)
    
    # Relationships
    orders = db.relationship("Order", back_populates="delivery_person")
    
    @property
    def full_name(self):
        return f"{self.delivery_person_first_name} {self.delivery_person_last_name}"
    
    @property
    def is_available_now(self):
        # Get current time in Dutch timezone
        now_dutch = datetime.now(ZoneInfo("Europe/Amsterdam"))

        # Make next_available_time timezone-aware if it isn't already
        if self.next_available_time.tzinfo is None:
            next_available = self.next_available_time.replace(tzinfo=ZoneInfo("Europe/Amsterdam"))
        else:
            next_available = self.next_available_time

        # Check if delivery person is currently available
        return now_dutch >= next_available
    
    @property
    def minutes_until_available(self):
        # Calculate minutes until delivery person is available
        if self.is_available_now:
            return 0
        delta = self.next_available_time - datetime.now(ZoneInfo("Europe/Amsterdam"))
        return int(delta.total_seconds() / 60)
    
    @property
    def next_available_time_aware(self):
        """Returns next_available_time as timezone-aware datetime"""
        if self.next_available_time.tzinfo is None:
            return self.next_available_time.replace(tzinfo=ZoneInfo("Europe/Amsterdam"))
        return self.next_available_time
    
    def __repr__(self):
        return f"<DeliveryPerson {self.delivery_person_id} {self.full_name}>"

class Order(db.Model):
    __tablename__ = "order"
    order_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.customer_id"), nullable=False)
    discount_id = db.Column(db.Integer, db.ForeignKey("discount_code.discount_id"), nullable=True)
    delivery_person_id = db.Column(db.Integer, db.ForeignKey("delivery_person.delivery_person_id"), nullable=False)
    order_time = db.Column(db.DateTime, default=lambda: datetime.now(ZoneInfo("Europe/Amsterdam")), nullable=False)
    delivery_address = db.Column(db.String(255), nullable=False)
    postal_code = db.Column(db.String(6), nullable=False)
    pickup_time = db.Column(db.DateTime, nullable=False) 
    total_price = db.Column(db.Numeric(8,2), nullable=False)
    
    # Relationships
    customer = db.relationship("Customer", back_populates="orders")
    discount_code = db.relationship("DiscountCode", back_populates="orders")
    delivery_person = db.relationship("DeliveryPerson", back_populates="orders")
    order_items = db.relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

    @property
    def expected_delivery_time(self):
        return self.pickup_time + timedelta(minutes=30)
    
    @property
    def item_count(self):
        return sum(item.amount for item in self.order_items)
    
    @property
    def raw_price(self):
        subtotal = 0.0
        for item in self.order_items:
                item_total = item.amount * item.menu_item.price
                subtotal += item_total
        return subtotal
    
    @property
    def status(self):
        """
        Calculate status based on current time and delivery timestamps.
        - pending: order placed, waiting for delivery person to pick up
        - out_for_delivery: delivery person has picked up, on the way
        - delivered: past expected delivery time
        """
        now = datetime.now(ZoneInfo("Europe/Amsterdam"))
        
        # Make datetime values timezone-aware if they aren't already
        expected_delivery = self.pickup_time + timedelta(minutes=30)
        if expected_delivery.tzinfo is None:
            expected_delivery = expected_delivery.replace(tzinfo=ZoneInfo("Europe/Amsterdam"))
        
        pickup = self.pickup_time
        if pickup.tzinfo is None:
            pickup = pickup.replace(tzinfo=ZoneInfo("Europe/Amsterdam"))
        
        if now >= expected_delivery:
            return 'delivered'
        elif now >= pickup:
            return 'out_for_delivery'
        else:
            return 'pending'
    
    @property
    def status_display(self):
        """Human-readable status with icon"""
        status = self.status
        if status == 'delivered':
            return '✓ Delivered'
        elif status == 'out_for_delivery':
            return '🚚 Out for Delivery'
        else:
            return '⏳ Pending'
        
    def __repr__(self):
        return f"<Order {self.order_id} customer={self.customer_id} total=${self.total_price}>"

class OrderItem(db.Model):
    __tablename__ = "order_item"
    order_id = db.Column(db.Integer, db.ForeignKey("order.order_id"), primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey("menu_item.item_id"), primary_key=True)
    amount = db.Column(db.Integer, default=1, nullable=False)
    
    # Relationships
    order = db.relationship("Order", back_populates="order_items")
    menu_item = db.relationship("MenuItem", back_populates="order_items")
    
    def __repr__(self):
        return f"<OrderItem order={self.order_id} item={self.item_id} amount={self.amount}>"


def seed_data():
    db.drop_all()
    db.create_all()
    fake = Faker("nl_NL")

    # --- Customers ---
    if Customer.query.count() == 0:
        for _ in range(10):
            c = Customer(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                birthdate=fake.date_of_birth(minimum_age=18, maximum_age=60),
                address=fake.address(),
                phone_number=fake.unique.phone_number(),
                gender=random.choice([0, 1, 2])
            )
            db.session.add(c)
        db.session.flush()

    # --- Delivery Persons ---
    if DeliveryPerson.query.count() == 0:
        postal_codes = ['6221AX', '6211RZ', '6215PD']
        for i in range(3):
            d = DeliveryPerson(
                delivery_person_first_name=fake.first_name(),
                delivery_person_last_name=fake.last_name(),
                postal_code=postal_codes[i],
                next_available_time=datetime.now(ZoneInfo("Europe/Amsterdam"))
            )
            db.session.add(d)
        db.session.flush()

    # Ingredients
    if Ingredient.query.count() == 0:
        db.session.add_all([
            Ingredient(ingredient_name="Tomato Sauce", price=1.50, vegetarian=True, vegan=True),
            Ingredient(ingredient_name="Mozzarella", price=2.00, vegetarian=True, vegan=False),
            Ingredient(ingredient_name="Pepperoni", price=2.50, vegetarian=False, vegan=False),
            Ingredient(ingredient_name="Mushrooms", price=1.75, vegetarian=True, vegan=True),
            Ingredient(ingredient_name="Bell Peppers", price=1.25, vegetarian=True, vegan=True),
            Ingredient(ingredient_name="Onions", price=1.00, vegetarian=True, vegan=True),
            Ingredient(ingredient_name="Olives", price=1.50, vegetarian=True, vegan=True),
            Ingredient(ingredient_name="Ham", price=2.75, vegetarian=False, vegan=False),
            Ingredient(ingredient_name="Pineapple", price=1.80, vegetarian=True, vegan=True),
            Ingredient(ingredient_name="Basil", price=0.75, vegetarian=True, vegan=True),
            Ingredient(ingredient_name="Parmesan", price=2.20, vegetarian=True, vegan=False),
            Ingredient(ingredient_name="Gorgonzola", price=2.30, vegetarian=True, vegan=False),
        ])
    db.session.flush()  # so ingredient IDs exist

    # Pizzas with ingredients
    if Pizza.query.count() == 0:
        tomato = Ingredient.query.filter_by(ingredient_name="Tomato Sauce").first()
        mozzarella = Ingredient.query.filter_by(ingredient_name="Mozzarella").first()
        pepperoni = Ingredient.query.filter_by(ingredient_name="Pepperoni").first()
        mushrooms = Ingredient.query.filter_by(ingredient_name="Mushrooms").first()
        peppers = Ingredient.query.filter_by(ingredient_name="Bell Peppers").first()
        onions = Ingredient.query.filter_by(ingredient_name="Onions").first()
        olives = Ingredient.query.filter_by(ingredient_name="Olives").first()
        ham = Ingredient.query.filter_by(ingredient_name="Ham").first()
        pineapple = Ingredient.query.filter_by(ingredient_name="Pineapple").first()
        basil = Ingredient.query.filter_by(ingredient_name="Basil").first()
        parmesan = Ingredient.query.filter_by(ingredient_name="Parmesan").first()
        gorgonzola = Ingredient.query.filter_by(ingredient_name="Gorgonzola").first()

        pizzas = [
            Pizza(name="Margherita", ingredients=[tomato, mozzarella, basil]),
            Pizza(name="Pepperoni", ingredients=[tomato, mozzarella, pepperoni]),
            Pizza(name="Veggie Deluxe", ingredients=[tomato, mozzarella, mushrooms, peppers, onions, olives]),
            Pizza(name="Hawaiian", ingredients=[tomato, mozzarella, ham, pineapple]),
            Pizza(name="Four Cheese", ingredients=[tomato, mozzarella, parmesan, gorgonzola]),
            Pizza(name="Meat Feast", ingredients=[tomato, mozzarella, ham, pepperoni]),
            Pizza(name="Capricciosa", ingredients=[tomato, mozzarella, ham, mushrooms, olives]),
            Pizza(name="Funghi", ingredients=[tomato, mozzarella, mushrooms]),
        ]
        db.session.add_all(pizzas)
        db.session.flush()

    # --- Drinks ---
    if Drink.query.count() == 0:
        drinks = [
            Drink(name="Coca Cola", price=2.00),
            Drink(name="Sprite", price=2.00),
            Drink(name="Ice Tea", price=2.50),
            Drink(name="Beer", price=3.50),
        ]
        db.session.add_all(drinks)
        db.session.flush()

    # Desserts
    if Dessert.query.count() == 0:
        desserts = [
            Dessert(name="Tiramisu", price=4.00),
            Dessert(name="Panna Cotta", price=3.50),
        ]
        db.session.add_all(desserts)
        db.session.flush()

    # Voeg alleen menu items toe als ze nog niet bestaan
    for p in Pizza.query.all():
        if not MenuItem.query.filter_by(item_type="pizza", item_ref_id=p.pizza_id).first():
            db.session.add(MenuItem(item_type="pizza", item_ref_id=p.pizza_id))

    for d in Drink.query.all():
        if not MenuItem.query.filter_by(item_type="drink", item_ref_id=d.drink_id).first():
            db.session.add(MenuItem(item_type="drink", item_ref_id=d.drink_id))

    for ds in Dessert.query.all():
        if not MenuItem.query.filter_by(item_type="dessert", item_ref_id=ds.dessert_id).first():
            db.session.add(MenuItem(item_type="dessert", item_ref_id=ds.dessert_id))


    # --- Discount Codes ---
    if DiscountCode.query.count() == 0:
        db.session.add_all([
            DiscountCode(percentage=10, discount_code="WELCOME10"),
            DiscountCode(percentage=15, discount_code="STUDENT15"),
            DiscountCode(percentage=20, discount_code="VIP20"),
        ])
        db.session.flush()


    # Orders
    if Order.query.count() == 0:
        customers = Customer.query.all()
        delivery_people = DeliveryPerson.query.all()
        menu_pizzas = MenuItem.query.filter_by(item_type="pizza").all()
        menu_drinks = MenuItem.query.filter_by(item_type="drink").all()
        menu_desserts = MenuItem.query.filter_by(item_type="dessert").all()

        base_date = datetime.now(ZoneInfo("Europe/Amsterdam"))

        for _ in range(20):
            customer = random.choice(customers)
            delivery_person = random.choice(delivery_people)

            #let the generated orders be in placed in the past month
            order_time = base_date - timedelta(days=random.randint(0, 30), hours=random.randint(0, 10), minutes=random.randint(0, 59))
            pickup_time = order_time + timedelta(minutes=random.randint(0, 60))

            order = Order(
                customer_id=customer.customer_id,
                delivery_person_id=delivery_person.delivery_person_id,
                order_time=order_time,
                pickup_time=pickup_time,
                delivery_address=fake.street_address(),
                postal_code=fake.postcode().replace(" ", "")[:6], #since in the database we fixed the length to 6 characters
                total_price=0,
            )
            db.session.add(order)
            db.session.flush()

            subtotal = 0
            added_item_ids = set()

            for _ in range(random.randint(1, 4)):
                pizza_item = random.choice(menu_pizzas)
                if pizza_item.item_id in added_item_ids:
                    continue  # skip if we already have this pizza in the orderitems
                qty = random.randint(1, 3)
                db.session.add(OrderItem(order_id=order.order_id, item_id=pizza_item.item_id, amount=qty))
                subtotal += pizza_item.price * qty
                added_item_ids.add(pizza_item.item_id)

            if random.random() < 0.6:
                drink_item = random.choice(menu_drinks)
                if drink_item.item_id in added_item_ids:
                    continue  # skip if its already added
                qty = random.randint(1, 2)
                db.session.add(OrderItem(order_id=order.order_id, item_id=drink_item.item_id, amount=qty))
                subtotal += drink_item.price * qty
                added_item_ids.add(drink_item.item_id)

            if random.random() < 0.3:
                dessert_item = random.choice(menu_desserts)
                if dessert_item.item_id in added_item_ids:
                    continue
                qty = 1
                db.session.add(OrderItem(order_id=order.order_id, item_id=dessert_item.item_id, amount=qty))
                subtotal += dessert_item.price * qty
                added_item_ids.add(dessert_item.item_id)

            order.total_price = round(subtotal, 2)

        db.session.commit()
