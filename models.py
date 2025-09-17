from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class MenuItem(db.Model):
    __tablename__ = "menu_items"
    item_id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(32), nullable=False)
    item_price = db.Column(db.Numeric(8, 2), nullable=False)
    
    # Relationships
    pizzas = db.relationship("Pizza", back_populates="menu_item", cascade="all, delete-orphan")
    drinks = db.relationship("Drink", back_populates="menu_item", cascade="all, delete-orphan")
    desserts = db.relationship("Dessert", back_populates="menu_item", cascade="all, delete-orphan")
    order_items = db.relationship("OrderItem", back_populates="menu_item")
    
    def __repr__(self):
        return f"<MenuItem {self.item_id} {self.item_name} ${self.item_price}>"

class Pizza(db.Model):
    __tablename__ = "pizzas"
    pizza_id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey("menu_items.item_id"), nullable=False)
    
    # Relationships
    menu_item = db.relationship("MenuItem", back_populates="pizzas")
    ingredients = db.relationship("Ingredient", secondary="pizza_ingredients", back_populates="pizzas")
    
    def __repr__(self):
        return f"<Pizza {self.pizza_id} item_id={self.item_id}>"

class Drink(db.Model):
    __tablename__ = "drinks"
    drink_id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey("menu_items.item_id"), nullable=False)
    
    # Relationships
    menu_item = db.relationship("MenuItem", back_populates="drinks")
    
    def __repr__(self):
        return f"<Drink {self.drink_id} item_id={self.item_id}>"

class Dessert(db.Model):
    __tablename__ = "desserts"
    dessert_id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey("menu_items.item_id"), nullable=False)
    
    # Relationships
    menu_item = db.relationship("MenuItem", back_populates="desserts")
    
    def __repr__(self):
        return f"<Dessert {self.dessert_id} item_id={self.item_id}>"

class Ingredient(db.Model):
    __tablename__ = "ingredients"
    ingredient_id = db.Column(db.Integer, primary_key=True)
    ingredient_name = db.Column(db.String(32), nullable=False, unique=True)
    price = db.Column(db.Numeric(8, 2), nullable=False)
    vegetarian = db.Column(db.Boolean, nullable=False, default=False)
    vegan = db.Column(db.Boolean, nullable=False, default=False)
    
    # Relationships
    pizzas = db.relationship("Pizza", secondary="pizza_ingredients", back_populates="ingredients")
    
    def __repr__(self):
        return f"<Ingredient {self.ingredient_id} {self.ingredient_name} ${self.price}>"

# Association table for Pizza-Ingredient many-to-many relationship
pizza_ingredients = db.Table('pizza_ingredients',
    db.Column('pizza_id', db.Integer, db.ForeignKey('pizzas.pizza_id'), primary_key=True),
    db.Column('ingredient_id', db.Integer, db.ForeignKey('ingredients.ingredient_id'), primary_key=True)
)

class Customer(db.Model):
    __tablename__ = "customers"
    customer_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(32), nullable=False)
    last_name = db.Column(db.String(32), nullable=False)
    birthdate = db.Column(db.Date, nullable=False)
    address = db.Column(db.String(255))
    phone_number = db.Column(db.String(32), nullable=False, unique=True)
    gender = db.Column(db.Integer)  # 0, 1, 2 for different gender options
    
    # Relationships
    orders = db.relationship("Order", back_populates="customer", cascade="all, delete-orphan")
    discounts = db.relationship("DiscountCode", secondary="customer_discount", back_populates="customers")
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def __repr__(self):
        return f"<Customer {self.customer_id} {self.full_name}>"

class DiscountCode(db.Model):
    __tablename__ = "discount_codes"
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
    db.Column('customer_id', db.Integer, db.ForeignKey('customers.customer_id'), primary_key=True),
    db.Column('discount_id', db.Integer, db.ForeignKey('discount_codes.discount_id'), primary_key=True),
    db.Column('used', db.Boolean, nullable=False, default=False)
)

