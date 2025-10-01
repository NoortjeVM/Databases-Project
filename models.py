from datetime import datetime
import math
from flask_sqlalchemy import SQLAlchemy
from datetime import date

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
        elif all (ing.vegeterian for ing in self.ingredients):
            return "vegetarian"
        return "non-vegeterian"
    
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
    ten_pizza_discount_used = db.Column(db.Integer, default=0)
    
    # Relationships
    orders = db.relationship("Order", back_populates="customer", cascade="all, delete-orphan")
    discounts = db.relationship("DiscountCode", secondary="customer_discount", back_populates="customers")
    
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
    
    @property
    def available_ten_pizza_discount(self):
        return math.floor(self.total_pizzas_ordered / 10) - self.ten_pizza_discount_used

    
    def __repr__(self):
        return f"<Customer {self.customer_id} {self.full_name}>"

class DiscountCode(db.Model):
    __tablename__ = "discount_code"
    discount_id = db.Column(db.Integer, primary_key=True)
    percentage = db.Column(db.Integer, nullable=False)
    discount_code = db.Column(db.String(32), nullable=False, unique=True)
    
    # Relationships
    customers = db.relationship("Customer", secondary="customer_discount", back_populates="discounts")
    orders = db.relationship("Order", back_populates="discount_code")
    
    def __repr__(self):
        return f"<DiscountCode {self.discount_id} {self.discount_code} {self.percentage}%>"

# Association table for Customer-Discount many-to-many relationship
customer_discount = db.Table('customer_discount',
    db.Column('customer_id', db.Integer, db.ForeignKey('customer.customer_id'), primary_key=True),
    db.Column('discount_id', db.Integer, db.ForeignKey('discount_code.discount_id'), primary_key=True),
    db.Column('used', db.Boolean, nullable=False, default=False)
)

class DeliveryPerson(db.Model):
    __tablename__ = "delivery_person"
    delivery_person_id = db.Column(db.Integer, primary_key=True)
    delivery_person_first_name = db.Column(db.String(32), nullable=False)
    delivery_person_last_name = db.Column(db.String(32), nullable=False)
    postal_code = db.Column(db.String(6), nullable=False)
    
    # Relationships
    orders = db.relationship("Order", back_populates="delivery_person")
    
    @property
    def full_name(self):
        return f"{self.delivery_person_first_name} {self.delivery_person_last_name}"
    
    def __repr__(self):
        return f"<DeliveryPerson {self.delivery_person_id} {self.full_name}>"

class Order(db.Model):
    __tablename__ = "order"
    order_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.customer_id"), nullable=False)
    discount_id = db.Column(db.Integer, db.ForeignKey("discount_code.discount_id"), nullable=True)
    delivery_person_id = db.Column(db.Integer, db.ForeignKey("delivery_person.delivery_person_id"), nullable=False)
    order_time = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    delivery_address = db.Column(db.String(255), nullable=False)
    postal_code = db.Column(db.String(6), nullable=False)
    
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
                item_total = item.amount * item.menu_item.get_price()
                subtotal += item_total
        return subtotal
    
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
    if Customer.query.count() == 0:
        db.session.add_all([
            Customer(first_name="Mario", last_name="Rossi", birthdate=datetime(1985, 5, 15).date(), 
                     address="Via Roma 123", phone_number="+1234567890", gender=1),
            Customer(first_name="Luigi", last_name="Bianchi", birthdate=datetime(1990, 8, 22).date(),
                     address="Via Milano 456", phone_number="+1234567891", gender=1),
            Customer(first_name="Maria", last_name="Verdi", birthdate=datetime(1988, 3, 10).date(),
                     address="Via Napoli 789", phone_number="+1234567892", gender=0),
            Customer(first_name="Giulia", last_name="Neri", birthdate=datetime(1995, 1, 20).date(),
                     address="Via Torino 111", phone_number="+1234567893", gender=0),
            Customer(first_name="Paolo", last_name="Ricci", birthdate=datetime(1982, 11, 2).date(),
                     address="Via Firenze 222", phone_number="+1234567894", gender=1),
            Customer(first_name="Francesca", last_name="Marino", birthdate=datetime(1991, 7, 7).date(),
                     address="Via Venezia 333", phone_number="+1234567895", gender=0),
            Customer(first_name="Antonio", last_name="Greco", birthdate=datetime(1987, 4, 18).date(),
                     address="Via Genova 444", phone_number="+1234567896", gender=1),
            Customer(first_name="Chiara", last_name="Fontana", birthdate=datetime(1993, 12, 5).date(),
                     address="Via Bologna 555", phone_number="+1234567897", gender=0),
            Customer(first_name="Stefano", last_name="Galli", birthdate=datetime(1980, 9, 30).date(),
                     address="Via Verona 666", phone_number="+1234567898", gender=1),
            Customer(first_name="Alessia", last_name="Costa", birthdate=datetime(1999, 2, 14).date(),
                     address="Via Bari 777", phone_number="+1234567899", gender=0),
        ])

    if DeliveryPerson.query.count() == 0:
        db.session.add_all([
            DeliveryPerson(delivery_person_first_name="Giovanni", delivery_person_last_name="Delivery", postal_code="1234AB"),
            DeliveryPerson(delivery_person_first_name="Francesco", delivery_person_last_name="Speed", postal_code="5678CD"),
            DeliveryPerson(delivery_person_first_name="Luca", delivery_person_last_name="Fast", postal_code="9012EF"),
        ])

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
        ])

    if MenuItem.query.count() == 0:
        # Create pizzas
        pizzas = [
            Pizza(name="Margherita"),
            Pizza(name="Pepperoni"),
            Pizza(name="Veggie Deluxe"),
            Pizza(name="Hawaiian"),
            Pizza(name="Four Cheese"),
            Pizza(name="Meat Feast"),
            Pizza(name="BBQ Chicken"),
            Pizza(name="Capricciosa"),
            Pizza(name="Diavola"),
            Pizza(name="Funghi"),
        ]
        db.session.add_all(pizzas)
        db.session.flush()  # get pizza_ids

        # Create drinks
        drinks = [
            Drink(name="Coca Cola", price=2.50),
            Drink(name="Water", price=1.00),
            Drink(name="Fanta", price=2.20),
        ]
        db.session.add_all(drinks)
        db.session.flush()

        # Create desserts
        desserts = [
            Dessert(name="Tiramisu", price=4.00),
            Dessert(name="Panna Cotta", price=3.50),
        ]
        db.session.add_all(desserts)
        db.session.flush()

        # Create corresponding menu items
        menu_items = []
        for pizza in pizzas:
            menu_items.append(MenuItem(item_type="pizza", item_ref_id=pizza.pizza_id))
        for drink in drinks:
            menu_items.append(MenuItem(item_type="drink", item_ref_id=drink.drink_id))
        for dessert in desserts:
            menu_items.append(MenuItem(item_type="dessert", item_ref_id=dessert.dessert_id))

        db.session.add_all(menu_items)

    if DiscountCode.query.count() == 0:
        db.session.add_all([
            DiscountCode(percentage=10, discount_code="WELCOME10"),
            DiscountCode(percentage=15, discount_code="STUDENT15"),
            DiscountCode(percentage=20, discount_code="VIP20"),
        ])

    db.session.commit()
