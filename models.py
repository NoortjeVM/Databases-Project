from datetime import datetime
import math
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Numeric
from datetime import date, timezone
from zoneinfo import ZoneInfo

db = SQLAlchemy()

class MenuItem(db.Model):
    __tablename__ = "menu_item"
    item_id = db.Column(db.Integer, primary_key=True)
    item_type = db.Column(db.String(20), nullable=False)  # "pizza", "drink", "dessert"
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
    expected_delivery_time = db.Column(db.DateTime, nullable=False)
    total_price = db.Column(db.Numeric(8,2), nullable=False)
    
    # Relationships
    customer = db.relationship("Customer", back_populates="orders")
    discount_code = db.relationship("DiscountCode", back_populates="orders")
    delivery_person = db.relationship("DeliveryPerson", back_populates="orders")
    order_items = db.relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    
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
        expected_delivery = self.expected_delivery_time
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
    # Customers
    if Customer.query.count() == 0:
        db.session.add_all([
            Customer(first_name="Mario", last_name="Rossi", birthdate=datetime(1985, 5, 15).date(),
                    address="Via Roma 123", phone_number="+1234567890", gender=1),
            Customer(first_name="Luigi", last_name="Bianchi", birthdate=datetime(1990, 8, 22).date(),
                    address="Via Milano 456", phone_number="+1234567891", gender=1),
            Customer(first_name="Maria", last_name="Verdi", birthdate=datetime(1988, 3, 10).date(),
                    address="Via Napoli 789", phone_number="+1234567892", gender=0),
            Customer(first_name="Giulia", last_name="Conti", birthdate=datetime(1995, 11, 2).date(),
                    address="Via Firenze 12", phone_number="+1234567893", gender=0),
            Customer(first_name="Francesco", last_name="Moretti", birthdate=datetime(1982, 1, 28).date(),
                    address="Via Torino 45", phone_number="+1234567894", gender=1),
            Customer(first_name="Chiara", last_name="Gallo", birthdate=datetime(1999, 7, 16).date(),
                    address="Corso Venezia 77", phone_number="+1234567895", gender=0),
            Customer(first_name="Lorenzo", last_name="Ricci", birthdate=datetime(1978, 9, 9).date(),
                    address="Piazza Duomo 3", phone_number="+1234567896", gender=1),
            Customer(first_name="Sara", last_name="Marini", birthdate=datetime(1993, 4, 4).date(),
                    address="Via Trieste 21", phone_number="+1234567897", gender=0),
            Customer(first_name="Elena", last_name="Romano", birthdate=datetime(2001, 6, 30).date(),
                    address="Via Genova 88", phone_number="+1234567898", gender=0),
            Customer(first_name="Davide", last_name="Giordano", birthdate=datetime(1987, 12, 19).date(),
                    address="Viale Garibaldi 9", phone_number="+1234567899", gender=1),
            Customer(first_name="Alessia", last_name="Barbieri", birthdate=datetime(1996, 2, 14).date(),
                    address="Via Bologna 56", phone_number="+1234567800", gender=0),
        ])

    # Delivery people
    if DeliveryPerson.query.count() == 0:
        db.session.add_all([
            DeliveryPerson(delivery_person_first_name="Giovanni", delivery_person_last_name="Delivery", postal_code="1234AB"),
            DeliveryPerson(delivery_person_first_name="Francesco", delivery_person_last_name="Speed", postal_code="5678CD"),
            DeliveryPerson(delivery_person_first_name="Luca", delivery_person_last_name="Fast", postal_code="9012EF"),
        ])

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
            Ingredient(ingredient_name="Vegan Mozzarella", price=2.00, vegetarian=True, vegan=True),
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
        vegan_mozzarella = Ingredient.query.filter_by(ingredient_name="Vegan Mozzarella").first()

        pizzas = [
            Pizza(name="Margherita", ingredients=[tomato, mozzarella, basil]),
            Pizza(name="Pepperoni", ingredients=[tomato, mozzarella, pepperoni]),
            Pizza(name="Veggie Deluxe", ingredients=[tomato, mozzarella, mushrooms, peppers, onions, olives]),
            Pizza(name="Hawaiian", ingredients=[tomato, mozzarella, ham, pineapple]),
            Pizza(name="Four Cheese", ingredients=[tomato, mozzarella, parmesan, gorgonzola]),
            Pizza(name="Meat Feast", ingredients=[tomato, mozzarella, ham, pepperoni]),
            Pizza(name="Capricciosa", ingredients=[tomato, mozzarella, ham, mushrooms, olives]),
            Pizza(name="Funghi", ingredients=[tomato, mozzarella, mushrooms]),
            Pizza(name="Vegan Garden", ingredients=[tomato, vegan_mozzarella, peppers, onions, mushrooms, olives]),
            Pizza(name="Vegan Tropical", ingredients=[tomato, vegan_mozzarella, pineapple, peppers, onions]),
            Pizza(name="Vegan Classic", ingredients=[tomato, vegan_mozzarella, basil, mushrooms, olives]),
        ]
        db.session.add_all(pizzas)
        db.session.flush()

    # Drinks
    if Drink.query.count() == 0:
        drinks = [
            Drink(name="Coca Cola", price=2.50),
            Drink(name="Water", price=1.00),
            Drink(name="Fanta", price=2.20),
            Drink(name="Sprite", price=2.20),
            Drink(name="Coca Cola Zero", price=2.50),
            Drink(name="Iced Tea", price=2.30),
            Drink(name="Sparkling Water", price=1.50),
            Drink(name="Lemonade", price=2.00),
            Drink(name="Apple Juice", price=2.40),
            Drink(name="Beer", price=3.00),
        ]
        db.session.add_all(drinks)
        db.session.flush()

    # Desserts
    if Dessert.query.count() == 0:
        desserts = [
            Dessert(name="Tiramisu", price=4.00),
            Dessert(name="Panna Cotta", price=3.50),
            Dessert(name="Tiramisu", price=4.00),
            Dessert(name="Panna Cotta", price=3.50),
            Dessert(name="Gelato", price=3.00),
            Dessert(name="Chocolate Lava Cake", price=4.50),
            Dessert(name="Fruity Sorbet", price=3.80),
            Dessert(name="Affogato", price=3.50),
            Dessert(name="Cheesecake", price=4.20),
        ]
        db.session.add_all(desserts)
        db.session.flush()

    # MenuItems wrapper
    if MenuItem.query.count() == 0:
        menu_items = []
        for pizza in Pizza.query.all():
            menu_items.append(MenuItem(item_type="pizza", item_ref_id=pizza.pizza_id))
        for drink in Drink.query.all():
            menu_items.append(MenuItem(item_type="drink", item_ref_id=drink.drink_id))
        for dessert in Dessert.query.all():
            menu_items.append(MenuItem(item_type="dessert", item_ref_id=dessert.dessert_id))
        db.session.add_all(menu_items)

    # Discount codes
    if DiscountCode.query.count() == 0:
        db.session.add_all([
            DiscountCode(percentage=10, discount_code="WELCOME10"),
            DiscountCode(percentage=15, discount_code="STUDENT15"),
            DiscountCode(percentage=20, discount_code="VIP20"),
        ])

    db.session.commit()