class DeliveryPerson(db.Model):
    __tablename__ = "delivery_persons"
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
    __tablename__ = "orders"
    order_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.customer_id"), nullable=False)
    discount_id = db.Column(db.Integer, db.ForeignKey("discount_codes.discount_id"), nullable=True)
    delivery_person_id = db.Column(db.Integer, db.ForeignKey("delivery_persons.delivery_person_id"), nullable=False)
    total_price = db.Column(db.Numeric(8, 2), nullable=False)
    order_time = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    delivery_address = db.Column(db.String(255))
    
    # Relationships
    customer = db.relationship("Customer", back_populates="orders")
    discount_code = db.relationship("DiscountCode", back_populates="orders")
    delivery_person = db.relationship("DeliveryPerson", back_populates="orders")
    order_items = db.relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    
    @property
    def item_count(self):
        return sum(item.amount for item in self.order_items)
    
    def __repr__(self):
        return f"<Order {self.order_id} customer={self.customer_id} total=${self.total_price}>"

class OrderItem(db.Model):
    __tablename__ = "order_items"
    order_id = db.Column(db.Integer, db.ForeignKey("orders.order_id"), primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey("menu_items.item_id"), primary_key=True)
    amount = db.Column(db.Integer, default=1, nullable=False)
    
    # Relationships
    order = db.relationship("Order", back_populates="order_items")
    menu_item = db.relationship("MenuItem", back_populates="order_items")
    
    def __repr__(self):
        return f"<OrderItem order={self.order_id} item={self.item_id} amount={self.amount}>"

def seed_data():
    """Seed the database with initial data"""
    if Customer.query.count() == 0:
        db.session.add_all([
            Customer(first_name="Mario", last_name="Rossi", birthdate=datetime(1985, 5, 15).date(), 
                    address="Via Roma 123", phone_number="+1234567890", gender=1),
            Customer(first_name="Luigi", last_name="Bianchi", birthdate=datetime(1990, 8, 22).date(),
                    address="Via Milano 456", phone_number="+1234567891", gender=1),
            Customer(first_name="Maria", last_name="Verdi", birthdate=datetime(1988, 3, 10).date(),
                    address="Via Napoli 789", phone_number="+1234567892", gender=0),
        ])
    
    if DeliveryPerson.query.count() == 0:
        db.session.add_all([
            DeliveryPerson(delivery_person_first_name="Giovanni", delivery_person_last_name="Delivery", postal_code="12345A"),
            DeliveryPerson(delivery_person_first_name="Francesco", delivery_person_last_name="Speed", postal_code="67890B"),
        ])
    
    if Ingredient.query.count() == 0:
        db.session.add_all([
            Ingredient(ingredient_name="Tomato Sauce", price=1.50, vegetarian=True, vegan=True),
            Ingredient(ingredient_name="Mozzarella", price=2.00, vegetarian=True, vegan=False),
            Ingredient(ingredient_name="Pepperoni", price=2.50, vegetarian=False, vegan=False),
            Ingredient(ingredient_name="Mushrooms", price=1.75, vegetarian=True, vegan=True),
            Ingredient(ingredient_name="Bell Peppers", price=1.25, vegetarian=True, vegan=True),
        ])
    
    if MenuItem.query.count() == 0:
        menu_items = [
            MenuItem(item_name="Margherita Pizza", item_price=12.99),
            MenuItem(item_name="Pepperoni Pizza", item_price=15.99),
            MenuItem(item_name="Veggie Pizza", item_price=14.99),
            MenuItem(item_name="Coca Cola", item_price=2.50),
            MenuItem(item_name="Water", item_price=1.50),
            MenuItem(item_name="Tiramisu", item_price=5.99),
        ]
        db.session.add_all(menu_items)
        db.session.commit()  # Commit to get IDs
        
        # Create pizzas, drinks, and desserts
        pizzas = [
            Pizza(item_id=1),  # Margherita
            Pizza(item_id=2),  # Pepperoni
            Pizza(item_id=3),  # Veggie
        ]
        drinks = [
            Drink(item_id=4),  # Coca Cola
            Drink(item_id=5),  # Water
        ]
        desserts = [
            Dessert(item_id=6),  # Tiramisu
        ]
        db.session.add_all(pizzas + drinks + desserts)
    
    if DiscountCode.query.count() == 0:
        db.session.add_all([
            DiscountCode(percentage=10, discount_code="WELCOME10"),
            DiscountCode(percentage=15, discount_code="STUDENT15"),
            DiscountCode(percentage=20, discount_code="VIP20"),
        ])
    
    db.session.commit()